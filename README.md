# FIT5136 自习室预订系统

一个纯文本终端自习室预订系统，支持学生注册登录、房间管理、预订和结账功能。

## 项目结构

```
/home/li/tmp/5136/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── main.py              # 主程序入口
│   ├── models.py            # 数据模型 (Account, Room, Booking)
│   ├── services.py          # 业务逻辑层
│   ├── repositories.py      # CSV 持久化层
│   └── ui.py                # 终端UI界面
├── tests/                   # 单元测试
│   ├── test_registration.py
│   ├── test_account.py
│   ├── test_room_management.py
│   ├── test_booking.py
│   └── test_checkout.py
├── data/                    # CSV 数据文件
│   ├── accounts.csv
│   ├── rooms.csv
│   └── bookings.csv
├── ui_prototype/            # LucidChart UI原型图
└── presentation/           # PPT演示文稿
```

## 功能特性

### 用户故事 1: 注册与登录
- **US 1.1** 注册与登录
  - 学号必须为纯数字
  - 邮箱格式验证
  - 密码长度 > 6 位
  - 注册成功发放 50 积分初始体验金
  - 管理员账号: `admin` / `admin123`

- **US 1.2** 查看账户信息
  - 显示学号、邮箱、余额
  - 显示历史预订记录

- **US 1.3** 查看所有房间
  - 学生可查看所有可用房间
  - 无需筛选条件，快速浏览

### 用户故事 2: 房间管理
- **US 2.1** 添加房间
  - 设置房间号、名称、容量、单价
  - 循环输入设备列表

- **US 2.2** 删除房间
  - 检查未来预订，有则拒绝删除
  - 二次确认 Y/N

### 用户故事 3: 预订房间
- **US 3.1** 筛选可用房间
  - 按日期、时间、 minimum 容量筛选
  - 过滤已预订冲突的房间

- **US 3.2** 确认预订
  - Double-check 防止重复预订
  - 生成预订ID

### 用户故事 4: 结账
- **US 4.1** 结账确认
  - 余额校验
  - 扣款并更新状态为 confirmed

- **US 4.2** Deal Package 折扣
  - 预订 ≥4 小时享受 8 折优惠

## 快速开始

### 运行测试
```bash
cd /home/li/tmp/5136
python -m pytest tests/ -v
```

### 运行程序
```bash
python src/main.py
```

### 使用示例

1. **注册新账户**
   ```
   选择: 1 (Register)
   输入学号: 33445566
   输入邮箱: student33445566@student.monash.edu
   输入密码: password123
   ```

2. **登录并预订房间**
   ```
   选择: 2 (Login)
   输入学号: 33445566
   输入密码: password123
   选择: 1 (Book Room)
   输入日期: 2026-03-28
   输入时间: 10:00 - 12:00
   输入容量: 4
   选择房间并确认预订
   ```

3. **结账**
   ```
   主菜单选择: 4 (Checkout)
   选择预订ID进行结账
   ```

4. **管理员操作**
   ```
   使用 admin/admin123 登录
   可进行添加/删除房间操作
   ```

## 界面预览

系统采用等宽字体 (Courier New, Consolas) 和颜色标识：

| 颜色 | 含义 |
|------|------|
| 绿色 | 成功消息 |
| 红色 | 错误消息 |
| 黄色 | 警告/确认提示 |
| 蓝色 | 信息提示 |

ASCII 表格展示数据和导航菜单。

## 技术栈

- **Python 3** - 编程语言
- **CSV** - 数据持久化
- **pytest** - 单元测试框架

## 测试覆盖

| 测试文件 | 测试数量 | 覆盖功能 |
|----------|----------|----------|
| test_registration.py | 25 | 注册、登录、管理员、参数化场景 |
| test_ui.py | 31 | UI层验证函数、处理器 |
| test_validation.py | 50 | 日期/时间验证、容量、折扣计算 |
| test_e2e.py | 36 | 端到端流程测试 |
| test_integration.py | - | 集成测试 |

**总计: 143 个测试用例，142 通过，1 跳过**

### 学生菜单
```
1. Book Room     - 筛选并预订房间
2. View Rooms    - 查看所有可用房间
3. View Account  - 查看账户信息和历史记录
4. Checkout      - 结账确认
0. Logout        - 退出登录
```

### 管理员菜单
```
1. Add Room          - 添加新房间
2. Delete Room       - 删除房间（二次确认）
3. View All Rooms    - 查看所有房间
4. View All Bookings - 查看所有预订
0. Logout            - 退出登录
```

## 开发说明

- 数据存储在 `data/` 目录下的 CSV 文件中
- 测试使用 `pytest` 的 `tmp_path` fixture 创建临时文件
- UI 层与业务逻辑层分离，便于维护
