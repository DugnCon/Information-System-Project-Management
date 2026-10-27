# Kiểm chứng phần cài đặt PLS-SEM

File này do `src/kiem_chung_plspm.py` sinh ra. Lược đồ trọng số đường dẫn, Mode A.

## 1. So với nghiệm giải tích (mô hình hai khối A → B, n = 500)

Nghiệm chính xác: trọng số mỗi khối là vectơ kỳ dị đầu tiên của X_A'X_B (tính bằng SVD).

|    |   dap_an_SVD |   tu_viet |   plspm |
|:---|-------------:|----------:|--------:|
| A0 |       0.6809 |    0.6809 |  0.68   |
| A1 |       0.8204 |    0.8204 |  0.8187 |
| A2 |       0.8938 |    0.8938 |  0.8946 |
| A3 |       0.9092 |    0.9092 |  0.9102 |
| B0 |       0.6758 |    0.6758 |  0.6869 |
| B1 |       0.8358 |    0.8358 |  0.8356 |
| B2 |       0.8943 |    0.8943 |  0.8902 |
| B3 |       0.9077 |    0.9077 |  0.9049 |

- Code tự viết lệch tối đa 2.6e-11 so với nghiệm chính xác.
- plspm 0.5.4 lệch tối đa 1.1e-02 so với nghiệm chính xác.

## 2. So với thư viện plspm trên dữ liệu mô phỏng 314 phiếu

### Mô hình bậc 1: 13 nhóm rủi ro → EF

- 13 hệ số đường dẫn: chênh lệch lớn nhất 0.010
- 55 loading: chênh lệch lớn nhất 0.024
- R²: chênh lệch lớn nhất 0.003

|              |   tu_viet |   plspm |
|:-------------|----------:|--------:|
| ('CL', 'EF') |     0.08  |   0.081 |
| ('CO', 'EF') |     0.099 |   0.1   |
| ('CN', 'EF') |     0.042 |   0.043 |
| ('FD', 'EF') |    -0.079 |  -0.077 |
| ('TC', 'EF') |     0.008 |   0.005 |
| ('RM', 'EF') |     0.004 |   0.001 |
| ('MR', 'EF') |     0.181 |   0.175 |
| ('EC', 'EF') |     0.042 |   0.04  |
| ('PO', 'EF') |     0.101 |   0.097 |
| ('LP', 'EF') |     0.066 |   0.072 |
| ('EN', 'EF') |     0.197 |   0.188 |
| ('SE', 'EF') |     0.17  |   0.18  |
| ('FM', 'EF') |     0.014 |   0.018 |

### Mô hình bậc 2 (lặp chỉ báo, như mục 3.3)

- 15 hệ số đường dẫn: chênh lệch lớn nhất 0.019
- 106 loading: chênh lệch lớn nhất 0.024
- R²: chênh lệch lớn nhất 0.003

|               |   tu_viet |   plspm |
|:--------------|----------:|--------:|
| ('INT', 'EF') |     0.302 |   0.298 |
| ('EXT', 'EF') |     0.492 |   0.494 |
| ('CL', 'INT') |     0.174 |   0.171 |
| ('CO', 'INT') |     0.131 |   0.149 |
| ('CN', 'INT') |     0.107 |   0.109 |
| ('FD', 'INT') |     0.203 |   0.193 |
| ('TC', 'INT') |     0.148 |   0.141 |
| ('RM', 'INT') |     0.181 |   0.172 |
| ('MR', 'INT') |     0.219 |   0.226 |
| ('EC', 'EXT') |     0.237 |   0.243 |
| ('PO', 'EXT') |     0.234 |   0.23  |
| ('LP', 'EXT') |     0.168 |   0.173 |
| ('EN', 'EXT') |     0.173 |   0.165 |
| ('SE', 'EXT') |     0.172 |   0.167 |
| ('FM', 'EXT') |     0.165 |   0.171 |

## Kết luận

Code tự viết trùng nghiệm giải tích tới 3e-11, nên phần cài đặt thuật toán là đúng. plspm 0.5.4 lệch khoảng 0,01–0,02 so với cả nghiệm giải tích lẫn code tự viết; độ lệch này nhỏ, không làm thay đổi kết luận (ví dụ ở mô hình bậc 2, cả hai đều cho hệ số bên ngoài ≈ 0,49 lớn hơn nội bộ ≈ 0,30).