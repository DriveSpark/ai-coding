# AI 全栈 SOP 模板库

本目录包含已审批的 AI 全栈 SOP 的首批可复用模板。

## 何时使用本库

在阅读完 SOP 设计规范之后、开始实际需求走查之前，使用这些模板。

推荐顺序：

1. 填写 `requirement-summary-card.md`（需求摘要卡）
2. 起草 `requirement-footprint-map.md`（需求影响面地图）
3. 使用 `ai-prompts.md`（AI 提示词包）带着证据向 AI 提问
4. 填写 `development-plan-sheet.md`（开发计划表）
5. 交付期间及之后，更新 `service-knowledge-card.md`（服务知识卡）
6. 需求关闭后，追加 `sop-update-log.md`（SOP 更新日志）

## 文件说明

- `requirement-summary-card.md`：将产品语言转化为工程语言
- `requirement-footprint-map.md`：梳理前端入口、候选服务及依赖关系
- `development-plan-sheet.md`：将分析结果转化为可执行的变更计划
- `ai-prompts.md`：提示词包，涵盖需求解码、服务定位、实现模式搜索、计划生成和复盘
- `service-knowledge-card.md`：逐个需求地构建长期服务认知
- `sop-update-log.md`：记录 SOP 变更内容及原因

## 维护规则

- 模板保持简短，能直接复制到实际任务笔记中使用
- 优先使用明确的字段而非大段叙述
- 只有经过实际使用验证确有必要时，才新增字段
- 保持文件名稳定，以便将来的脚本或自动化工具复用
