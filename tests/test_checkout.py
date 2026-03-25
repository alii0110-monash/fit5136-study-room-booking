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


def test_checkout_success(services):
    """Checkout succeeds with sufficient balance."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    booking = booking_service.booking_repo.find_by_student_id("33445566")[0]
    result = booking_service.checkout(booking.booking_id, "33445566")

    assert result.success is True


def test_checkout_insufficient_balance(services):
    """AC2: Insufficient balance fails checkout."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])

    # Create a booking that costs more than initial 50 credits
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "16:00")

    booking = booking_service.booking_repo.find_by_student_id("33445566")[0]

    # Should fail due to insufficient balance (50 credits, costs 90)
    result = booking_service.checkout(booking.booking_id, "33445566")

    assert result.success is False
    assert "insufficient" in result.message.lower()


def test_checkout_wrong_student_fails(services):
    """Checkout with wrong student ID fails."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student1@monash.edu", "password123")
    account_service.register("33445567", "student2@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    booking = booking_service.booking_repo.find_by_student_id("33445566")[0]

    # Try to checkout with different student
    result = booking_service.checkout(booking.booking_id, "33445567")

    assert result.success is False


def test_deal_package_discount_4_hours(services):
    """AC1-AC4: >=4 hours gets 20% discount."""
    booking_service = services[1]

    # 5 hours from 09:00 to 14:00
    price, discount = booking_service.calculate_price("09:00", "14:00", 15.0)

    # 5 * 15 * 0.8 = 60
    assert price == 60.0
    assert "Deal Package" in discount or "20%" in discount


def test_deal_package_discount_exactly_4_hours(services):
    """AC1-AC4: Exactly 4 hours gets discount."""
    booking_service = services[1]

    # 4 hours
    price, discount = booking_service.calculate_price("09:00", "13:00", 15.0)

    # 4 * 15 * 0.8 = 48
    assert price == 48.0


def test_no_discount_under_4_hours(services):
    """<4 hours no discount."""
    booking_service = services[1]

    # 3 hours from 09:00 to 12:00
    price, discount = booking_service.calculate_price("09:00", "12:00", 15.0)

    # 3 * 15 = 45
    assert price == 45.0
    assert discount == ""


def test_checkout_already_confirmed_fails(services):
    """Already confirmed booking cannot be checked out again."""
    room_service, booking_service, account_service = services

    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Room 101", 4, 15.0, [])
    booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")

    booking = booking_service.booking_repo.find_by_student_id("33445566")[0]
    booking_service.checkout(booking.booking_id, "33445566")

    # Try to checkout again
    result = booking_service.checkout(booking.booking_id, "33445566")

    assert result.success is False
    assert "already" in result.message.lower()
