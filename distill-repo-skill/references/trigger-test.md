# Trigger test: >=20 truy vấn

Chi tiết cho bước kiểm tra trigger trong PHA 5. Mục đích: description (frontmatter + H1) phải đủ rõ để skill được tìm thấy đúng lúc, và không bị tìm thấy sai lúc.

## 1. Lập bộ truy vấn TRƯỚC khi chạy

- Tổng >=20 truy vấn, không chứa tên skill trong bất kỳ truy vấn nào.
- 10 truy vấn nên khớp: các cách diễn đạt tự nhiên của Boss khi muốn chưng cất/rút skill từ một repo, kể cả repo không có file hướng dẫn sẵn.
- 10 truy vấn không nên khớp: tạo skill từ ý tưởng không có repo nguồn, hỏi cú pháp, việc nhỏ, hoặc việc đã có skill chuyên biệt. Ngoại lệ HARDEN-EXISTING: truy vấn "kiểm chứng và vá một skill đã tồn tại, làm trên bản sao, không sửa gốc" là nên khớp (không xếp vào nhóm không nên khớp chỉ vì nó nhắc tới sửa skill sẵn có); sửa skill sẵn có tùy ý, không theo chế độ HARDEN-EXISTING, vẫn là không nên khớp.
- Truy vấn viết bằng cách diễn đạt tự nhiên, không sao chép nguyên văn description của skill, không nhắc tên skill.
- Ghi bộ truy vấn, ngưỡng và ngày chốt vào file TRƯỚC khi chạy.

## 2. Ngưỡng chốt trước

Ghi vào file trước khi chạy, ví dụ:

```
Ngưỡng: <số>/20 truy vấn đúng (đúng = nên khớp thì ra skill này, không nên khớp thì không xếp skill này trên skill chuyên biệt)
```

Không hạ ngưỡng sau khi thấy kết quả để cho đạt.

## 3. Chạy và ghi

- Chạy skill search cho từng truy vấn, ghi: truy vấn, có ra skill này không, vị trí xếp hạng, skill nào xếp trên (nếu có).
- Tính tỉ lệ đúng tổng, tỉ lệ đúng nhóm nên khớp, tỉ lệ đúng nhóm không nên khớp.
- Nếu dưới ngưỡng: sửa description (frontmatter + H1 cho khớp nhau), chạy lại toàn bộ bộ truy vấn, ghi lại kết quả mỗi vòng. Lặp cho tới khi đạt ngưỡng.
- Báo cáo cuối ghi: bộ truy vấn, ngưỡng chốt trước, tỉ lệ đúng cuối cùng, số vòng đã sửa description.

## 4. Lưu ý

- Trigger test chỉ kiểm tra khả năng được tìm thấy, không thay thế kiểm chứng A/B ở references/verification.md.
- Nếu description sửa nhiều vòng vẫn không đạt, báo rõ và không ghi là đã đạt.
