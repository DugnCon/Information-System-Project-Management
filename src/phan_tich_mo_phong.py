"""Chạy lại toàn bộ quy trình phân tích của bài báo trên dữ liệu mô phỏng.

Cronbach's α → RII → PIM → PLS-SEM (mô hình bậc 2, cách lặp chỉ báo) → bootstrapping → so sánh với bài báo.

Chạy:  python src/phan_tich_mo_phong.py [số lần bootstrap, mặc định 5000]
Kết quả: results/mo-phong.md, results/tables/mp_*.csv, results/figures/mp_*.png
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pls_sem import PLSSEM, gof, tom_tat_bootstrap  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "data" / "simulated"
PUB = ROOT / "data" / "published"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"

NOI_BO = ["CL", "CO", "CN", "FD", "TC", "RM", "MR"]
BEN_NGOAI = ["EC", "PO", "LP", "EN", "SE", "FM"]
NHOM = NOI_BO + BEN_NGOAI
CAU_EF = ["EF1", "EF2", "EF4", "EF5"]          # bỏ EF3 như tác giả
MUC = ["VL", "L", "M", "H", "VH"]

bao_cao = []


def ghi(s=""):
    bao_cao.append(s)


def bang(df, **kw):
    ghi(df.to_markdown(**kw))
    ghi()


def rii_sang_muc(x):
    return MUC[min(int(x / 0.2), 4)]


# ---------------------------------------------------------------- 1. Cronbach, RII, PIM
def phan_tich_mo_ta(td, xs):
    cau = {g: [c for c in td.columns if c.startswith(g)] for g in NHOM}
    cau["EF"] = [c for c in td.columns if c.startswith("EF")]

    def alpha(X):
        k = X.shape[1]
        return k / (k - 1) * (1 - X.var(ddof=1).sum() / X.sum(axis=1).var(ddof=1))

    b5 = pd.read_csv(PUB / "bang5_cronbach.csv").set_index("ma").cronbach_alpha
    cr = pd.DataFrame({"so_cau": {g: len(c) for g, c in cau.items()},
                       "alpha_mo_phong": {g: alpha(td[c]) for g, c in cau.items()},
                       "alpha_bai_bao": b5.reindex(list(cau)).to_dict()}).round(3)
    cr.to_csv(TABLES / "mp_cronbach.csv")
    ghi("## 1. Độ tin cậy Cronbach's α")
    ghi()
    bang(cr)
    ghi("Bài báo tính α trên dữ liệu khảo sát thử (pilot), còn ở đây tính trên toàn bộ 314 phiếu mô phỏng, "
        "nên chỉ so sánh được mức độ, không so được từng con số.")
    ghi()

    cau_rr = [c for g in NHOM for c in cau[g]]
    rii = pd.DataFrame({"rii_tac_dong": td[cau_rr].mean() / 5, "rii_xac_suat": xs[cau_rr].mean() / 5})
    rii["rii_tong"] = rii.rii_tac_dong * rii.rii_xac_suat
    rii["hang"] = rii.rii_tong.rank(ascending=False, method="min").astype(int)
    rii["muc_tac_dong"] = rii.rii_tac_dong.map(rii_sang_muc)
    rii["muc_xac_suat"] = rii.rii_xac_suat.map(rii_sang_muc)
    rii = rii.sort_values("hang").round(3)
    rii.to_csv(TABLES / "mp_rii.csv", index_label="cau")

    b7 = pd.read_csv(PUB / "bang7_rii_top10.csv").set_index("ma")
    so = b7[["rii_tong", "hang_tong"]].join(rii[["rii_tong", "hang"]], rsuffix="_mp")
    so.columns = ["rii_bai_bao", "hang_bai_bao", "rii_mo_phong", "hang_mo_phong"]
    ghi("## 2. RII")
    ghi()
    ghi("Top 10 của bài báo, so với RII tính trên dữ liệu mô phỏng:")
    ghi()
    bang(so.sort_values("hang_bai_bao"))
    trung = len(set(rii.index[:10]) & set(b7.index))
    ghi(f"{trung}/10 rủi ro của top 10 bài báo vẫn nằm trong top 10 mô phỏng. Sai lệch nhỏ đến từ việc làm tròn "
        "điểm sang thang 1–5 và từ nhiễu ngẫu nhiên khi sinh 314 phiếu.")
    ghi()
    ve_pim(rii)
    return rii


def ve_pim(rii):
    top = rii.head(10)
    diem = np.outer(np.arange(1, 6), np.arange(1, 6))
    vung = np.where(diem >= 15, 2, np.where(diem >= 8, 1, 0))
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(vung, cmap=matplotlib.colors.ListedColormap(["#9bd39b", "#f5d76e", "#ef8a7a"]), origin="lower")
    o = {}
    for ma, r in top.iterrows():
        o.setdefault((MUC.index(r.muc_xac_suat), MUC.index(r.muc_tac_dong)), []).append(ma)
    for (i, j), ds in o.items():
        ax.text(j, i, "\n".join(", ".join(ds[k:k + 3]) for k in range(0, len(ds), 3)),
                ha="center", va="center", fontsize=8, weight="bold")
    ten = ["Rất thấp", "Thấp", "Trung bình", "Cao", "Rất cao"]
    ax.set_xticks(range(5), ten)
    ax.set_yticks(range(5), ten)
    ax.set_xlabel("Mức tác động (quy đổi từ RII)")
    ax.set_ylabel("Mức xác suất (quy đổi từ RII)")
    ax.set_title("Top 10 rủi ro trên dữ liệu mô phỏng")
    fig.tight_layout()
    fig.savefig(FIGURES / "mp_ma_tran_pim.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- 2. PLS-SEM
def mo_hinh(td):
    khoi = {g: [c for c in td.columns if c.startswith(g)] for g in NHOM}
    khoi["INT"] = [c for g in NOI_BO for c in khoi[g]]          # lặp chỉ báo
    khoi["EXT"] = [c for g in BEN_NGOAI for c in khoi[g]]
    khoi["EF"] = CAU_EF
    duong = [(g, "INT") for g in NOI_BO] + [(g, "EXT") for g in BEN_NGOAI] + [("INT", "EF"), ("EXT", "EF")]
    return PLSSEM(khoi, duong), khoi


def phan_tich_pls(td, B):
    m, khoi = mo_hinh(td)
    kq = m.uoc_luong(td)
    ghi("## 3. PLS-SEM – mô hình đo lường")
    ghi()
    ghi(f"Mô hình bậc 2 theo cách lặp chỉ báo: khối INT gồm 31 câu, EXT gồm 20 câu, EF gồm 4 câu (đã bỏ EF3). "
        f"Thuật toán hội tụ sau {kq.so_vong_lap} vòng lặp.")
    ghi()

    tc = PLSSEM.do_tin_cay(kq, td, khoi).round(3)
    b8 = pd.read_csv(PUB / "bang8_chi_so_nhom.csv").set_index("nhom")
    b8 = b8.rename(index={"EF": "EF"})
    tc = tc.join(b8[["ave", "cr"]].rename(columns={"ave": "ave_bai_bao", "cr": "cr_bai_bao"}))
    tc.to_csv(TABLES / "mp_do_tin_cay.csv")
    bang(tc)
    ghi("CR của INT và EXT vượt 0.95, giống bài báo (0.976 và 0.972). Theo Hair và cộng sự (2019), CR > 0.95 là "
        "dấu hiệu các câu hỏi trùng lặp. Với cách lặp chỉ báo thì điều này gần như chắc chắn xảy ra, vì một khối gom tới 20–31 câu.")
    ghi()

    ave = tc.ave
    fl = PLSSEM.fornell_larcker(kq, NHOM + ["EF"], ave).round(3)
    fl.to_csv(TABLES / "mp_fornell_larcker.csv")
    vi_pham = []
    for i in fl.index:
        khac = fl.loc[i].drop(i)
        if khac.max() >= fl.loc[i, i]:
            vi_pham.append(f"{i} ({khac.idxmax()}: {khac.max():.3f} ≥ √AVE {fl.loc[i, i]:.3f})")
    ghi("### Fornell–Larcker")
    ghi()
    ghi("Vi phạm: " + (", ".join(vi_pham) if vi_pham else "không có") + ".")
    ghi()

    H = PLSSEM.htmt(td, khoi, NHOM + ["EF"]).round(3)
    H.to_csv(TABLES / "mp_htmt.csv")
    tri = H.stack()
    ghi("### HTMT")
    ghi()
    ghi(f"Trung bình {tri.mean():.3f}, lớn nhất {tri.max():.3f} ({tri.idxmax()[0]}–{tri.idxmax()[1]}). "
        f"{(tri > 0.85).sum()}/{len(tri)} cặp > 0.85, {(tri > 0.90).sum()}/{len(tri)} cặp > 0.90.")
    ghi()
    cap = tri[tri > 0.85].sort_values(ascending=False)
    if len(cap):
        ghi("Các cặp vượt ngưỡng 0.85: " + ", ".join(f"{a}–{b} {v:.3f}" for (a, b), v in cap.items()) + ".")
        ghi()
    ghi("HTMT được tính từ tương quan giữa các câu hỏi nên không bị \"pha loãng\" như tương quan giữa điểm biến tiềm ẩn. "
        "Vì dữ liệu mô phỏng giữ đúng tương quan của Bảng 9 trong bài báo, kết quả này cho thấy nếu tác giả tính HTMT "
        "thì nhiều khả năng sẽ có các cặp vượt ngưỡng.")
    ghi()
    ve_htmt(H)

    # ---- mô hình cấu trúc
    ghi("## 4. PLS-SEM – mô hình cấu trúc")
    ghi()
    print(f"Bootstrapping {B} lần...")
    hs_bs, th_bs = m.bootstrap(td, B=B, seed=7, hien=max(B // 5, 1))
    hs = tom_tat_bootstrap(kq.he_so.set_index(["tu", "den"]).beta, hs_bs).round(4)
    hs.to_csv(TABLES / "mp_he_so_duong_dan.csv")

    b11 = pd.read_csv(PUB / "bang11_duong_dan.csv")
    b11["se_bai_bao"] = (b11.beta / b11.t).round(4)
    b11 = b11.set_index("tu")
    chinh = hs.loc[[("INT", "EF"), ("EXT", "EF")]].reset_index()
    chinh["beta_bai_bao"] = [b11.at["INT", "beta"], b11.at["EXT", "beta"]]
    chinh["se_bai_bao"] = [b11.at["INT", "se_bai_bao"], b11.at["EXT", "se_bai_bao"]]
    ghi("### Đường dẫn bậc 2 → thành công dự án")
    ghi()
    bang(chinh.round(4), index=False)

    f2 = m.f2(kq).round(3)
    f2.to_csv(TABLES / "mp_f2.csv", index=False)
    f2_ef = f2[f2.den == "EF"].set_index("tu")
    r2 = kq.r2.round(3)
    ghi(f"R²(EF) = {r2['EF']:.3f} (bài báo 0.720); f²(INT) = {f2_ef.at['INT', 'f2']:.3f} (bài báo 0.042); "
        f"f²(EXT) = {f2_ef.at['EXT', 'f2']:.3f} (bài báo 0.471). R²(INT) = {r2['INT']:.3f}, R²(EXT) = {r2['EXT']:.3f} "
        "(gần 1 là đương nhiên với cách lặp chỉ báo).")
    ghi()
    ghi("Dữ liệu được sinh với quan hệ thật EF = 0.200·INT + 0.673·EXT (R² thật ≈ 0.72). PLS-SEM ước lượng trên điểm "
        "tổ hợp có lẫn sai số đo nên R² thu được thấp hơn và hai hệ số bị kéo lại gần nhau, đúng với hạn chế đã nêu ở "
        "mục 2.7 (Dijkstra và Henseler, 2015). Kết luận định tính vẫn giữ nguyên: rủi ro bên ngoài tác động mạnh hơn "
        "rủi ro nội bộ.")
    ghi()

    print("Blindfolding Q²...")
    q2 = m.q2(td, ["EF", "INT", "EXT"]).round(3)
    q2.to_csv(TABLES / "mp_q2.csv", index=False)
    q2["q2_bai_bao"] = [0.369, 0.527, 0.590]
    ghi("### Q² (blindfolding, D = 7)")
    ghi()
    bang(q2, index=False)

    ave_gof = ave[NHOM + ["EF"]]
    g = gof(ave_gof, kq.r2[["EF"]])
    ghi(f"GoF = √(AVE trung bình của 13 nhóm và EF × R² của EF) = √({ave_gof.mean():.3f} × {kq.r2['EF']:.3f}) = {g:.3f}. "
        "Bài báo: 0.638 với AVE trung bình 0.566.")
    ghi()

    # ---- 13 "giả thuyết": tổng hiệu ứng của nhóm bậc 1 lên EF
    th = tom_tat_bootstrap(kq.tong_hieu_ung.set_index(["tu", "den"]).tong, th_bs)
    th = th.xs("EF", level="den").loc[NHOM].round(4)
    th["beta_bai_bao"] = b11.loc[NHOM, "beta"]
    th["se_bai_bao"] = b11.loc[NHOM, "se_bai_bao"]
    th["t_bai_bao"] = b11.loc[NHOM, "t"]
    th.to_csv(TABLES / "mp_tong_hieu_ung.csv")
    ghi("### 13 giả thuyết H1–H13: tổng hiệu ứng của từng nhóm lên thành công dự án")
    ghi()
    ghi("Trong mô hình bậc 2, mỗi nhóm chỉ tác động lên EF gián tiếp qua INT hoặc EXT. "
        "Tổng hiệu ứng = (hệ số nhóm → khái niệm bậc 2) × (hệ số khái niệm bậc 2 → EF).")
    ghi()
    bang(th[["beta", "se", "t", "beta_bai_bao", "se_bai_bao", "t_bai_bao"]])
    ghi(f"Theo cách ước lượng chuẩn, tổng hiệu ứng của từng nhóm chỉ {th.beta.min():.3f}–{th.beta.max():.3f} với "
        f"t = {th.t.min():.1f}–{th.t.max():.1f}, sai số chuẩn {th.se.min():.3f}–{th.se.max():.3f}. Bài báo in hệ số "
        f"{th.beta_bai_bao.min():.3f}–{th.beta_bai_bao.max():.3f}, sai số chỉ {th.se_bai_bao.min():.3f}–"
        f"{th.se_bai_bao.max():.3f} và t = {th.t_bai_bao.min():.0f}–{th.t_bai_bao.max():.0f}. "
        "Như vậy 13 hệ số trong bài không phải tổng hiệu ứng theo cách lặp chỉ báo; bài báo cũng không cho biết chúng "
        "được tính bằng cách nào. Thứ tự tương đối thì giống nhau: các nhóm bên ngoài (EC, PO) và MR, FD có hệ số lớn nhất.")
    ghi()
    ve_so_sanh(th)
    return kq


def ve_htmt(H):
    M = H.values
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(np.ma.masked_invalid(M), cmap="RdYlGn_r", vmin=0.5, vmax=1.0)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if not np.isnan(M[i, j]):
                ax.text(j, i, f"{M[i, j]:.2f}".lstrip("0"), ha="center", va="center", fontsize=7,
                        weight="bold" if M[i, j] > 0.85 else "normal")
    ax.set_xticks(range(len(H)), H.columns)
    ax.set_yticks(range(len(H)), H.index)
    fig.colorbar(im, ax=ax, fraction=0.04, label="HTMT")
    ax.set_title("HTMT giữa các nhóm rủi ro (dữ liệu mô phỏng)\nin đậm: vượt ngưỡng 0,85")
    fig.tight_layout()
    fig.savefig(FIGURES / "mp_htmt.png", dpi=200)
    plt.close(fig)


def ve_so_sanh(th):
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(th))
    ax.bar(x - 0.2, th.beta_bai_bao, 0.4, label="Bài báo (Bảng 11)", color="#f58518")
    ax.bar(x + 0.2, th.beta, 0.4, yerr=1.96 * th.se, capsize=3, label="Mô phỏng (± 1,96 SE)", color="#4c78a8")
    ax.set_xticks(x, th.index)
    ax.set_ylabel("Hệ số tác động lên thành công dự án")
    ax.set_title("13 nhóm rủi ro: hệ số trong bài báo và tổng hiệu ứng trên dữ liệu mô phỏng")
    ax.axvline(6.5, color="#999", ls=":")
    ax.text(3, ax.get_ylim()[1] * 0.95, "Nội bộ", ha="center")
    ax.text(9.5, ax.get_ylim()[1] * 0.95, "Bên ngoài", ha="center")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "mp_so_sanh_he_so.png", dpi=200)
    plt.close(fig)


def main():
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    td = pd.read_csv(SIM / "tac_dong.csv").drop(columns="phieu")
    xs = pd.read_csv(SIM / "xac_suat.csv").drop(columns="phieu")

    ghi("# Kết quả phân tích trên dữ liệu mô phỏng")
    ghi()
    ghi(f"File này do `src/phan_tich_mo_phong.py` sinh ra. Dữ liệu: 314 phiếu mô phỏng (`data/simulated/`), "
        f"bootstrapping {B} lần.")
    ghi()
    phan_tich_mo_ta(td, xs)
    phan_tich_pls(td, B)
    (ROOT / "results" / "mo-phong.md").write_text("\n".join(bao_cao), encoding="utf-8")
    print("\n".join(bao_cao))


if __name__ == "__main__":
    main()
