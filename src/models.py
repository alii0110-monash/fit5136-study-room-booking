from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Account:
    student_id: str
    email: str
    password: str
    balance: int = 50  # Initial experience credits

    def to_csv_row(self) -> list:
        return [self.student_id, self.email, self.password, str(self.balance)]

    @classmethod
    def from_csv_row(cls, row: list) -> 'Account':
        return cls(
            student_id=row[0],
            email=row[1],
            password=row[2],
            balance=int(row[3])
        )


@dataclass
class Room:
    room_id: str
    name: str
    capacity: int
    price_per_hour: float
    equipment: list[str] = field(default_factory=list)

    def to_csv_row(self) -> list:
        equipment_str = ','.join(self.equipment) if self.equipment else ''
        return [self.room_id, self.name, str(self.capacity), str(self.price_per_hour), equipment_str]

    @classmethod
    def from_csv_row(cls, row: list) -> 'Room':
        equipment = row[4].split(',') if len(row) > 4 and row[4] else []
        return cls(
            room_id=row[0],
            name=row[1],
            capacity=int(row[2]),
            price_per_hour=float(row[3]),
            equipment=equipment
        )


@dataclass
class Booking:
    booking_id: str
    student_id: str
    room_id: str
    date: str
    start_time: str
    end_time: str
    total_price: float
    status: str = "pending"  # pending, confirmed

    def to_csv_row(self) -> list:
        return [
            self.booking_id,
            self.student_id,
            self.room_id,
            self.date,
            self.start_time,
            self.end_time,
            str(self.total_price),
            self.status
        ]

    @classmethod
    def from_csv_row(cls, row: list) -> 'Booking':
        return cls(
            booking_id=row[0],
            student_id=row[1],
            room_id=row[2],
            date=row[3],
            start_time=row[4],
            end_time=row[5],
            total_price=float(row[6]),
            status=row[7] if len(row) > 7 else "pending"
        )


@dataclass
class Result:
    success: bool
    message: str
    data: Optional[any] = None

    def __bool__(self) -> bool:
        return self.success
