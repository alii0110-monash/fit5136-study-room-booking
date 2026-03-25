import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services import AccountService, BookingService, RoomService
from repositories import AccountRepository, BookingRepository, RoomRepository


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

    account_service = AccountService(account_repo, booking_repo, room_repo)
    booking_service = BookingService(booking_repo, room_repo, account_repo)
    room_service = RoomService(room_repo, booking_repo)

    return account_service, booking_service, room_service


def test_view_account_details(services):
    """AC2-AC4: View account shows student_id, email, balance."""
    account_service, _, _ = services

    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    details = account_service.get_account_details("33445566")

    assert details is not None
    assert details['student_id'] == "33445566"
    assert details['email'] == "student33445566@student.monash.edu"
    assert details['balance'] == 50


def test_account_has_history(services):
    """AC3: Account details include booking history."""
    account_service, booking_service, room_service = services

    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    room_service.add_room("101", "Study Room 101", 4, 15.0, ["Whiteboard"])
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    details = account_service.get_account_details("33445566")

    assert 'history' in details
    assert len(details['history']) == 1


def test_account_history_correct_fields(services):
    """AC4: History shows booking_id, room, date, time, price, status."""
    account_service, booking_service, room_service = services

    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    room_service.add_room("101", "Study Room 101", 4, 15.0, ["Whiteboard"])
    result = booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    details = account_service.get_account_details("33445566")
    history = details['history'][0]

    assert 'booking_id' in history
    assert 'room_name' in history
    assert 'date' in history
    assert 'start_time' in history
    assert 'end_time' in history
    assert 'total_price' in history
    assert 'status' in history
