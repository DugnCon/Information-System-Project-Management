# Kết quả kiểm tra lại số liệu đã công bố

File này do `src/kiem_tra_so_lieu.py` sinh ra. Sai số chấp nhận: ±0.0015 (làm tròn 3 chữ số).

## 1. RII tổng = RII tác động × RII xác suất (Bảng 7)

| ma   |   rii_tac_dong |   rii_xac_suat |   rii_tong |   rii_tong_tinh_lai | ket_qua   |   hang_tong |   hang_tinh_lai |
|:-----|---------------:|---------------:|-----------:|--------------------:|:----------|------------:|----------------:|
| CL1  |          0.675 |          0.821 |      0.554 |              0.5542 | khớp      |           4 |               4 |
| CL2  |          0.779 |          0.742 |      0.578 |              0.578  | khớp      |           1 |               1 |
| FD1  |          0.707 |          0.718 |      0.508 |              0.5076 | khớp      |           9 |               9 |
| FD4  |          0.717 |          0.793 |      0.568 |              0.5686 | khớp      |           2 |               2 |
| FD5  |          0.714 |          0.779 |      0.556 |              0.5562 | khớp      |           3 |               3 |
| TC3  |          0.625 |          0.875 |      0.547 |              0.5469 | khớp      |           7 |               7 |
| EC1  |          0.634 |          0.796 |      0.504 |              0.5047 | khớp      |          10 |              10 |
| RM1  |          0.678 |          0.757 |      0.513 |              0.5132 | khớp      |           8 |               8 |
| PO1  |          0.656 |          0.836 |      0.549 |              0.5484 | khớp      |           5 |               5 |
| FM3  |          0.645 |          0.85  |      0.548 |              0.5482 | khớp      |           6 |               6 |

10/10 dòng khớp trong sai số làm tròn. Thứ hạng tính lại giống thứ hạng trong bài.

## 2. Ma trận PIM (Bảng 6) so với RII (Bảng 7)

Quy đổi RII sang mức theo thang chia đều 0.2 (giả định của mình, bài báo không nói cách quy đổi).

|   hang_pim | ma   | tac_dong   | xac_suat   |   rii_tac_dong |   rii_xac_suat | tac_dong_tu_rii   | xac_suat_tu_rii   | nhat_quan   |   hang_rii |
|-----------:|:-----|:-----------|:-----------|---------------:|---------------:|:------------------|:------------------|:------------|-----------:|
|          1 | FD4  | VH         | VH         |          0.717 |          0.793 | H                 | H                 | KHÔNG       |          2 |
|          2 | FD5  | VH         | H          |          0.714 |          0.779 | H                 | H                 | KHÔNG       |          3 |
|          3 | PO1  | H          | VH         |          0.656 |          0.836 | H                 | VH                | có          |          5 |
|          4 | FD1  | H          | VH         |          0.707 |          0.718 | H                 | H                 | KHÔNG       |          9 |
|          5 | CL1  | H          | VH         |          0.675 |          0.821 | H                 | VH                | có          |          4 |
|          8 | RM1  | H          | H          |          0.678 |          0.757 | H                 | H                 | có          |          8 |

3/6 rủi ro có mức trong Bảng 6 khớp với RII ở Bảng 7. Thứ hạng giữa hai cách cũng khác nhau, ví dụ CL2 'Chính phủ bất ổn' đứng đầu RII nhưng không có trong top 10 PIM.

## 3. AVE và CR tính lại từ loading (Bảng 8)

AVE = trung bình bình phương loading; CR = (Σλ)² / ((Σλ)² + Σ(1 − λ²)).

| nhom   |   so_cau |   loading_min |   ave_bai_bao |   ave_tinh_lai | ave   |   cr_bai_bao |   cr_tinh_lai | cr   |
|:-------|---------:|--------------:|--------------:|---------------:|:------|-------------:|--------------:|:-----|
| CL     |        6 |         0.721 |         0.593 |          0.593 | khớp  |        0.897 |         0.897 | khớp |
| CO     |        3 |         0.855 |         0.764 |          0.764 | khớp  |        0.907 |         0.907 | khớp |
| CN     |        3 |         0.823 |         0.735 |          0.735 | khớp  |        0.893 |         0.893 | khớp |
| FD     |        5 |         0.803 |         0.768 |          0.768 | khớp  |        0.943 |         0.943 | khớp |
| TC     |        4 |         0.784 |         0.705 |          0.705 | khớp  |        0.905 |         0.905 | khớp |
| RM     |        5 |         0.757 |         0.695 |          0.695 | khớp  |        0.919 |         0.919 | khớp |
| MR     |        5 |         0.88  |         0.808 |          0.808 | khớp  |        0.955 |         0.955 | khớp |
| EC     |        4 |         0.864 |         0.779 |          0.779 | khớp  |        0.934 |         0.934 | khớp |
| PO     |        4 |         0.878 |         0.793 |          0.793 | khớp  |        0.939 |         0.939 | khớp |
| LP     |        3 |         0.799 |         0.734 |          0.734 | khớp  |        0.892 |         0.892 | khớp |
| EN     |        3 |         0.886 |         0.805 |          0.805 | khớp  |        0.925 |         0.925 | khớp |
| SE     |        3 |         0.863 |         0.808 |          0.808 | khớp  |        0.926 |         0.926 | khớp |
| FM     |        3 |         0.87  |         0.763 |          0.763 | khớp  |        0.906 |         0.906 | khớp |
| EF     |        5 |         0.591 |         0.549 |          0.494 | LỆCH  |        0.826 |         0.828 | LỆCH |

