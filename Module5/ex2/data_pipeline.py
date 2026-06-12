from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self._data: list[tuple[int, str]] = []
        self._name = name
        self._count = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def _store(self, value: str) -> None:
        self._data.append((self._count, value))
        self._count += 1

    def get_stats(self) -> tuple[str, int, int]:
        return (self._name, self._count, len(self._data))

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available in processor")
        return self._data.pop(0)

    def extract(self, nb: int) -> list[tuple[int, str]]:
        return [self.output() for i in range(min(nb, len(self._data)))]


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")

        values_only = []
        for index, value in data:
            values_only.append(value)

        print(",".join(values_only))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")

        json_entries = []
        for key, value in data:
            entry = f'"item_{key}": "{value}"'
            json_entries.append(entry)

        formatted_string = ", ".join(json_entries)
        print(f"{{{formatted_string}}}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print(
                    f"DataStream error - Can't process element"
                    f" in stream: {element}"
                )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            plugin.process_output(proc.extract(nb))

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name, total, remaining = proc.get_stats()
            print(
                f"{name}: total {total} items processed"
                f", remaining {remaining} on processor"
            )


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(str(item))


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(item)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    def _is_log(self, data: Any) -> bool:
        return (
            isinstance(data, dict)
            and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
            and "log_level" in data
            and "log_message" in data
        )

    def validate(self, data: Any) -> bool:
        if self._is_log(data):
            return True
        if isinstance(data, list):
            return all(self._is_log(x) for x in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._store(f"{item['log_level']}: {item['log_message']}")


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
            {"log_level": "INFO", "log_message": "User wil is connected"},
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
