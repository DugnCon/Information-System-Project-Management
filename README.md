# Quản lý dự án HTTT – Báo cáo giữa kỳ

Đề tài: tìm hiểu và tái hiện bài báo

> Kassem, M.A. (2022). *Risk Management Assessment in Oil and Gas Construction Projects Using Structural Equation Modeling (PLS-SEM)*. Gases, 2(2), 33–60. https://doi.org/10.3390/gases2020003

Nội dung chính: quản lý rủi ro dự án, chỉ số RII, ma trận xác suất – tác động (PIM) và mô hình PLS-SEM.

## Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| `data/published/` | Số liệu gõ lại từ các bảng trong bài báo (CSV) |
| `data/simulated/` | Dữ liệu khảo sát mô phỏng 314 phiếu |
| `src/` | Code Python: kiểm tra số liệu, RII, PIM, PLS-SEM, vẽ sơ đồ, quản lý dự án |
| `results/` | Bảng và hình kết quả phân tích |
| `report/` | Báo cáo LaTeX theo mẫu KLTN (biên dịch bằng XeLaTeX) |
| `quan-ly-du-an/` | WBS, Gantt, sổ rủi ro (Excel) và kế hoạch MS Project |
| `slides/` | Slide thuyết trình |

## Chạy lại phân tích

```
pip install -r requirements.txt
python src/kiem_tra_so_lieu.py
python src/ve_so_do.py
python src/quan_ly_du_an.py
```

Hạn nộp: 04/11/2026.
