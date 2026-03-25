import csv
import os
from typing import List, Optional
from models import Account, Room, Booking

# Get the project root (parent of src directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_data_dir():
    """Get data directory, checking environment variable first."""
    return os.environ.get('FIT5136_DATA_DIR', os.path.join(PROJECT_ROOT, "data"))


class AccountRepository:
    def __init__(self, filepath: str = None):
        if filepath is None:
            filepath = os.path.join(_get_data_dir(), "accounts.csv")
        self.filepath = filepath

    def save(self, account: Account) -> None:
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(account.to_csv_row())

    def find_by_student_id(self, student_id: str) -> Optional[Account]:
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[0] == student_id:
                    return Account.from_csv_row(row)
        return None

    def update_balance(self, student_id: str, new_balance: int) -> bool:
        rows = []
        updated = False
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows.append(header)
            for row in reader:
                if row and row[0] == student_id:
                    row[3] = str(new_balance)
                    updated = True
                if row:
                    rows.append(row)

        if updated:
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        return updated

    def exists(self, student_id: str) -> bool:
        return self.find_by_student_id(student_id) is not None

    def get_all(self) -> List[Account]:
        accounts = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    accounts.append(Account.from_csv_row(row))
        return accounts


class RoomRepository:
    def __init__(self, filepath: str = None):
        if filepath is None:
            filepath = os.path.join(_get_data_dir(), "rooms.csv")
        self.filepath = filepath

    def save(self, room: Room) -> None:
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(room.to_csv_row())

    def find_by_room_id(self, room_id: str) -> Optional[Room]:
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[0] == room_id:
                    return Room.from_csv_row(row)
        return None

    def find_all(self) -> List[Room]:
        rooms = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    rooms.append(Room.from_csv_row(row))
        return rooms

    def delete(self, room_id: str) -> bool:
        rows = []
        deleted = False
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows.append(header)
            for row in reader:
                if row and row[0] == room_id:
                    deleted = True
                elif row:
                    rows.append(row)

        if deleted:
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        return deleted

    def exists(self, room_id: str) -> bool:
        return self.find_by_room_id(room_id) is not None


class BookingRepository:
    def __init__(self, filepath: str = None):
        if filepath is None:
            filepath = os.path.join(_get_data_dir(), "bookings.csv")
        self.filepath = filepath

    def save(self, booking: Booking) -> None:
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(booking.to_csv_row())

    def find_by_booking_id(self, booking_id: str) -> Optional[Booking]:
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[0] == booking_id:
                    return Booking.from_csv_row(row)
        return None

    def find_by_student_id(self, student_id: str) -> List[Booking]:
        bookings = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[1] == student_id:
                    bookings.append(Booking.from_csv_row(row))
        return bookings

    def find_by_room_id(self, room_id: str) -> List[Booking]:
        bookings = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[2] == room_id:
                    bookings.append(Booking.from_csv_row(row))
        return bookings

    def update_status(self, booking_id: str, new_status: str) -> bool:
        rows = []
        updated = False
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows.append(header)
            for row in reader:
                if row and row[0] == booking_id:
                    row[7] = new_status
                    updated = True
                rows.append(row)

        if updated:
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
        return updated

    def find_conflicting(self, room_id: str, date: str, start_time: str, end_time: str) -> List[Booking]:
        """Find all bookings that conflict with the given time slot."""
        conflicts = []
        bookings = self.find_by_room_id(room_id)
        for booking in bookings:
            if booking.date == date and booking.status == "confirmed":
                if not (end_time <= booking.start_time or start_time >= booking.end_time):
                    conflicts.append(booking)
        return conflicts

    def find_pending(self, room_id: str, date: str, start_time: str, end_time: str) -> List[Booking]:
        """Find pending bookings that conflict with the given time slot."""
        conflicts = []
        bookings = self.find_by_room_id(room_id)
        for booking in bookings:
            if booking.date == date and booking.status == "pending":
                if not (end_time <= booking.start_time or start_time >= booking.end_time):
                    conflicts.append(booking)
        return conflicts

    def get_all(self) -> List[Booking]:
        bookings = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row:
                    bookings.append(Booking.from_csv_row(row))
        return bookings

    def get_future_bookings(self, room_id: str) -> List[Booking]:
        """Get all confirmed future bookings for a room."""
        bookings = []
        with open(self.filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if row and row[2] == room_id and row[7] == "confirmed":
                    bookings.append(Booking.from_csv_row(row))
        return bookings
