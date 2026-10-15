---
name: subagent-orchestration
description: Orchestrate subagents optimally in any repo — 3-phase pattern (research → implement → review), parallelization rules, minimal-context briefs, review gates. Use when delegating multi-agent work.
version: "1"
---

# Điều phối subagents tối ưu — dùng khi giao việc cho nhiều subagents trong bất kỳ repo nào

v1 — sẽ tiến hoá theo kinh nghiệm thực tế, không cố định.

## Pattern 3 phases

```
Phase 1: RESEARCH (song song) → Phase 2: IMPLEMENT (tuần tự) → Phase 3: REVIEW (song song)
```

Đã kiểm chứng trên SpoofX: 3 researchers → 1 writer → 2 reviewers, tất cả PASS.

## Phase 1: Research (song song)

**Khi nào song song được:** subtask độc lập, không sửa cùng file, output là tài liệu.

**Brief mẫu:**
```
Task: <một câu cụ thể>
Skill: <đường dẫn SKILL.md — đọc trước>
Context:
- Repo: <đường dẫn, branch>
- Files: <3-5 file liên quan>
- Pattern hiện có: <file mẫu>
Constraints: <rules liên quan + điều cấm>
Output: <format + đường dẫn>
Non-goals: <explicit>
```

**Nguyên tắc:**
- Output ra file markdown riêng, không sửa repo
- Evidence không đủ → nói cần gì, không đoán
- Tối đa 3-4 agents song song

## Phase 2: Implement (1 writer, tuần tự)

**Tại sao 1 writer:** tránh conflict khi sửa cùng file/khu vực.

**Brief mẫu:**
```
Task: <implement từ research packages>
Skill: <skill implement của repo>
Inputs: <research outputs Phase 1>
Rules: <bắt buộc>
Constraints: <chỉ sửa files nào>
Output: <files sửa, chưa commit> + summary
Non-goals: commit, push, PR, build
```

**Nguyên tắc:**
- Chỉ implement research đã xong (DRAFT → bỏ qua, ghi lý do)
- Chưa commit — parent quyết sau review

## Phase 3: Review (song song)

**2 reviewers:**
1. Technical: wiring, patterns, correctness
2. Safety: security, privacy, charter

**Nguyên tắc:** read-only, cả 2 PASS mới merge.

## Checklist cho repo mới

1. **Skills**: repo có skills không? Không → brief chi tiết hơn để bù
2. **Reviewers**: có specs không? Không → định nghĩa checklist trong brief
3. **Rules**: đọc AGENTS.md, trích điểm bắt buộc vào brief
4. **Phases**: task tách được không? Đơn giản → gộp Phase 1+2
5. **Song song**: subtasks độc lập? Cùng file?

## Anti-patterns

1. Giao cả repo cho agent (context quá lớn)
2. Nhiều writers cùng lúc (conflict)
3. Bỏ Phase 1 (writer đoán thay vì evidence)
4. Bỏ Phase 3 (lỗi safety lọt)
5. Brief mơ hồ (làm sai hướng)
6. Không giới hạn files được sửa (lan man)

## Chi tiết
Xem [references/general.md](references/general.md) — bản đầy đủ với ví dụ SpoofX.
