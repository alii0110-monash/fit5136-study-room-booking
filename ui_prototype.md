# UI Prototype
## UI Prototype 团队任务分配清单
### [成员A] 前台与资金流线长
**核心职责**：负责绘制学生注册/登录、查看账户历史的终端界面。同时，负责结账处理流程（必须清晰体现“余额校验”及“4小时 Deal Package 折扣”的系统反馈文本）。

**分配包含**
- Screen 1:欢迎与鉴权页（绘制 Welcome 菜单，以及详细的注册和发初始资金流程）。
  - [关键更新] 管理员登录流分支：在登录模块中，必须体现出角色分流(Role Check)。当管理员账号登录时，系统需给出正确的反馈提示，以便成员 C 能够将这根线准确连到 Screen 6(管理员主菜单)。
- Screen 3:账户与历史页（绘制 ASCII 表格和余额显示，注意标注体现“原则2: 减少记忆负担”的底部返回提示）。
- Screen 5:结账页（绘制账单明细和 Deal Package 的折扣提示信息，以及绿色的成功反馈）。

**异常与拦截屏幕绘制**
- 学号已被注册：展示当用户输入了已经存在于 accounts.csv 中的学号时，系统亮起红灯并提示：`[ERROR] Student ID already exists. Please try logging in or use a different ID.`，并引导其重新输入或返回主菜单。
- 余额不足：展示当预订总价(如 60 积分)大于账户余额(如 50 积分)时，结账被拦截的屏幕：`[ERROR] Insufficient balance. Booking cancelled.`，并提示 `Press [0] to return to Main Menu`。

### [成员B] 预订与后台流线长
**核心职责**：负责绘制学生端的房间筛选与预订确认流（需体现时间冲突的拦截提示）。同时，负责绘制管理员端的添加房间(含可选设备循环输入)与删除房间流程。

**分配包含**
- Screen 4:筛选与预订页（绘制输入日期时间的提示、列出可用房间，以及最核心的 Double-check 确认交互，体现“原则3:允许撤销”）。
- Screen 7:添加房间（绘制管理员端循环输入 Optional equipment 的终端交互）。
- Screen 8:删除房间（绘制带有警告意味的红色或高亮 `[WARNING]` 二次确认屏幕）。

**异常与拦截屏幕绘制**
- 无匹配房间：当学生输入的条件极其苛刻，系统搜索不到结果时，需展示：`[INFO] No rooms available for the selected criteria. Please try different dates/times.`。
- Double-check 失败：画一个屏幕展示用户在最后一步按确认付款时，系统检测到冲突：`[WARNING] Sorry! The room was just booked by another user. Please select another room.`。
- 拒绝删除：当管理员试图删除一个还有未来预订的房间时，系统果断拒绝的红色提示屏：`[ERROR] Cannot delete Room 101. There are pending future bookings.`。

### [成员C] 全局架构与规范卫士
**核心职责**：拼图与缝合：梳理 A 和 B 的产出，用准确的控制流箭头连接主菜单与各级子菜单。

**分配包含**
- Screen 2 & 6:绘制学生主菜单(Screen 2)和管理员主菜单(Screen 6)，作为分发给 A 和 B 功能流的入口枢纽。

**核心质检与优化任务**
1. **文本审计(Text Audit)**【关键更新】：在最终缝合前，必须拿着负责写 User Story 同学交付的英文定稿，逐字核对 UI 界面中的英文提示词是否与 Acceptance Criteria 中的描述 100% 完全一致。
2. **视觉品控**：统一全画板的终端字体(等宽字体)、字号，以及颜色规范(成功一律绿色，错误/警告一律红色)。
3. **学术输出与批注补齐**：在 LucidChart 画布旁，负责撰写并标注“Ben Shneiderman 可用性设计原则”的英文批注。务必找到成员 A 和 B 画的那些绿色成功提示和红色错误提示，并在旁边显眼地标注出：`Principle 1: Offer informative feedback (提供信息反馈)`，确保三大原则在图中全数凑齐。
4. **起点指引与图例**：在整个大画布的角落画一个小框，说明颜色、字体和箭头的图例 (Legend)含义。拼图完成后，必须在 Screen 1(Welcome 屏幕)的最上方放置一个非常醒目的、独立颜色的 `[START HERE]` 标签。
5. **闭环登出流 (Logout / Exit Loop)**：确保学生和管理员主菜单的 `[0] Logout` 选项，有清晰的箭头指回 Screen 1 (Welcome 屏幕)，形成真正的系统生命周期闭环。
6. **模拟数据审计 (Mock Data Audit)**：强制检查 A 和 B 画板上的数据真实性。绝对不能出现 "User1", "Room A" 这种占位符。必须使用逼真的数据，例如：蒙纳士 8 位学号 33445566，邮箱 @student.monash.edu，房间名 Woodside Room 101，真实容量 4 pax 等。