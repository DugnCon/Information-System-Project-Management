# Ghi chú 03 – Kết quả nghiên cứu (mục 4, 5 của bài báo)

## 4.1 Độ tin cậy (Bảng 5)

Tính trên dữ liệu khảo sát thử. Các nhóm có α từ 0.771 (LP) đến 0.944 (MR). Gộp cả 51 câu thì α = 0.974. Riêng 5 câu về ảnh hưởng tới thành công dự án có α = 0.81. Tất cả đều > 0.7, nên đạt.

Bảng 5 in bị lệch: cột "số câu" bị đẩy xuống một dòng so với tên nhóm. Đọc đúng thì là CL 6, CO 3, CN 3, FD 5, TC 4, RM 5, MR 5, EC 4, PO 4, LP 3, EN 3, SE 3, FM 3.

## 4.2 Hỏi chuyên gia

4 chuyên gia trên 20 năm kinh nghiệm, góp ý gộp, bỏ một số yếu tố. Kết quả là từ 61 yếu tố còn 51.

## 4.3.4 Ma trận PIM – top 10 (Bảng 6)

| # | Rủi ro | Nhóm |
|---|---|---|
| 1 | Ước tính chi phí dự án sai | Khả thi và thiết kế |
| 2 | Ước tính tiến độ sai | Khả thi và thiết kế |
| 3 | Bất ổn chính trị | Chính trị |
| 4 | Nghiên cứu khả thi không đúng | Khả thi và thiết kế |
| 5 | Chậm ra quyết định | Chủ đầu tư |
| 6 | Thiếu dự án hạ tầng | Kinh tế |
| 7 | Vật liệu kém chất lượng | Nguồn lực, vật tư |
| 8 | Thiếu lao động, năng suất thấp | Nguồn lực, vật tư |
| 9 | Quản lý hợp đồng kém | Tư vấn |
| 10 | Phối hợp giữa các nhà thầu kém | Nhà thầu |

Cột tác động và xác suất trong bản PDF bị lệch hàng, không ghép chắc chắn được từng dòng. Riêng dòng 1 rõ ràng là VH – VH.

Nhận xét: 3 trong top 4 là rủi ro **khả thi và thiết kế**, tức là lỗi xảy ra ngay từ giai đoạn lập dự án. Điều này rất gần với môn mình học: ước tính sai chi phí và tiến độ chính là chuyện của lập kế hoạch dự án.

## 4.3.5 RII – top 10 (Bảng 7)

| Hạng | Mã | Rủi ro | RII tổng |
|---|---|---|---|
| 1 | CL2 | Chính phủ bất ổn | 0.578 |
| 2 | FD4 | Ước tính chi phí sai | 0.568 |
| 3 | FD5 | Ước tính tiến độ sai | 0.556 |
| 4 | CL1 | Chậm ra quyết định | 0.554 |
| 5 | PO1 | Bất ổn chính trị | 0.549 |
| 6 | FM3 | Chiến tranh trong nước | 0.548 |
| 7 | TC3 | Điều khoản hợp đồng không rõ | 0.547 |
| 8 | RM1 | Thiếu lao động, năng suất thấp | 0.513 |
| 9 | FD1 | Nghiên cứu khả thi không đúng | 0.508 |
| 10 | EC1 | Khủng hoảng kinh tế, tài chính | 0.504 |

Lạ: "Chính phủ bất ổn" lại xếp vào nhóm **chủ đầu tư** (CL2). Giải thích được nếu chủ đầu tư là nhà nước, nhưng nó lại gần như trùng với PO1 "Bất ổn chính trị".

RII tác động và RII xác suất của từng dòng cũng bị lệch hàng trong PDF. Hôm làm kiểm tra số liệu phải ghép lại bằng cách nhân thử cho ra đúng RII tổng.

## 4.3.6 PLS-SEM

### Mô hình đo lường (Bảng 8, 9, 10)

- Loading của 51 câu hỏi nằm trong khoảng 0.721 (CL6) đến 0.924 (MR3). Đều > 0.7.
- AVE các nhóm bậc 1 từ 0.593 (CL) đến 0.808 (MR, SE). Bậc 2: rủi ro nội bộ AVE 0.570, CR 0.976; bên ngoài AVE 0.638, CR 0.972.
- Biến kết quả (5 câu): AVE 0.549, CR 0.826, α 0.74. Loading: 0.595, 0.761, 0.741, 0.800, 0.591 → có **2 câu dưới 0.7**.
- Fornell–Larcker (Bảng 9) và cross-loading (Bảng 10): tác giả kết luận đạt.

