# Ghi chú 02 – Phương pháp nghiên cứu (mục 3 của bài báo)

## Quy trình tổng thể

Đọc mục 3 rồi tóm lại theo thứ tự:

1. Đọc tài liệu và lập danh sách rủi ro ban đầu (61 yếu tố).
2. Thiết kế bảng hỏi (Hình 2 của bài báo).
3. Khảo sát thử (pilot) rồi hỏi 4 chuyên gia trên 20 năm kinh nghiệm → bớt còn 51 yếu tố.
4. Gửi bảng hỏi chính thức: phát 360 phiếu, thu về 323, dùng được **314**.
5. Phân tích theo 4 bước:
   - SPSS v25: thống kê mô tả, Cronbach's α;
   - RII: xếp hạng rủi ro;
   - Ma trận xác suất – tác động: xếp rủi ro vào vùng;
   - PLS-SEM bằng SmartPLS 3: kiểm định 13 giả thuyết.

Người trả lời: khoảng 44% ở tuổi 40–50, 41% ở tuổi 30–40, chỉ 12 người dưới 30. Về kinh nghiệm: 102 người 10–20 năm, 81 người 5–10 năm, 66 người 20–30 năm, 20 người trên 30 năm. Cộng lại là 269, còn 45 người bài không nói rõ, chắc là dưới 5 năm.

## Bảng hỏi gồm 8 phần

a. Giới thiệu
b. Thông tin người trả lời
c. Câu hỏi chung về quản lý rủi ro ở Yemen
d. **Tác động** của rủi ro nội bộ (thang 1–5)
e. **Xác suất** của rủi ro nội bộ (thang 1–5)
f. **Tác động** của rủi ro bên ngoài
g. **Xác suất** của rủi ro bên ngoài
h. Ảnh hưởng của rủi ro tới thành công dự án

Mỗi yếu tố rủi ro được chấm **hai lần**: một lần cho xác suất xảy ra, một lần cho mức tác động. Đây là chỗ quan trọng, vì RII và ma trận đều cần cả hai con số.

## 1. Cronbach's alpha

Dùng để kiểm tra các câu hỏi trong cùng một nhóm có "nói cùng một chuyện" hay không, tức là độ nhất quán nội bộ. Ví dụ 6 câu về chủ đầu tư thì người trả lời phải chấm khá đồng đều với nhau.

- α < 0.3: dữ liệu không đáng tin.
- α > 0.7: chấp nhận được.

Bảng 5: các nhóm có α từ 0.771 (LP) đến 0.944 (MR); cả 51 câu gộp lại là 0.974.

## 2. RII – Chỉ số tầm quan trọng tương đối

Công thức trong bài (công thức 1):

    RII = W / (A × N)

- W: tổng điểm người trả lời chấm cho yếu tố đó (thang 1–5)
- A: điểm cao nhất của thang, ở đây là 5
- N: số người trả lời

RII nằm trong khoảng từ 1/5 = 0.2 đến 1. Càng gần 1 thì càng quan trọng.

**Chỗ bài viết sai:** bài định nghĩa W là "điểm trung bình có trọng số", giá trị từ 1 đến 5. Nếu W là trung bình thì không được chia thêm cho N nữa, vì như vậy là chia N hai lần. Công thức đúng (theo các bài khác về RII) là W = tổng điểm = Σ(điểm × số người chấm điểm đó). Ghi lại để nêu trong phần phản biện.

### Tự tính thử một ví dụ

Giả sử 5 người chấm **tác động** của rủi ro "Chậm ra quyết định": 5, 4, 4, 3, 5.

- W = 5 + 4 + 4 + 3 + 5 = 21
- RII(tác động) = 21 / (5 × 5) = **0.84**

Cũng 5 người đó chấm **xác suất**: 4, 3, 4, 4, 3.

- W = 18
- RII(xác suất) = 18 / 25 = **0.72**

RII tổng thể theo cách của bài báo (mục 4.3.5: Risk Index = xác suất × mức độ nghiêm trọng):

    RII(tổng) = RII(tác động) × RII(xác suất) = 0.84 × 0.72 = 0.605

Thử kiểm lại với số thật trong Bảng 7: "Chậm ra quyết định" (CL1) có RII tác động 0.675 và RII xác suất 0.821, nhân lại được 0.554, đúng bằng số trong bảng. Vậy cách hiểu này đúng.

Bảng 7 in ra bị lệch cột, nhiều số không nằm đúng hàng. Hôm làm hướng 1 (23/10) phải gõ lại cẩn thận rồi nhân thử từng dòng.

## 3. Ma trận xác suất – tác động (PIM)