Riêng biến kết quả EF (bài báo: AVE 0.549, CR 0.826), thử bỏ từng câu:

| bo_cau     |   so_cau |   ave |    cr |
|:-----------|---------:|------:|------:|
| (không bỏ) |        5 | 0.494 | 0.828 |
| EF2        |        4 | 0.529 | 0.816 |
| EF4        |        4 | 0.473 | 0.779 |
| EF5        |        4 | 0.481 | 0.784 |
| EF1        |        4 | 0.458 | 0.769 |
| EF3        |        4 | 0.531 | 0.817 |

Không phương án nào cho ra đúng AVE 0.549, kể cả khi bỏ EF3 như tác giả nói.

## 4. Fornell–Larcker (Bảng 9)

Bản PDF in Bảng 9 theo từng đường chéo; ma trận đã được dựng lại trong data/published/bang9_fornell_larcker.csv.

| nhom   |   can_ave_bang9 |   can_ave_tu_bang8 |   tuong_quan_max | voi_nhom   |   khoang_cach | dat       |
|:-------|----------------:|-------------------:|-----------------:|:-----------|--------------:|:----------|
| CL     |           0.77  |              0.77  |            0.768 | CO         |         0.002 | đạt       |
| CN     |           0.857 |              0.857 |            0.814 | FD         |         0.043 | đạt       |
| CO     |           0.874 |              0.874 |            0.787 | MR         |         0.087 | đạt       |
| EC     |           0.883 |              0.883 |            0.871 | PO         |         0.012 | đạt       |
| EN     |           0.897 |              0.897 |            0.755 | FD         |         0.142 | đạt       |
| FD     |           0.876 |              0.876 |            0.819 | TC         |         0.057 | đạt       |
| FM     |           0.873 |              0.873 |            0.804 | SE         |         0.069 | đạt       |
| LP     |           0.857 |              0.857 |            0.782 | SE         |         0.075 | đạt       |
| PO     |           0.89  |              0.891 |            0.871 | EC         |         0.019 | đạt       |
| MR     |           0.899 |              0.899 |            0.845 | RM         |         0.054 | đạt       |
| RM     |           0.833 |              0.834 |            0.845 | MR         |        -0.012 | KHÔNG ĐẠT |
| SE     |           0.899 |              0.899 |            0.846 | EC         |         0.053 | đạt       |
| TC     |           0.839 |              0.84  |            0.819 | FD         |         0.02  | đạt       |

Tương quan giữa các nhóm: trung bình 0.712, lớn nhất 0.871; 1/78 cặp > 0.85 và 8/78 cặp > 0.80.
**Không đạt** ở: RM (tương quan với MR = 0.845 > √AVE = 0.833). Bài báo lại kết luận tất cả đều đạt.
Sát ngưỡng (chênh < 0.03): CL (+0.002), EC (+0.012), PO (+0.019), TC (+0.020).

Tương quan giữa biến tiềm ẩn đã cao như vậy thì HTMT (tính từ tương quan giữa các câu hỏi, không bị suy giảm) nhiều khả năng còn cao hơn, có thể vượt ngưỡng 0.85. Không tính được HTMT vì thiếu dữ liệu gốc.

## 5. Hệ số đường dẫn (Bảng 11)

Độ lệch chuẩn bootstrap suy ra = β / t.

