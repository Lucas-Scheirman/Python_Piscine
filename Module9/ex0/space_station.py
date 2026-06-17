try:
    from datetime import datetime
    from typing import Optional
    from pydantic import BaseModel, Field, ValidationError
except ImportError as e:
    print(f"Error importing modules: {e}")
    raise


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 8, 30, 0),
        is_operational=True,
    )

    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Non-Operational"
    print(f"Status: {status}")
    print("=" * 40)

    try:
        SpaceStation(
            station_id="ISS002",
            name="Bad Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=80.0,
            last_maintenance=datetime(2024, 1, 15, 8, 30, 0),
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
