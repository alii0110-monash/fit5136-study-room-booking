# UI Prototype (LucidChart)

## 概述

UI 原型设计基于 FIT5136 Study Room Booking System 的用户故事，使用 LucidChart 绘制终端界面流程图。

## 屏幕列表

### Member A (Screens 1, 3, 5 + Exception Screens)
| Screen | 文件 | 描述 |
|--------|------|------|
| Screen 1 | 01_welcome_auth | 欢迎与鉴权（含管理员分支） |
| Screen 3 | 03_account_history | 账户与历史页 |
| Screen 5 | 05_checkout | 结账页（含 Deal Package） |
| Exception | exception_duplicate_id | 学号已注册 |
| Exception | exception_insufficient_balance | 余额不足 |

### Member B (Screens 4, 7, 8 + Exception Screens)
| Screen | 文件 | 描述 |
|--------|------|------|
| Screen 4 | 04_booking_flow | 筛选与预订（含 Double-check） |
| Screen 7 | 07_add_room | 添加房间（含设备循环） |
| Screen 8 | 08_delete_room | 删除房间（含 WARNING 确认） |
| Exception | exception_no_rooms | 无匹配房间 |
| Exception | exception_double_check_failed | Double-check 失败 |
| Exception | exception_delete_rejected | 删除被拒绝 |

### Member C (Screens 2 & 6 + Integration)
| Screen | 文件 | 描述 |
|--------|------|------|
| Screen 2 | 02_student_menu | 学生主菜单 |
| Screen 6 | 06_admin_menu | 管理员主菜单 |
| Complete | 09_complete_system_flow | 完整系统流程图 |
| Legend | 10_legend | 图例与颜色说明 |

## 设计规范

### 颜色编码
| 颜色 | Hex | 含义 |
|------|-----|------|
| 绿色 | `#90EE90` | 成功消息、初始屏幕 |
| 红色 | `#FFB6C1` | 错误、警告、管理员菜单 |
| 蓝色 | `#87CEEB` | 学生屏幕、信息 |
| 黄色 | `#FFE4B5` | 确认提示 |
| 灰色 | `#F0F0F0` | 输入字段、数据表格 |

### 可用性原则 (Ben Shneiderman)
- **P1**: 提供反馈 - 绿色成功、红色错误、黄色确认
- **P2**: 减少记忆负担 - 清晰的标签和导航
- **P3**: 允许撤销 - Y/N 确认防止误操作

### 关键标注
1. **[START HERE]** - Screen 1 上方醒目标签
2. **闭环验证** - Logout 箭头指回 Screen 1
3. **Mock Data** - 真实数据示例（蒙纳士学号、房间名）
4. **P1/P2/P3** - 可用性原则英文标注

## 导出说明

1. 创建 LucidChart 文档
2. 每个屏幕设计为独立框架
3. 导出为图片或可分享链接
4. 添加屏幕间导航箭头
5. 包含图例和可用性原则标注

## Mermaid 同步

Mermaid 流程图保存在 `/mermaid/` 目录，与 LucidChart 保持同步。

```bash
# 验证 Mermaid 语法
node validate-mermaid.js
```
