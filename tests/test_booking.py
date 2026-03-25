import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services import RoomService, BookingService, AccountService
from repositories import RoomRepository, BookingRepository, AccountRepository


@pytest.fixture
def services(tmp_path):
    """Create services with temporary CSV files."""
    accounts_csv = tmp_path / "accounts.csv"
    accounts_csv.write_text("student_id,email,password,balance\n")

    rooms_csv = tmp_path / "rooms.csv"
    rooms_csv.write_text("room_id,name,capacity,price_per_hour,equipment\n")

    bookings_csv = tmp_path / "bookings.csv"
    bookings_csv.write_text("booking_id,student_id,room_id,date,start_time,end_time,total_price,status\n")

    account_repo = AccountRepository(str(accounts_csv))
    room_repo = RoomRepository(str(rooms_csv))
    booking_repo = BookingRepository(str(bookings_csv))

    account_service = AccountService(account_repo)
    booking_service = BookingService(booking_repo, room_repo, account_repo)
    room_service = RoomService(room_repo, booking_repo)

    return room_service, booking_service, account_service


def test_filter_rooms_by_criteria(services):
    """AC1-AC4: Filter rooms by date, time, capacity."""
    room_service, _, _ = services

    room_service.add_room("101", "Room 101", 4, 15.0, [])
    room_service.add_room("102", "Room 102", 2, 10.0, [])

    # Filter for 2+ people
    rooms = room_service.filter_rooms("2026-03-28", "10:00", "12:00", 2)

    assert len(rooms) == 2


def test_filter_rooms_excludes_insufficient_capacity(services):
    """Rooms with insufficient capacity are excluded."""
    room_service, _, _ = services

    room_service.add_room("101", "Room 101", 4, 15.0, [])
    room_service.add_room("102", "Room 102", 2, 10.0, [])

    # Filter for 4+ people
    rooms = room_service.filter_rooms("2026-03-28", "10:00", "12:00", 4)

    assert len(rooms) == 1
    assert rooms[0].capacity >= 4


def test_double_check_prevents_double_booking(services):
    """AC3: Double-check prevents double booking same slot."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student1@monash.edu", "password123")
    account_service.register("33445567", "student2@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])

    # Student 1 books
    result1 = booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")
    assert result1.success is True

    # Student 2 tries to book same slot - should fail due to double-check
    result2 = booking_service.create_booking("33445567", "101", "2026-03-28", "10:00", "12:00")

    # The room should show as unavailable due to pending booking
    assert result2.success is False
    assert "not available" in result2.message.lower() or "warning" in result2.message.lower()


def test_create_booking_success(services):
    """Create booking succeeds with valid data."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])

    result = booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    assert result.success is True
    assert "booking_id" in result.message.lower() or result.data is not None


def test_create_booking_nonexistent_room_fails(services):
    """Booking nonexistent room fails."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student@monash.edu", "password123")

    result = booking_service.create_booking("33445566", "999", "2026-03-28", "10:00", "12:00")

    assert result.success is False
    assert "not found" in result.message.lower()
