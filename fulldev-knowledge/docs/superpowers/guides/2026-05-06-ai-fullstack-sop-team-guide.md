# AI Fullstack SOP Team Guide

## 1. 这套文档是干什么的

这不是一套“为了写文档而写文档”的材料，而是一套帮助团队在已有项目里更高效完成需求开发的工作流。

它的目标是帮助大家在拿到需求后，更快完成下面几件事：

- 把需求文档翻译成工程语言
- 判断需求会落到哪些页面、接口、服务
- 更稳定地使用 AI 做分析和方案收敛
- 在开发前形成可执行的改动、联调、验收清单
- 把一次需求的经验沉淀成团队可复用的方法

一句话理解：

`这套文档不是知识库，而是 AI 协作工作流。`

## 2. 谁应该看哪份文档

团队里不同角色，不需要看同样的材料。

### 日常开发同学

优先看：

- [README.md](../templates/README.md)
- [requirement-summary-card.md](../templates/requirement-summary-card.md)
- [requirement-footprint-map.md](../templates/requirement-footprint-map.md)
- [development-plan-sheet.md](../templates/development-plan-sheet.md)
- [ai-prompts.md](../templates/ai-prompts.md)

这些是每天真正会用到的文件。

### 想理解整套方法的人

看这个设计稿：

- [2026-05-05-ai-fullstack-sop-design.md](../specs/2026-05-05-ai-fullstack-sop-design.md)

它回答的是“为什么这样设计”和“完整流程是什么”。

### 维护这套 SOP 的人

除了设计稿，还要看这个实现计划：

- [2026-05-05-ai-fullstack-sop-template-library.md](../plans/2026-05-05-ai-fullstack-sop-template-library.md)

它记录了模板库是怎么落地的，适合后续扩展或维护。

## 3. 团队使用顺序

如果拿到一个真实需求，建议严格按这个顺序使用。

### 第一步：先看模板入口

先打开：

- [README.md](../templates/README.md)

作用：

- 知道整套模板的使用顺序
- 知道应该先填哪张卡
- 避免一上来就直接问 AI 或直接进代码

### 第二步：填写需求摘要卡

打开：

- [requirement-summary-card.md](../templates/requirement-summary-card.md)

作用：

- 把产品需求翻译成工程语言
- 先明确用户、入口、动作、结果、成功标准、未知项

适合回答的问题：

- 谁在用这个需求
- 从哪个端进入
- 用户做了什么动作
- 系统最终要给出什么结果
- 什么叫“这个需求做成了”

### 第三步：填写需求落点图

打开：

- [requirement-footprint-map.md](../templates/requirement-footprint-map.md)

作用：

- 定位这个需求会落到哪些页面、接口和服务
- 把“模糊感觉”变成“可验证判断”

适合回答的问题：

- Android 和 PC Web 分别落在哪
- 变化是展示、字段、接口还是业务规则
- 主服务更像 UC、钱包、资管、交易，还是 MIS
- 哪些上下游服务、状态或异步链路可能被影响

### 第四步：用 AI 提示词做分析

打开：

- [ai-prompts.md](../templates/ai-prompts.md)

作用：

- 不让 AI 直接“盲猜方案”
- 先让 AI 帮你做需求解码、服务定位、相似实现搜索
- 在你已有证据的基础上收敛成可执行方案

推荐顺序：

1. 先用 `Requirement Decoding`
2. 再用 `Service Location`
3. 再用 `Similar Pattern Search`
4. 最后用 `Development Plan Generation`

不要跳过前两步直接问“这个需求怎么做”。

### 第五步：形成开发方案单

打开：

- [development-plan-sheet.md](../templates/development-plan-sheet.md)

作用：

- 把分析结果变成开发动作
- 明确 Android、PC Web、后端、联调、测试、Code Review、风险、验收

适合回答的问题：

- 哪些改动在 Android
- 哪些改动在 PC Web
- 哪些改动在后端
- 接口和字段口径怎么定
- 测试策略和责任人怎么定
- 联调顺序是什么
- Code Review 在哪里进入
- 最后要怎么验收

