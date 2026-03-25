# 画图
## 1. 第一参考准则:User Story 的验收标准 (Acceptance Criteria)
UI 图上的每一个跳转、每一句提示，都必须在 User Story 中找到依据。
**参考方式**：逐句翻译。
**例子**：如果 User Story 1.1 的 AC 写着“注册成功后，终端显示绿色的‘注册成功，已为您发放 50 积分初始体验金’提示”。那么负责画这段的成员 A，就必须在 LucidChart 里画一个黑框，里面用绿色字体写上这句话。连标点符号和数字都最好一模一样。

## 2. 第二参考准则:终端命令行 (Terminal/CLI) 的视觉风格
由于项目限制了是纯文本应用程序 (Text-based application)，画图成员绝对不能参考现代的网页(没有按钮、没有下拉菜单、没有精美的图片)。
**参考方式**：参考经典的 DOS 系统、Linux 终端或 Python 控制台的样式。
**视觉元素**：
- 所有的选项都是用数字列表:1. Book Room | 2. Exit
- 所有的输入都是一问一答:Enter Room ID: [光标]
- 所有的表格都是用键盘符号拼出来的 ASCII 表格(用 | 和 - 组成)。
- 字体必须统一使用等宽字体(如 Courier New, Consolas, Monaco)。

## 3. 第三参考准则:Ben Shneiderman 的可用性原则
作业要求(Rubric)明确规定 UI 必须体现可用性原则。这是画“菜单层级”和“报错信息”的最高指导思想。
**参考方式**：
- 原则1(提供反馈): 任何操作后，必须画出系统的反馈框(如绿色的 [SUCCESS] 或红色的 [ERROR] )。
- 原则2(减少记忆负担): 任何屏幕的最下方，都必须画上一行类似 Press [0] to return to Main Menu 的导航提示，不能让屏幕变成死胡同。
- 原则3(允许撤销): 在扣钱或删除数据前，必须画一个 Confirm? (Y/N) 的二次确认屏幕。

## 4. 第四参考准则:逼真的业务数据 (Realistic Mock Data)
需求文档(SRS 第 9 条)的硬性规定。
**参考方式**：拒绝使用敷衍的占位符。
**例子**：画图时，不要写 Welcome, User 1，要写成 Welcome, Student 33445566 (FIT5136) ;房间名不要写 Room A，要写成 Woodside Study Room 101。