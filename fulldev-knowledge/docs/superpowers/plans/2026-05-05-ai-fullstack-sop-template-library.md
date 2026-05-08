# AI Fullstack SOP Template Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first reusable template library for the approved AI fullstack SOP so the next real requirement can be run through the process immediately.

**Architecture:** Keep the deliverable documentation-first and minimal: one index file that explains when to use each template, plus six focused Markdown templates that map directly to the SOP outputs. Reuse the approved design spec as the source of truth and keep filenames ASCII so they are stable for future automation and iteration.

**Tech Stack:** Markdown, git, ripgrep, sed

---

## File Structure

**Existing files**

- `docs/superpowers/specs/2026-05-05-ai-fullstack-sop-design.md`

**Files to create**

- `docs/superpowers/templates/README.md`
- `docs/superpowers/templates/requirement-summary-card.md`
- `docs/superpowers/templates/requirement-footprint-map.md`
- `docs/superpowers/templates/development-plan-sheet.md`
- `docs/superpowers/templates/ai-prompts.md`
- `docs/superpowers/templates/service-knowledge-card.md`
- `docs/superpowers/templates/sop-update-log.md`

**Files to modify**

- None

## Task 1: Create the template library index

**Files:**
- Create: `docs/superpowers/templates/README.md`

- [ ] **Step 1: Create the templates directory**

Run: `mkdir -p docs/superpowers/templates`
Expected: command exits `0`

- [ ] **Step 2: Add the index file**

Create `docs/superpowers/templates/README.md` with:

```md
# AI Fullstack SOP Template Library

This directory contains the first reusable templates for the approved AI fullstack SOP.

## When to use this library

Use these templates after reading the SOP design spec and before starting a real requirement walkthrough.

Recommended order:

1. Fill `requirement-summary-card.md`
2. Draft `requirement-footprint-map.md`
3. Use `ai-prompts.md` to query AI with evidence
4. Fill `development-plan-sheet.md`
5. During and after delivery, update `service-knowledge-card.md`
6. After the requirement closes, append `sop-update-log.md`

## Files

- `requirement-summary-card.md`: Convert product language into engineering language
- `requirement-footprint-map.md`: Capture front-end entry points, candidate services, and dependencies
- `development-plan-sheet.md`: Turn analysis into an execution-ready change plan
- `ai-prompts.md`: Prompt pack for requirement decoding, service location, implementation pattern search, plan generation, and retrospectives
- `service-knowledge-card.md`: Build long-term service understanding one requirement at a time
- `sop-update-log.md`: Record what changed in the SOP and why

## Maintenance rules

- Keep templates short enough to copy into a real task note
- Prefer explicit fields over prose
- Add fields only after real usage proves they are needed
- Keep filenames stable so future scripts or automations can reuse them
```

- [ ] **Step 3: Verify the index headings**

Run: `rg -n "^#|^##" docs/superpowers/templates/README.md`
Expected:

```text
1:# AI Fullstack SOP Template Library
5:## When to use this library
18:## Files
27:## Maintenance rules
```

- [ ] **Step 4: Commit the index file**

```bash
git add docs/superpowers/templates/README.md
git commit -m "docs: add SOP template library index"
```

## Task 2: Create the requirement analysis templates

**Files:**
- Create: `docs/superpowers/templates/requirement-summary-card.md`
- Create: `docs/superpowers/templates/requirement-footprint-map.md`

- [ ] **Step 1: Add the requirement summary card**

Create `docs/superpowers/templates/requirement-summary-card.md` with:

```md
# Requirement Summary Card

## Basic Info

- Requirement name:
- Source:
- Owner:
- Priority:
- Target release:

## User and Scenario

- User role:
- Entry platform:
- Entry page or flow:
- Trigger action:
- Expected result:

## Success Criteria

- Primary success path:
- Data success criteria:
- Interaction success criteria:
- Boundary or exception expectations:

## Unknowns

- Open question 1:
- Open question 2:
- Open question 3:

## Initial Risks

- Risk 1:
- Risk 2:
- Risk 3:
```

- [ ] **Step 2: Add the requirement footprint map**

Create `docs/superpowers/templates/requirement-footprint-map.md` with:

```md
# Requirement Footprint Map

## Front-End Entry Points

- Android entry:
- PC Web entry:
- Shared interaction changes:

## Change Type

- [ ] Display only
- [ ] New field
- [ ] Existing API extension
- [ ] New API
- [ ] New business rule
- [ ] State transition change

## Candidate Interfaces

- Existing API candidate 1:
- Existing API candidate 2:
- New API guess:

## Primary Service Judgment

- Primary service candidate:
- Why this service owns the result:
- Secondary service candidates:

## Upstream and Downstream

- Caller:
- Direct dependencies:
- Data write location:
- State impact:
- Async impact:

## Validation Points

- Point 1:
- Point 2:
- Point 3:
```

- [ ] **Step 3: Verify both analysis templates exist and start with the right titles**

Run: `sed -n '1,20p' docs/superpowers/templates/requirement-summary-card.md docs/superpowers/templates/requirement-footprint-map.md`
Expected: output starts with `# Requirement Summary Card` and `# Requirement Footprint Map`

- [ ] **Step 4: Commit the requirement analysis templates**

```bash
git add docs/superpowers/templates/requirement-summary-card.md docs/superpowers/templates/requirement-footprint-map.md
git commit -m "docs: add requirement analysis templates"
```

## Task 3: Create the execution planning template

**Files:**
- Create: `docs/superpowers/templates/development-plan-sheet.md`

- [ ] **Step 1: Add the development plan sheet**

Create `docs/superpowers/templates/development-plan-sheet.md` with:

