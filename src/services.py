"""
Business Logic Layer for FIT5136 Study Room Booking System
"""

import re
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from models import Account, Room, Booking, Result
from repositories import AccountRepository, RoomRepository, BookingRepository


class AccountService:
    def __init__(self, account_repo: AccountRepository = None, booking_repo: BookingRepository = None,
                 room_repo: RoomRepository = None):
        self.account_repo = account_repo or AccountRepository()
        self.booking_repo = booking_repo or BookingRepository()
        self.room_repo = room_repo or RoomRepository()

    def _validate_registration(self, student_id: str, email: str, password: str) -> Result:
        """Validate registration input. Returns Result with success=True or error message."""
        # Validate student_id: must be numeric only
        if not student_id.isdigit():
            return Result(success=False, message="[ERROR] Student ID must be numbers only (e.g., 33445566)")

        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return Result(success=False, message="[ERROR] Invalid email format (e.g., student@monash.edu)")

        # Validate password length
        if len(password) <= 6:
            return Result(success=False, message="[ERROR] Password must be more than 6 characters")

        # Check if student_id already exists
        if self.account_repo.exists(student_id):
            return Result(success=False, message="[ERROR] Student ID already registered")

        return Result(success=True, message="Validation passed")

    def register(self, student_id: str, email: str, password: str) -> Result:
        """Register a new account."""
        # Validate first
        validation = self._validate_registration(student_id, email, password)
        if not validation.success:
            return validation

        # Create new account with 50 initial balance
        account = Account(student_id=student_id, email=email, password=password, balance=50)
        self.account_repo.save(account)

        return Result(success=True, message="注册成功，已为您发放 50 积分初始体验金", data=account)

    def login(self, student_id: str, password: str) -> Optional[Account]:
        """Login with student_id and password."""
        # Special handling for admin account
        if student_id == "admin" and password == "admin123":
            admin_account = Account(student_id="admin", email="admin@monash.edu", password="admin123", balance=0)
            return admin_account

        account = self.account_repo.find_by_student_id(student_id)
        if account and account.password == password:
            return account
        return None

    def get_account_details(self, student_id: str) -> Optional[dict]:
        """Get account details with booking history."""
        account = self.account_repo.find_by_student_id(student_id)
        if not account:
            return None

        bookings = self.booking_repo.find_by_student_id(student_id)

        history = []
        for b in bookings:
            room = self.room_repo.find_by_room_id(b.room_id)
            room_name = room.name if room else f"Room {b.room_id}"
            history.append({
                'booking_id': b.booking_id,
                'room_id': b.room_id,
                'room_name': room_name,
                'date': b.date,
                'start_time': b.start_time,
                'end_time': b.end_time,
                'total_price': b.total_price,
                'status': b.status
            })

        return {
            'student_id': account.student_id,
            'email': account.email,
            'balance': account.balance,
            'history': history
        }


