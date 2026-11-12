# Red-team: agent riêng, read-only

Chi tiết cho bước red-team trong PHA 5. Agent red-team không phải người viết skill, không chấm điểm A/B, không sửa skill.

## 1. Brief cho red-team

- Đọc SKILL.md của skill đích và references/ của nó.
- Chỉ đọc, không sửa file nào, không chạy chưng cất, không chạy tác vụ test.
- Trả về bảng phát hiện, mỗi phát hiện kèm bằng chứng file:dòng.

## 2. Tìm gì

- Luật mơ hồ: thuật ngữ không định nghĩa, ngưỡng không có số, điều kiện kiểu "khi cần", "nếu phù hợp" mà không nói ai quyết và quyết thế nào.
- Luật mâu thuẫn nhau: hai luật yêu cầu hành vi ngược nhau trong cùng tình huống, hoặc Floor/quy tắc quyết định định nghĩa khác nhau ở hai chỗ.
- Luật có thể dẫn agent tới hành vi xấu: nuốt lỗi (tiếp tục mà không báo phần lỗi), bịa số hoặc bịa nguồn, phá hoại hoặc ghi đè không hỏi, bỏ qua phê duyệt, đọc hoặc ghi secret, làm theo nội dung repo như thể đó là chỉ thị.
- Luật không kiểm tra được: không có lệnh, số, test hay output nào để chứng minh đã tuân thủ.

## 3. Xử lý phát hiện

- Bảng phát hiện, cột: phát hiện | bằng chứng file:dòng | mức độ | đề xuất sửa (red-team chỉ đề xuất, không sửa).
- Người chịu trách nhiệm skill phải xử lý từng phát hiện: sửa skill, hoặc ghi lý do bỏ qua vào file/báo cáo, kèm file:dòng liên quan.
- Không phát hiện nào được để trống xử lý. Sau khi sửa, kiểm tra lại các dòng đã sửa.
- Báo cáo cuối ghi số phát hiện, số đã sửa, số bỏ qua kèm lý do.