| tu   | den   |   beta |      t | p      |   do_lech_chuan_suy_ra |
|:-----|:------|-------:|-------:|:-------|-----------------------:|
| CL   | EF    |  0.169 | 26.25  | <0.001 |                 0.0064 |
| CN   | EF    |  0.097 | 30.864 | <0.001 |                 0.0031 |
| CO   | EF    |  0.114 | 32.193 | <0.001 |                 0.0035 |
| EC   | EF    |  0.231 | 44.082 | <0.001 |                 0.0052 |
| EN   | EF    |  0.154 | 29.027 | <0.001 |                 0.0053 |
| EXT  | EF    |  0.673 | 10.495 | <0.001 |                 0.0641 |
| FD   | EF    |  0.197 | 35.234 | <0.001 |                 0.0056 |
| FM   | EF    |  0.152 | 36.113 | <0.001 |                 0.0042 |
| INT  | EF    |  0.2   |  3.121 | 0.002  |                 0.0641 |
| LP   | EF    |  0.152 | 33.357 | <0.001 |                 0.0046 |
| PO   | EF    |  0.236 | 42.177 | <0.001 |                 0.0056 |
| MR   | EF    |  0.213 | 36.28  | <0.001 |                 0.0059 |
| RM   | EF    |  0.186 | 40.916 | <0.001 |                 0.0045 |
| SE   | EF    |  0.18  | 40.554 | <0.001 |                 0.0044 |
| TC   | EF    |  0.143 | 43.683 | <0.001 |                 0.0033 |

13 nhóm bậc 1 có độ lệch chuẩn chỉ 0.0031–0.0064, nhỏ hơn khoảng 10–20 lần so với hai nhóm bậc 2 (≈ 0.064). Với mẫu 314 phiếu, đường dẫn trực tiếp thông thường hiếm khi có sai số nhỏ như vậy.

Thử giả thuyết 'β của nhóm bậc 1 = trọng số lên nhóm bậc 2 × β của nhóm bậc 2':

- Nội bộ: β_nhóm / 0.200 = CL 0.84, CO 0.57, CN 0.48, FD 0.98, TC 0.71, RM 0.93, MR 1.06
- Bên ngoài: β_nhóm / 0.673 = EC 0.34, PO 0.35, LP 0.23, EN 0.23, SE 0.27, FM 0.23

Bên nội bộ có tỷ lệ lớn nhất 1.06 (MR), vượt 1 nên không thể là loading; bên ngoài thì tỷ lệ chỉ 0.23–0.35, quá nhỏ cho một loading. Vậy giả thuyết đơn giản này không giải thích được. Bài báo không nói rõ 13 hệ số này được ước lượng thế nào, nên không kiểm chứng được.

## 6. Q² = 1 − SSE/SSO (Bảng 14)

|   dong |   sso |      sse |    q2 |   q2_tinh_lai |   so_cau_suy_ra | bien_suy_ra         | ket_qua   |
|-------:|------:|---------:|------:|--------------:|----------------:|:--------------------|:----------|
|      1 |  1256 |  792.239 | 0.369 |         0.369 |               4 | EF (4 câu, đã bỏ 1) | khớp      |
|      2 |  6280 | 2574.26  | 0.59  |         0.59  |              20 | Bên ngoài (20 câu)  | khớp      |
|      3 |  9734 | 4602.7   | 0.527 |         0.527 |              31 | Nội bộ (31 câu)     | khớp      |

SSO = số phiếu × số câu hỏi của biến, nên chia SSO cho 314 sẽ biết mỗi dòng là biến nào. Bảng 14 không ghi tên dòng rõ ràng; suy ra: 0.369 là EF (chỉ còn 4 câu, khớp việc bỏ EF3), 0.590 là rủi ro bên ngoài, 0.527 là rủi ro nội bộ. Vậy mục 5.3 nói đúng, còn phần Kết luận (nội bộ 0.590, bên ngoài 0.527) bị nhầm.

## 7. GoF = √(R² × AVE trung bình)

√(0.720 × 0.566) = 0.638 → khớp với 0.638 bài báo công bố.

Bài không nói 0.566 là trung bình AVE của những biến nào. Thử các cách lấy trung bình:

- 13 nhóm bậc 1: 0.750 → GoF = 0.735
- 13 nhóm bậc 1 + EF: 0.736 → GoF = 0.728
- INT + EXT: 0.604 → GoF = 0.659
- INT + EXT + EF: 0.586 → GoF = 0.649
- INT + EF: 0.559 → GoF = 0.635
- EXT + EF: 0.594 → GoF = 0.654

Không cách nào ra đúng 0.566. Nếu lấy trung bình 13 nhóm bậc 1 (cách thường dùng) thì GoF ≈ 0.735.

## 8. f² và R² khi bỏ từng biến

f² = (R²_có − R²_bỏ) / (1 − R²_có) ⇒ R²_bỏ = R²_có − f² × (1 − R²_có).

- Bỏ rủi ro nội bộ (f² = 0.042): R² còn 0.708
- Bỏ rủi ro bên ngoài (f² = 0.471): R² còn 0.588

Bỏ rủi ro bên ngoài mà R² vẫn còn 0.588 nghĩa là riêng rủi ro nội bộ đã giải thích được ~59%. Như vậy hai nhóm chồng lấn nhau rất nhiều, phù hợp với tương quan cao ở Bảng 9.
