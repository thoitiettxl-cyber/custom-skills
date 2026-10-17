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

## 2026-10-16 — Sing-box: đo trước khi sửa

- **Verify giả thuyết bằng bảng mẫu thô trước khi đổi code:** nghi password "rotate mỗi exec" (TTL ngắn) → probe 908 domains liên tiếp (~1h) bằng 1 credential duy nhất: 908/908 CONNECT 200, 0× 407 → giả thuyết SAI, password ổn định. Bằng chứng: `~/workspace/apk-domains/egress-probe-full.tsv` (908 dòng).

## 2026-10-17 — Sing-box watchdog: trigger log và live test

- **Trigger quét log phải theo byte offset, không tail N:** watchdog chỉ xét lines mới hơn offset trong `.authfail-offset` (reset khi rotate; lần đầu chỉ baseline, không act). Không offset → quét lại dòng cũ → vòng lặp restart.
- **Chứng minh chuỗi log bằng instance cố tình hỏng, không dùng live:** trigger `authentication required` được chứng minh bằng instance tạm đặt password sai — không bao giờ thử trên tunnel live.
- **Process cha sống lâu đóng băng env:** env của run.sh bị đóng băng lúc start (chứng minh qua /proc: run.sh pid 27410 sha8 `1f4cf5f2` vs fresh shell `601243fd`) → khi trigger, kill run.sh (không chỉ child) rồi respawn lấy env tươi.
- **Live test bắt 2 bug mà review tĩnh bỏ sót** (fix ngay cùng commit): (1) watchdog dùng chung `.watchdog.lock` với run.sh — run.sh giữ lock suốt đời nên `flock -n` của watchdog luôn fail, exit im lặng không bao giờ check; fix: lock riêng `.watchdog-wd.lock`. (2) `sleep 3` sau kill không đủ — sing-box child thừa kế fd lock từ run.sh, instance mới bị "another instance holds the lock"; fix: wait loop tối đa 20s chờ cả run.sh lẫn child chết hẳn.

## 2026-10-17 — Linkage survey: red-team bắt bug thật

- **Review ngoài trước apply bắt bug thật:** red-team bắt 2 lỗi thật — 7 scripts quên strip `//` phía A gây báo oan; regex của một check bắt nhầm tên class. Rule: giữ review gate độc lập trước khi apply; reviewer đọc diff/code, không đọc tóm tắt.

## 2026-10-17 — Security audit run-1: kỷ luật verify và báo cáo

- **Cô lập held-out bằng cấu trúc, không bằng lời dặn:** recall item creatorPackage được hunter h-u03 rediscover độc lập → recall 1/1. Bằng chứng: worktree sạch detached tại d08d2e9, 0 untracked files; held-out list chỉ nằm ở PLAN.md phía parent, không có trong snapshot; brief hunter không chứa nội dung plan; mapping "commit = known finding" chưa từng commit vào repo.
- **Trích nguyên văn định nghĩa status khi báo cáo:** đã báo "16/16 complete / 100% trust-boundary" rồi phải sửa thành 12/16 = 75% sau khi đọc lại HUNTING.md (`candidate` ≠ `covered`; covered đòi "no candidate").
- **Finalize artifact trước khi verifier thấy:** rework findings 1-2 (attacker model, precondition, severity) inline TRƯỚC khi spawn Phase-5 → cả 3 verifier trả "verified" ngay vòng đầu, không tốn vòng replace.
- **Verifier độc lập sinh evidence mới:** v-fp5 (chưa từng thấy candidate) không chỉ confirm mà tìm ra cơ chế spoof cụ thể (`createPackageContext`) + phát hiện receiver không bao giờ đọc `creatorUid` (grep toàn repo: 0 tham chiếu).
- **Vi phạm thứ tự phải ghi nhận:** spawn v-fp5 trước khi gửi breakdown (trái điều kiện Boss) → ghi vào run-notes.md ngay theo lệnh Boss, không lặng lẽ cho qua.
- **Ledger chi tiêu theo invocation:** trần 25→31, mỗi spawn đánh số (26/31, 27/31…), tổng dừng ở 29/31.

## Changelog (thiết kế, chưa kiểm chứng)

### 2026-10-17 — v2: kỷ luật verify/báo cáo từ audit run-1 + bài học sing-box watchdog

- **v2 thay thế 5.3 (reset baseline, không phải downgrade):** dòng 5.x là các bước tăng dần từ v5 (Floor/Target); v2 là baseline mới hợp nhất toàn bộ — đọc v2 thay cho mọi bản 5.x trước đó.
- lessons.md: 6 lessons audit (cô lập held-out, quote định nghĩa status, finalize trước verify, verifier độc lập, ghi nhận vi phạm thứ tự, ledger chi tiêu) + đo-trước-sửa (password rotation) + trigger log theo offset + instance hỏng chứng minh chuỗi log + env đóng băng + 2 bug live test + red-team bắt bug thật.
- SKILL.md: bổ sung ledger chi tiêu + quote định nghĩa (Phase 0), cô lập held-out bằng cấu trúc (Phase 1), verifier independence + finalize-trước-verify (Phase 3). Gate verify→propose→approve→live test→commit giữ nguyên.

### 2026-10-16 — Floor/Target cho goal khó

- **Goal khó cần tách Floor/Target để không xung đột với stop rule:** một ngưỡng duy nhất vừa là "mục tiêu tham vọng" vừa là điều kiện dừng sẽ ép agent hoặc bỏ cuộc sớm, hoặc nới lỏng metric để "đạt". v5 tách thành Floor (chỉ mức này quyết pass/fail và vòng lặp 3 vòng / không cải thiện / Boss quyết) và Target (khó nhưng khả thi, đưa vào brief như mức đạt được). Rule: đạt Floor, chưa đạt Target → PASS — agent báo evidence về điểm chặn, cấm đổi cách đo; external verifier bắt buộc điều này.

### 2026-10-16 — 5.1: Floor thay threshold, thêm block TDD ở Phase 2, general.md thành v1 lịch sử.

### 2026-10-16 — 5.2: refactor thành finding Phase 3, file test vào whitelist.

### 2026-10-16 — 5.3: Phase 2 trỏ sang skill tdd.
