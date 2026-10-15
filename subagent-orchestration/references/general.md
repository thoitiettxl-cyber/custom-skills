# Quy trình điều phối Subagents tối ưu (dùng cho mọi repo)

## Tổng quan
Pattern 3 phases đã kiểm chứng trên SpoofX (3 researchers → 1 writer → 2 reviewers, tất cả PASS):
```
Phase 1: RESEARCH (song song) → Phase 2: IMPLEMENT (tuần tự) → Phase 3: REVIEW (song song)
```

## Phase 1: Research (song song)

**Khi nào song song được:** các subtask độc lập, không sửa cùng file, output là tài liệu (không phải code).

**Brief mẫu cho mỗi agent:**
```
Task: <một câu, cụ thể>
Skill: <đường dẫn SKILL.md — bắt buộc đọc trước khi làm>
Context:
- Repo: <đường dẫn, branch>
- Files liên quan: <3-5 file, không cả repo>
- Pattern hiện có: <file mẫu để follow>
Constraints:
- <rules liên quan, chỉ cái cần thiết>
- <điều cấm cụ thể>
Output: <format + đường dẫn file output>
Non-goals: <liệt kê explicit những gì KHÔNG làm>
```

**Nguyên tắc:**
- Mỗi agent output ra file markdown riêng (không sửa repo)
- Nếu evidence không đủ: agent phải nói cần gì, không được đoán
- Tối đa 3-4 agents song song (nhiều hơn khó theo dõi)

## Phase 2: Implement (tuần tự — 1 writer)

**Tại sao tuần tự:** tránh conflict khi nhiều agents sửa cùng file/khu vực.

**Brief mẫu:**
```
Task: <implement từ các research packages>
Skill: <skill implement của repo>
Inputs: <danh sách research outputs từ Phase 1>
Existing code: <files mẫu để follow>
Rules: <rules bắt buộc>
What to do: <steps cụ thể>
Constraints:
- <coding conventions>
- <điều cấm>
- Chỉ sửa: <danh sách file được phép>
Output: <files đã sửa, chưa commit> + summary markdown
Non-goals: commit, push, PR, build, test trên device
```

**Nguyên tắc:**
- Writer KHÔNG tự quyết scope — chỉ implement những gì Phase 1 đã research xong
- Nếu research nào ở trạng thái DRAFT → writer bỏ qua, ghi rõ lý do
- Output chưa commit — parent quyết định merge sau review

## Phase 3: Review (song song)

**2 loại reviewer chạy song song:**
1. **Technical reviewer**: wiring, patterns, conventions, correctness
2. **Safety reviewer**: security, privacy, charter boundaries

**Brief mẫu:**
```
Role: <reviewer role>
Spec: <đường dẫn tới reviewer spec nếu có>
What to review: <git diff hoặc danh sách files>
Checklist: <từ spec, liệt kê cụ thể>
Output: Verdict PASS/FAIL + issues với file:line, ghi ra markdown
Non-goals: sửa code, commit
```

**Nguyên tắc:**
- Reviewers read-only (không sửa file)
- Cả 2 phải PASS mới được merge
- Warnings không blocking được ghi lại nhưng không chặn

## Áp dụng cho repo mới (checklist)

Khi mang pattern này sang repo khác, cần xác định:

1. **Skills**: repo có skills cho research/implement/review không? Nếu không, viết brief chi tiết hơn để bù.
2. **Reviewers**: có reviewer specs không? Nếu không, định nghĩa checklist thủ công trong brief.
3. **Rules**: đọc AGENTS.md + rules của repo, trích những điểm bắt buộc vào brief.
4. **Phases**: task có tách được thành research/implement/review không? Nếu task đơn giản (1 file, rõ ràng), gộp Phase 1+2.
5. **Song song**: subtasks có độc lập không? Có sửa cùng file không?

## Anti-patterns

1. **Giao cả repo cho agent** → context quá lớn, chậm, lỗi nhiều
2. **Nhiều writers cùng lúc** → conflict, khó review
3. **Bỏ Phase 1** → writer đoán thay vì dựa trên evidence
4. **Bỏ Phase 3** → lỗi safety lọt vào code
5. **Brief mơ hồ** → agent làm sai hướng, phải làm lại
6. **Không giới hạn files được sửa** → agent sửa lan man ngoài scope
