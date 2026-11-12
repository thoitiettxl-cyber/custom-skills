# Verification: DEV / HELD-OUT / REPLAY / ablation

Chi tiết cho PHA 5 trong SKILL.md. SKILL.md giữ quy tắc bắt buộc; file này giữ quy trình thực hiện.

## 1. Floor file (ghi TRƯỚC khi chạy)

Tạo một file riêng, chốt trước khi chạy bất kỳ lượt nào:

```
Floor_abs: <số>/N (chốt SAU baseline nhánh A, TRƯỚC nhánh B/ablation/HELD-OUT)
Delta: <số điểm, lớn hơn dao động trong nhánh>
N: <số mục nhóm (a)>
Cách diễn giải: <điểm nhóm (a) được tính thế nào, trên tập nào>
Quy tắc quyết định: PASS chỉ khi HELD-OUT >= Floor_abs VÀ hơn nhánh A >= Delta; xấp xỉ A là NO-BENEFIT-DETECTED, dưới Floor_abs là FAIL-ABS, chưa đủ điều kiện là UNVERIFIED
Skill chốt (cho HELD-OUT): <đường dẫn + ngày chốt>
Nhánh so sánh (HARDEN-EXISTING): A (không skill) / B (skill hiện tại) / N (<tên>.next, nếu có sửa)
Ngưỡng trigger: xem references/trigger-test.md
```

Không sửa Floor, cách diễn giải hay quy tắc quyết định sau khi đã thấy kết quả, để cho thắng.

## 2. Tập DEV và HELD-OUT

- DEV: >=2 tác vụ, dùng để lặp và sửa skill. Chỉ vòng lặp DEV mới được sửa skill.
- HELD-OUT: >=2 tác vụ, chạy đúng 1 đợt ở cuối, sau khi skill đã chốt.
- KHÔNG sửa skill sau khi thấy kết quả HELD-OUT. Số báo cáo là số HELD-OUT.
- Cảnh báo: sửa skill rồi chạy lại cùng tập HELD-OUT sẽ làm mất tính held-out; muốn sửa tiếp thì cần quyết định mới về tập HELD-OUT.
- Tác vụ cùng stack với REPO nhưng khác domain, trừ REPLAY (xem mục 3).

## 3. REPLAY (>=1 tác vụ mỗi tập)

1. Chọn một repo cùng stack, và kiểm tra repo/commit đó KHÔNG nằm trong nguồn đã dùng để chưng cất skill (đối chiếu danh sách nguồn ở PHA 0 và references/PROVENANCE.md của skill đang đo). Ghi repo, commit fix, commit cha vào file trước khi chạy.
2. Chọn một commit fix có test kèm trong lịch sử repo đó.
3. Reset về commit cha, vào thư mục tạm riêng. Chỉ giao mô tả vấn đề, không giao diff của commit fix và không giao test của commit fix.
4. Chấm bằng test của chính commit fix, giữ kín: test không nằm trong brief, agent không được xem test trước khi làm xong.
5. Không đủ nguồn sạch: nêu rõ trong báo cáo là thiếu REPLAY sạch, hạ độ chắc chắn, không ghi REPLAY là đã kiểm chứng sạch.

## 4. Greenfield (tác vụ còn lại)

- Thiết kế một bẫy ẩn buộc agent tự quyết chính sách, ví dụ lỗi từng phần: một phần tác vụ thất bại, agent phải quyết tiếp tục, bỏ qua phần lỗi, hay dừng và báo.
- Bộ test giữ kín: viết trước, đặt ngoài thư mục agent viết code, không nằm trong brief.
- Brief không nhắc quy tắc nào của skill đang đo, cho mọi nhánh (A, B, N và C_g).
- Nhánh A: môi trường không có skill (thư mục tạm riêng, đường dẫn skills trống hoặc HOME khác). Nhánh B: có skill hiện tại. Nhánh N (HARDEN-EXISTING, nếu có sửa): có <tên>.next. Rubric và tác vụ test không được đưa vào brief của agent viết skill.

## 5. Số lượt và độ dao động

