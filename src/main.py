#!/usr/bin/env python3
"""
FIT5136 Study Room Booking System
Main Entry Point
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services import AccountService, RoomService, BookingService
from repositories import AccountRepository, RoomRepository, BookingRepository
from ui import (
    clear_screen,
    show_welcome_screen,
    show_registration_flow,
    show_login_flow,
    show_student_menu,
    show_account_details,
    show_booking_flow,
    show_checkout_flow,
    show_admin_menu,
    show_add_room_flow,
    show_delete_room_flow,
    show_all_rooms,
    show_all_bookings,
    get_input,
    print_error,
    print_success,
    print_header,
    SUCCESS,
    ERROR
)


class App:
    def __init__(self):
        # Create shared repositories
        account_repo = AccountRepository()
        room_repo = RoomRepository()
        booking_repo = BookingRepository()

        # Create services with shared repositories
        self.account_service = AccountService(account_repo, booking_repo, room_repo)
        self.room_service = RoomService(room_repo, booking_repo)
        self.booking_service = BookingService(booking_repo, room_repo, account_repo)
        self.current_user = None
        self.is_admin = False

    def run(self):
        """Main application loop."""
        while True:
            if self.current_user is None:
                self._run_auth_flow()
            elif self.is_admin:
                self._run_admin_flow()
            else:
                self._run_student_flow()

    def _run_auth_flow(self):
        """Handle unauthenticated user flow."""
        show_welcome_screen()
        choice = get_input("Select option")

        if choice == '1':
            self.show_registration()
        elif choice == '2':
            self.show_login()
        elif choice == '0':
            self.exit_app()
        else:
            print_error("Invalid option. Please try again.")
            input("Press Enter to continue...")

    def show_registration(self):
        """Handle user registration."""
        result = show_registration_flow(self.account_service)
        # show_registration_flow handles its own success/failure UI
        # Just return to main menu
        pass

    def show_login(self):
        """Handle user login."""
        account = show_login_flow(self.account_service)
        if account:
            self.current_user = account
            self.is_admin = (account.student_id == "admin")

    def _run_student_flow(self):
        """Handle authenticated student flow."""
        show_student_menu()
        choice = get_input("Select option")

        if choice == '1':
            self.show_booking()
        elif choice == '2':
            self.show_rooms()
        elif choice == '3':
            self.show_account()
        elif choice == '4':
            self.show_checkout()
        elif choice == '0':
            self.logout()
        else:
            print_error("Invalid option. Please try again.")
            input("Press Enter to continue...")

    def show_booking(self):
        """Handle room booking flow."""
        show_booking_flow(self.booking_service, self.room_service, self.current_user.student_id)

    def show_account(self):
        """Handle account details view."""
        show_account_details(self.account_service, self.current_user.student_id)

    def show_rooms(self):
        """Show all rooms."""
        show_all_rooms(self.room_service)

    def show_checkout(self):
        """Handle checkout flow."""
        show_checkout_flow(self.booking_service, self.room_service, self.account_service, self.current_user.student_id)

    def _run_admin_flow(self):
        """Handle admin flow."""
        show_admin_menu()
        choice = get_input("Select option")

        if choice == '1':
            self.show_add_room()
        elif choice == '2':
            self.show_delete_room()
        elif choice == '3':
            self.show_rooms()
        elif choice == '4':
            self.show_bookings()
        elif choice == '0':
            self.logout()
        else:
            print_error("Invalid option. Please try again.")
            input("Press Enter to continue...")

    def show_add_room(self):
        """Handle add room flow."""
        show_add_room_flow(self.room_service)

    def show_delete_room(self):
        """Handle delete room flow."""
        show_delete_room_flow(self.room_service, self.booking_service)

    def show_rooms(self):
        """Show all rooms."""
        show_all_rooms(self.room_service)

    def show_bookings(self):
        """Show all bookings."""
        show_all_bookings(self.booking_service)

    def logout(self):
        """Logout current user."""
        self.current_user = None
        self.is_admin = False
        print_success("Logged out successfully!")
        input("Press Enter to continue...")

    def exit_app(self):
        """Exit the application."""
        clear_screen()
        print_header("Goodbye!")
        print(f"{SUCCESS}Thank you for using FIT5136 Study Room Booking System!{SUCCESS}")
        print()
        sys.exit(0)


def main():
    """Application entry point."""
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("\n")
        print(f"{ERROR}Application interrupted. Goodbye!{ERROR}")
        sys.exit(0)
    except Exception as e:
        print(f"{ERROR}An error occurred: {str(e)}{ERROR}")
        raise


if __name__ == "__main__":
    main()
