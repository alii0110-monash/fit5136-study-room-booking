# Mermaid Flowcharts - FIT5136 Study Room Booking System

## Overview

Mermaid 格式的 UI 流程图，对应 LucidChart 原型设计。所有屏幕采用完整的终端界面展示，包含标题、用户信息、定价明细、导航选项等。

## 文件列表

### Member A - 前台与资金流线长
**负责：注册/登录、账户历史、结账流程**

| 文件 | Screen | 描述 |
|------|--------|------|
| `01_welcome_auth.flowchart.mmd` | Screen 1 | 欢迎与鉴权（含注册/登录流程、管理员分支） |
| `03_account_history.flowchart.mmd` | Screen 3 | 账户与历史页（含预订历史表格） |
| `05_checkout.flowchart.mmd` | Screen 5 | 结账页（含 Deal Package 折扣明细） |
| `exception_duplicate_id.mmd` | - | 异常：学号已注册 |
| `exception_insufficient_balance.mmd` | - | 异常：余额不足 |

### Member B - 预订与后台流线长
**负责：筛选预订、添加/删除房间**

| 文件 | Screen | 描述 |
|------|--------|------|
| `04_booking_flow.flowchart.mmd` | Screen 4 | 筛选与预订页（含 Double-check 确认） |
| `07_add_room.flowchart.mmd` | Screen 7 | 添加房间（含设备循环输入） |
| `08_delete_room.flowchart.mmd` | Screen 8 | 删除房间（含 WARNING 二次确认） |
| `exception_no_rooms.mmd` | - | 异常：无匹配房间 |
| `exception_double_check_failed.mmd` | - | 异常：Double-check 失败（房间已被预订） |
| `exception_delete_rejected.mmd` | - | 异常：删除被拒绝（未来预订存在） |

### Member C - 全局架构与规范卫士
**负责：主菜单、完整流程图、图例**

| 文件 | Screen | 描述 |
|------|--------|------|
| `02_student_menu.flowchart.mmd` | Screen 2 | 学生主菜单 |
| `06_admin_menu.flowchart.mmd` | Screen 6 | 管理员主菜单 |
| `09_complete_system_flow.mmd` | - | 完整系统流程图（所有屏幕集成） |
| `10_legend.mmd` | - | 图例与颜色说明、可用性原则 |

## 设计规范

### 屏幕格式
每个屏幕节点包含完整的终端界面：
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
| 颜色 | Hex | 含义 |
|------|-----|------|
| 绿色 | `#90EE90` | 成功消息、初始屏幕 |
| 红色 | `#FFB6C1` | 错误、警告、管理员菜单 |
| 蓝色 | `#87CEEB` | 学生屏幕、信息 |
| 黄色 | `#FFE4B5` | 确认提示 |
| 灰色 | `#F0F0F0` | 输入字段、数据表格 |
| 紫色 | `#E6E6FA` | 可用性原则区域 |

### 可用性原则 (Ben Shneiderman)
| 原则 | 标注 | 描述 |
|------|------|------|
| P1 | `[P1: Offer informative feedback]` | 提供反馈 - 绿色成功、红色错误、黄色确认 |
| P2 | `[P2: Reduce memory load]` | 减少记忆负担 - 清晰的标签和导航 |
| P3 | `[P3: Permit reversible actions]` | 允许撤销 - Y/N 确认防止误操作 |

## 查看方式

### VS Code
安装 "Mermaid Preview" 插件，直接打开 `.mmd` 文件预览。

### 在线编辑器
- https://mermaid.live
- https://mermaid.js.org/live_editor

### 本地验证
```bash
node validate-mermaid.js
```

## 文件统计
- **Member A**: 5 个文件
- **Member B**: 6 个文件
- **Member C**: 4 个文件
- **总计**: 15 个 Mermaid 图表

## 关键功能标注

### Deal Package 折扣 (US 4.2)
```
[DEAL PACKAGE APPLIED]
4-Hour Special Discount: -20%
Discounted Total  : $48.00
```

### Double-check 确认 (US 3.2)
```
[WARNING] Room No Longer Available
The room you selected was just booked by another user.
```

### 删除确认 (US 2.2)
```
[P3: Permit reversible actions]
[WARNING] Confirmation Required
Are you sure you want to delete this room?
Confirm? (Y/N): Y_
```

### 角色分流 (US 1.1)
```
L2 -->|"Student"| STUDENT_MENU["Screen 2: Student Menu"]
L2 -->|"Admin"| ADMIN_MENU["Screen 6: Admin Menu"]
```
