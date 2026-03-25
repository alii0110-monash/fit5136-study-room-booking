import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services import AccountService
from repositories import AccountRepository


@pytest.fixture
def account_service(tmp_path):
    """Create account service with temporary CSV file."""
    csv_path = tmp_path / "accounts.csv"
    csv_path.write_text("student_id,email,password,balance\n")
    repo = AccountRepository(str(csv_path))
    return AccountService(repo)


def test_registration_success(account_service):
    """AC1: Valid student ID, email, password>6chars -> success with 50 credits"""
    result = account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    assert result.success is True
    assert "50" in result.message


def test_registration_duplicate_student_id(account_service):
    """AC2: Duplicate student ID -> error"""
    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    result = account_service.register("33445566", "another@student.monash.edu", "pass1234")
    assert result.success is False
    assert "already registered" in result.message


def test_registration_invalid_email(account_service):
    """AC1: Invalid email format -> error"""
    result = account_service.register("33445567", "not-an-email", "password123")
    assert result.success is False
    assert "email" in result.message.lower()


def test_registration_student_id_not_numeric(account_service):
    """AC1: Student ID must be numeric -> error"""
    result = account_service.register("abc123", "student@monash.edu", "password123")
    assert result.success is False
    assert "numbers only" in result.message.lower()


def test_registration_password_too_short(account_service):
    """AC1: Password <= 6 chars -> error"""
    result = account_service.register("33445568", "student33445568@student.monash.edu", "short")
    assert result.success is False
    assert "6" in result.message


def test_login_success(account_service):
    """Login success returns account."""
    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    account = account_service.login("33445566", "password123")
    assert account is not None
    assert account.student_id == "33445566"


def test_login_wrong_password(account_service):
    """Wrong password returns None."""
    account_service.register("33445566", "student33445566@student.monash.edu", "password123")
    account = account_service.login("33445566", "wrongpassword")
    assert account is None


def test_login_nonexistent_student(account_service):
    """Login with non-existent student returns None."""
    account = account_service.login("99999999", "password123")
    assert account is None


def test_admin_login():
    """Admin login with special credentials."""
    service = AccountService()
    admin = service.login("admin", "admin123")
    assert admin is not None
    assert admin.student_id == "admin"


# =============================================================================
# Parametrized Table-Driven Tests - Cover Multiple Scenarios in One Test
# =============================================================================

@pytest.mark.parametrize("student_id,email,password,should_pass,expected_hint", [
    # Valid cases
    ("33445566", "student@monash.edu", "password123", True, None),
    ("12345678", "user@student.monash.edu", "securepass", True, None),
    ("99999999", "test@test.com", "longenoughpassword", True, None),

    # Invalid student_id cases
    ("abc123", "test@test.com", "password123", False, "numbers only"),
    ("abc", "test@test.com", "password123", False, "numbers only"),
    ("12abc34", "test@test.com", "password123", False, "numbers only"),
    ("", "test@test.com", "password123", False, "numbers only"),

    # Invalid email cases
    ("33445501", "not-email", "password123", False, "email"),
    ("33445502", "@monash.edu", "password123", False, "email"),
    ("33445503", "student@", "password123", False, "email"),
    ("33445504", "student@.edu", "password123", False, "email"),
    ("33445505", "student monash", "password123", False, "email"),

    # Invalid password cases
    ("33445510", "test@test.com", "short", False, "6"),
    ("33445511", "test@test.com", "123456", False, "6"),
    ("33445512", "test@test.com", "a", False, "6"),
    ("33445513", "test@test.com", "", False, "6"),
], ids=lambda x: f"{'pass' if len(str(x)) > 20 else x}"[:20])
def test_registration_all_scenarios(account_service, student_id, email, password, should_pass, expected_hint):
    """Table-driven test: validate registration with multiple input combinations."""
    result = account_service.register(student_id, email, password)

    if should_pass:
        assert result.success is True, f"Expected success for {student_id}, {email}, but got: {result.message}"
        assert "50" in result.message
    else:
        assert result.success is False, f"Expected failure for {student_id}, {email}, but got success"
        assert expected_hint.lower() in result.message.lower(), \
            f"Expected '{expected_hint}' in message, got: {result.message}"
