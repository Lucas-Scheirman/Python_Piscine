from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[tuple[int, str]] = []
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

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available in processor")
        return self._data.pop(0)


class NumericProcessor(DataProcessor):
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
    def _is_log(self, d: Any) -> bool:
        return (
            isinstance(d, dict)
            and all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in d.items()
            )
            and "log_level" in d
            and "log_message" in d
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
    print("=== Code Nexus - Data Processor ===")
    print("Testing Numeric Processor...")
    test_num = NumericProcessor()
    value_test_int = 42
    value_test_str = "Hello"
    print(
        f"Trying to validate input '{value_test_int}': "
        f"{test_num.validate(value_test_int)}"
    )
    print(
        f"Trying to validate input '{value_test_str}': "
        f"{test_num.validate(value_test_str)}"
    )
    try:
        print(
            "Test invalid ingestion of string 'foo' without prior validation:"
        )
        test_num.ingest("Foo")
    except Exception as e:
        print(f"Got exception: {e}")
    data_num: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data_num}")
    test_num.ingest(data_num)
    print("Extracting 3 values...")
    for i in range(3):
        rank, value = test_num.output()
        print(f"Numeric value {rank}: {value}")
    print("\n")
    print("Testing Text Processor...")
    test_text = TextProcessor()
    value_test_int = 42
    value_test_str = "Hello"
    print(
        f"Trying to validate input '{value_test_int}': "
        f"{test_text.validate(value_test_int)}"
    )
    print(
        f"Trying to validate input '{value_test_str}': "
        f"{test_text.validate(value_test_str)}"
    )
    data_text = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data_text}")
    test_text.ingest(data_text)
    print("Extracting 1 value...")
    for i in range(1):
        rank, value = test_text.output()
        print(f"Text value {rank}: {value}")
    print("\n")
    print("Testing Log Processor...")
    test_log = LogProcessor()
    value_test_str = "Hello"
    print(
        f"Trying to validate input '{value_test_str}': "
        f"{test_log.validate(value_test_str)}"
    )
    valid_log = {"log_level": "INFO", "log_message": "ok"}
    print(
        f"Trying to validate a valid log entry: "
        f"{test_log.validate(valid_log)}"
    )
    data_log = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {data_log}")
    test_log.ingest(data_log)
    print("Extracting 2 values...")
    for i in range(2):
        rank, value = test_log.output()
        print(f"Log entry {rank}: {value}")
