from abc import ABC, abstractmethod
from typing import Any


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
    print("=== Code Nexus - Data Stream ===\n")
    print("Initialize Data Stream...")
    test = DataStream()
    test.print_processors_stats()
    print("\n")
    print("Registering Numeric Processor\n")
    test_num = NumericProcessor()
    test.register_processor(test_num)
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
    print("Registering other data processors")
    test_text = TextProcessor()
    test_log = LogProcessor()
    test.register_processor(test_text)
    test.register_processor(test_log)
    print("Send the same batch again")
    test.process_stream(stream)
    test.print_processors_stats()
    print("\n")
    print(
        "Consume some elements from the data processors:"
        " Numeric 3, Text 2, Log 1"
    )
    for i in range(3):
        test_num.output()
    for i in range(2):
        test_text.output()
    for i in range(1):
        test_log.output()
    test.print_processors_stats()