### Mô hình cấu trúc (Bảng 11 – 14, Hình 8)

Ghép Bảng 11 với Hình 8 (cùng thứ tự theo bảng chữ cái tiếng Anh) được hệ số đường dẫn:

| Đường dẫn → Ảnh hưởng tới thành công dự án | β | t |
|---|---|---|
| CL Chủ đầu tư | 0.169 | 26.250 |
| CN Tư vấn | 0.097 | 30.864 |
| CO Nhà thầu | 0.114 | 32.193 |
| EC Kinh tế | 0.231 | 44.082 |
| EN Môi trường, an toàn | 0.154 | 29.027 |
| **Rủi ro bên ngoài** | **0.673** | 10.495 |
| FD Khả thi và thiết kế | 0.197 | 35.234 |
| FM Bất khả kháng | 0.152 | 36.113 |
| **Rủi ro nội bộ** | **0.200** | 3.121 |
| LP Người dân địa phương | 0.152 | 33.357 |
| PO Chính trị | 0.236 | 42.177 |
| MR Quản lý dự án | 0.213 | 36.280 |
| RM Nguồn lực, vật tư | 0.186 | 40.916 |
| SE An ninh | 0.180 | 40.554 |
| TC Đấu thầu, hợp đồng | 0.143 | 43.683 |

Cột t trong PDF cũng bị lệch nên mình ghép theo thứ tự. Phải kiểm tra lại khi gõ CSV.

Các chỉ số còn lại:
- **R² = 0.720**: 72% biến động của "ảnh hưởng tới thành công dự án" được giải thích bởi rủi ro nội bộ và bên ngoài.
- **f²**: bên ngoài 0.471 (lớn), nội bộ 0.042 (nhỏ).
- **Q²** (Bảng 14): 0.369, 0.590, 0.527. Đều > 0, nên mô hình có khả năng dự báo.
- **GoF** = √(R² × AVE trung bình) = √(0.720 × 0.566) = 0.638 > 0.36.

Tự kiểm tra GoF: 0.720 × 0.566 = 0.4075, căn bậc hai được 0.638. Đúng. Nhưng trong bài, công thức in ra là "R2 × AVE2", thiếu dấu căn. Lỗi trình bày.

### Kết luận chính của tác giả

- Rủi ro **bên ngoài** ảnh hưởng mạnh hơn nhiều so với nội bộ (β 0.673 so với 0.200, f² 0.471 so với 0.042).
- Trong nhóm nội bộ, mạnh nhất là quản lý dự án (0.213), khả thi và thiết kế (0.197), nguồn lực (0.186).
- Trong nhóm bên ngoài, mạnh nhất là chính trị (0.236), kinh tế (0.231), an ninh (0.180).

## Mục 5.2 – Năm hậu quả của rủi ro (EF1–EF5)

Xếp theo điểm trung bình:

| Mã | Hậu quả | Điểm TB | Hạng |
|---|---|---|---|
| EF1 | Trễ tiến độ | 3.917 | 1 |
| EF4 | Không đạt mục tiêu dự án | 3.420 | 2 |
| EF5 | Dự án bị dừng | 2.975 | 3 |
| EF2 | Vượt chi phí | 2.755 | 4 |
| EF3 | Chất lượng kém | 2.755 | "6" |

Chỉ có 5 hậu quả mà EF3 lại xếp hạng 6. Tác giả còn nói đã **bỏ EF3** khỏi mô hình, nhưng Bảng 8 vẫn in đủ 5 loading.

## Mục 6 – Khuyến nghị (tóm tắt)

- Chủ đầu tư: lập kế hoạch quản lý rủi ro, ra quyết định nhanh, hạn chế thay đổi, thanh toán đúng hạn.
- Nhà thầu: thuê kỹ sư giỏi, đào tạo văn hoá quản lý rủi ro, có chiến lược chuỗi cung ứng dài hạn.
- Tư vấn: theo sát hiện trường, báo cáo tiến độ hàng quý.
- Chính phủ: cải thiện hạ tầng, giảm thủ tục, chống tham nhũng trong đấu thầu dầu khí.

Khuyến nghị khá chung chung, không gắn với con số nào trong mô hình. Ví dụ không nói vì β của nhóm MR cao nhất trong nội bộ nên phải ưu tiên việc gì trước.
