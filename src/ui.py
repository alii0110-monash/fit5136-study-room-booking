"""
UI Layer for FIT5136 Study Room Booking System
Separated into pure functions (logic) and I/O wrappers
"""

import os
import sys
from datetime import datetime
from typing import Optional, Tuple, List, Dict, Any


# =============================================================================
# Pure Functions (Logic) - No I/O, returns data
# =============================================================================

def validate_date(date_str: str) -> Tuple[bool, str]:
    """Validate date is not in the past. Returns (success, error_message)."""
    if not date_str:
        return False, "[ERROR] Date cannot be empty (e.g., 2026-03-28)"
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if input_date < today:
            return False, "[ERROR] Date cannot be in the past (e.g., 2026-03-28)"
        return True, ""
    except ValueError:
        return False, "[ERROR] Invalid date format. Use YYYY-MM-DD (e.g., 2026-03-28)"


def validate_time_range(start_time: str, end_time: str) -> Tuple[bool, str]:
    """Validate end time is after start time. Returns (success, error_message)."""
    if not start_time or not end_time:
        return False, "[ERROR] Time cannot be empty (e.g., 09:00)"
    try:
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")
        if end_dt <= start_dt:
            return False, "[ERROR] End time must be later than start time (e.g., 09:00-12:00)"
        return True, ""
    except ValueError:
        return False, "[ERROR] Invalid time format. Use HH:MM (e.g., 09:00)"


def validate_capacity(capacity_str: str) -> Tuple[bool, int, str]:
    """Validate capacity is positive integer. Returns (success, value, error_message)."""
    if not capacity_str:
        return True, 1, ""  # Default to 1
    try:
        capacity = int(capacity_str)
        if capacity < 1:
            return False, 0, "[ERROR] Capacity must be at least 1 (e.g., 4)"
        return True, capacity, ""
    except ValueError:
        return False, 0, "[ERROR] Invalid capacity. Must be a number (e.g., 4)"


def handle_registration(account_service, student_id: str, email: str, password: str) -> Tuple[bool, str, Optional[Any]]:
    """
    Handle registration logic. Returns (success, message, data).
    - On success: data is Account object
    - On failure: data is None
    """
    result = account_service.register(student_id, email, password)
    return result.success, result.message, result.data if result.success else None


def handle_login(account_service, student_id: str, password: str) -> Tuple[bool, str, Optional[Any]]:
    """
    Handle login logic. Returns (success, message, account).
    - On success: account object
    - On failure: account is None
    """
    account = account_service.login(student_id, password)
    if account:
        return True, f"Welcome back, {account.student_id}!", account
    return False, "Invalid credentials", None


