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


def test_add_room_with_equipment(services):
    """AC1-AC4: Add room with equipment."""
    room_service, _, _ = services

    result = room_service.add_room("101", "Woodside Study Room 101", 4, 15.0, ["Whiteboard", "TV"])

    assert result.success is True
    assert "101" in result.message


def test_add_room_duplicate_fails(services):
    """Duplicate room ID fails."""
    room_service, _, _ = services

    room_service.add_room("101", "Study Room 101", 4, 15.0, [])
    result = room_service.add_room("101", "Another Room", 6, 20.0, [])

    assert result.success is False
    assert "already exists" in result.message


def test_delete_room_with_future_booking_fails(services):
    """AC2: Room with future booking cannot be deleted."""
    room_service, booking_service, account_service = services

    # Setup: create account and room
    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Study Room 101", 4, 15.0, [])
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")
    booking_service.checkout(booking_service.booking_repo.find_by_student_id("33445566")[0].booking_id, "33445566")

    # Try to delete
    result = room_service.delete_room("101", confirm=True)

    assert result.success is False
    assert "Cannot delete" in result.message or "future booking" in result.message


def test_delete_room_requires_confirmation(services):
    """AC3: Delete without confirmation returns confirm prompt."""
    room_service, _, _ = services

    room_service.add_room("101", "Study Room 101", 4, 15.0, [])

    # Without confirmation flag
    result = room_service.delete_room("101", confirm=False)

    assert result.success is False
    assert "Y/N" in result.message or "confirm" in result.message.lower()


def test_delete_room_success(services):
    """Delete room without bookings succeeds."""
    room_service, _, _ = services

    room_service.add_room("101", "Study Room 101", 4, 15.0, [])
    result = room_service.delete_room("101", confirm=True)

    assert result.success is True


def test_get_all_rooms(services):
    """Get all rooms returns list."""
    room_service, _, _ = services

    room_service.add_room("101", "Room 101", 4, 15.0, [])
    room_service.add_room("102", "Room 102", 6, 20.0, [])

    rooms = room_service.get_all_rooms()

    assert len(rooms) == 2
