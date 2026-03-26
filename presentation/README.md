# FIT5136 Study Room Booking System - Presentation

## 演示文稿

`FIT5136_S1_2026_AppliedXX_TeamX_A1-presentation.pptx`

## 幻灯片结构

| # | 幻灯片 | 内容 |
|---|--------|------|
| 1 | Title Slide | FIT5136_S1_2026_AppliedXX_TeamX_A1-presentation |
| 2 | Agenda | 四大板块概览 |
| 3 | System Overview | High-level flow + 需求对齐 |
| 4 | User Story 1 & 2 | 注册/登录、账户管理 + 截图演示 |
| 5 | User Story 3 | 预订流程 + UI原型 |
| 6 | Usability Principles | Ben Shneiderman三大原则 + 设计证据 |
| 7 | Summary | 关键成果 |
| 8 | LucidChart Link | 完整UI原型链接 |
| 9 | AI Declaration | AI工具使用声明 |
| 10 | Cover Sheet | 附录 |

## 演讲时间分配

| Section | Time | Speaker | Description |
|---------|------|---------|-------------|
| Opening | 2 min (120s) | Member 1 | 开场概览 |
| US 1&2 | 3 min (180s) | Members 2&3 | 注册登录、账户管理 |
| US 3 + UI | 2 min (120s) | Member 4 | 预订流程 + UI演示 |
| Usability + Summary | 1.5 min (90s) | Member 5 | 可用性原则 + 总结 |
| Q&A Buffer | 1.5 min (90s) | All | 问答缓冲 |
| **Total** | **10 min (600s)** | - | - |

## 视觉要求

- **高对比度**: 黑底白字 或 白底黑字
- **大字体**: 确保最后一排可见
- **非拥挤**: 充足留白
- **无障碍**: 颜色+文字双重标识

## 内容要点

### 系统功能 (US 1-4)
1. **注册登录**: 学号验证、邮箱格式、初始50积分
2. **房间管理**: 添加/删除、设备配置、未来预订检查
3. **预订流程**: 日期时间筛选、容量过滤、Double-check
4. **结账**: 余额校验、Deal Package 8折优惠

### 可用性原则
| 原则 | 实现 |
|------|------|
| P1: 提供反馈 | 绿色成功 `[SUCCESS]`、红色错误 `[ERROR]`、黄色确认 |
| P2: 减少记忆负担 | 底部返回提示、步骤指示、清晰标签 |
| P3: 允许撤销 | Y/N 二次确认防止误操作 |

### Deal Package 折扣
```
预订 ≥4 小时 → 总价 8 折
示例: 4小时 x $15 = $60 → 折扣后 $48
```

### Double-check
```
在最终确认前，系统再次检查房间可用性
如果已被预订 → [WARNING] Room No Longer Available
```

## 链接

- **LucidChart**: 完整UI原型
- **GitHub**: https://github.com/alii0110-monash/fit5136-study-room-booking
