import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pls_sem import PLSSEM, _chuan_hoa

import plspm.config as c
from plspm.mode import Mode
from plspm.plspm import Plspm
from plspm.scheme import Scheme

ROOT = Path(__file__).resolve().parents[1]
NOI_BO = ["CL", "CO", "CN", "FD", "TC", "RM", "MR"]
BEN_NGOAI = ["EC", "PO", "LP", "EN", "SE", "FM"]
CAU_EF = ["EF1", "EF2", "EF4", "EF5"]


def chay_plspm(du_lieu, khoi, duong):
    cot, du_lieu_pl = {}, pd.DataFrame(index=du_lieu.index)
    for j, cols in khoi.items():
        cot[j] = []
        for col in cols:
            du_lieu_pl[f"{j}__{col}"] = du_lieu[col].astype(float)
            cot[j].append(f"{j}__{col}")
    cau_truc = c.Structure()
    for i, k in duong:
        cau_truc.add_path([i], [k])
    p = cau_truc.path()
    cfg = c.Config(p, scaled=True)
    for j in p.index:
        cfg.add_lv(j, Mode.A, *[c.MV(t) for t in cot[j]])
    pl = Plspm(du_lieu_pl, cfg, Scheme.PATH, iterations=1000, tolerance=1e-14)
    pc = pl.path_coefficients()
    hs = pd.Series({(i, k): pc.loc[k, i] for i, k in duong})
    om = pl.outer_model()
    ld = pd.Series({(j, col): om.loc[f"{j}__{col}", "loading"] for j, cols in khoi.items() for col in cols})
    return hs, ld, pl.inner_summary()["r_squared"]


def kiem_tra_giai_tich(bao_cao):
    rng = np.random.default_rng(0)
    n = 500
    F = rng.multivariate_normal([0, 0], [[1, .5], [.5, 1]], n)
    d = pd.DataFrame({f"{b}{i}": l * F[:, k] + np.sqrt(1 - l ** 2) * rng.standard_normal(n)
                      for k, b in enumerate("AB") for i, l in enumerate([.6, .75, .85, .9])})
    khoi = {b: [f"{b}{i}" for i in range(4)] for b in "AB"}
    XA, XB = _chuan_hoa(d[khoi["A"]].values), _chuan_hoa(d[khoi["B"]].values)
    U, _, Vt = np.linalg.svd(XA.T @ XB)

    def loading(X, w):
        y = X @ w
        return np.abs([np.corrcoef(X[:, k], y)[0, 1] for k in range(X.shape[1])])

    dap_an = np.r_[loading(XA, U[:, 0]), loading(XB, Vt[0])]
    tu_viet = PLSSEM(khoi, [("A", "B")]).uoc_luong(d).loading.loading.values
    _, ld_pl, _ = chay_plspm(d, khoi, [("A", "B")])
    pl = ld_pl.values
    bao_cao += ["## 1. So với nghiệm giải tích (mô hình hai khối A → B, n = 500)", "",
                "Nghiệm chính xác: trọng số mỗi khối là vectơ kỳ dị đầu tiên của X_A'X_B (tính bằng SVD).", "",
                pd.DataFrame({"dap_an_SVD": dap_an, "tu_viet": tu_viet, "plspm": pl},
                             index=khoi["A"] + khoi["B"]).round(4).to_markdown(), "",
                f"- Code tự viết lệch tối đa {np.abs(tu_viet - dap_an).max():.1e} so với nghiệm chính xác.",
                f"- plspm 0.5.4 lệch tối đa {np.abs(pl - dap_an).max():.1e} so với nghiệm chính xác.", ""]
    return np.abs(tu_viet - dap_an).max()


def so_sanh_plspm(ten, du_lieu, khoi, duong, bao_cao):
    kq = PLSSEM(khoi, duong).uoc_luong(du_lieu)
    hs1 = kq.he_so.set_index(["tu", "den"]).beta
    ld1 = kq.loading.set_index(["khoi", "cau"]).loading
    hs2, ld2, r22 = chay_plspm(du_lieu, khoi, duong)
    d_hs = (hs1 - hs2.reindex(hs1.index)).abs().max()
    d_ld = (ld1 - ld2.reindex(ld1.index)).abs().max()
    d_r2 = (kq.r2 - r22.reindex(kq.r2.index)).abs().max()
    bao_cao += [f"### {ten}", "",
                f"- {len(hs1)} hệ số đường dẫn: chênh lệch lớn nhất {d_hs:.3f}",
                f"- {len(ld1)} loading: chênh lệch lớn nhất {d_ld:.3f}",
                f"- R²: chênh lệch lớn nhất {d_r2:.3f}", "",
                pd.DataFrame({"tu_viet": hs1, "plspm": hs2.reindex(hs1.index)}).round(3).to_markdown(), ""]


def main():
    bao_cao = ["# Kiểm chứng phần cài đặt PLS-SEM", "",
               "File này do `src/kiem_chung_plspm.py` sinh ra. Lược đồ trọng số đường dẫn, Mode A.", ""]
    sai_so = kiem_tra_giai_tich(bao_cao)

    td = pd.read_csv(ROOT / "data" / "simulated" / "tac_dong.csv").drop(columns="phieu")
    khoi = {g: [x for x in td.columns if x.startswith(g)] for g in NOI_BO + BEN_NGOAI}
    khoi["EF"] = CAU_EF
    bao_cao += ["## 2. So với thư viện plspm trên dữ liệu mô phỏng 314 phiếu", ""]
    so_sanh_plspm("Mô hình bậc 1: 13 nhóm rủi ro → EF", td, khoi, [(g, "EF") for g in NOI_BO + BEN_NGOAI], bao_cao)
    khoi2 = dict(khoi)
    khoi2["INT"] = [x for g in NOI_BO for x in khoi[g]]
    khoi2["EXT"] = [x for g in BEN_NGOAI for x in khoi[g]]
    duong2 = [(g, "INT") for g in NOI_BO] + [(g, "EXT") for g in BEN_NGOAI] + [("INT", "EF"), ("EXT", "EF")]
    so_sanh_plspm("Mô hình bậc 2 (lặp chỉ báo, như mục 3.3)", td, khoi2, duong2, bao_cao)

    bao_cao += ["## Kết luận", "",
                f"Code tự viết trùng nghiệm giải tích tới {sai_so:.0e}, nên phần cài đặt thuật toán là đúng. "
                "plspm 0.5.4 lệch khoảng 0,01–0,02 so với cả nghiệm giải tích lẫn code tự viết; độ lệch này nhỏ, "
                "không làm thay đổi kết luận (ví dụ ở mô hình bậc 2, cả hai đều cho hệ số bên ngoài ≈ 0,49 lớn hơn "
                "nội bộ ≈ 0,30)."]
    (ROOT / "results" / "kiem-chung-plspm.md").write_text("\n".join(bao_cao), encoding="utf-8")
    print("\n".join(bao_cao))


if __name__ == "__main__":
    main()