Ma trận 5×5: trục ngang là tác động, trục dọc là xác suất. Mỗi trục có 5 mức: Rất thấp (VL), Thấp (L), Trung bình (M), Cao (H), Rất cao (VH).

Mỗi ô được tô màu theo vùng:
- **Đỏ**: rủi ro nghiêm trọng, phải né tránh hoặc giảm thiểu bằng mọi giá.
- **Vàng**: rủi ro trung bình, cần kiểm soát.
- **Xanh**: rủi ro thấp, chỉ cần theo dõi hoặc chấp nhận.

Bảng 6 có top 10 rủi ro. Đứng đầu là "Ước tính chi phí sai" với tác động VH và xác suất VH, rơi vào vùng đỏ đậm nhất.

So với RII: RII cho ra **một con số để xếp hạng**, còn ma trận cho ra **vùng để quyết định cách ứng phó**. Hai cái bổ sung cho nhau. Một điều lạ là thứ hạng giữa hai cách không giống nhau: theo RII thì "Chính phủ bất ổn" đứng số 1, nhưng trong ma trận lại là "Ước tính chi phí sai". Cần tìm hiểu thêm vì sao.

Liên hệ PMBOK: ma trận này chính là công cụ của quy trình **Phân tích rủi ro định tính** (Perform Qualitative Risk Analysis). Môn mình học có nhắc tới nên đưa vào Chương 1.

## 4. SEM – hiểu ở mức cơ bản

Vấn đề: "rủi ro từ chủ đầu tư" là thứ **không đo trực tiếp được**, nên gọi là **biến tiềm ẩn**. Ta chỉ đo được qua các câu hỏi cụ thể CL1…CL6, gọi là **biến quan sát**.

SEM gồm 2 phần:
- **Mô hình đo lường (outer model):** biến tiềm ẩn ↔ các câu hỏi. Kiểm tra xem câu hỏi có đo đúng khái niệm không (loading, AVE, CR).
- **Mô hình cấu trúc (inner model):** biến tiềm ẩn → biến tiềm ẩn. Kiểm tra quan hệ, ví dụ "rủi ro chủ đầu tư" ảnh hưởng tới "thành công dự án" mạnh cỡ nào (hệ số đường dẫn, R²).

Mô hình của bài có **2 bậc**:

    51 câu hỏi → 13 nhóm rủi ro (bậc 1) → rủi ro nội bộ / bên ngoài (bậc 2) → ảnh hưởng tới thành công dự án (5 câu hỏi)

### Vì sao chọn PLS-SEM chứ không phải CB-SEM

Theo bài báo (mục 3.2.5):
- PLS-SEM nhắm tới việc tối đa phương sai được giải thích của biến phụ thuộc, tức là thiên về **dự báo**.
- Không cần dữ liệu phân phối chuẩn. Dữ liệu Likert thường không chuẩn.
- Không cần cỡ mẫu quá lớn.
- Chạy được mô hình phức tạp, nhiều biến.

CB-SEM thì thiên về **kiểm định lý thuyết**, cần dữ liệu chuẩn và mẫu lớn. Chỗ này để dành tới hôm 26/10 đọc sách của Hair và cộng sự rồi viết kỹ hơn.

### Các bước đánh giá PLS-SEM (Bảng 3 của bài)

Mô hình đo lường:
1. Độ tin cậy từng câu hỏi (outer loading ≥ 0.7)
2. Độ tin cậy tổng hợp (CR)
3. AVE ≥ 0.5 (giá trị hội tụ)
4. Giá trị phân biệt: cross-loading, Fornell–Larcker

Mô hình cấu trúc:
1. Kiểm định giả thuyết (hệ số đường dẫn, t, p)
2. R²
3. f²
4. Q²
5. GoF

Ghi chú: bài **không làm HTMT**, trong khi Henseler và cộng sự (2015) đã chỉ ra Fornell–Larcker hay bỏ sót vấn đề. Đây là chỗ mình có thể làm thêm ở phần tái hiện.

## Câu hỏi còn chưa hiểu, để hỏi hoặc tìm thêm

- Thuật toán PLS ước lượng trọng số như thế nào? Đọc chương 3 sách Hair.
- Bootstrapping 5000 lần làm cụ thể ra sao, vì sao cho ra t và p?
- Bài không nói cách chuyển từ trung bình điểm sang mức VL/L/M/H/VH khi xếp vào ma trận. Ngưỡng là bao nhiêu?
- Biến "thành công dự án" đo bằng 5 hậu quả xấu, tức là điểm càng cao thì dự án càng **thất bại**. Vậy hệ số dương nghĩa là rủi ro làm tăng ảnh hưởng xấu. Cần nói rõ chỗ này khi trình bày, tránh hiểu ngược.
