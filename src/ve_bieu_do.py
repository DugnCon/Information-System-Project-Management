"""Biểu đồ từ số liệu đã công bố, dùng trong báo cáo.

  - bd_nguoi_tra_loi.png   : cơ cấu kinh nghiệm và độ tuổi người trả lời (mục 4.3 bài báo)
  - bd_fornell_larcker.png : ma trận Fornell–Larcker (Bảng 9), tô đỏ ô vi phạm
  - bd_thai_binh_2.png     : tổng mức đầu tư và tiến độ dự án Nhiệt điện Thái Bình 2

Chạy:  python src/ve_bieu_do.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "data" / "published"
FIG = ROOT / "results" / "figures"
N = 314


def ve_nguoi_tra_loi():
    """Số liệu mục 4.3.1–4.3.2 của bài báo. Bài không nêu nhóm kinh nghiệm còn lại (45 người)
    và không nêu tỷ lệ nhóm trên 50 tuổi, nên để là 'không nêu rõ'."""
    kinh_nghiem = pd.Series({"5–10 năm": 81, "10–20 năm": 102, "20–30 năm": 66, "> 30 năm": 20})
    kinh_nghiem["Không nêu rõ"] = N - kinh_nghiem.sum()
    tuoi = pd.Series({"< 30 tuổi": 12 / N, "30–40 tuổi": 0.41, "40–50 tuổi": 0.44})
    tuoi["Không nêu rõ"] = 1 - tuoi.sum()

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.3, 1]})
    mau = ["#4c78a8"] * 4 + ["#bbbbbb"]
    a1.bar(kinh_nghiem.index, kinh_nghiem.values, color=mau)
    for x, v in enumerate(kinh_nghiem.values):
        a1.text(x, v + 2, f"{v}\n({v / N:.1%})".replace(".", ","), ha="center", fontsize=8)
    a1.set_ylim(0, 125)
    a1.set_ylabel("Số người trả lời")
    a1.set_title("Số năm kinh nghiệm (n = 314)")
    a1.tick_params(axis="x", labelsize=8)

    a2.pie(tuoi.values, labels=[f"{k}\n{v:.1%}".replace(".", ",") for k, v in tuoi.items()], startangle=90, counterclock=False,
           colors=["#9ecae1", "#4c78a8", "#08519c", "#bbbbbb"], textprops={"fontsize": 8},
           wedgeprops={"width": 0.45, "edgecolor": "white"})
    a2.set_title("Độ tuổi")
    fig.suptitle("Đặc điểm người trả lời khảo sát (số liệu mục 4.3 của Kassem, 2022)", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "bd_nguoi_tra_loi.png", dpi=200)
    plt.close(fig)


def ve_fornell_larcker():
    fl = pd.read_csv(PUB / "bang9_fornell_larcker.csv", index_col=0)
    M = fl.values.copy()
    S = np.where(np.isnan(M), M.T, M)
    ten = list(fl.index)
    n = len(ten)
    can = np.diag(S)

    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    hien = np.where(np.tril(np.ones((n, n), bool)), M, np.nan)
    im = ax.imshow(np.ma.masked_invalid(hien), cmap="YlOrRd", vmin=0.5, vmax=0.95)
    for i in range(n):
        for j in range(i + 1):
            v = M[i, j]
            if i == j:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec="#1f4e78", lw=1.5))
                ax.text(j, i, f"{v:.3f}".lstrip("0"), ha="center", va="center", fontsize=7, weight="bold",
                        color="white")
            else:
                vi_pham = v > min(can[i], can[j])
                if vi_pham:
                    ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec="#1f4e78", lw=3))
                ax.text(j, i, (f"{v:.3f}" if vi_pham else f"{v:.2f}").lstrip("0"), ha="center", va="center",
                        fontsize=7, weight="bold" if vi_pham else "normal", color="white" if vi_pham else "black")
    ax.set_xticks(range(n), ten)
    ax.set_yticks(range(n), ten)
    fig.colorbar(im, ax=ax, fraction=0.04, label="Tương quan giữa các nhóm")
    ax.set_title("Ma trận Fornell–Larcker (Bảng 9 của bài báo, dựng lại)\n"
                 "đường chéo: √AVE; ô viền đậm: tương quan lớn hơn √AVE (vi phạm)", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIG / "bd_fornell_larcker.png", dpi=200)
    plt.close(fig)


def ve_thai_binh_2():
    """Số liệu: kết luận thanh tra (Báo Đấu thầu, 07/08/2020) và tin khánh thành (Bộ Công Thương, 2023).
    Mốc kết thúc kế hoạch chỉ là ước tính: khởi công 2011 + gói EPC 45 tháng."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.2), gridspec_kw={"width_ratios": [1, 1.7]})

    tmdt = pd.Series({"Phê duyệt\nban đầu (7/2010)": 31505.4, "Sau 2 lần\nđiều chỉnh (2016)": 41799.1})
    a1.bar(tmdt.index, tmdt.values, color=["#9ecae1", "#c00000"], width=0.55)
    for x, v in enumerate(tmdt.values):
        a1.text(x, v + 600, f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."), ha="center", fontsize=9)
    a1.annotate("+32,7%", xy=(0.72, 39000), xytext=(0.45, 44500), ha="center", fontsize=11, color="#c00000",
                weight="bold", arrowprops=dict(arrowstyle="->", color="#c00000"))
    a1.set_ylim(0, 50000)
    a1.set_ylabel("Tỷ đồng")
    a1.set_title("Tổng mức đầu tư")

    bat_dau, ket_thuc_kh, ket_thuc_tt = 2011.0, 2011.0 + 45 / 12, 2023 + 4 / 12
    a2.barh(1, ket_thuc_kh - bat_dau, left=bat_dau, height=0.4, color="#9ecae1", label="Kế hoạch (gói EPC 45 tháng)")
    a2.barh(0, ket_thuc_tt - bat_dau, left=bat_dau, height=0.4, color="#2e75b6", label="Thực tế")
    a2.axvline(2018 + 7 / 12, color="#555", ls=":", lw=1)
    a2.text(2018 + 7 / 12 - 0.15, 1.45, "8/2018: công trường\nhoạt động lại", fontsize=8, ha="right")
    a2.axvspan(2016, 2020, ymin=0.02, ymax=0.08, color="#f4a582", alpha=0.6)
    a2.text(2018, -0.5, "Lãi vay phát sinh 2016–2019: 81,867 triệu USD", fontsize=8, ha="center", color="#c00000")
    a2.text(ket_thuc_kh + 0.1, 1, f"≈ {ket_thuc_kh:.0f}", va="center", fontsize=9)
    a2.text(ket_thuc_tt + 0.1, 0, "4/2023\nkhánh thành", va="center", fontsize=8)
    a2.set_yticks([0, 1], ["Thực tế", "Kế hoạch"])
    a2.set_xlim(2010, 2025.5)
    a2.set_ylim(-0.75, 1.9)
    a2.set_title("Tiến độ (năm)")
    a2.legend(loc="upper left", fontsize=8)
    fig.suptitle("Dự án Nhiệt điện Thái Bình 2: vượt chi phí và trễ tiến độ", fontsize=11)
    fig.tight_layout()
    fig.savefig(FIG / "bd_thai_binh_2.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    FIG.mkdir(parents=True, exist_ok=True)
    ve_nguoi_tra_loi()
    ve_fornell_larcker()
    ve_thai_binh_2()
    print("Đã vẽ:", *sorted(p.name for p in FIG.glob("bd_*.png")))
