"""Sinh bộ dữ liệu khảo sát mô phỏng 314 phiếu theo đúng cấu trúc bài báo công bố.

Không có dữ liệu gốc, nên dữ liệu được sinh sao cho khớp với các số liệu đã in:
  - tương quan giữa 13 nhóm rủi ro = ma trận Bảng 9 (đường chéo = 1);
  - loading của 51 câu hỏi và 5 câu hậu quả = Bảng 8;
  - biến kết quả EF = 0.200 * Nội bộ + 0.673 * Bên ngoài + nhiễu (Bảng 11);
  - điểm trung bình tác động / xác suất của top 10 rủi ro = RII Bảng 7 (RII = trung bình / 5);
  - điểm trung bình 5 câu hậu quả = mục 5.2 của bài báo.

Chạy:  python src/mo_phong.py
Kết quả: data/simulated/tac_dong.csv, xac_suat.csv, muc_tieu.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "data" / "published"
OUT = ROOT / "data" / "simulated"

N = 314
SEED = 2022
NOI_BO = ["CL", "CO", "CN", "FD", "TC", "RM", "MR"]
BEN_NGOAI = ["EC", "PO", "LP", "EN", "SE", "FM"]
BETA_NOI_BO, BETA_BEN_NGOAI = 0.200, 0.673
TB_HAU_QUA = {"EF1": 3.917, "EF2": 2.755, "EF3": 2.755, "EF4": 3.420, "EF5": 2.975}
DO_RONG = 0.95        # độ lệch chuẩn của điểm liên tục trước khi làm tròn sang thang 1–5
TQ_XS_TD = 0.5        # tương quan giữa điểm xác suất và điểm tác động của cùng một câu


def ma_tran_tuong_quan():
    fl = pd.read_csv(PUB / "bang9_fornell_larcker.csv", index_col=0)
    m = fl.values.copy()
    m = np.where(np.isnan(m), m.T, m)
    np.fill_diagonal(m, 1.0)
    return pd.DataFrame(m, index=fl.index, columns=fl.columns)


def sang_likert(z, tb):
    """Chuyển điểm chuẩn hoá z sang thang 1–5 có trung bình xấp xỉ tb."""
    return np.clip(np.rint(tb + DO_RONG * z), 1, 5).astype(int)


def muc_tieu_rii(rng, cau):
    """RII tác động và xác suất mục tiêu cho từng câu: top 10 lấy từ Bảng 7, còn lại rút ngẫu nhiên
    sao cho RII tổng < 0.50 (thấp hơn top 10)."""
    b7 = pd.read_csv(PUB / "bang7_rii_top10.csv").set_index("ma")
    dong = []
    for c in cau:
        if c in b7.index:
            td, xs = b7.at[c, "rii_tac_dong"], b7.at[c, "rii_xac_suat"]
        else:
            while True:
                td, xs = rng.uniform(0.55, 0.72), rng.uniform(0.58, 0.80)
                if td * xs < 0.50:
                    break
        dong.append({"cau": c, "rii_tac_dong_muc_tieu": round(td, 3), "rii_xac_suat_muc_tieu": round(xs, 3),
                     "trong_top10_bai_bao": c in b7.index})
    return pd.DataFrame(dong)


def sinh_du_lieu():
    rng = np.random.default_rng(SEED)
    phi = ma_tran_tuong_quan()
    nhom = list(phi.index)
    ld = pd.read_csv(PUB / "bang8_loading.csv")

    # 1. điểm 13 nhóm rủi ro bậc 1, tương quan theo Bảng 9
    F = pd.DataFrame(rng.multivariate_normal(np.zeros(len(nhom)), phi.values, size=N), columns=nhom)

    # 2. hai khái niệm bậc 2 = trung bình chuẩn hoá các nhóm con; EF theo hệ số đường dẫn của bài báo
    chuan = lambda s: (s - s.mean()) / s.std(ddof=0)
    INT, EXT = chuan(F[NOI_BO].mean(axis=1)), chuan(F[BEN_NGOAI].mean(axis=1))
    r = np.corrcoef(INT, EXT)[0, 1]
    r2_ly_thuyet = BETA_NOI_BO ** 2 + BETA_BEN_NGOAI ** 2 + 2 * BETA_NOI_BO * BETA_BEN_NGOAI * r
    nhieu = np.sqrt(max(1 - r2_ly_thuyet, 0.05))
    EF = BETA_NOI_BO * INT + BETA_BEN_NGOAI * EXT + nhieu * rng.standard_normal(N)
    EF = chuan(EF)

    # 3. câu hỏi: x* = λ·F + sqrt(1-λ²)·e, rồi làm tròn sang Likert
    cau_rui_ro = ld[ld.nhom != "EF"]
    mt = muc_tieu_rii(rng, list(cau_rui_ro.cau))
    tac_dong, xac_suat = {}, {}
    for (_, row), (_, m) in zip(cau_rui_ro.iterrows(), mt.iterrows()):
        lam = row.loading
        z = lam * F[row.nhom] + np.sqrt(1 - lam ** 2) * rng.standard_normal(N)
        tac_dong[row.cau] = sang_likert(z, 5 * m.rii_tac_dong_muc_tieu)
        zp = TQ_XS_TD * z + np.sqrt(1 - TQ_XS_TD ** 2) * rng.standard_normal(N)
        xac_suat[row.cau] = sang_likert(zp, 5 * m.rii_xac_suat_muc_tieu)
    for _, row in ld[ld.nhom == "EF"].sort_values("cau").iterrows():
        z = row.loading * EF + np.sqrt(1 - row.loading ** 2) * rng.standard_normal(N)
        tac_dong[row.cau] = sang_likert(z, TB_HAU_QUA[row.cau])

    td = pd.DataFrame(tac_dong)
    xs = pd.DataFrame(xac_suat)
    td.insert(0, "phieu", np.arange(1, N + 1))
    xs.insert(0, "phieu", np.arange(1, N + 1))
    return td, xs, mt, r, r2_ly_thuyet


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    td, xs, mt, r, r2 = sinh_du_lieu()
    td.to_csv(OUT / "tac_dong.csv", index=False)
    xs.to_csv(OUT / "xac_suat.csv", index=False)
    mt.to_csv(OUT / "muc_tieu.csv", index=False)
    print(f"Đã sinh {len(td)} phiếu, {td.shape[1] - 1} câu tác động/hậu quả, {xs.shape[1] - 1} câu xác suất.")
    print(f"Tương quan Nội bộ – Bên ngoài suy ra từ Bảng 9: r = {r:.3f}")
    print(f"R² suy ra từ β của bài báo: 0.200² + 0.673² + 2·0.200·0.673·r = {r2:.3f} (bài báo: 0.720)")


if __name__ == "__main__":
    main()
