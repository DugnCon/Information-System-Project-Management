# Kết quả phân tích trên dữ liệu mô phỏng

File này do `src/phan_tich_mo_phong.py` sinh ra. Dữ liệu: 314 phiếu mô phỏng (`data/simulated/`), bootstrapping 5000 lần.

## 1. Độ tin cậy Cronbach's α

|    |   so_cau |   alpha_mo_phong |   alpha_bai_bao |
|:---|---------:|-----------------:|----------------:|
| CL |        6 |            0.869 |           0.898 |
| CO |        3 |            0.898 |           0.883 |
| CN |        3 |            0.848 |           0.834 |
| FD |        5 |            0.918 |           0.926 |
| TC |        4 |            0.875 |           0.838 |
| RM |        5 |            0.882 |           0.895 |
| MR |        5 |            0.934 |           0.944 |
| EC |        4 |            0.913 |           0.922 |
| PO |        4 |            0.918 |           0.915 |
| LP |        3 |            0.875 |           0.771 |
| EN |        3 |            0.904 |           0.861 |
| SE |        3 |            0.869 |           0.899 |
| FM |        3 |            0.873 |           0.878 |
| EF |        5 |            0.796 |           0.81  |

Bài báo tính α trên dữ liệu khảo sát thử (pilot), còn ở đây tính trên toàn bộ 314 phiếu mô phỏng, nên chỉ so sánh được mức độ, không so được từng con số.

## 2. RII

Top 10 của bài báo, so với RII tính trên dữ liệu mô phỏng:

| ma   |   rii_bai_bao |   hang_bai_bao |   rii_mo_phong |   hang_mo_phong |
|:-----|--------------:|---------------:|---------------:|----------------:|
| CL2  |         0.578 |              1 |          0.548 |               2 |
| FD4  |         0.568 |              2 |          0.56  |               1 |
| FD5  |         0.556 |              3 |          0.545 |               3 |
| CL1  |         0.554 |              4 |          0.54  |               4 |
| PO1  |         0.549 |              5 |          0.536 |               5 |
| FM3  |         0.548 |              6 |          0.523 |               7 |
| TC3  |         0.547 |              7 |          0.524 |               6 |
| RM1  |         0.513 |              8 |          0.492 |              10 |
| FD1  |         0.508 |              9 |          0.5   |               8 |
| EC1  |         0.504 |             10 |          0.482 |              13 |

9/10 rủi ro của top 10 bài báo vẫn nằm trong top 10 mô phỏng. Sai lệch nhỏ đến từ việc làm tròn điểm sang thang 1–5 và từ nhiễu ngẫu nhiên khi sinh 314 phiếu.

## 3. PLS-SEM – mô hình đo lường

Mô hình bậc 2 theo cách lặp chỉ báo: khối INT gồm 31 câu, EXT gồm 20 câu, EF gồm 4 câu (đã bỏ EF3). Thuật toán hội tụ sau 7 vòng lặp.

| khoi   |   so_cau |   loading_min |   alpha |    cr |   ave |   ave_bai_bao |   cr_bai_bao |
|:-------|---------:|--------------:|--------:|------:|------:|--------------:|-------------:|
| CL     |        6 |         0.699 |   0.869 | 0.902 | 0.606 |         0.593 |        0.897 |
| CO     |        3 |         0.902 |   0.898 | 0.937 | 0.831 |         0.764 |        0.907 |
| CN     |        3 |         0.845 |   0.848 | 0.908 | 0.767 |         0.735 |        0.893 |
| FD     |        5 |         0.808 |   0.918 | 0.939 | 0.756 |         0.768 |        0.943 |
| TC     |        4 |         0.823 |   0.875 | 0.914 | 0.727 |         0.705 |        0.905 |
| RM     |        5 |         0.78  |   0.882 | 0.914 | 0.681 |         0.695 |        0.919 |
| MR     |        5 |         0.872 |   0.934 | 0.95  | 0.791 |         0.808 |        0.955 |
| EC     |        4 |         0.87  |   0.913 | 0.939 | 0.793 |         0.779 |        0.934 |
| PO     |        4 |         0.883 |   0.918 | 0.942 | 0.803 |         0.793 |        0.939 |
| LP     |        3 |         0.878 |   0.875 | 0.923 | 0.8   |         0.734 |        0.892 |
| EN     |        3 |         0.913 |   0.904 | 0.94  | 0.839 |         0.805 |        0.925 |
| SE     |        3 |         0.863 |   0.869 | 0.92  | 0.792 |         0.808 |        0.926 |
| FM     |        3 |         0.882 |   0.873 | 0.922 | 0.798 |         0.763 |        0.906 |
| INT    |       31 |         0.571 |   0.971 | 0.973 | 0.535 |         0.57  |        0.976 |
| EXT    |       20 |         0.71  |   0.966 | 0.969 | 0.608 |         0.638 |        0.972 |
| EF     |        4 |         0.701 |   0.777 | 0.858 | 0.603 |         0.549 |        0.826 |

CR của INT và EXT vượt 0.95, giống bài báo (0.976 và 0.972). Theo Hair và cộng sự (2019), CR > 0.95 là dấu hiệu các câu hỏi trùng lặp. Với cách lặp chỉ báo thì điều này gần như chắc chắn xảy ra, vì một khối gom tới 20–31 câu.

### Fornell–Larcker

Vi phạm: không có.

### HTMT

