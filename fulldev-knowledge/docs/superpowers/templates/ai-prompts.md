# AI Prompt Pack

## 1. Requirement Decoding

```text
Below is a product requirement. Do not give a solution yet.
First break it into:
1. user role
2. entry platform
3. trigger action
4. expected system result
5. success criteria
6. unknowns
7. initial risks
```

## 2. Service Location

```text
Based on the requirement summary and current project structure, identify the likely services involved.
Output:
1. primary service candidate
2. upstream and downstream services
3. judgment evidence
4. data or state impact
5. async impact
6. validation points
Do not invent certainty where evidence is missing.
```

## 3. Similar Pattern Search

```text
Based on this requirement and the existing codebase, find the most similar implementation patterns.
Summarize them from four angles:
1. page or interaction pattern
2. API structure
3. state transition
4. validation logic
List the concrete files or modules when possible.
```

## 4. Development Plan Generation

```text
Using the requirement summary, footprint map, and similar patterns, generate an implementation-ready change plan.
Output:
1. Android change points
2. PC Web change points
3. API suggestion
4. back-end change points
5. risk list
6. confirmation items
7. integration sequence
```

## 5. Retrospective and SOP Update

```text
Below is the actual delivery process and issues encountered.
Summarize them into:
1. service knowledge card updates
2. reusable case notes
3. pitfalls
4. SOP changes worth making
Only keep updates that are proven useful by the real task.
```
