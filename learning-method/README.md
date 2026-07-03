# README

> 本目录不是单独摆着阅读的说明书，而是要放进一个具体的学习工作区里，配合目标项目一起给 AI 使用。
> 你要做的是：让 AI 读取本目录，并明确告诉它要仿写哪个真实项目。

## 落地用法

### 1. 标准目录结构

```text
flutter-work/
├── xxx-project/
└── docs/
    ├── learning-method/
    │   ├── README.md
    │   ├── AI-仿写执行协议.md
    │   ├── 000-文档约定.md
    │   ├── 01-仿写学习法-design.md
    │   ├── 02-仿写学习法.md
    │   └── templates/
    └── <技术栈>/
```

说明：

- `xxx-project/`：你想仿写、想学习的真实项目。
- `docs/learning-method/`：这套方法论本体，给 AI 阅读和执行。
- `docs/<技术栈>/`：AI 按方法论产出的仿写计划、阶段总结、差距分析存放位置；不需要提前手动创建，AI 在产出时按需创建即可。

### 2. 使用步骤

1. 新建一个学习工作区，例如 `flutter-work/`。
2. 把目标项目放进工作区里，例如 `flutter-work/xxx-project/`。
3. 在工作区下新建 `docs/`，把整个 `learning-method/` 放进 `docs/`。
4. 把下面的指令模板直接发给 AI，它会先阅读 `docs/learning-method/README.md`，再按 `docs/learning-method/AI-仿写执行协议.md` 执行。
5. 将模板里的 `xxx-project/` 替换成你的目标项目实际路径，将 `{语言/框架/技术栈}` 替换成你这次想学习的内容。

### 3. 给 AI 的指令模板

把下面这段话发给 AI 即可。请把其中的 `xxx-project/` 替换成你的目标项目实际路径：

```text
请先阅读 `docs/learning-method/README.md`，了解这套方法论的落地使用方式。
然后按 `docs/learning-method/AI-仿写执行协议.md` 执行。

我要通过仿写 `xxx-project/` 学习 {语言/框架/技术栈}。
请先整体理解目标项目，再按方法论推进，并把产出写到 `docs/<技术栈>/`。
```

### 4. 文档分工

- `README.md`：落地使用说明，告诉用户和 AI 这套方法论怎么接到真实学习工作区里。
- `AI-仿写执行协议.md`：AI 执行入口，定义角色、前提、执行要求和行为红线。
- `000-文档约定.md`：命名规则、目录结构和扩展规则。
- `02-仿写学习法.md`：执行主手册，包含五步流程、AI 交互协议和案例索引。
- `01-仿写学习法-design.md`：维护专用，日常执行仿写任务时不是必读文档。
- `templates/`：仿写计划、阶段总结、差距分析模板来源。