### 第六步：做完需求后沉淀经验

有两份模板：

- [service-knowledge-card.md](../templates/service-knowledge-card.md)
- [sop-update-log.md](../templates/sop-update-log.md)

它们的区别是：

- `service-knowledge-card`
  记录对某个服务的长期认知，比如交易服务、钱包服务、资管服务，以及由谁维护、最近一次何时验证

- `sop-update-log`
  记录这次实践告诉我们 SOP 哪里该改、哪里该补

## 4. 每份模板分别解决什么问题

### README

文件：

- [README.md](../templates/README.md)

解决：

- 第一次用这套东西时，不知道先看哪个、先填哪个

### Requirement Summary Card

文件：

- [requirement-summary-card.md](../templates/requirement-summary-card.md)

解决：

- 需求文档很产品化，不容易直接进入工程分析

### Requirement Footprint Map

文件：

- [requirement-footprint-map.md](../templates/requirement-footprint-map.md)

解决：

- 这个需求到底会改哪些端、哪些接口、哪些服务

### AI Prompt Pack

文件：

- [ai-prompts.md](../templates/ai-prompts.md)

解决：

- 怎样让 AI 输出更稳定，而不是泛泛而谈

### Development Plan Sheet

文件：

- [development-plan-sheet.md](../templates/development-plan-sheet.md)

解决：

- 怎样把分析结果转成真正可以执行的开发和联调方案

### Service Knowledge Card

文件：

- [service-knowledge-card.md](../templates/service-knowledge-card.md)

解决：

- 怎样把对某个后端服务的理解沉淀下来，而不是每次重新摸索

### SOP Update Log

文件：

- [sop-update-log.md](../templates/sop-update-log.md)

解决：

- 怎样让 SOP 随实践持续变好，而不是写完就不动

## 5. 一次真实需求应该怎么跑

建议团队用下面这个最小流程试跑：

1. 先读需求文档
2. 填 `Requirement Summary Card`
3. 填 `Requirement Footprint Map`
4. 用 `AI Prompt Pack` 做 2 到 4 轮分析
5. 填 `Development Plan Sheet`
6. 开发、联调、验收
7. 完成后补 `Service Knowledge Card` 或 `SOP Update Log`

如果团队第一次试用，不需要一开始全量铺开。

建议第一次只强制用这 4 份：

- `README`
- `Requirement Summary Card`
- `Requirement Footprint Map`
- `Development Plan Sheet`

等第一轮跑顺，再把 `AI Prompt Pack` 和沉淀类模板纳入正式流程。

## 6. 推荐团队推广方式

不要一开始就把它当成“标准文档规范”去推，那样阻力会很大。

更好的方式是：

1. 先挑一个真实需求试跑
2. 让 1 到 2 个开发同学按模板走一遍
3. 复盘哪里真的节省了时间
4. 再把这套方法分享到团队

推荐口径：

`这不是增加文档负担，而是为了让大家在已有项目里更快完成需求定位、AI 协作、开发方案和经验沉淀。`

## 7. 常见误区

### 误区 1：直接问 AI “这个需求怎么做”

不建议。  
先填摘要卡和落点图，再问 AI，效果会稳很多。

### 误区 2：拿到需求立刻钻后端代码

不建议。  
先定位前端承载点，再反推服务，效率更高。

### 误区 3：把模板当正式汇报材料

不建议。  
这些模板首先是工作过程工具，不是面向管理层的展示材料。

### 误区 4：第一次就要求全团队完整使用所有模板

不建议。  
先从最小链路开始，更容易落地。

## 8. 推荐给团队的一句话介绍

可以直接这样介绍：

`这是一套面向已有项目需求开发的 AI 协作工作流。它帮助我们把需求文档更快翻译成工程动作，更稳定地定位服务、使用 AI、形成开发方案，并把每次实践沉淀成团队资产。`

## 9. 下一步建议

如果要正式在团队里推广，建议按这个顺序继续：

1. 先用一个真实需求试跑
2. 把试跑过程记录到 `SOP Update Log`
3. 根据结果更新模板
4. 再整理成一版团队培训材料或群分享版本
