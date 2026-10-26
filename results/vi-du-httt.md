# Ví dụ 2 – Monte Carlo cho dự án HTTT mẫu

File này do `src/vi_du_httt.py` sinh ra. Thông số dự án là giả định để minh hoạ.

- Đường găng (thời lượng khả dĩ): T1 → T2 → T3 → T5 → T7 → T8 → T9 → T10 → T12 = 90 ngày
- Hạn chót hợp đồng (giả định): 95 ngày
- Không tính rủi ro: trung bình 99.6, P50 99.5, P80 103.9, P90 106.2; xác suất kịp hạn 18.7%
- Có rủi ro: trung bình 118.9, P50 118.2, P80 128.2, P90 134.1; xác suất kịp hạn 0.7%
- Xác suất xong đúng kế hoạch 90 ngày khi có rủi ro: 0.1%

## Chỉ số tới hạn

|     |   chi_so |
|:----|---------:|
| T1  |     1    |
| T2  |     1    |
| T3  |     0.99 |
| T4  |     0.01 |
| T5  |     0.99 |
| T6  |     0.01 |
| T7  |     0.99 |
| T8  |     1    |
| T9  |     1    |
| T10 |     1    |
| T11 |     0    |
| T12 |     1    |

## Độ nhạy (ngày tăng thêm khi rủi ro xảy ra)

|     |   neu_xay_ra |   ky_vong |
|:----|-------------:|----------:|
| R1  |         9.71 |      3.89 |
| R11 |         7.56 |      3.03 |
| R3  |         7.99 |      2.4  |
| R2  |         4.98 |      1.74 |
| R10 |         6.7  |      1.67 |
| R7  |         5.29 |      1.59 |
| R5  |         6.92 |      1.38 |
| R9  |         3.6  |      1.08 |
| R8  |         6.94 |      1.04 |
| R12 |         9.84 |      0.49 |
| R4  |         0.33 |      0.12 |
| R6  |         0.45 |      0.11 |