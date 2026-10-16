---
name: subagent-orchestration
description: Orchestrate subagents optimally — outcome-first (Phase 0), depth/range research, implement, review, iterate to metric. Use when delegating multi-agent work.
version: "4"
---

# Điều phối subagents tối ưu

v4 — theo Felix Rieseberg "How to be more ambitious": Altitude/Depth/Range.

## Phase 0: Outcome (Altitude)

Hỏi trước mọi task: **outcome là gì, không phải task là gì.**

- Outcome / Metric + Threshold / Verifier (tool agent tự chạy, không tự đánh giá) / Diễn giải (chốt TRƯỚC khi chạy)
- **Readiness check:** agent có đủ data, môi trường, tools để tự reproduce và verify không? Chưa → build cái đó trước.

## Pattern

```
Phase 0: OUTCOME → Phase 1: RESEARCH (song song) → Phase 2: IMPLEMENT (1 writer)
→ Phase 3: REVIEW (song song) → Live test → [lặp nếu metric < threshold]
```

## Phase 1: Research (song song)

Subtask độc lập, không sửa cùng file, output là tài liệu.

**Depth — hỏi trước khi viết brief:** chuyên gia hàng đầu sẽ làm gì mà tôi chưa yêu cầu; họ bắt đầu từ dữ liệu thô nào; dùng phương pháp/công cụ gì; điều gì (không phải bạn hay tôi) chứng minh kết quả đúng.

**Range — chọn agent theo động từ:** đổi danh từ thành động từ ("khiến người bận tin câu chuyện nhân-quả trong 30 phút" thay vì "cái deck"). Mỗi agent = một lĩnh vực + 1 red-team. Rule: agent **LÀM** việc chuyên gia làm, không đóng vai giọng văn.

**Brief mẫu:**
```
Outcome: <Phase 0> | Metric: <số + ngưỡng>
Task: <một câu> | Skill: <SKILL.md — đọc trước>
Context: <repo, branch, 3-5 files, pattern mẫu>
Challenge: <giả định cần kiểm từ dữ liệu thô>
Constraints: <rules + điều cấm> | Output: <format + path> | Non-goals: <explicit>
```

**Nguyên tắc:** output file riêng, không sửa repo · evidence thiếu → nói cần gì, không đoán · tối đa 3-4 song song · review framing câu hỏi trước khi chạy · kết luận gắn `[STATIC]`/`[CẦN ĐO]` + file:line.

## Phase 2: Implement (1 writer)

Tránh conflict khi sửa cùng file. Brief thêm Outcome + Metric ở đầu. Chỉ implement research đã xong (DRAFT → bỏ qua, ghi lý do). Chưa commit — parent quyết sau review. Non-goals: commit, push, PR, build.

## Phase 3: Review (song song)

1. Technical 2. Safety 3. Red-team (adversarial — tìm cách phá). Read-only, tất cả PASS mới merge.

## Gate: verify → propose → approve → live test → commit

Cho fix đụng runtime/framework: Verify (file:line, `[STATIC]`/`[CẦN ĐO]`) → Propose (diff, chưa sửa) → Approve (Boss duyệt) → Live test (đo theo tiêu chí đặt TRƯỚC) → Commit. **Duyệt diff, không duyệt tóm tắt** — soi theo tiêu chí kiểm được bằng máy. Không bỏ qua live test vì "logic đã đúng".

## Vòng lặp sau live test

`metric >= threshold → xong` · `metric < threshold → về Phase 1 với evidence mới`. Dừng: N vòng (mặc định 3) / không cải thiện / Boss quyết.

## Checklist repo mới

Không skills → brief chi tiết hơn để bù. Không specs → định nghĩa checklist trong brief. Task đơn giản → gộp Phase 1+2. Trích rules bắt buộc từ AGENTS.md vào brief.

## Anti-patterns

Cả repo cho agent · nhiều writers · bỏ Phase 0 (đúng task, sai outcome) · bỏ Phase 1 (đoán thay vì evidence) · bỏ Phase 3 · brief mơ hồ · không giới hạn files · agent tự đánh giá mình.

## Chi tiết

- [references/general.md](references/general.md) — bản đầy đủ
- [references/lessons.md](references/lessons.md) — kinh nghiệm thực tế
