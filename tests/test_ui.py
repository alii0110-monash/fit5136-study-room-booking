"""
UI Layer Tests for FIT5136 Study Room Booking System
Tests pure functions from ui module
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ui import (
    validate_date,
    validate_time_range,
    validate_capacity,
    handle_registration,
    handle_login,
    get_account_display_data,
    get_available_rooms,
    handle_room_selection,
    create_booking_record,
    handle_checkout,
    handle_add_room,
    handle_delete_room,
)


@pytest.fixture
def services(tmp_path):
    """Create services with temporary CSV files."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

    from services import AccountService, RoomService, BookingService
    from repositories import AccountRepository, RoomRepository, BookingRepository

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

    # Setup test data
    account_service.register("33445566", "student@monash.edu", "password123")
    room_service.add_room("101", "Study Room 101", 4, 15.0, ["Whiteboard"])

    return account_service, room_service, booking_service


class TestValidateDate:
    """Tests for date validation"""

    def test_valid_future_date(self):
        """Future date should be valid"""
        future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        valid, error = validate_date(future)
        assert valid is True
        assert error == ""

    def test_today_is_valid(self):
        """Today's date should be valid"""
        today = datetime.now().strftime("%Y-%m-%d")
        valid, error = validate_date(today)
        assert valid is True

    def test_past_date_invalid(self):
        """Past date should be invalid"""
        past = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        valid, error = validate_date(past)
        assert valid is False
        assert "past" in error.lower()

    def test_empty_date_invalid(self):
        """Empty date should be invalid"""
        valid, error = validate_date("")
        assert valid is False
        assert "empty" in error.lower()

    def test_invalid_format_invalid(self):
        """Invalid format should be invalid"""
        valid, error = validate_date("not-a-date")
        assert valid is False
        assert "format" in error.lower()


class TestValidateTimeRange:
    """Tests for time range validation"""

    def test_valid_range(self):
        """Start before end should be valid"""
        valid, error = validate_time_range("09:00", "12:00")
        assert valid is True
        assert error == ""

    def test_end_before_start_invalid(self):
        """End before start should be invalid"""
        valid, error = validate_time_range("14:00", "10:00")
        assert valid is False
        assert "later" in error.lower()

    def test_same_time_invalid(self):
        """Same time should be invalid"""
        valid, error = validate_time_range("10:00", "10:00")
        assert valid is False

    def test_empty_times_invalid(self):
        """Empty times should be invalid"""
        valid, error = validate_time_range("", "")
        assert valid is False

    def test_invalid_format(self):
        """Invalid format should be invalid"""
        valid, error = validate_time_range("9am", "12pm")
        assert valid is False
        assert "format" in error.lower()


class TestValidateCapacity:
    """Tests for capacity validation"""

    def test_valid_capacity(self):
        """Positive integer should be valid"""
        valid, value, error = validate_capacity("4")
        assert valid is True
        assert value == 4
        assert error == ""

    def test_zero_capacity_invalid(self):
        """Zero capacity should be invalid"""
        valid, value, error = validate_capacity("0")
        assert valid is False
        assert "at least 1" in error.lower()

    def test_negative_capacity_invalid(self):
        """Negative capacity should be invalid"""
        valid, value, error = validate_capacity("-1")
        assert valid is False

    def test_empty_capacity_defaults_to_1(self):
        """Empty capacity should default to 1"""
        valid, value, error = validate_capacity("")
        assert valid is True
        assert value == 1

    def test_non_numeric_invalid(self):
        """Non-numeric should be invalid"""
        valid, value, error = validate_capacity("abc")
        assert valid is False


class TestHandleRegistration:
    """Tests for registration handler"""

    def test_valid_registration_success(self, services):
        """Valid registration should succeed"""
        account_service = services[0]
        success, message, data = handle_registration(
            account_service, "33445700", "new@monash.edu", "password123"
        )
        assert success is True
        assert "50" in message
        assert data is not None

    def test_duplicate_student_id_fails(self, services):
        """Duplicate student ID should fail"""
        account_service = services[0]
        success, message, data = handle_registration(
            account_service, "33445566", "another@monash.edu", "password123"
        )
        assert success is False
        assert "already registered" in message.lower()
        assert data is None

    def test_invalid_email_fails(self, services):
        """Invalid email should fail"""
        account_service = services[0]
        success, message, data = handle_registration(
            account_service, "33445701", "not-email", "password123"
        )
        assert success is False
        assert "email" in message.lower()