Trung bình 0.729, lớn nhất 0.872 (MR–RM). 3/91 cặp > 0.85, 0/91 cặp > 0.90.

Các cặp vượt ngưỡng 0.85: MR–RM 0.872, PO–EC 0.867, SE–EC 0.859.

HTMT được tính từ tương quan giữa các câu hỏi nên không bị "pha loãng" như tương quan giữa điểm biến tiềm ẩn. Vì dữ liệu mô phỏng giữ đúng tương quan của Bảng 9 trong bài báo, kết quả này cho thấy nếu tác giả tính HTMT thì nhiều khả năng sẽ có các cặp vượt ngưỡng.

## 4. PLS-SEM – mô hình cấu trúc

### Đường dẫn bậc 2 → thành công dự án

| tu   | den   |   beta |     se |      t |   p |   ci_2.5% |   ci_97.5% |   beta_bai_bao |   se_bai_bao |
|:-----|:------|-------:|-------:|-------:|----:|----------:|-----------:|---------------:|-------------:|
| INT  | EF    | 0.3024 | 0.0642 | 4.708  |   0 |    0.1815 |     0.4319 |          0.2   |       0.0641 |
| EXT  | EF    | 0.4919 | 0.064  | 7.6816 |   0 |    0.3574 |     0.6115 |          0.673 |       0.0641 |

R²(EF) = 0.581 (bài báo 0.720); f²(INT) = 0.067 (bài báo 0.042); f²(EXT) = 0.178 (bài báo 0.471). R²(INT) = 1.000, R²(EXT) = 1.000 (gần 1 là đương nhiên với cách lặp chỉ báo).

Dữ liệu được sinh với quan hệ thật EF = 0.200·INT + 0.673·EXT (R² thật ≈ 0.72). PLS-SEM ước lượng trên điểm tổ hợp có lẫn sai số đo nên R² thu được thấp hơn và hai hệ số bị kéo lại gần nhau, đúng với hạn chế đã nêu ở mục 2.7 (Dijkstra và Henseler, 2015). Kết luận định tính vẫn giữ nguyên: rủi ro bên ngoài tác động mạnh hơn rủi ro nội bộ.

### Q² (blindfolding, D = 7)

| bien   |   so_cau |   sso |      sse |    q2 |   q2_bai_bao |
|:-------|---------:|------:|---------:|------:|-------------:|
| EF     |        4 |  1256 |  822.698 | 0.345 |        0.369 |
| INT    |       31 |  9734 | 4814.53  | 0.505 |        0.527 |
| EXT    |       20 |  6280 | 2718.74  | 0.567 |        0.59  |

GoF = √(AVE trung bình của 13 nhóm và EF × R² của EF) = √(0.756 × 0.581) = 0.663. Bài báo: 0.638 với AVE trung bình 0.566.

### 13 giả thuyết H1–H13: tổng hiệu ứng của từng nhóm lên thành công dự án

Trong mô hình bậc 2, mỗi nhóm chỉ tác động lên EF gián tiếp qua INT hoặc EXT. Tổng hiệu ứng = (hệ số nhóm → khái niệm bậc 2) × (hệ số khái niệm bậc 2 → EF).

| tu   |   beta |     se |      t |   beta_bai_bao |   se_bai_bao |   t_bai_bao |
|:-----|-------:|-------:|-------:|---------------:|-------------:|------------:|
| CL   | 0.0526 | 0.0115 | 4.5709 |          0.169 |       0.0064 |      26.25  |
| CO   | 0.0395 | 0.0086 | 4.6129 |          0.114 |       0.0035 |      32.193 |
| CN   | 0.0325 | 0.0071 | 4.5564 |          0.097 |       0.0031 |      30.864 |
| FD   | 0.0614 | 0.0131 | 4.7013 |          0.197 |       0.0056 |      35.234 |
| TC   | 0.0446 | 0.0095 | 4.7117 |          0.143 |       0.0033 |      43.683 |
| RM   | 0.0547 | 0.0116 | 4.7136 |          0.186 |       0.0045 |      40.916 |
| MR   | 0.0661 | 0.014  | 4.7247 |          0.213 |       0.0059 |      36.28  |
| EC   | 0.1166 | 0.0151 | 7.7012 |          0.231 |       0.0052 |      44.082 |
| PO   | 0.1149 | 0.0147 | 7.8022 |          0.236 |       0.0056 |      42.177 |
| LP   | 0.0827 | 0.0109 | 7.61   |          0.152 |       0.0046 |      33.357 |
| EN   | 0.0851 | 0.0111 | 7.669  |          0.154 |       0.0053 |      29.027 |
| SE   | 0.0847 | 0.0111 | 7.5994 |          0.18  |       0.0044 |      40.554 |
| FM   | 0.0811 | 0.0108 | 7.5058 |          0.152 |       0.0042 |      36.113 |

Theo cách ước lượng chuẩn, tổng hiệu ứng của từng nhóm chỉ 0.033–0.117 với t = 4.6–7.8, sai số chuẩn 0.007–0.015. Bài báo in hệ số 0.097–0.236, sai số chỉ 0.003–0.006 và t = 26–44. Như vậy 13 hệ số trong bài không phải tổng hiệu ứng theo cách lặp chỉ báo; bài báo cũng không cho biết chúng được tính bằng cách nào. Thứ tự tương đối thì giống nhau: các nhóm bên ngoài (EC, PO) và MR, FD có hệ số lớn nhất.
