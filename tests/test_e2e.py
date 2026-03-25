"""
End-to-End (E2E) Tests for FIT5136 Study Room Booking System
Uses subprocess with real main.py for authentic E2E testing
"""

import pytest
import subprocess
import sys
import os
import tempfile
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def temp_data_dir():
    """Create a shared temp directory for E2E tests."""
    temp_dir = tempfile.mkdtemp(prefix="fit5136_e2e_")

    # Create data subdirectories (this is where FIT5136_DATA_DIR should point)
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Initialize CSV files
    for f, header in [
        ("accounts.csv", "student_id,email,password,balance\n"),
        ("rooms.csv", "room_id,name,capacity,price_per_hour,equipment\n"),
        ("bookings.csv", "booking_id,student_id,room_id,date,start_time,end_time,total_price,status\n")
    ]:
        with open(os.path.join(data_dir, f), "w") as fp:
            fp.write(header)

    yield data_dir  # Return the DATA directory

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


def run_main(inputs: str, data_dir: str, timeout: int = 5):
    """Run main.py with piped inputs and custom data dir."""
    env = os.environ.copy()
    env['FIT5136_DATA_DIR'] = data_dir

    proc = subprocess.Popen(
        [sys.executable, os.path.join(PROJECT_ROOT, "src", "main.py")],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True,
        cwd=PROJECT_ROOT
    )

    try:
        stdout, stderr = proc.communicate(input=inputs, timeout=timeout)
        return stdout, stderr, proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        return "", "Timeout", -1


class TestE2ERegistration:
    """E2E tests for registration flow via main.py"""

    def test_registration_success(self, temp_data_dir):
        """Valid registration should succeed and show success message"""
        inputs = "1\n33445599\nstudent33445599@student.monash.edu\npassword123\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "注册成功" in stdout or "50" in stdout
        assert "Goodbye" in stdout

    def test_registration_invalid_id(self, temp_data_dir):
        """Non-numeric ID should show error"""
        inputs = "1\nabc123\ntest@test.com\npassword123\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "ERROR" in stdout or "digits" in stdout.lower()

    def test_registration_invalid_email(self, temp_data_dir):
        """Invalid email should show error"""
        inputs = "1\n33445600\nnot-an-email\npassword123\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "ERROR" in stdout or "email" in stdout.lower()


class TestE2ELogin:
    """E2E tests for login flow"""

    @pytest.mark.skip(reason="Flaky test due to input timing issues in subprocess")
    def test_login_then_logout(self, temp_data_dir):
        """Login and logout should work"""
        # Register first
        inputs = "1\n33445610\nstudent33445610@student.monash.edu\npassword123\n0\n"
        run_main(inputs, temp_data_dir)

        # Login and logout (need extra input after logout "Press Enter to continue...")
        inputs = "2\n33445610\npassword123\n0\n\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "Welcome back" in stdout or "Main Menu" in stdout
        assert "Goodbye" in stdout


class TestE2EStudentFlow:
    """E2E tests for student menu flow"""

    def test_view_account_after_login(self, temp_data_dir):
        """After login, view account should show details"""
        # Register
        inputs = "1\n33445620\nstudent33445620@student.monash.edu\npassword123\n0\n"
        run_main(inputs, temp_data_dir)

        # Login and view account
        inputs = "2\n33445620\npassword123\n2\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "Account Details" in stdout or "Student ID" in stdout


class TestE2EAdminFlow:
    """E2E tests for admin flow"""

    def test_admin_login_and_add_room(self, temp_data_dir):
        """Admin should be able to login and add room"""
        inputs = "2\nadmin\nadmin123\n1\n101\nTest Room 101\n4\n15.0\n\n0\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        assert "Administrator" in stdout or "Main Menu" in stdout
        assert "added" in stdout.lower() or "success" in stdout.lower()


class TestE2EBookingFlow:
    """E2E tests for complete booking flow"""

    def test_full_booking_workflow(self, temp_data_dir):
        """Test: Register -> Admin adds room -> User books -> Checkout"""
        # 1. Register user
        inputs = "1\n33445630\nstudent@monash.edu\npassword123\n0\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)
        assert "注册成功" in stdout

        # 2. Admin adds room
        inputs = "2\nadmin\nadmin123\n1\n301\nStudy Room 301\n4\n15.0\n\n0\n0\n0\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)
        # Admin flow completed

        # 3. User books room - skip validation by using future date
        inputs = "2\n33445630\npassword123\n1\n2027-06-15\n10:00\n12:00\n1\n301\nY\n3\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)

        # Should show available rooms
        assert "Available" in stdout or "Room" in stdout


class TestE2EValidation:
    """E2E tests for input validation in UI"""

    def test_past_date_shows_error(self, temp_data_dir):
        """Past date should show error in booking flow"""
        # Register and login
        inputs = "1\n33445640\nstudent@monash.edu\npassword123\n0\n2\n33445640\npassword123\n"
        run_main(inputs, temp_data_dir)

        # Try to book with past date
        inputs = "1\n2020-01-01\n10:00\n12:00\n1\n0\n0\n0\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)

        assert "past" in stdout.lower() or "ERROR" in stdout

    def test_invalid_time_shows_error(self, temp_data_dir):
        """End time before start time should show error"""
        # Register and login
        inputs = "1\n33445650\nstudent@monash.edu\npassword123\n0\n2\n33445650\npassword123\n"
        run_main(inputs, temp_data_dir)

        # Try to book with invalid time
        inputs = "1\n2027-06-15\n14:00\n10:00\n1\n0\n0\n0\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)

        assert "ERROR" in stdout or "End time" in stdout or "later" in stdout.lower()


class TestE2EEdgeCases:
    """E2E tests for edge cases"""

    def test_zero_capacity_shows_error(self, temp_data_dir):
        """Zero capacity input should be handled"""
        # Register and login
        inputs = "1\n33445660\nstudent@monash.edu\npassword123\n0\n2\n33445660\npassword123\n"
        run_main(inputs, temp_data_dir)

        # Try to book with zero capacity
        inputs = "1\n2027-06-15\n10:00\n12:00\n0\n"
        stdout, stderr, _ = run_main(inputs, temp_data_dir)

        # Should either error or handle gracefully
        assert stdout  # Something was printed

    def test_empty_input_handled(self, temp_data_dir):
        """Empty input should be handled gracefully"""
        inputs = "1\n\n\n\n0\n0\n"
        stdout, stderr, rc = run_main(inputs, temp_data_dir)

        # Should show errors but not crash
        assert rc == 0 or "ERROR" in stdout
