"""
Integration Tests for FIT5136 Study Room Booking System
Tests real data persistence and cross-module workflows
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services import AccountService, RoomService, BookingService
from repositories import AccountRepository, RoomRepository, BookingRepository
from datetime import datetime, timedelta


@pytest.fixture
def clean_data_dir():
    """Backup and restore real data directory."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    backup_dir = os.path.join(data_dir, 'backup')

    # Backup existing files
    os.makedirs(backup_dir, exist_ok=True)
    for f in ['accounts.csv', 'rooms.csv', 'bookings.csv']:
        src = os.path.join(data_dir, f)
        bkp = os.path.join(backup_dir, f)
        if os.path.exists(src):
            with open(src, 'r') as sf:
                with open(bkp, 'w') as bf:
                    bf.write(sf.read())

    # Initialize empty files
    for f in ['accounts.csv', 'rooms.csv', 'bookings.csv']:
        src = os.path.join(data_dir, f)
        if f == 'accounts.csv':
            with open(src, 'w') as sf:
                sf.write("student_id,email,password,balance\n")
        elif f == 'rooms.csv':
            with open(src, 'w') as sf:
                sf.write("room_id,name,capacity,price_per_hour,equipment\n")
        elif f == 'bookings.csv':
            with open(src, 'w') as sf:
                sf.write("booking_id,student_id,room_id,date,start_time,end_time,total_price,status\n")

    yield data_dir

    # Restore backup
    for f in ['accounts.csv', 'rooms.csv', 'bookings.csv']:
        src = os.path.join(data_dir, f)
        bkp = os.path.join(backup_dir, f)
        if os.path.exists(bkp):
            with open(bkp, 'r') as bf:
                with open(src, 'w') as sf:
                    sf.write(bf.read())


def test_registration_persists_to_csv(clean_data_dir):
    """验证注册数据真正写入CSV文件"""
    service = AccountService()

    result = service.register("33445566", "student33445566@student.monash.edu", "password123")
    assert result.success is True

    # 读取真实CSV验证
    csv_path = os.path.join(clean_data_dir, 'accounts.csv')
    with open(csv_path, 'r') as f:
        content = f.read()
        assert "33445566" in content
        assert "student33445566@student.monash.edu" in content
        assert "50" in content  # initial balance


def test_login_after_restart(clean_data_dir):
    """验证重启后仍能登录"""
    # 注册
    service = AccountService()
    service.register("33445566", "student33445566@student.monash.edu", "password123")

    # 模拟重启 - 创建新的service实例
    new_service = AccountService()
    account = new_service.login("33445566", "password123")

    assert account is not None
    assert account.student_id == "33445566"


def test_room_persists_and_retrieved(clean_data_dir):
    """验证房间数据持久化和检索"""
    room_service = RoomService()

    room_service.add_room("101", "Woodside Study Room 101", 4, 15.0, ["Whiteboard", "TV"])

    # 模拟重启 - 创建新实例
    new_room_service = RoomService()
    rooms = new_room_service.get_all_rooms()

    assert len(rooms) == 1
    assert rooms[0].room_id == "101"
    assert rooms[0].name == "Woodside Study Room 101"


def test_booking_checkout_workflow(clean_data_dir):
    """测试预订 -> 结账完整流程"""
    account_service = AccountService()
    room_service = RoomService()
    booking_service = BookingService()

    # 注册用户
    account_service.register("33445566", "student@monash.edu", "password123")

    # 添加房间
    room_service.add_room("101", "Study Room 101", 4, 15.0, [])

    # 创建预订
    result = booking_service.create_booking("33445566", "101", "2026-03-28", "10:00", "12:00")
    assert result.success is True
    booking_id = result.data['booking'].booking_id

    # 结账
    result = booking_service.checkout(booking_id, "33445566")
    assert result.success is True

    # 验证账户余额减少
    details = account_service.get_account_details("33445566")
    assert details['balance'] == 20  # 50 - 30 (2 hours * 15/hour) = 20

    # 验证预订状态变为confirmed
    booking = booking_service.get_booking(booking_id)
    assert booking.status == "confirmed"


def test_full_user_journey(clean_data_dir):
    """测试完整用户旅程: 注册 -> 登录 -> 查看账户 -> 预订 -> 结账"""
    account_service = AccountService()
    room_service = RoomService()
    booking_service = BookingService()

    # 1. 注册
    result = account_service.register("33445566", "student@monash.edu", "password123")
    assert result.success is True

    # 2. 登录
    account = account_service.login("33445566", "password123")
    assert account is not None

    # 3. 查看账户
    details = account_service.get_account_details("33445566")
    assert details['balance'] == 50
    assert len(details['history']) == 0

    # 4. 管理员添加房间
    admin_service = RoomService()
    admin_service.add_room("101", "Study Room 101", 4, 15.0, ["Whiteboard"])

    # 5. 用户预订
    result = booking_service.create_booking("33445566", "101", "2026-04-01", "09:00", "13:00")
    assert result.success is True
    # 4小时应该享受8折: 4*15*0.8 = 48

    # 6. 结账
    booking_id = result.data['booking'].booking_id
    result = booking_service.checkout(booking_id, "33445566")
    assert result.success is True

    # 7. 验证最终余额 50 - 48 = 2
    details = account_service.get_account_details("33445566")
    assert details['balance'] == 2
    assert len(details['history']) == 1
    assert details['history'][0]['status'] == "confirmed"