class RoomService:
    def __init__(self, room_repo: RoomRepository = None, booking_repo: BookingRepository = None):
        self.room_repo = room_repo or RoomRepository()
        self.booking_repo = booking_repo or BookingRepository()

    def add_room(self, room_id: str, name: str, capacity: int, price_per_hour: float, equipment: List[str]) -> Result:
        """Add a new room."""
        # Validate
        if not room_id or not room_id.strip():
            return Result(success=False, message="[ERROR] Room ID cannot be empty (e.g., 101)")
        if not name or not name.strip():
            return Result(success=False, message="[ERROR] Room name cannot be empty (e.g., Study Room 101)")
        if capacity < 1:
            return Result(success=False, message="[ERROR] Capacity must be at least 1 (e.g., 4)")
        if price_per_hour <= 0:
            return Result(success=False, message="[ERROR] Price must be greater than 0 (e.g., 15.0)")

        # Check if room_id already exists
        if self.room_repo.exists(room_id):
            return Result(success=False, message=f"[ERROR] Room {room_id} already exists")

        room = Room(
            room_id=room_id,
            name=name,
            capacity=capacity,
            price_per_hour=price_per_hour,
            equipment=equipment or []
        )
        self.room_repo.save(room)

        return Result(success=True, message=f"Room {room_id} added successfully", data=room)

    def delete_room(self, room_id: str, confirm: bool = False) -> Result:
        """Delete a room if no future bookings exist."""
        if not confirm:
            return Result(success=False, message="[CONFIRM] Are you sure you want to delete this room? (Y/N)")

        # Check for future confirmed bookings
        future_bookings = self.booking_repo.get_future_bookings(room_id)
        if future_bookings:
            return Result(success=False, message=f"[ERROR] Cannot delete Room {room_id} - there are future bookings")

        success = self.room_repo.delete(room_id)
        if success:
            return Result(success=True, message=f"Room {room_id} deleted successfully")
        return Result(success=False, message=f"[ERROR] Room {room_id} not found")

    def filter_rooms(self, date: str, start_time: str, end_time: str, min_capacity: int) -> List[Room]:
        """Filter available rooms based on criteria and availability."""
        all_rooms = self.room_repo.find_all()
        available_rooms = []

        for room in all_rooms:
            # Check capacity
            if room.capacity < min_capacity:
                continue

            # Check for conflicts (only confirmed bookings block a room)
            conflicts = self.booking_repo.find_conflicting(room.room_id, date, start_time, end_time)
            if len(conflicts) == 0:
                available_rooms.append(room)

        return available_rooms

    def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by ID."""
        return self.room_repo.find_by_room_id(room_id)

    def get_all_rooms(self) -> List[Room]:
        """Get all rooms."""
        return self.room_repo.find_all()


class BookingService:
    def __init__(self, booking_repo: BookingRepository = None, room_repo: RoomRepository = None,
                 account_repo: AccountRepository = None):
        self.booking_repo = booking_repo or BookingRepository()
        self.room_repo = room_repo or RoomRepository()
        self.account_repo = account_repo or AccountRepository()

    def _validate_date(self, date_str: str) -> Result:
        """Validate date is not in the past."""
        try:
            input_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if input_date < today:
                return Result(success=False, message="[ERROR] Date cannot be in the past (e.g., 2026-03-28)")
            return Result(success=True, message="Validation passed")
        except ValueError:
            return Result(success=False, message="[ERROR] Invalid date format. Use YYYY-MM-DD (e.g., 2026-03-28)")

    def _validate_time_range(self, start_time: str, end_time: str) -> Result:
        """Validate end time is after start time."""
        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            if end_dt <= start_dt:
                return Result(success=False, message="[ERROR] End time must be later than start time (e.g., 09:00-12:00)")
            return Result(success=True, message="Validation passed")
        except ValueError:
            return Result(success=False, message="[ERROR] Invalid time format. Use HH:MM (e.g., 09:00)")

    def calculate_price(self, start_time: str, end_time: str, base_price: float) -> Tuple[float, str]:
        """Calculate price with Deal Package discount (>=4 hours = 20% off)."""
        start_h, start_m = map(int, start_time.split(':'))
        end_h, end_m = map(int, end_time.split(':'))

        start_minutes = start_h * 60 + start_m
        end_minutes = end_h * 60 + end_m
        duration_hours = (end_minutes - start_minutes) / 60.0

        if duration_hours <= 0:
            return 0.0, ""

        total_price = duration_hours * base_price
        discount_info = ""

        if duration_hours >= 4:
            discounted_price = total_price * 0.8
            discount_info = f"Deal Package Applied (20% off): {duration_hours:.1f} hours"
            return discounted_price, discount_info

        return total_price, discount_info

    def create_booking(self, student_id: str, room_id: str, date: str, start_time: str, end_time: str,
                       skip_validation: bool = False) -> Result:
        """Create a new booking."""
        # Validate if not skipped (UI layer may validate separately)
        if not skip_validation:
            date_validation = self._validate_date(date)
            if not date_validation.success:
                return date_validation

            time_validation = self._validate_time_range(start_time, end_time)
            if not time_validation.success:
                return time_validation

        # Get room
        room = self.room_repo.find_by_room_id(room_id)
        if not room:
            return Result(success=False, message=f"[ERROR] Room {room_id} not found")

        # Double-check availability (both pending and confirmed bookings)
        confirmed_conflicts = self.booking_repo.find_conflicting(room_id, date, start_time, end_time)
        pending_conflicts = self.booking_repo.find_pending(room_id, date, start_time, end_time)

        if confirmed_conflicts or pending_conflicts:
            return Result(success=False, message="[WARNING] Room is not available for the selected time slot")

        # Calculate price
        total_price, discount_info = self.calculate_price(start_time, end_time, room.price_per_hour)

        # Create booking with pending status
        booking_id = str(uuid.uuid4())[:8].upper()
        booking = Booking(
            booking_id=booking_id,
            student_id=student_id,
            room_id=room_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            total_price=total_price,
            status="pending"
        )
        self.booking_repo.save(booking)

        return Result(
            success=True,
            message=f"Booking created successfully! Booking ID: {booking_id}",
            data={
                'booking': booking,
                'discount_info': discount_info
            }
        )

    def checkout(self, booking_id: str, student_id: str) -> Result:
        """Process checkout for a booking."""
        # Get booking
        booking = self.booking_repo.find_by_booking_id(booking_id)
        if not booking:
            return Result(success=False, message="[ERROR] Booking not found")

        # Verify ownership
        if booking.student_id != student_id:
            return Result(success=False, message="[ERROR] Booking not found for this student")

        # Check if already confirmed
        if booking.status == "confirmed":
            return Result(success=False, message="[ERROR] Booking already confirmed")

        # Get account
        account = self.account_repo.find_by_student_id(student_id)
        if not account:
            return Result(success=False, message="[ERROR] Account not found")

        # Check balance
        if account.balance < booking.total_price:
            return Result(success=False, message="[ERROR] Insufficient balance")

        # Deduct balance and confirm booking
        new_balance = account.balance - int(booking.total_price)
        self.account_repo.update_balance(student_id, new_balance)
        self.booking_repo.update_status(booking_id, "confirmed")

        return Result(
            success=True,
            message=f"Checkout successful! Remaining balance: {new_balance} credits",
            data={'new_balance': new_balance}
        )

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        """Get a booking by ID."""
        return self.booking_repo.find_by_booking_id(booking_id)

    def get_student_bookings(self, student_id: str) -> List[Booking]:
        """Get all bookings for a student."""
        return self.booking_repo.find_by_student_id(student_id)

    def get_pending_bookings(self, student_id: str) -> List[Booking]:
        """Get pending bookings for a student."""
        all_bookings = self.booking_repo.find_by_student_id(student_id)
        return [b for b in all_bookings if b.status == "pending"]