def get_account_display_data(account_service, student_id: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Get account details for display. Returns (success, data_dict, error_message).
    """
    details = account_service.get_account_details(student_id)
    if not details:
        return False, {}, "Account not found"
    return True, details, ""


def get_available_rooms(room_service, date: str, start_time: str, end_time: str, min_capacity: int) -> List:
    """Get available rooms based on criteria."""
    return room_service.filter_rooms(date, start_time, end_time, min_capacity)


def handle_room_selection(booking_service, room_id: str, date: str, start_time: str, end_time: str) -> Tuple[bool, str]:
    """Handle room selection and double-check. Returns (success, error_message)."""
    conflicts = booking_service.booking_repo.find_conflicting(room_id, date, start_time, end_time)
    if conflicts:
        return False, f"[WARNING] Room {room_id} is no longer available!"
    return True, ""


def create_booking_record(booking_service, student_id: str, room_id: str, date: str, start_time: str, end_time: str) -> Tuple[bool, str, Any]:
    """Create a booking. Returns (success, message, booking_data)."""
    result = booking_service.create_booking(student_id, room_id, date, start_time, end_time)
    return result.success, result.message, result.data if result.success else None


def handle_checkout(booking_service, booking_id: str, student_id: str) -> Tuple[bool, str, Optional[int]]:
    """
    Handle checkout. Returns (success, message, new_balance).
    new_balance is None on failure.
    """
    result = booking_service.checkout(booking_id, student_id)
    if result.success:
        return True, result.message, result.data.get('new_balance') if result.data else None
    return False, result.message, None


def get_checkout_summary(booking_service, room_service, booking) -> Dict[str, Any]:
    """Get checkout summary data."""
    room = room_service.get_room(booking.room_id)
    total_price, discount_info = booking_service.calculate_price(
        booking.start_time, booking.end_time, room.price_per_hour if room else 0
    )
    return {
        'booking': booking,
        'room_name': room.name if room else booking.room_id,
        'total_price': total_price,
        'discount_info': discount_info
    }


def get_pending_bookings_for_student(booking_service, room_service, student_id: str) -> List[Dict]:
    """Get pending bookings with room names for a student."""
    pending = booking_service.get_pending_bookings(student_id)
    result = []
    for b in pending:
        room = room_service.get_room(b.room_id)
        result.append({
            'booking': b,
            'room_name': room.name if room else b.room_id
        })
    return result


def handle_add_room(room_service, room_id: str, name: str, capacity: int, price: float, equipment: List[str]) -> Tuple[bool, str]:
    """Handle add room logic. Returns (success, message)."""
    result = room_service.add_room(room_id, name, capacity, price, equipment)
    return result.success, result.message


def handle_delete_room(room_service, booking_service, room_id: str, confirm: bool) -> Tuple[bool, str]:
    """Handle delete room logic. Returns (success, message)."""
    result = room_service.delete_room(room_id, confirm)
    return result.success, result.message


# =============================================================================
# UI Constants
# =============================================================================

COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m'
}

SUCCESS = COLORS['GREEN']
ERROR = COLORS['RED']
WARNING = COLORS['YELLOW']
INFO = COLORS['BLUE']
BOLD = COLORS['BOLD']
RESET = COLORS['RESET']


# =============================================================================
# I/O Functions (print/get) - Side effects only
# =============================================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}{title:^60}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")


def print_footer():
    print(f"\n{INFO}Press [0] to return to Main Menu{RESET}")


def print_error(message: str):
    print(f"\n{ERROR}{message}{RESET}\n")


def print_success(message: str):
    print(f"\n{SUCCESS}{message}{RESET}\n")


def print_warning(message: str):
    print(f"\n{WARNING}{message}{RESET}\n")


def print_info(message: str):
    print(f"\n{INFO}{message}{RESET}\n")


def print_divider():
    print(f"{BOLD}-{'-' * 58}{RESET}")


def print_ascii_table(headers: list, rows: list):
    """Print an ASCII table with headers and rows."""
    if not headers:
        return
    col_widths = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    header_line = "|"
    for i, h in enumerate(headers):
        header_line += f" {h:^{col_widths[i]}} |"
    print(f"{BOLD}{header_line}{RESET}")
    print_divider()

    for row in rows:
        row_line = "|"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                row_line += f" {str(cell):^{col_widths[i]}} |"
        print(row_line)


def get_input(prompt: str) -> str:
    return input(f"{BOLD}{prompt}{RESET}: ").strip()


def get_yes_no(prompt: str) -> bool:
    while True:
        response = get_input(f"{prompt} (Y/N)").upper()
        if response == 'Y':
            return True
        elif response == 'N':
            return False
        else:
            print_warning("Please enter Y or N")


# =============================================================================
# Screen Functions (I/O wrappers calling pure functions)
# =============================================================================

def show_welcome_screen():
    clear_screen()
    print_header("FIT5136 Study Room Booking System")
    print(f"{BOLD}[START HERE]{RESET}\n")
    print("Welcome to the Study Room Booking System!\n")
    print("1. Register")
    print("2. Login")
    print("0. Exit")
    print()


def show_registration_flow(account_service):
    clear_screen()
    print_header("Registration")

    student_id = get_input("Enter Student ID (numbers only)")
    email = get_input("Enter Email (student email)")
    password = get_input("Enter Password (>6 characters)")

    success, message, data = handle_registration(account_service, student_id, email, password)

    if success:
        print_success(message)
        input("Press Enter to continue...")
        return data
    else:
        print_error(message)
        input("Press Enter to continue...")
        return None


def show_login_flow(account_service):
    clear_screen()
    print_header("Login")

    student_id = get_input("Enter Student ID")
    password = get_input("Enter Password")

    success, message, account = handle_login(account_service, student_id, password)

    if success:
        print_success(message)
        input("Press Enter to continue...")
        return account
    else:
        print_error(message)
        input("Press Enter to continue...")
        return None


def show_student_menu():
    clear_screen()
    print_header("Student Main Menu")
    print("1. Book Room")
    print("2. View Rooms")
    print("3. View Account")
    print("4. Checkout")
    print("0. Logout")
    print()


def show_account_details(account_service, student_id: str):
    clear_screen()
    print_header("Account Details")

    success, details, error_msg = get_account_display_data(account_service, student_id)

    if not success:
        print_error(error_msg)
        return

    print_ascii_table(
        ["Field", "Value"],
        [
            ["Student ID", details['student_id']],
            ["Email", details['email']],
            ["Balance", f"{details['balance']} credits"]
        ]
    )

    print()
    print(f"{BOLD}Booking History:{RESET}")

    if details['history']:
        history_headers = ["Booking ID", "Room", "Date", "Time", "Price", "Status"]
        history_rows = []
        for h in details['history']:
            time_str = f"{h['start_time']}-{h['end_time']}"
            history_rows.append([
                h['booking_id'],
                h['room_name'],
                h['date'],
                time_str,
                f"{h['total_price']:.0f}",
                h['status'].upper()
            ])
        print_ascii_table(history_headers, history_rows)
    else:
        print_info("No booking history")

    print_footer()
    input()


def show_booking_flow(booking_service, room_service, student_id: str):
    from services import RoomService, AccountService

    while True:
        clear_screen()
        print_header("Book a Room")

        # Get and validate date
        date = get_input("Enter Date (YYYY-MM-DD)")
        valid, error = validate_date(date)
        if not valid:
            print_error(error)
            input("Press Enter to continue...")
            continue

        # Get and validate time
        start_time = get_input("Enter Start Time (HH:MM)")
        end_time = get_input("Enter End Time (HH:MM)")
        valid, error = validate_time_range(start_time, end_time)
        if not valid:
            print_error(error)
            input("Press Enter to continue...")
            continue

        # Get and validate capacity
        capacity_str = get_input("Enter Minimum Capacity")
        valid, capacity, error = validate_capacity(capacity_str)
        if not valid:
            print_error(error)
            input("Press Enter to continue...")
            continue

        # Filter available rooms
        available_rooms = get_available_rooms(room_service, date, start_time, end_time, capacity)

        if not available_rooms:
            print_warning("No rooms available for the selected criteria")
            print()
            print("1. Try different criteria")
            print("0. Return to Main Menu")
            choice = get_input("Select option")
            if choice == '0':
                return
            continue

        print()
        print(f"{BOLD}Available Rooms:{RESET}")
        room_headers = ["Room ID", "Name", "Capacity", "Price/Hour", "Equipment"]
        room_rows = []
        for r in available_rooms:
            equipment = ', '.join(r.equipment) if r.equipment else 'None'
            room_rows.append([r.room_id, r.name, r.capacity, f"${r.price_per_hour:.2f}", equipment])

        print_ascii_table(room_headers, room_rows)

        print()
        room_id = get_input("Enter Room ID to book (or 0 to go back)")

        if room_id == '0':
            return

        # Double-check availability
        valid, error = handle_room_selection(booking_service, room_id, date, start_time, end_time)
        if not valid:
            print_error(error)
            input("Press Enter to continue...")
            continue

        # Create booking
        room = room_service.get_room(room_id)
        total_price, discount_info = booking_service.calculate_price(start_time, end_time, room.price_per_hour)

        clear_screen()
        print_header("Confirm Booking")
        print_ascii_table(
            ["Detail", "Value"],
            [
                ["Room ID", room_id],
                ["Room Name", room.name],
                ["Date", date],
                ["Time", f"{start_time} - {end_time}"],
                ["Base Price", f"${total_price:.2f}"]
            ]
        )
        if discount_info:
            print(f"\n{SUCCESS}{discount_info}{RESET}")

        confirm = get_yes_no("Confirm booking")
        if not confirm:
            print_info("Booking cancelled")
            input("Press Enter to continue...")
            return

        success, message, _ = create_booking_record(booking_service, student_id, room_id, date, start_time, end_time)

        if success:
            print_success(message)
        else:
            print_error(message)

        input("Press Enter to continue...")
        return


def show_checkout_flow(booking_service, room_service, account_service, student_id: str):
    clear_screen()
    print_header("Checkout")

    pending_list = get_pending_bookings_for_student(booking_service, room_service, student_id)

    if not pending_list:
        print_warning("No pending bookings to checkout")
        print_footer()
        input()
        return

    print(f"{BOLD}Pending Bookings:{RESET}")
    booking_headers = ["Booking ID", "Room ID", "Date", "Time", "Price"]
    booking_rows = []
    for item in pending_list:
        b = item['booking']
        booking_rows.append([
            b.booking_id,
            item['room_name'],
            b.date,
            f"{b.start_time}-{b.end_time}",
            f"${b.total_price:.2f}"
        ])

    print_ascii_table(booking_headers, booking_rows)

    print()
    booking_id = get_input("Enter Booking ID to checkout (or 0 to go back)")

    if booking_id == '0':
        return

    # Find booking
    booking = booking_service.get_booking(booking_id)
    if not booking or booking.student_id != student_id:
        print_error("Booking not found")
        input("Press Enter to continue...")
        return

    if booking.status == "confirmed":
        print_warning("Booking already confirmed")
        input("Press Enter to continue...")
        return

    # Get checkout summary
    summary = get_checkout_summary(booking_service, room_service, booking)

    clear_screen()
    print_header("Checkout Confirmation")
    print_ascii_table(
        ["Detail", "Value"],
        [
            ["Booking ID", booking.booking_id],
            ["Room", summary['room_name']],
            ["Date", booking.date],
            ["Time", f"{booking.start_time} - {booking.end_time}"],
            ["Total Price", f"${summary['total_price']:.2f}"]
        ]
    )

    if summary['discount_info']:
        print(f"\n{SUCCESS}{summary['discount_info']}{RESET}")

    # Check balance
    success, details, error_msg = get_account_display_data(account_service, student_id)
    if not success:
        print_error(error_msg)
        input("Press Enter to continue...")
        return
    print(f"\nYour balance: {details['balance']} credits")

    if details['balance'] < summary['total_price']:
        print_error("[ERROR] Insufficient balance")
        input("Press Enter to continue...")
        return

    confirm = get_yes_no("Confirm checkout")
    if not confirm:
        print_info("Checkout cancelled")
        input("Press Enter to continue...")
        return

    success, message, _ = handle_checkout(booking_service, booking_id, student_id)

    if success:
        print_success(message)
    else:
        print_error(message)

    input("Press Enter to continue...")


def show_admin_menu():
    clear_screen()
    print_header("Administrator Main Menu")
    print("1. Add Room")
    print("2. Delete Room")
    print("3. View All Rooms")
    print("4. View All Bookings")
    print("0. Logout")
    print()


def show_add_room_flow(room_service):
    while True:
        clear_screen()
        print_header("Add New Room")

        room_id = get_input("Enter Room ID")
        name = get_input("Enter Room Name")
        capacity_str = get_input("Enter Capacity")
        price_str = get_input("Enter Price per Hour ($)")

        try:
            capacity = int(capacity_str)
            price = float(price_str)
        except ValueError:
            print_error("Invalid capacity or price")
            input("Press Enter to continue...")
            continue

        # Collect equipment
        equipment = []
        print(f"\n{INFO}Enter equipment (one at a time, or 'done' to finish){RESET}")
        while True:
            eq = get_input("Equipment (or 'done')")
            if eq.lower() == 'done':
                break
            if eq:
                equipment.append(eq)

        success, message = handle_add_room(room_service, room_id, name, capacity, price, equipment)

        if success:
            print_success(message)
        else:
            print_error(message)

        print()
        print("1. Add another room")
        print("0. Return to Admin Menu")
        choice = get_input("Select option")

        if choice == '0':
            return


def show_delete_room_flow(room_service, booking_service):
    clear_screen()
    print_header("Delete Room")

    rooms = room_service.get_all_rooms()

    if not rooms:
        print_warning("No rooms to delete")
        input("Press Enter to continue...")
        return

    print(f"{BOLD}Available Rooms:{RESET}")
    room_headers = ["Room ID", "Name", "Capacity", "Price/Hour"]
    room_rows = []
    for r in rooms:
        room_rows.append([r.room_id, r.name, r.capacity, f"${r.price_per_hour:.2f}"])

    print_ascii_table(room_headers, room_rows)

    print()
    room_id = get_input("Enter Room ID to delete (or 0 to go back)")

    if room_id == '0':
        return

    # Check for future bookings
    future_bookings = booking_service.booking_repo.get_future_bookings(room_id)
    if future_bookings:
        print_error(f"[WARNING] Cannot delete Room {room_id} - there are future bookings")
        input("Press Enter to continue...")
        return

    # Confirmation
    print_warning(f"[CONFIRM] Are you sure you want to delete this room? (Y/N)")
    confirm = get_input("Confirm deletion")

    if confirm.upper() == 'Y':
        success, message = handle_delete_room(room_service, booking_service, room_id, confirm=True)
        if success:
            print_success(message)
        else:
            print_error(message)
    else:
        print_info("Deletion cancelled")

    input("Press Enter to continue...")


def show_all_rooms(room_service):
    clear_screen()
    print_header("All Rooms")

    rooms = room_service.get_all_rooms()

    if not rooms:
        print_warning("No rooms available")
        input("Press Enter to continue...")
        return

    room_headers = ["Room ID", "Name", "Capacity", "Price/Hour", "Equipment"]
    room_rows = []
    for r in rooms:
        equipment = ', '.join(r.equipment) if r.equipment else 'None'
        room_rows.append([r.room_id, r.name, r.capacity, f"${r.price_per_hour:.2f}", equipment])

    print_ascii_table(room_headers, room_rows)

    print_footer()
    input()


def show_all_bookings(booking_service):
    clear_screen()
    print_header("All Bookings")

    bookings = booking_service.booking_repo.get_all()

    if not bookings:
        print_warning("No bookings found")
        input("Press Enter to continue...")
        return

    booking_headers = ["Booking ID", "Student ID", "Room ID", "Date", "Time", "Price", "Status"]
    booking_rows = []
    for b in bookings:
        booking_rows.append([
            b.booking_id,
            b.student_id,
            b.room_id,
            b.date,
            f"{b.start_time}-{b.end_time}",
            f"${b.total_price:.2f}",
            b.status.upper()
        ])

    print_ascii_table(booking_headers, booking_rows)

    print_footer()
    input()


# Import here to avoid circular dependency
from services import AccountService, RoomService, BookingService
