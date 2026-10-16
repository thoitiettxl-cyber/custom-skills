---
name: subagent-orchestration
description: Orchestrate subagents optimally in any repo — 3-phase pattern (research → implement → review), parallelization rules, minimal-context briefs, review gates. Use when delegating multi-agent work.
version: "3"
---

# Điều phối subagents tối ưu — dùng khi giao việc cho nhiều subagents trong bất kỳ repo nào

v3 — sẽ tiến hoá theo kinh nghiệm thực tế, không cố định.

## Pattern 3 phases

```
Phase 1: RESEARCH (song song) → Phase 2: IMPLEMENT (tuần tự) → Phase 3: REVIEW (song song)
```

Đã kiểm chứng trên SpoofX: 3 researchers → 1 writer → 2 reviewers, tất cả PASS.

## Gate: verify → propose → approve → live test → commit

Áp dụng khi fix đụng tới runtime/framework (không chỉ code tĩnh):
1. **Verify**: điều tra có bằng chứng (file:line), mọi kết luận gắn nhãn `[STATIC]` hoặc `[CẦN ĐO]`
2. **Propose**: trình bày diff/spec thay đổi, chưa sửa code
3. **Approve**: Boss duyệt mới implement
4. **Live test**: chạy trên môi trường thật, đo theo tiêu chí đã đặt TRƯỚC (không biện giải sau)
5. **Commit**: chỉ khi live test pass

Không bỏ qua bước 4 với lý do "logic đã đúng".

**Duyệt diff, không duyệt tóm tắt:** "chỉ log, không đổi logic" là lời agent tự báo — chưa được kiểm chứng cho tới khi thấy diff thật. Người duyệt soi diff theo tiêu chí kiểm được bằng máy (phân loại hunk, file:line), không duyệt theo bản tóm tắt của agent.

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
- **Review câu hỏi trước khi agent chạy:** người review ngoài kiểm tra framing của câu hỏi (có đo đúng thứ cần đo không), không chỉ kiểm tra câu trả lời. Câu hỏi sai khung → agent trả lời đúng câu hỏi sai.
- **Mọi kết luận gắn nhãn:** `[STATIC]` (chứng minh từ code, kèm file:line) hoặc `[CẦN ĐO]` (cần đo runtime, chưa có bằng chứng). Không trình bày suy đoán như sự thật.

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

## Kinh nghiệm thực tế (v3 — tiến hoá theo từng lần dùng)

- **Chỉ tin code, bỏ qua chú thích** (2026-10-15, điều tra reverse-skill): khảo sát repo lạ thì grep code thực thi trước, đọc doc sau chỉ để đối chiếu. Kết quả: 45 skills, chỉ 1 có code Android thật (`apk-reverse`); `mobile-reverse` 0 file code dù doc viết đầy đủ Frida/Objection/MSTG.
- Định nghĩa "file thực thi" trong brief (loại `.md` chứa snippet ra khỏi đếm).
- Rule "match → verify context → mới tính": grep hit chưa đủ — false positive (biến `index` match "android" trong `review_case.py`).
- Cross-check version doc-vs-manifest là kỹ thuật rẻ phát hiện drift (SKILL.md ghi jadx 1.5.5 vs manifest pin 1.5.6).
- `mkdir -p` trước khi redirect output `gh api` — không thì fail im lặng tạo file rỗng.
- **Reviewer ngoài bắt lỗi framing câu hỏi, không chỉ câu trả lời** (2026-10-16, diagnostic v2 SpoofX): 9 câu hỏi feasibility hỏi "làm được không" nhưng thiếu "làm vậy có đổi kết quả đo không". Boss chỉ ra câu 1,2,3,6 đặt sai khung → phải viết lại vòng review bổ sung với 8 câu hiệu chỉnh. Rule: đưa câu hỏi cho reviewer duyệt trước khi agent chạy.
- **Subagent read-only không xác nhận được runtime** (2026-10-16, điều tra split-prefs): 3 agents song song cho kết quả chi tiết kèm file:line, nhưng chỉ chứng minh "code làm gì", không chứng minh "framework/runtime làm gì". Boss yêu cầu mọi kết luận gắn `[STATIC]`/`[CẦN ĐO]`. Rule: nhãn bắt buộc trên mọi báo cáo điều tra.
- **Đặt tiêu chí diễn giải trước khi đo** (2026-10-16, diagnostic v2): bảng 6 dòng (mismatch@t0+t2s=F1, mismatch@t0+match@t2s=trễ, target chạy trước=cần restart, torn read, loại P3, read-back vô nghĩa) được chốt trước khi build APK. Rule: không biện giải sau khi có số liệu.
- **Brief ghi rõ format evidence** (2026-10-16): brief yêu cầu "[STATIC]/[CẦN ĐO] + file:line" cho báo cáo có cấu trúc tốt hơn hẳn brief mơ hồ. Rule: ghi format evidence ngay trong brief, không để agent tự chọn.
- **Duyệt diff thật, không duyệt lời agent** (2026-10-16, implement diagnostic v2): agent báo "chỉ log, không đổi logic" nhưng Boss yêu cầu thấy git diff đầy đủ mới duyệt — lời tự báo chưa phải bằng chứng. Rule: gate approve nhận diff + phân loại hunk, không nhận tóm tắt.
- **Định nghĩa loại hunk cho phép trước** (2026-10-16): với change "chỉ log", 4 loại hunk được chấp nhận: LOG / LOCAL-TS / EXECUTOR / TOGGLE. Hunk nào sửa dòng gốc, đổi thứ tự write, đổi return/exception flow thì liệt kê riêng như vi phạm. Rule: đặt whitelist hunk trong brief implement.
- **Self-test phải đi qua đúng đường cần chứng minh** (2026-10-16): hash chuỗi cố định chỉ chứng minh hàm sha đúng, không chứng minh hai phía dùng cùng canonical form. Phải thêm fixture cố định đi qua hàm canonical ở cả hai phía. Rule: test cái đang nghi, không test cái đã chắc.
- **Nhóm đối chứng có thể "chữa" bug** (2026-10-16): fresh pull phía writer có thể làm lành stale → FAIL(A) < FAIL(C) nghĩa là read-back là thuốc chứ không phải thước đo. Rule: pre-register diễn giải cho trường hợp phép đo làm đổi kết quả, trước khi có số liệu.
- **Nêu rõ cỡ mẫu chứng minh được gì** (2026-10-16): 0 lỗi/20 lần chỉ loại được tỷ lệ lỗi trên ~14% (95%), không chứng minh bug biến mất. Rule: báo cáo nêu giới hạn thống kê, không overclaim.
