# Mermaid Flowcharts - FIT5136 Study Room Booking System

## Overview
Mermaid 格式的 UI 流程图，对应 LucidChart 原型设计。

## 任务分配 (根据 ui_prototype.md)

### Member A - 前台与资金流线长
负责：注册/登录、账户历史、结账流程

| 文件 | 描述 |
|------|------|
| `01_welcome_auth.flowchart.mmd` | Screen 1: 欢迎与鉴权（含注册/登录流程） |
| `03_account_history.flowchart.mmd` | Screen 3: 账户与历史页 |
| `05_checkout.flowchart.mmd` | Screen 5: 结账页（含 Deal Package 折扣） |
| `exception_duplicate_id.mmd` | 异常：学号已注册 |
| `exception_insufficient_balance.mmd` | 异常：余额不足 |

### Member B - 预订与后台流线长
负责：筛选预订、添加/删除房间

| 文件 | 描述 |
|------|------|
| `04_booking_flow.flowchart.mmd` | Screen 4: 筛选与预订页（含 Double-check） |
| `07_add_room.flowchart.mmd` | Screen 7: 添加房间（含设备循环输入） |
| `08_delete_room.flowchart.mmd` | Screen 8: 删除房间（含二次确认） |
| `exception_no_rooms.mmd` | 异常：无匹配房间 |
| `exception_double_check_failed.mmd` | 异常：Double-check 失败 |
| `exception_delete_rejected.mmd` | 异常：删除被拒绝（未来预订存在） |

### Member C - 全局架构与规范卫士
负责：主菜单、完整流程图、图例

| 文件 | 描述 |
|------|------|
| `02_student_menu.flowchart.mmd` | Screen 2: 学生主菜单 |
| `06_admin_menu.flowchart.mmd` | Screen 6: 管理员主菜单 |
| `09_complete_system_flow.mmd` | 完整系统流程图（所有屏幕集成） |
| `10_legend.mmd` | 图例与颜色说明 |

## 设计规范 (drawing.md)

### 颜色编码
| 颜色 | 含义 |
|------|------|
| `#90EE90` 绿色 | 成功消息、初始屏幕 |
| `#FFB6C1` 红色 | 错误、警告、管理员菜单 |
| `#87CEEB` 蓝色 | 学生屏幕、信息 |
| `#FFE4B5` 黄色 | 确认提示 |
| `#F0F0F0` 灰色 | 输入字段、数据表格 |

### 可用性原则 (Ben Shneiderman)
- **P1**: 提供反馈 - 绿色成功、红色错误、黄色确认
- **P2**: 减少记忆负担 - 清晰的标签和导航
- **P3**: 允许撤销 - Y/N 确认防止误操作

## 查看方式

### VS Code
安装 "Mermaid Preview" 插件，直接打开 `.mmd` 文件预览。

### 在线
- https://mermaid.live
- https://mermaid.js.org/live_editor

## 文件统计
- **Member A**: 5 个文件
- **Member B**: 6 个文件
- **Member C**: 4 个文件
- **总计**: 15 个 Mermaid 图表