- >=5 lượt/nhánh/tác vụ, cùng brief (trừ sự hiện diện của skill, hoặc nhóm luật bị bỏ ở ablation).
- Ghi cho mỗi lượt: thời gian, số dòng, số lượt tool, điểm nhóm (a), điểm nhóm (b).
- Báo theo từng tác vụ và theo tập: trung bình, min-max, số lượt đạt Floor.
- Độ dao động trong nhánh = khoảng min-max của các lượt cùng nhánh. Nếu chênh lệch trung bình giữa hai nhánh nhỏ hơn độ dao động lớn hơn trong hai nhánh thì kết luận là không phân biệt được, không kết luận nhánh nào tốt hơn.
- Giảm dưới 5 lượt: ghi lý do, trạng thái UNVERIFIED.
- Định nghĩa "lượt": một lượt = một ngữ cảnh agent sạch và độc lập (một agent
  chạy đúng một run). Số lượt báo cáo = số ngữ cảnh độc lập, không phải tổng
  số run. Một batch (một agent chạy nhiều run của cùng một nhánh-task) chỉ
  tính là MỘT ngữ cảnh, không phải nhiều lượt.
- Batch chỉ dùng cho calibration (thăm dò trên DEV): các run trong cùng batch
  là tương quan, không độc lập. Bảng run phải ghi cả hai số: số run và số ngữ
  cảnh độc lập.
- Cấm dùng kết quả batch để suy Delta (Delta phải suy từ range của baseline
  chạy một-agent-mỗi-run, ghi trước khi B/N chạy) và cấm dùng kết quả batch
  để quyết định cắt/giữ nhóm luật ở ablation. Run batch không tính vào yêu cầu
  >=5 lượt/nhánh/tác vụ: 5 run từ 1 agent = 1 lượt, dưới ngưỡng thì tập kết
  luận đó là UNVERIFIED.

## 6. Ablation (chỉ trên DEV)

1. Chia luật thành 3-8 nhóm theo chủ đề, ghi lý do chia nhóm vào file trước khi chạy.
2. Mỗi nhóm g chạy thêm nhánh C_g = skill bỏ nhóm g, còn lại giữ nguyên, chạy trên DEV.
3. Quy tắc quyết định chốt trước khi chạy ablation:
   - Bỏ g làm giảm nhóm (a) theo hướng nhất quán -> giữ nhóm g, nhãn "đã kiểm chứng".
   - Bỏ g không đổi nhóm (a) VÀ không có bằng chứng lịch sử mạnh -> cắt nhóm g.
   - Không tác vụ nào chạm g -> giữ nhóm g, nhãn "chưa kiểm chứng"; nếu được, thiết kế thêm tác vụ chạm g rồi chạy lại ablation trên DEV.
4. Bảng ablation trong báo cáo cuối, cột: nhóm | luật | điểm nhóm (a) đầy đủ (DEV) | điểm nhóm (a) bỏ nhóm (DEV) | chênh | quyết định | nhãn.
5. Luật không được chạm tới trong ablation và trong A/B thì gắn nhãn "chưa kiểm chứng" trong skill đích, không cắt chỉ vì chưa chạm tới.

## 7. Chấm điểm

- Nhóm (a): do máy chấm, từ test giữ kín, exit code, đếm bằng lệnh. Ghi output thô, không sửa tay.
- Nhóm (b): >=2 verifier mù độc lập, không chung ngữ cảnh, không thấy điểm của nhau và không biết nhánh nào là nhánh nào. Mỗi verifier chấm riêng.
- Nếu hai verifier lệch nhau: chạy verifier thứ ba, ghi cả ba số, không trung bình để giấu lệch, không sửa số.
- Orchestrator không tự sửa số của verifier. Người viết skill không chấm điểm.

## 8. Vòng lặp và trạng thái

- Vòng lặp chỉ trên DEV: điểm < Floor_abs -> quay lại PHA 1-4 với bằng chứng mới; tối đa 5 vòng, hoặc dừng khi 2 vòng liên tiếp không cải thiện, rồi báo Boss.
- Trạng thái cuối chỉ một trong bốn: PASS / NO-BENEFIT-DETECTED / FAIL-ABS / UNVERIFIED, theo ĐIỀU KIỆN PASS ở SKILL.md. "HELD-OUT >= Floor_abs" mà không hơn A >= Delta là NO-BENEFIT-DETECTED, không phải PASS.
