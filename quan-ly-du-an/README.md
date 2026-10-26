# Quản lý dự án làm báo cáo

Áp dụng chính các công cụ của môn học để quản lý việc làm báo cáo giữa kỳ.

| File | Mở bằng | Nội dung |
|---|---|---|
| `quan-ly-du-an.xlsx` | Excel | 5 sheet: WBS, Gantt, Rủi ro, Barem, Nhật ký |
| `ke-hoach.xml` | MS Project | Kế hoạch dự án: WBS, lịch 7 ngày, baseline, % hoàn thành, ngày trạng thái |

Hai file được sinh từ cùng một bảng công việc trong `src/quan_ly_du_an.py`, nên luôn khớp nhau.

## Excel – `quan-ly-du-an.xlsx`

- **WBS**: phân rã công việc, ngày kế hoạch (KH, theo PLAN.md) và ngày thực tế (TT, theo lịch sử commit). Chênh lệch, trạng thái, % của nhóm và % toàn dự án đều là công thức. Ô `B2` là ngày báo cáo.
- **Gantt**: □ = kế hoạch, ■ = thực tế; cột viền đỏ là ngày báo cáo. Sheet tự cập nhật theo WBS.
- **Rủi ro**: sổ đăng ký rủi ro của chính dự án này. Điểm = P × I, vùng màu dùng cùng quy ước với ma trận PIM trong báo cáo.
- **Barem**: đối chiếu barem slide 52 và yêu cầu hình thức slide 54, tính điểm dự kiến.
- **Nhật ký**: số commit theo ngày.

Ô **nền vàng, chữ xanh** là ô nhập tay. Các ô khác là công thức, không sửa.

## MS Project – `ke-hoach.xml`

1. Mở MS Project → **File → Open** → chọn kiểu file **XML Format (\*.xml)** → chọn `ke-hoach.xml` → chọn *As a new project*.
2. **File → Save As** → lưu thành `ke-hoach.mpp`.
3. Xem **View → Tracking Gantt** để thấy baseline (kế hoạch ban đầu) so với thực tế. Ngày trạng thái là 26/10/2026.

## Cập nhật tiến độ

Sửa ngày thực tế và % hoàn thành trong `CONG_VIEC`, sửa `NGAY_BAO_CAO` ở đầu `src/quan_ly_du_an.py`, rồi chạy:

```
python src/quan_ly_du_an.py
```
