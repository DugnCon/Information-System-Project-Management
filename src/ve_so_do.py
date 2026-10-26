"""Vẽ sơ đồ tư duy chủ đề và sơ đồ mô hình nghiên cứu cho báo cáo.

Chạy:  python src/ve_so_do.py
Kết quả: report/hinh/so_do_tu_duy.png, report/hinh/mo_hinh_nghien_cuu.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "hinh"


def hop(ax, x, y, chu, mau, w=None, h=None, co=9, dam=False, chu_mau="black"):
    """Vẽ một hộp chữ bo góc, tâm tại (x, y)."""
    t = ax.text(x, y, chu, ha="center", va="center", fontsize=co, color=chu_mau,
                weight="bold" if dam else "normal", zorder=3, linespacing=1.3)
    if w is None:
        ax.figure.canvas.draw()
        bb = t.get_window_extent().transformed(ax.transData.inverted())
        w, h = bb.width + 0.25, bb.height + 0.2
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=mau, ec="#444", lw=0.8, zorder=2))
    return w, h


# ---------------------------------------------------------------- sơ đồ tư duy
NHANH = [
    ("Khái niệm nền tảng", "#cfe2f3", [
        "Dự án: tạm thời, duy nhất",
        "Rủi ro = xác suất × tác động",
        "Thành công: thời gian,\nchi phí, chất lượng"]),
    ("Khung quản lý rủi ro", "#d9ead3", [
        "PMBOK 6: 7 quy trình",
        "PMBOK 7: miền Uncertainty",
        "ISO 31000:2018"]),
    ("Phương pháp của bài báo", "#fff2cc", [
        "Khảo sát 314 phiếu, Likert 1–5",
        "Cronbach's α",
        "RII: xếp hạng rủi ro",
        "Ma trận xác suất – tác động",
        "PLS-SEM (SmartPLS 3)"]),
    ("Mô hình nghiên cứu", "#fce5cd", [
        "51 yếu tố → 13 nhóm",
        "Nội bộ (7) / Bên ngoài (6)",
        "5 hậu quả: trễ, vượt chi,\nchất lượng, mục tiêu, dừng"]),
    ("Kết quả chính", "#ead1dc", [
        "R² = 0.72, GoF = 0.638",
        "Bên ngoài β 0.673 > nội bộ 0.200",
        "Top: chính phủ bất ổn,\nước tính chi phí sai"]),
    ("Tái hiện & phản biện", "#f4cccc", [
        "Tính lại RII, AVE, CR, Q²: khớp",
        "Fornell–Larcker: RM không đạt",
        "AVE biến kết quả, GoF: lệch",
        "Dữ liệu mô phỏng + HTMT"]),
    ("Liên hệ thực tế", "#d0e0e3", [
        "Dự án dầu khí Việt Nam",
        "Dự án hệ thống thông tin",
        "Monte Carlo tiến độ"]),
]


# vị trí (x, y) của từng nhánh: 4 nhánh bên phải, 3 nhánh bên trái
VI_TRI = [(3.3, 4.7), (3.3, 1.75), (3.3, -1.5), (3.3, -4.75), (-4.3, -3.6), (-4.3, 0.0), (-4.3, 3.6)]


def ve_so_do_tu_duy():
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(-10.8, 10)
    ax.set_ylim(-6.3, 6.3)
    ax.axis("off")

    hop(ax, 0, 0, "QUẢN LÝ RỦI RO\nDỰ ÁN XÂY DỰNG DẦU KHÍ\nBẰNG PLS-SEM", "#3d5a80",
        co=12, dam=True, chu_mau="white")

    buoc = 0.6
    for (ten, mau, la), (cx, cy) in zip(NHANH, VI_TRI):
        huong = 1 if cx > 0 else -1
        ax.plot([0, cx], [0, cy], color="#888", lw=2, zorder=1)
        bw, _ = hop(ax, cx, cy, ten, mau, co=10.5, dam=True)

        lx = cx + huong * 4.1
        y0 = cy + buoc * (len(la) - 1) / 2
        for i, chu in enumerate(la):
            ly = y0 - i * buoc
            lw, _ = hop(ax, lx, ly, chu, "white", co=8.5)
            ax.plot([cx + huong * bw / 2, lx - huong * lw / 2], [cy, ly], color="#aaa", lw=0.8, zorder=1)

    fig.tight_layout()
    fig.savefig(OUT / "so_do_tu_duy.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- mô hình nghiên cứu
NOI_BO = [("CL", "Chủ đầu tư"), ("CO", "Nhà thầu"), ("CN", "Tư vấn"), ("FD", "Khả thi và thiết kế"),
          ("TC", "Đấu thầu và hợp đồng"), ("RM", "Nguồn lực và vật tư"), ("MR", "Quản lý dự án")]
BEN_NGOAI = [("EC", "Kinh tế quốc gia"), ("PO", "Chính trị"), ("LP", "Người dân địa phương"),
             ("EN", "Môi trường và an toàn"), ("SE", "An ninh"), ("FM", "Bất khả kháng")]


def ve_mo_hinh():
    beta = pd.read_csv(ROOT / "data" / "published" / "bang11_duong_dan.csv").set_index("tu").beta

    fig, ax = plt.subplots(figsize=(15, 9))
    ax.set_xlim(0, 15)
    ax.set_ylim(0.8, 9.6)
    ax.axis("off")

    x_nhom, w_nhom = 2.0, 3.7
    noi_bo = (7.2, 7.2)
    ben_ngoai = (7.2, 2.9)
    ket_qua = (11.0, 5.05)

    def cot_nhom(ds, y_tren, dich, mau):
        for k, (ma, ten) in enumerate(ds):
            y = y_tren - k * 0.6
            hop(ax, x_nhom, y, f"{ma} – {ten}   (β = {beta[ma]:.3f})", mau, w=w_nhom, h=0.46, co=9)
            ax.annotate("", xy=(dich[0] - 1.2, dich[1]), xytext=(x_nhom + w_nhom / 2, y),
                        arrowprops=dict(arrowstyle="-|>", color="#888", lw=0.7, shrinkA=0, shrinkB=2))

    cot_nhom(NOI_BO, 9.0, noi_bo, "#dbe9f6")
    cot_nhom(BEN_NGOAI, 4.4, ben_ngoai, "#fde9d9")
    ax.text(0.1, 9.45, "Rủi ro nội bộ – giả thuyết H1–H7", fontsize=9.5, weight="bold", color="#3d85c6")
    ax.text(0.1, 4.85, "Rủi ro bên ngoài – giả thuyết H8–H13", fontsize=9.5, weight="bold", color="#e69138")

    hop(ax, *noi_bo, "RỦI RO NỘI BỘ\n(khái niệm bậc 2)\nAVE 0.570 · CR 0.976", "#9fc5e8",
        w=2.4, h=1.2, co=9.5, dam=True)
    hop(ax, *ben_ngoai, "RỦI RO BÊN NGOÀI\n(khái niệm bậc 2)\nAVE 0.638 · CR 0.972", "#f9cb9c",
        w=2.4, h=1.2, co=9.5, dam=True)
    hop(ax, *ket_qua, "ẢNH HƯỞNG TỚI\nTHÀNH CÔNG DỰ ÁN\n\nR² = 0.720", "#b6d7a8",
        w=2.6, h=1.6, co=10, dam=True)

    for (x0, y0), nhan, lech in [(noi_bo, "β = 0.200   f² = 0.042", 0.45), (ben_ngoai, "β = 0.673   f² = 0.471", -0.45)]:
        dich = (ket_qua[0] - 1.3, ket_qua[1] + lech)
        ax.annotate("", xy=dich, xytext=(x0 + 1.2, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
        ax.text((x0 + 1.2 + dich[0]) / 2, (y0 + dich[1]) / 2 + 0.35, nhan, ha="center", va="center",
                fontsize=9.5, rotation=np.degrees(np.arctan2(dich[1] - y0, dich[0] - x0 - 1.2)) * 0.75,
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1))

    hau_qua = ["EF1 Trễ tiến độ", "EF2 Vượt chi phí", "EF3 Chất lượng kém (*)", "EF4 Không đạt mục tiêu",
               "EF5 Dự án bị dừng"]
    for k, hq in enumerate(hau_qua):
        y = 6.25 - k * 0.6
        hop(ax, 13.75, y, hq, "#f3f9ef", w=2.4, h=0.42, co=8.5)
        ax.annotate("", xy=(12.55, y), xytext=(ket_qua[0] + 1.3, ket_qua[1]),
                    arrowprops=dict(arrowstyle="-|>", color="#888", lw=0.7, shrinkA=0, shrinkB=0))
    ax.text(14.95, 3.2, "(*) tác giả nói đã loại khỏi mô hình", ha="right", fontsize=7.5, style="italic")
    ax.text(14.95, 1.0, "Hệ số β, AVE, CR, R², f² lấy từ Bảng 8, 11, 12, 13 của Kassem (2022)",
            ha="right", fontsize=7.5, color="#555")

    fig.tight_layout()
    fig.savefig(OUT / "mo_hinh_nghien_cuu.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ve_so_do_tu_duy()
    ve_mo_hinh()
    print("Đã vẽ:", *sorted(p.name for p in OUT.glob("*.png")))
