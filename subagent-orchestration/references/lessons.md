# Kinh nghiệm thực tế — tiến hoá theo từng lần dùng subagent-orchestration

Mỗi lesson: ngày, task, chuyện gì xảy ra, bằng chứng, rule rút ra. Chỉ lesson có bằng chứng thật.

## 2026-10-15 — Điều tra reverse-skill

- **Chỉ tin code, bỏ qua chú thích:** khảo sát repo lạ thì grep code thực thi trước, đọc doc sau chỉ để đối chiếu. Kết quả: 45 skills, chỉ 1 có code Android thật (`apk-reverse`); `mobile-reverse` 0 file code dù doc viết đầy đủ Frida/Objection/MSTG.
- Định nghĩa "file thực thi" trong brief (loại `.md` chứa snippet ra khỏi đếm).
- Rule "match → verify context → mới tính": grep hit chưa đủ — false positive (biến `index` match "android" trong `review_case.py`).
- Cross-check version doc-vs-manifest là kỹ thuật rẻ phát hiện drift (SKILL.md ghi jadx 1.5.5 vs manifest pin 1.5.6).
- `mkdir -p` trước khi redirect output `gh api` — không thì fail im lặng tạo file rỗng.

## 2026-10-16 — Diagnostic v2 SpoofX

- **Reviewer ngoài bắt lỗi framing câu hỏi, không chỉ câu trả lời:** 9 câu hỏi feasibility hỏi "làm được không" nhưng thiếu "làm vậy có đổi kết quả đo không". Boss chỉ ra câu 1,2,3,6 đặt sai khung → phải viết lại vòng review bổ sung với 8 câu hiệu chỉnh. Rule: đưa câu hỏi cho reviewer duyệt trước khi agent chạy.
- **Subagent read-only không xác nhận được runtime:** 3 agents song song cho kết quả chi tiết kèm file:line, nhưng chỉ chứng minh "code làm gì", không chứng minh "framework/runtime làm gì". Boss yêu cầu mọi kết luận gắn `[STATIC]`/`[CẦN ĐO]`. Rule: nhãn bắt buộc trên mọi báo cáo điều tra.
- **Đặt tiêu chí diễn giải trước khi đo:** bảng 6 dòng (mismatch@t0+t2s=F1, mismatch@t0+match@t2s=trễ, target chạy trước=cần restart, torn read, loại P3, read-back vô nghĩa) được chốt trước khi build APK. Rule: không biện giải sau khi có số liệu.
- **Brief ghi rõ format evidence:** brief yêu cầu "[STATIC]/[CẦN ĐO] + file:line" cho báo cáo có cấu trúc tốt hơn hẳn brief mơ hồ. Rule: ghi format evidence ngay trong brief, không để agent tự chọn.
- **Duyệt diff thật, không duyệt lời agent:** agent báo "chỉ log, không đổi logic" nhưng Boss yêu cầu thấy git diff đầy đủ mới duyệt — lời tự báo chưa phải bằng chứng. Rule: gate approve nhận diff + phân loại hunk, không nhận tóm tắt.
- **Định nghĩa loại hunk cho phép trước:** với change "chỉ log", 4 loại hunk được chấp nhận: LOG / LOCAL-TS / EXECUTOR / TOGGLE. Hunk nào sửa dòng gốc, đổi thứ tự write, đổi return/exception flow thì liệt kê riêng như vi phạm. Rule: đặt whitelist hunk trong brief implement.
- **Self-test phải đi qua đúng đường cần chứng minh:** hash chuỗi cố định chỉ chứng minh hàm sha đúng, không chứng minh hai phía dùng cùng canonical form. Phải thêm fixture cố định đi qua hàm canonical ở cả hai phía. Rule: test cái đang nghi, không test cái đã chắc.
- **Nhóm đối chứng có thể "chữa" bug:** fresh pull phía writer có thể làm lành stale → FAIL(A) < FAIL(C) nghĩa là read-back là thuốc chứ không phải thước đo. Rule: pre-register diễn giải cho trường hợp phép đo làm đổi kết quả, trước khi có số liệu.
- **Nêu rõ cỡ mẫu chứng minh được gì:** 0 lỗi/20 lần chỉ loại được tỷ lệ lỗi trên ~14% (95%), không chứng minh bug biến mất. Rule: báo cáo nêu giới hạn thống kê, không overclaim.