```md
# Development Plan Sheet

## Scope

- In scope:
- Out of scope:

## Front-End Changes

### Android

- Page or module:
- UI or interaction changes:
- Request or response fields:
- Validation or state handling:

### PC Web

- Page or module:
- UI or interaction changes:
- Request or response fields:
- Validation or state handling:

## Back-End Changes

- Primary service:
- Controller or API changes:
- Service logic changes:
- DTO or VO changes:
- Enum or state changes:
- Table, cache, or MQ changes:

## Reused Pattern

- Reference implementation 1:
- Reference implementation 2:
- Reuse notes:

## Integration Plan

- Dependency order:
- Can run in parallel:
- Mock needed:
- Real environment checks:

## Risks and Confirmation Items

- Risk 1:
- Risk 2:
- Confirmation item 1:
- Confirmation item 2:

## Acceptance Checklist

- [ ] Main user flow passes
- [ ] Data fields are correct
- [ ] Exception flow is covered
- [ ] Old logic still works
```

- [ ] **Step 2: Verify planning sections**

Run: `rg -n "^##|^###" docs/superpowers/templates/development-plan-sheet.md`
Expected:

```text
3:## Scope
8:## Front-End Changes
10:### Android
17:### PC Web
24:## Back-End Changes
33:## Reused Pattern
39:## Integration Plan
46:## Risks and Confirmation Items
53:## Acceptance Checklist
```

- [ ] **Step 3: Commit the execution planning template**

```bash
git add docs/superpowers/templates/development-plan-sheet.md
git commit -m "docs: add development plan template"
```

## Task 4: Create the AI prompt pack

**Files:**
- Create: `docs/superpowers/templates/ai-prompts.md`

- [ ] **Step 1: Add the AI prompt pack**

Create `docs/superpowers/templates/ai-prompts.md` with:

````md
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
````

- [ ] **Step 2: Verify the five prompt sections**

Run: `rg -n "^## " docs/superpowers/templates/ai-prompts.md`
Expected:

```text
3:## 1. Requirement Decoding
17:## 2. Service Location
31:## 3. Similar Pattern Search
43:## 4. Development Plan Generation
57:## 5. Retrospective and SOP Update
```

- [ ] **Step 3: Commit the AI prompt pack**

```bash
git add docs/superpowers/templates/ai-prompts.md
git commit -m "docs: add AI prompt pack"
```

## Task 5: Create the long-term knowledge templates

**Files:**
- Create: `docs/superpowers/templates/service-knowledge-card.md`
- Create: `docs/superpowers/templates/sop-update-log.md`

- [ ] **Step 1: Add the service knowledge card**

Create `docs/superpowers/templates/service-knowledge-card.md` with:

```md
# Service Knowledge Card

## Service Identity

- Service name:
- Domain:
- Main responsibility:

## Typical Entry Points

- Front-end entry:
- API entry:
- Batch or async entry:

## Dependencies

- Upstream callers:
- Downstream services:
- Storage objects:
- MQ or async links:

## Stable Patterns

- Common business objects:
- Common state changes:
- Common validation points:

## Known Risks

- Risk 1:
- Risk 2:
- Risk 3:

## Related Cases

- Case 1:
- Case 2:
```

- [ ] **Step 2: Add the SOP update log**

Create `docs/superpowers/templates/sop-update-log.md` with:

```md
# SOP Update Log

## Update Record

- Date:
- Requirement or case:
- Updated by:

## What changed

- Added:
- Removed:
- Adjusted:

## Why the old flow was not enough

- Problem 1:
- Problem 2:

## Evidence from practice

- What happened in the real task:
- What proved useful:
- What should still be observed:
```

- [ ] **Step 3: Verify the knowledge templates**

Run: `sed -n '1,80p' docs/superpowers/templates/service-knowledge-card.md docs/superpowers/templates/sop-update-log.md`
Expected: output includes `# Service Knowledge Card` and `# SOP Update Log`

- [ ] **Step 4: Commit the long-term knowledge templates**

```bash
git add docs/superpowers/templates/service-knowledge-card.md docs/superpowers/templates/sop-update-log.md
git commit -m "docs: add knowledge and SOP iteration templates"
```

## Task 6: Verify the full library and align it with the spec

**Files:**
- Test: `docs/superpowers/specs/2026-05-05-ai-fullstack-sop-design.md`
- Test: `docs/superpowers/templates/README.md`
- Test: `docs/superpowers/templates/*.md`

- [ ] **Step 1: List all template files**

Run: `rg --files docs/superpowers/templates`
Expected:

```text
docs/superpowers/templates/README.md
docs/superpowers/templates/requirement-summary-card.md
docs/superpowers/templates/requirement-footprint-map.md
docs/superpowers/templates/development-plan-sheet.md
docs/superpowers/templates/ai-prompts.md
docs/superpowers/templates/service-knowledge-card.md
docs/superpowers/templates/sop-update-log.md
```

- [ ] **Step 2: Verify the spec-template mapping**

Run: `rg -n "需求摘要卡|需求落点图|开发方案单|AI 提示词|服务认知卡|SOP 更新记录" docs/superpowers/specs/2026-05-05-ai-fullstack-sop-design.md`
Expected: output shows all six deliverables named in the spec

- [ ] **Step 3: Verify every template has a top-level heading**

Run: `rg -n "^# " docs/superpowers/templates/*.md`
Expected: one top-level heading per template file

- [ ] **Step 4: Commit any verification-driven template fixes**

```bash
git add docs/superpowers/templates
git commit -m "docs: verify SOP template library"
```

## Self-Review

- Spec coverage: This plan covers the V1 template library recommended in the design spec, including the index file, six core templates, and a final verification task.
- Placeholder scan: No `TODO`, `TBD`, or underspecified implementation steps remain.
- Type consistency: Template names and filenames are consistent across the plan and align with the design spec outputs.
