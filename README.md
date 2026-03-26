# FIT5136 自习室预订系统 (MSSRB)

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
├── tests/                   # 单元测试 (pytest)
│   ├── test_registration.py
│   ├── test_account.py
│   ├── test_room_management.py
│   ├── test_booking.py
│   └── test_checkout.py
├── data/                    # CSV 数据文件
│   ├── accounts.csv
│   ├── rooms.csv
│   └── bookings.csv
├── mermaid/                 # Mermaid 流程图 (15个文件)
│   ├── member_a/           # Screen 1, 3, 5 + 异常处理
│   ├── member_b/           # Screen 4, 7, 8 + 异常处理
│   └── member_c/           # Screen 2, 6 + 完整流程 + 图例
├── ui_prototype/            # LucidChart UI原型图
└── presentation/           # PPT演示文稿
```

## 功能特性

### 用户故事 1: 注册与登录
| US | 功能 | 描述 |
|----|------|------|
| US 1.1 | 注册 | 学号纯数字、合法邮箱、密码>6位，注册成功发放50积分 |
| US 1.2 | 登录 | 学生/管理员角色分流 |
| US 1.3 | 查看账户 | 显示学号、邮箱、余额、历史预订记录 |

### 用户故事 2: 房间管理
| US | 功能 | 描述 |
|----|------|------|
| US 2.1 | 添加房间 | 房间号、名称、容量、单价、设备循环输入 |
| US 2.2 | 删除房间 | 未来预订检查、二次确认Y/N |

### 用户故事 3: 预订房间
| US | 功能 | 描述 |
|----|------|------|
| US 3.1 | 筛选房间 | 按日期、时间、最低容量筛选 |
| US 3.2 | 确认预订 | Double-check防重复预订 |

### 用户故事 4: 结账
| US | 功能 | 描述 |
|----|------|------|
| US 4.1 | 结账确认 | 余额校验、扣款、状态更新 |
| US 4.2 | Deal Package | 预订≥4小时享8折优惠 |

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

### 管理员账号
```
用户名: admin
密码: admin123
```

## 使用示例

### 1. 注册新账户
```
选择: 1 (Register)
输入学号: 33445566
输入邮箱: student33445566@student.monash.edu
输入密码: password123
→ [SUCCESS] Registration successful! Initial bonus: 50 credits added!
```

### 2. 登录并预订房间
```
选择: 2 (Login)
输入学号: 33445566
输入密码: password123
→ Welcome back!

主菜单选择: 1 (Book Room)
输入日期: 2026-03-28
输入时间: 14:00 - 18:00
输入容量: 4
→ 选择房间 → 确认预订
→ [DEAL PACKAGE] 4小时以上享8折优惠!
```

### 3. 结账
```
主菜单选择: 4 (Checkout)
选择预订ID: BR-00003
确认? Y
→ [SUCCESS] Booking Confirmed! Amount Paid: $48.00
```

### 4. 管理员操作
```
使用 admin/admin123 登录
主菜单:
  1. Add Room - 添加新房间
  2. Delete Room - 删除房间（二次确认）
  3. View All Rooms - 查看所有房间
  4. View All Bookings - 查看所有预订
  0. Logout - 退出登录
```

## 界面预览

系统采用等宽字体 (Courier New, Consolas) 和颜色标识：

```
==========================================
MSSRB - Checkout Confirmation
==========================================
Booking ID: BR-00003

Room        : Woodside 101
Date        : 2026-03-28
Time        : 14:00 - 18:00 (4 hours)

Pricing Breakdown:
Base Price  : $15/hour x 4 hours = $60.00

[DEAL PACKAGE APPLIED]
4-Hour Special Discount: -20%
Discounted Total  : $48.00

Your Current Balance: 50 credits
After Payment        : 2 credits

Confirm checkout? (Y/N): Y_
```

### 颜色编码
| 颜色 | 含义 | 示例 |
|------|------|------|
| 绿色 (#90EE90) | 成功消息、初始屏幕 | `[SUCCESS] Registration successful` |
| 红色 (#FFB6C1) | 错误、警告、管理员菜单 | `[ERROR] Insufficient balance` |
| 蓝色 (#87CEEB) | 学生屏幕、信息 | Account Details, Student Menu |
| 黄色 (#FFE4B5) | 确认提示 | `Confirm checkout? (Y/N)` |
| 灰色 (#F0F0F0) | 输入字段、数据表格 | `Enter Room ID: _` |

### 学生菜单
```
==========================================
MSSRB - Student Main Menu
==========================================
Logged in as: 33445566 (Student)
Balance: 50 credits
==========================================

1. Book Room     - 筛选并预订房间
2. View Rooms    - 查看所有可用房间
3. View Account  - 查看账户信息和历史记录
4. Checkout      - 结账确认
0. Logout        - 退出登录
```

### 管理员菜单
```
==========================================
MSSRB - Administrator Main Menu
==========================================
Logged in as: Admin
==========================================

1. Add Room          - 添加新房间
2. Delete Room       - 删除房间（二次确认）
3. View All Rooms    - 查看所有房间
4. View All Bookings - 查看所有预订
0. Logout            - 退出登录
```

## 可用性原则 (Ben Shneiderman)

| 原则 | 描述 | 实现 |
|------|------|------|
| P1: 提供反馈 | 每项操作都有明确的系统响应 | 绿色成功、红色错误、黄色确认 |
| P2: 减少记忆负担 | 清晰的标签和导航 | 底部返回提示、步骤指示 |
| P3: 允许撤销 | 确认防止误操作 | Y/N二次确认 |

## 技术栈

- **Python 3** - 编程语言
- **CSV** - 数据持久化
- **pytest** - 单元测试框架
- **Mermaid** - 流程图绘制
- **LucidChart** - UI原型设计

## 测试覆盖

| 测试文件 | 测试数量 | 覆盖功能 |
|----------|----------|----------|
| test_registration.py | 25 | 注册、登录、管理员、参数化场景 |
| test_account.py | - | 账户查看、历史记录 |
| test_room_management.py | - | 添加/删除房间、设备 |
| test_booking.py | - | 筛选、Double-check、预订 |
| test_checkout.py | - | 结账、余额校验、折扣计算 |

**总计: 143 个测试用例，142 通过，1 跳过**

## 开发说明

- 数据存储在 `data/` 目录下的 CSV 文件中
- 测试使用 `pytest` 的 `tmp_path` fixture 创建临时文件
- UI 层与业务逻辑层分离，便于维护
- Mermaid 流程图保存在 `mermaid/` 目录，支持语法验证

## GitHub 仓库

```
https://github.com/alii0110-monash/fit5136-study-room-booking
```