class TestHandleLogin:
    """Tests for login handler"""

    def test_valid_login_success(self, services):
        """Valid login should succeed"""
        account_service = services[0]
        success, message, account = handle_login(account_service, "33445566", "password123")
        assert success is True
        assert "33445566" in message
        assert account.student_id == "33445566"

    def test_wrong_password_fails(self, services):
        """Wrong password should fail"""
        account_service = services[0]
        success, message, account = handle_login(account_service, "33445566", "wrongpass")
        assert success is False
        assert "invalid" in message.lower()
        assert account is None

    def test_nonexistent_user_fails(self, services):
        """Nonexistent user should fail"""
        account_service = services[0]
        success, message, account = handle_login(account_service, "99999999", "password123")
        assert success is False
        assert account is None


class TestGetAccountDisplayData:
    """Tests for account display data"""

    def test_existing_account(self, services):
        """Existing account should return data"""
        account_service = services[0]
        success, data, error = get_account_display_data(account_service, "33445566")
        assert success is True
        assert data['student_id'] == "33445566"
        assert data['balance'] == 50

    def test_nonexistent_account(self, services):
        """Nonexistent account should fail"""
        account_service = services[0]
        success, data, error = get_account_display_data(account_service, "99999999")
        assert success is False
        assert "not found" in error.lower()


class TestHandleRoomSelection:
    """Tests for room selection and double-check"""

    def test_available_room_success(self, services):
        """Available room should succeed"""
        booking_service = services[2]
        valid, error = handle_room_selection(booking_service, "101", "2026-04-01", "10:00", "12:00")
        assert valid is True
        assert error == ""

    def test_conflict_room_fails(self, services):
        """Room with conflict should fail"""
        account_service, room_service, booking_service = services

        # Create a confirmed booking first
        booking_service.create_booking(
            "33445566", "101", "2026-04-01", "10:00", "12:00",
            skip_validation=True
        )
        booking_id = booking_service.booking_repo.find_by_student_id("33445566")[0].booking_id
        booking_service.checkout(booking_id, "33445566")

        # Try to book same slot
        valid, error = handle_room_selection(booking_service, "101", "2026-04-01", "10:00", "12:00")
        assert valid is False
        assert "not available" in error.lower() or "no longer available" in error.lower()


class TestHandleAddRoom:
    """Tests for add room handler"""

    def test_valid_room_add_success(self, services):
        """Valid room addition should succeed"""
        room_service = services[1]
        success, message = handle_add_room(room_service, "102", "Room 102", 6, 20.0, ["TV"])
        assert success is True
        assert "added" in message.lower()

    def test_duplicate_room_fails(self, services):
        """Duplicate room ID should fail"""
        room_service = services[1]
        success, message = handle_add_room(room_service, "101", "Another Room", 4, 15.0, [])
        assert success is False
        assert "already exists" in message.lower()


class TestHandleDeleteRoom:
    """Tests for delete room handler"""

    def test_delete_without_future_bookings(self, services):
        """Room without future bookings should be deleted"""
        room_service, booking_service = services[1], services[2]

        # First add a new room to delete
        room_service.add_room("999", "Temp Room", 2, 10.0, [])

        success, message = handle_delete_room(room_service, booking_service, "999", confirm=True)
        assert success is True

    def test_delete_requires_confirmation(self, services):
        """Delete without confirmation should prompt"""
        room_service, booking_service = services[1], services[2]

        # First add a new room to delete
        room_service.add_room("998", "Temp Room 2", 2, 10.0, [])

        success, message = handle_delete_room(room_service, booking_service, "998", confirm=False)
        assert success is False
        assert "confirm" in message.lower()


class TestCheckout:
    """Tests for checkout handler"""

    def test_successful_checkout(self, services):
        """Successful checkout should deduct balance"""
        account_service, room_service, booking_service = services

        # Create booking
        result = booking_service.create_booking(
            "33445566", "101", "2026-04-01", "10:00", "12:00",
            skip_validation=True
        )
        booking_id = result.data['booking'].booking_id

        # Checkout
        success, message, new_balance = handle_checkout(booking_service, booking_id, "33445566")
        assert success is True
        assert new_balance == 20  # 50 - 30 = 20

    def test_checkout_insufficient_balance(self, services):
        """Insufficient balance should fail"""
        account_service, room_service, booking_service = services

        # Create booking that costs more than 50
        result = booking_service.create_booking(
            "33445566", "101", "2026-04-01", "09:00", "14:00",
            skip_validation=True
        )
        booking_id = result.data['booking'].booking_id

        # Checkout should fail
        success, message, _ = handle_checkout(booking_service, booking_id, "33445566")
        assert success is False
        assert "insufficient" in message.lower()
