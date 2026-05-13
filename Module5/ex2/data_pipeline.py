from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
        self._name: str = ""
        self._count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return self._data.pop(0)


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join([value for key, value in data]))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        print(
            "{"
            + ",".join([f'"item_{key}": "{value}"' for key, value in data])
            + "}"
        )


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for process in self._processors:
            list_ = []
            for i in range(min(nb, len(process._data))):
                list_.append(process.output())
            plugin.process_output(list_)

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            find = False
            for x in self._processors:
                if x.validate(element):
                    x.ingest(element)
                    find = True
                    break
            if not find:
                print(
                    f"DataStream error - Can't process element"
                    f" in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        else:
            for proc in self._processors:
                print(
                    f"{proc._name}: total {proc._count} items processed"
                    f", remaining {len(proc._data)} on processor"
                )


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
        self._count = 0
        self._name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        return (
            isinstance(data, (int, float))
            and not isinstance(data, bool)
            or isinstance(data, list)
            and all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        )

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data.append((self._count, str(item)))
                self._count += 1
        else:
            self._data.append((self._count, str(data)))
            self._count += 1


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
        self._count = 0
        self._name = "Text Processor"

    def validate(self, data: Any) -> bool:
        return (
            isinstance(data, str)
            or isinstance(data, list)
            and all(isinstance(x, str) for x in data)
        )

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._data.append((self._count, item))
                self._count += 1
        else:
            self._data.append((self._count, data))
            self._count += 1


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
        self._count = 0
        self._name = "Log Processor"

    def validate(self, data: Any) -> bool:
        return (
            isinstance(data, dict)
            and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
            or isinstance(data, list)
            and all(
                isinstance(x, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in x.items()
                )
                for x in data
            )
        )

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._data.append(
                    (
                        self._count,
                        f"{item['log_level']}: {item['log_message']}",
                    )
                )
                self._count += 1
        else:
            self._data.append(
                (
                    self._count,
                    f"{data['log_level']}: {data['log_message']}",
                )
            )
            self._count += 1


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    test = DataStream()
    test.print_processors_stats()
    print("\n")
    print("Registering Processors")
    test_num = NumericProcessor()
    test_text = TextProcessor()
    test_log = LogProcessor()
    test.register_processor(test_num)
    test.register_processor(test_text)
    test.register_processor(test_log)
    stream = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil isconnected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {stream}")
    test.process_stream(stream)
    test.print_processors_stats()
    print("\n")
    print("Send 3 processed data from each processor to a CSV plugin:")
    test.output_pipeline(3, CSVExportPlugin())
    test.print_processors_stats()
    print("\n")
    stream = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {stream}")
    test.process_stream(stream)
    test.print_processors_stats()
    print("\n")
    print("Send 5 processed data from each processor to a JSON plugin:")
    test.output_pipeline(5, JSONExportPlugin())
    test.print_processors_stats()
