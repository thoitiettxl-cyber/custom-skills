---
name: subagent-orchestration
description: Orchestrate subagents optimally — outcome-first (Phase 0), depth/range research, implement, review, iterate to metric. Use when delegating multi-agent work.
version: "5.2"
---

# Điều phối subagents tối ưu

v5.2 — theo Felix Rieseberg "How to be more ambitious": Altitude/Depth/Range.

## Phase 0: Outcome (Altitude)

Hỏi trước mọi task: **outcome là gì, không phải task là gì.**

- Outcome / Metric + Floor + Target / Verifier (tool agent tự chạy, không tự đánh giá) / Diễn giải (chốt TRƯỚC khi chạy)
  - **Floor** <số>: dưới mức này = FAIL; chỉ Floor quyết định pass/fail và vòng lặp (3 vòng / không cải thiện / Boss quyết).
  - **Target** <số, cố tình khó nhưng khả thi>: đưa vào brief của agent, nói rõ là đạt được.
  - Đạt Floor nhưng chưa đạt Target → xong (PASS). Agent báo evidence điểm chặn, không đổi cách đo.
- **Readiness check:** agent có đủ data, môi trường, tools để tự reproduce và verify không? Chưa → build cái đó trước.

## Pattern

```
Phase 0: OUTCOME → Phase 1: RESEARCH (song song) → Phase 2: IMPLEMENT (1 writer)
→ Phase 3: REVIEW (song song) → Live test → [lặp nếu metric < Floor]
```

## Phase 1: Research (song song)

Subtask độc lập, không sửa cùng file, output là tài liệu.

**Depth — hỏi trước khi viết brief:** chuyên gia hàng đầu sẽ làm gì mà tôi chưa yêu cầu; họ bắt đầu từ dữ liệu thô nào; dùng phương pháp/công cụ gì; điều gì (không phải bạn hay tôi) chứng minh kết quả đúng.

**Range — chọn agent theo động từ:** đổi danh từ thành động từ ("khiến người bận tin câu chuyện nhân-quả trong 30 phút" thay vì "cái deck"). Mỗi agent = một lĩnh vực + 1 red-team. Rule: agent **LÀM** việc chuyên gia làm, không đóng vai giọng văn.

**Brief mẫu:**
```
Outcome: <Phase 0> | Metric: <số> | Floor: <FAIL line> | Target: <hard but feasible>
Task: <một câu> | Skill: <SKILL.md — đọc trước>
Context: <repo, branch, 3-5 files, pattern mẫu>
Challenge: <giả định cần kiểm từ dữ liệu thô>
Discover: <tín hiệu lạ / điểm mù tìm thấy trong dữ liệu thô; phải validate trên held-out data mà agent chưa thấy, nếu không thì gắn tag [CẦN ĐO]>. Chỉ dùng khi task có dữ liệu thô (logs, crashes, metrics); nếu không thì "Discover: N/A". Không bịa finding để lấp đầy.
Constraints: <rules + điều cấm> | Output: <format + path> | Non-goals: <explicit>
```

**Nguyên tắc:** output file riêng, không sửa repo · evidence thiếu → nói cần gì, không đoán · tối đa 3-4 song song · review framing câu hỏi trước khi chạy · kết luận gắn `[STATIC]`/`[CẦN ĐO]` + file:line.

## Phase 2: Implement (1 writer)

Tránh conflict khi sửa cùng file. Brief thêm Outcome + Metric ở đầu. Chỉ implement research đã xong (DRAFT → bỏ qua, ghi lý do). Chưa commit — parent quyết sau review. Non-goals: commit, push, PR, build.

- TDD (chỉ khi task có logic code testable được; log-only/config changes bỏ qua):
  - Seam: chốt trước, Boss duyệt; mỗi seam ghi "bắt được / bỏ sót".
  - Mỗi vòng: 1 seam → 1 test đỏ → code tối thiểu → xanh.
  - Expected = literal/ví dụ có lời giải/spec; cấm tính lại bằng logic của code.
  - Writer không refactor. Đề xuất refactor ghi thành finding ở Phase 3; parent quyết sau review. Phần "bỏ sót" của seam → [CẦN ĐO]. Live test gate vẫn bắt buộc.
  - File test nằm trong danh sách được phép sửa, khai báo trong brief.

## Phase 3: Review (song song)

1. Technical 2. Safety 3. Red-team (adversarial — tìm cách phá). Read-only, tất cả PASS mới merge.

## Gate: verify → propose → approve → live test → commit

Cho fix đụng runtime/framework: Verify (file:line, `[STATIC]`/`[CẦN ĐO]`) → Propose (diff, chưa sửa) → Approve (Boss duyệt) → Live test (đo theo tiêu chí đặt TRƯỚC) → Commit. **Duyệt diff, không duyệt tóm tắt** — soi theo tiêu chí kiểm được bằng máy. Không bỏ qua live test vì "logic đã đúng".

## Vòng lặp sau live test

`metric >= Floor → xong` · `metric < Floor → về Phase 1 với evidence mới`. Dừng: N vòng (mặc định 3) / không cải thiện / Boss quyết.

## Checklist repo mới

Không skills → brief chi tiết hơn để bù. Không specs → định nghĩa checklist trong brief. Task đơn giản → gộp Phase 1+2. Trích rules bắt buộc từ AGENTS.md vào brief.

## Anti-patterns

Cả repo cho agent · nhiều writers · bỏ Phase 0 (đúng task, sai outcome) · bỏ Phase 1 (đoán thay vì evidence) · bỏ Phase 3 · brief mơ hồ · không giới hạn files · agent tự đánh giá mình.

## Chi tiết

- [references/general.md](references/general.md) — bản v1 (lịch sử)
- [references/lessons.md](references/lessons.md) — kinh nghiệm thực tế
