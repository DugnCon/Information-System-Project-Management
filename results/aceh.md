# Áp dụng quy trình của Kassem (2022) trên dữ liệu thật: chậm trễ dự án xây dựng ở Aceh

File này do `src/du_lieu_that_aceh.py` sinh ra. Dữ liệu: Rauzana (2021), Mendeley Data, doi:10.17632/2wckhrzz5j.1, CC BY 4.0. n = 68 nhà thầu, 60 yếu tố, 10 nhóm, biến kết quả Y (4 câu).

## 1. Kiểm tra đọc dữ liệu so với bài gốc (Rauzana & Dharma, 2022)

- Cronbach's α thấp nhất: Chính trị 0.638 (bài gốc: Chính trị 0,638)
- Cronbach's α cao nhất: Lao động 0.944 (bài gốc: Lao động 0,944)
- Tổng điểm cao nhất: X8.5 = 327 (bài gốc: X8.5 = 327); thấp nhất: X8.1 = 234 (bài gốc: X8.1 = 234)
- Cronbach's α của Y1–Y4: 0.946 → bốn câu đo cùng một khái niệm, dùng làm biến kết quả.

## 2. RII theo mức ảnh hưởng (RII = tổng điểm / (5 × n))

| 9    | yeu_to                                      | nhom      |   rii |   hang |
|:-----|:--------------------------------------------|:----------|------:|-------:|
| X8.5 | Chậm phê duyệt ngân sách                    | Chính trị | 0.962 |      1 |
| X3.2 | Chủ đầu tư chậm thanh toán                  | Tài chính | 0.938 |      2 |
| X8.6 | Tổ chức quần chúng phản đối vì lợi ích nhóm | Chính trị | 0.935 |      3 |
| X3.4 | Chi phí vận hành, quản lý của nhà thầu cao  | Tài chính | 0.932 |      4 |
| X3.1 | Tình hình tài chính kém khi thi công        | Tài chính | 0.932 |      4 |
| X6.3 | Lỗi thiết kế của đơn vị lập kế hoạch        | Thực hiện | 0.926 |      6 |
| X8.3 | Ý kiến cơ quan khác làm thay đổi thiết kế   | Chính trị | 0.921 |      7 |
| X6.4 | Phát sinh khối lượng                        | Thực hiện | 0.918 |      8 |
| X2.1 | Thiết bị hỏng                               | Thiết bị  | 0.918 |      8 |
| X1.4 | Vật tư hư hỏng khi lưu kho                  | Vật tư    | 0.915 |     10 |

RII trung bình theo nhóm: Tài chính 0.918, Thiết bị 0.910, Vật tư 0.884, Thực hiện 0.880, Chính trị 0.878, Quản lý 0.875, Tội phạm 0.870, Lao động 0.868, Môi trường 0.846, Giám đốc dự án 0.816.

## 3. PLS-SEM

### Mô hình đo lường (mô hình bậc 1: 10 nhóm → Y)

| khoi   | nhom           |   so_cau |   loading_min |   alpha |    cr |   ave |
|:-------|:---------------|---------:|--------------:|--------:|------:|------:|
| X1     | Vật tư         |        9 |         0.703 |   0.943 | 0.949 | 0.677 |
| X2     | Thiết bị       |        3 |         0.731 |   0.819 | 0.886 | 0.725 |
| X3     | Tài chính      |        4 |         0.683 |   0.916 | 0.948 | 0.821 |
| X4     | Môi trường     |        5 |         0.784 |   0.903 | 0.938 | 0.753 |
| X5     | Lao động       |        8 |         0.779 |   0.944 | 0.958 | 0.74  |
| X6     | Thực hiện      |        4 |         0.289 |   0.787 | 0.897 | 0.711 |
| X7     | Quản lý        |        8 |         0.724 |   0.937 | 0.947 | 0.69  |
| X8     | Chính trị      |        6 |        -0.35  |   0.638 | 0.842 | 0.576 |
| X9     | Tội phạm       |        6 |         0.332 |   0.913 | 0.721 | 0.332 |
| X10    | Giám đốc dự án |        7 |        -0.013 |   0.902 | 0.867 | 0.535 |
| Y      | Y (chậm trễ)   |        4 |         0.914 |   0.946 | 0.967 | 0.879 |

- 14/64 câu có loading < 0,708. AVE < 0,5 ở: Tội phạm.
- HTMT: lớn nhất 0.549; 0/55 cặp > 0,85.

### Mô hình cấu trúc bậc 1 (10 nhóm → Y)

| nhom           |   beta |    se |     t |     p |
|:---------------|-------:|------:|------:|------:|
| Chính trị      |  0.3   | 0.088 | 3.39  | 0.001 |
| Giám đốc dự án |  0.243 | 0.13  | 1.859 | 0.063 |
| Quản lý        |  0.229 | 0.076 | 3.002 | 0.003 |
| Lao động       |  0.223 | 0.097 | 2.298 | 0.022 |
| Tài chính      |  0.217 | 0.084 | 2.57  | 0.01  |
| Vật tư         |  0.174 | 0.099 | 1.753 | 0.08  |
| Tội phạm       |  0.158 | 0.18  | 0.88  | 0.379 |
| Thiết bị       |  0.152 | 0.083 | 1.831 | 0.067 |
| Môi trường     |  0.123 | 0.084 | 1.457 | 0.145 |
| Thực hiện      |  0.045 | 0.072 | 0.623 | 0.534 |

- R²(Y) = 0.683; Q²(Y) = 0.576; GoF = 0.680
- Số nhóm có ý nghĩa (p < 0,05): 4/10 (Chính trị, Quản lý, Lao động, Tài chính).

### Mô hình bậc 2 như Kassem (nội bộ / bên ngoài → Y)

Nội bộ: Vật tư, Thiết bị, Tài chính, Lao động, Thực hiện, Quản lý, Giám đốc dự án. Bên ngoài: Môi trường, Chính trị, Tội phạm.

|              |   beta |     se |     t |      p |   ci_2.5% |   ci_97.5% |
|:-------------|-------:|-------:|------:|-------:|----------:|-----------:|
| ('INT', 'Y') | 0.47   | 0.1824 | 2.577 | 0.01   |   -0.0124 |     0.7172 |
| ('EXT', 'Y') | 0.3215 | 0.1796 | 1.79  | 0.0735 |   -0.1008 |     0.6146 |

- R²(Y) = 0.343; f² nội bộ = 0.335; f² bên ngoài = 0.157

## 4. So sánh với Kassem (2022)

| Chỉ số | Kassem – Yemen (công bố) | Aceh – dữ liệu thật (tính lại) |
|---|---|---|
| Cỡ mẫu | 314 | 68 |
| R² của biến kết quả | 0,720 | 0.343 |
| β nội bộ / bên ngoài | 0,200 / 0,673 | 0.470 / 0.321 |
| t nội bộ / bên ngoài | 3,1 / 10,5 | 2.6 / 1.8 |
| Số nhóm bậc 1 có ý nghĩa | 13/13 (t = 26–44) | 4/10 (mô hình bậc 1) |
