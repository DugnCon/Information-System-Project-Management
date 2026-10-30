"""Áp dụng quy trình phân tích của Kassem (2022) lên một bộ dữ liệu THẬT, công khai.

Dữ liệu: Rauzana, A. (2021). Dataset of Causes of delays in construction projects. Mendeley Data, V1,
doi:10.17632/2wckhrzz5j.1 (CC BY 4.0). Bài báo gốc: Rauzana & Dharma (2022), PLoS ONE 17(1): e0263337.
68 nhà thầu ở Aceh (Indonesia) chấm mức ảnh hưởng (1–5) của 60 nguyên nhân chậm trễ thuộc 10 nhóm (X1–X10)
và 4 câu Y1–Y4 (bài gốc không định nghĩa Y; α = 0,946 nên dùng làm biến kết quả "mức độ chậm trễ").

Quy trình: kiểm tra đọc dữ liệu so với bài gốc → Cronbach's α → RII → PLS-SEM (bậc 1 và bậc 2) → so với Kassem.
Không dựng được ma trận PIM vì mỗi yếu tố chỉ được chấm một lần (không tách xác suất và tác động).

Chạy:  python src/du_lieu_that_aceh.py [số lần bootstrap, mặc định 2000]
Kết quả: results/aceh.md, results/tables/aceh_*.csv, results/figures/aceh_*.png
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
FILE = ROOT / "data" / "external" / "aceh" / "Dataset_1.xlsx"
TAB = ROOT / "results" / "tables"
FIG = ROOT / "results" / "figures"

NHOM = {"X1": "Vật tư", "X2": "Thiết bị", "X3": "Tài chính", "X4": "Môi trường", "X5": "Lao động",
        "X6": "Thực hiện", "X7": "Quản lý", "X8": "Chính trị", "X9": "Tội phạm", "X10": "Giám đốc dự án"}
NOI_BO = ["X1", "X2", "X3", "X5", "X6", "X7", "X10"]       # do các bên trong dự án gây ra
BEN_NGOAI = ["X4", "X8", "X9"]                              # môi trường, chính trị, tội phạm

TEN = {  # dịch từ bảng yếu tố của Rauzana & Dharma (2022)
    "X1.1": "Thiếu vật tư xây dựng", "X1.2": "Thay đổi hình dạng, chức năng, quy cách vật tư",
    "X1.3": "Giao vật tư chậm", "X1.4": "Vật tư hư hỏng khi lưu kho", "X1.5": "Khan hiếm vật tư",
    "X1.6": "Đặt hàng vật tư không chính xác", "X1.7": "Sử dụng vật tư lãng phí", "X1.8": "Vật tư về muộn",
    "X1.9": "Tính sai nhu cầu vật tư",
    "X2.1": "Thiết bị hỏng", "X2.2": "Thiếu thiết bị", "X2.3": "Năng suất thiết bị thấp",
    "X3.1": "Tình hình tài chính kém khi thi công", "X3.2": "Chủ đầu tư chậm thanh toán",
    "X3.3": "Không được ngân hàng cấp vốn lưu động bổ sung", "X3.4": "Chi phí vận hành, quản lý của nhà thầu cao",
    "X4.1": "Ảnh hưởng của thời tiết", "X4.2": "An toàn môi trường kém", "X4.3": "Vấn đề địa chất tại công trường",
    "X4.4": "Nhà thầu thiếu trao đổi với cộng đồng", "X4.5": "Thiết bị nặng khó vào công trường",
    "X5.1": "Thiếu lao động", "X5.2": "Lao động thiếu năng lực", "X5.3": "Chủ đầu tư can thiệp",
    "X5.4": "Lao động mệt mỏi do tăng ca", "X5.5": "Công nhân thiếu ý thức an toàn lao động",
    "X5.6": "Thay công nhân mới", "X5.7": "Công nhân nghỉ việc nhiều", "X5.8": "Lực lượng lao động thiếu động lực",
    "X6.1": "Chậm cấp phép", "X6.2": "Thay đổi thiết kế", "X6.3": "Lỗi thiết kế của đơn vị lập kế hoạch",
    "X6.4": "Phát sinh khối lượng",
    "X7.1": "Kiểm soát thời gian yếu", "X7.2": "Sắp xếp trình tự công việc chưa tốt",
    "X7.3": "Không rà soát quy cách trước khi thi công", "X7.4": "Không có quy trình cho từng công việc",
    "X7.5": "Hiểu sai hồ sơ hợp đồng", "X7.6": "Quản lý an toàn, sức khỏe nghề nghiệp kém",
    "X7.7": "Quy trình quản lý chất lượng không phù hợp", "X7.8": "Chọn sai biện pháp thi công",
    "X8.1": "Tin tức bất lợi trên báo chí", "X8.2": "Thiếu phối hợp giữa các cơ quan khi ra quyết định",
    "X8.3": "Ý kiến cơ quan khác làm thay đổi thiết kế", "X8.4": "Thủ tục cấp phép phức tạp",
    "X8.5": "Chậm phê duyệt ngân sách", "X8.6": "Tổ chức quần chúng phản đối vì lợi ích nhóm",
    "X9.1": "Mất vật tư, thiết bị", "X9.2": "Phá hoại dụng cụ, vật tư, công trình", "X9.3": "Tham nhũng vặt",
    "X9.4": "Công nhân dùng chất cấm", "X9.5": "Bị tống tiền từ bên ngoài", "X9.6": "Công nhân đánh nhau",
    "X10.1": "Giám đốc dự án chọn nhân sự kém", "X10.2": "Giám đốc dự án thiếu kinh nghiệm phân công",
    "X10.3": "Giám đốc dự án thiếu kinh nghiệm lập tiến độ", "X10.4": "Giám đốc dự án kém giao tiếp với chủ đầu tư",
    "X10.5": "Giao tiếp kém với đội ngũ và nhà thầu phụ", "X10.6": "Không thúc đẩy cả đội làm việc hết mình",
    "X10.7": "Thiếu giám sát, kiểm soát khi thi công",
}

bao_cao = []


def ghi(*dong):
    bao_cao.extend(dong if dong else [""])


def doc_du_lieu():
    raw = pd.read_excel(FILE, header=None)
    hdr = raw.iloc[9]
    df = raw.iloc[10:78].copy()
    df.columns = hdr
    cot = [c for c in hdr if isinstance(c, str) and c[0] in "XY"]
    return df[cot].apply(pd.to_numeric).reset_index(drop=True)


def alpha(X):
    k = X.shape[1]
    return k / (k - 1) * (1 - X.var(ddof=1).sum() / X.sum(axis=1).var(ddof=1))


def main():
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    df = doc_du_lieu()
    n = len(df)
    khoi = {g: [c for c in df.columns if c.split(".")[0] == g] for g in NHOM}
    khoi["Y"] = ["Y1", "Y2", "Y3", "Y4"]

    ghi("# Áp dụng quy trình của Kassem (2022) trên dữ liệu thật: chậm trễ dự án xây dựng ở Aceh", "",
        f"File này do `src/du_lieu_that_aceh.py` sinh ra. Dữ liệu: Rauzana (2021), Mendeley Data, "
        f"doi:10.17632/2wckhrzz5j.1, CC BY 4.0. n = {n} nhà thầu, 60 yếu tố, 10 nhóm, biến kết quả Y (4 câu).", "")

    # ---- 1. kiểm tra đọc dữ liệu so với bài gốc
    a = pd.Series({g: alpha(df[c]) for g, c in khoi.items()})
    tong = df[[c for g in NHOM for c in khoi[g]]].sum()
    ghi("## 1. Kiểm tra đọc dữ liệu so với bài gốc (Rauzana & Dharma, 2022)", "",
        f"- Cronbach's α thấp nhất: {NHOM[a.drop('Y').idxmin()]} {a.drop('Y').min():.3f} (bài gốc: Chính trị 0,638)",
        f"- Cronbach's α cao nhất: {NHOM[a.drop('Y').idxmax()]} {a.drop('Y').max():.3f} (bài gốc: Lao động 0,944)",
        f"- Tổng điểm cao nhất: {tong.idxmax()} = {tong.max()} (bài gốc: X8.5 = 327); thấp nhất: "
        f"{tong.idxmin()} = {tong.min()} (bài gốc: X8.1 = 234)",
        f"- Cronbach's α của Y1–Y4: {a['Y']:.3f} → bốn câu đo cùng một khái niệm, dùng làm biến kết quả.", "")
    pd.DataFrame({"nhom": [NHOM.get(g, "Y") for g in a.index], "so_cau": [len(khoi[g]) for g in a.index],
                  "alpha": a.round(3)}).to_csv(TAB / "aceh_cronbach.csv", index_label="ma")

    # ---- 2. RII (chỉ theo mức ảnh hưởng)
    rii = (df[[c for g in NHOM for c in khoi[g]]].mean() / 5).rename("rii").to_frame()
    rii["nhom"] = [NHOM[c.split(".")[0]] for c in rii.index]
    rii["yeu_to"] = [TEN[c] for c in rii.index]
    rii["hang"] = rii.rii.rank(ascending=False, method="min").astype(int)
    rii = rii.sort_values("hang")
    rii.to_csv(TAB / "aceh_rii.csv", index_label="ma")
    rii_nhom = rii.groupby("nhom").rii.mean().sort_values(ascending=False)
    ghi("## 2. RII theo mức ảnh hưởng (RII = tổng điểm / (5 × n))", "",
        rii.head(10)[["yeu_to", "nhom", "rii", "hang"]].round(3).to_markdown(), "",
        "RII trung bình theo nhóm: " + ", ".join(f"{k} {v:.3f}" for k, v in rii_nhom.items()) + ".", "")
    ve_rii(rii)

    # ---- 3. PLS-SEM
    ghi("## 3. PLS-SEM", "")
    # mô hình 1: 10 nhóm → Y
    m1 = PLSSEM(khoi, [(g, "Y") for g in NHOM])
    k1 = m1.uoc_luong(df)
    tc = PLSSEM.do_tin_cay(k1, df, khoi)
    tc["nhom"] = [NHOM.get(g, "Y (chậm trễ)") for g in tc.index]
    tc.round(3).to_csv(TAB / "aceh_do_tin_cay.csv")
    yeu = k1.loading[k1.loading.loading < 0.708]
    ghi("### Mô hình đo lường (mô hình bậc 1: 10 nhóm → Y)", "",
        tc[["nhom", "so_cau", "loading_min", "alpha", "cr", "ave"]].round(3).to_markdown(), "",
        f"- {len(yeu)}/{len(k1.loading)} câu có loading < 0,708. AVE < 0,5 ở: "
        + (", ".join(tc[tc.ave < 0.5].nhom) or "không nhóm nào") + ".")
    H = PLSSEM.htmt(df, khoi, list(NHOM) + ["Y"])
    tri = H.stack()
    vuot = tri[tri > 0.85].sort_values(ascending=False)
    ghi(f"- HTMT: lớn nhất {tri.max():.3f}; {len(vuot)}/{len(tri)} cặp > 0,85"
        + (" (" + ", ".join(f"{NHOM.get(a_, a_)}–{NHOM.get(b_, b_)} {v:.2f}" for (a_, b_), v in vuot.head(6).items()) + ")"
           if len(vuot) else "") + ".", "")
    H.round(3).to_csv(TAB / "aceh_htmt.csv")

    print(f"Bootstrapping {B} lần (mô hình 1)...")
    hs_bs, _ = m1.bootstrap(df, B=B, seed=11)
    hs1 = tom_tat_bootstrap(k1.he_so.set_index(["tu", "den"]).beta, hs_bs).reset_index()
    hs1["nhom"] = hs1.tu.map(NHOM)
    hs1 = hs1.sort_values("beta", ascending=False)
    hs1.round(4).to_csv(TAB / "aceh_he_so_bac1.csv", index=False)
    q2 = m1.q2(df, ["Y"]).q2.iloc[0]
    co_y_nghia = hs1[hs1.p < 0.05]
    ghi("### Mô hình cấu trúc bậc 1 (10 nhóm → Y)", "",
        hs1[["nhom", "beta", "se", "t", "p"]].round(3).to_markdown(index=False), "",
        f"- R²(Y) = {k1.r2['Y']:.3f}; Q²(Y) = {q2:.3f}; GoF = {gof(tc.ave, k1.r2):.3f}",
        f"- Số nhóm có ý nghĩa (p < 0,05): {len(co_y_nghia)}/10"
        + (" (" + ", ".join(co_y_nghia.nhom) + ")" if len(co_y_nghia) else "") + ".", "")

    # mô hình 2: bậc 2 như Kassem
    khoi2 = dict(khoi)
    khoi2["INT"] = [c for g in NOI_BO for c in khoi[g]]
    khoi2["EXT"] = [c for g in BEN_NGOAI for c in khoi[g]]
    duong2 = [(g, "INT") for g in NOI_BO] + [(g, "EXT") for g in BEN_NGOAI] + [("INT", "Y"), ("EXT", "Y")]
    m2 = PLSSEM(khoi2, duong2)
    k2 = m2.uoc_luong(df)
    print(f"Bootstrapping {B} lần (mô hình 2)...")
    hs_bs2, _ = m2.bootstrap(df, B=B, seed=12)
    hs2 = tom_tat_bootstrap(k2.he_so.set_index(["tu", "den"]).beta, hs_bs2).loc[[("INT", "Y"), ("EXT", "Y")]]
    f2 = m2.f2(k2).set_index(["tu", "den"]).f2
    ghi("### Mô hình bậc 2 như Kassem (nội bộ / bên ngoài → Y)", "",
        "Nội bộ: " + ", ".join(NHOM[g] for g in NOI_BO) + ". Bên ngoài: " + ", ".join(NHOM[g] for g in BEN_NGOAI) + ".", "",
        hs2.round(4).to_markdown(), "",
        f"- R²(Y) = {k2.r2['Y']:.3f}; f² nội bộ = {f2[('INT', 'Y')]:.3f}; f² bên ngoài = {f2[('EXT', 'Y')]:.3f}", "")
    hs2.round(4).to_csv(TAB / "aceh_he_so_bac2.csv")
    ve_he_so(hs1)

    # ---- 4. so sánh với Kassem
    ghi("## 4. So sánh với Kassem (2022)", "",
        "| Chỉ số | Kassem – Yemen (công bố) | Aceh – dữ liệu thật (tính lại) |",
        "|---|---|---|",
        f"| Cỡ mẫu | 314 | {n} |",
        f"| R² của biến kết quả | 0,720 | {k2.r2['Y']:.3f} |",
        f"| β nội bộ / bên ngoài | 0,200 / 0,673 | {hs2.beta.iloc[0]:.3f} / {hs2.beta.iloc[1]:.3f} |",
        f"| t nội bộ / bên ngoài | 3,1 / 10,5 | {hs2.t.iloc[0]:.1f} / {hs2.t.iloc[1]:.1f} |",
        f"| Số nhóm bậc 1 có ý nghĩa | 13/13 (t = 26–44) | {len(co_y_nghia)}/10 (mô hình bậc 1) |", "")
    (ROOT / "results" / "aceh.md").write_text("\n".join(bao_cao), encoding="utf-8")
    print("\n".join(bao_cao))


def ve_rii(rii):
    top = rii.head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 5))
    mau = {"Chính trị": "#e6550d", "Môi trường": "#fd8d3c", "Tội phạm": "#fdae6b"}
    ax.barh([f"{m} – {t}" for m, t in zip(top.index, top.yeu_to)], top.rii,
            color=[mau.get(g, "#4c78a8") for g in top.nhom])
    for y, v in enumerate(top.rii):
        ax.text(v + 0.003, y, f"{v:.3f}".replace(".", ","), va="center", fontsize=8)
    ax.set_xlim(0.8, 1.0)
    ax.set_xlabel("RII (mức ảnh hưởng)")
    ax.set_title("Top 10 nguyên nhân chậm trễ ở Aceh theo RII\n(cam: nhóm bên ngoài; xanh: nhóm nội bộ)")
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "aceh_rii_top10.png", dpi=200)
    plt.close(fig)


def ve_he_so(hs1):
    d = hs1.sort_values("beta")
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(d))
    mau = ["#c00000" if p < 0.05 else "#9ecae1" for p in d.p]
    ax.barh(y, d.beta, color=mau)
    ax.errorbar(d.beta, y, xerr=[d.beta - d["ci_2.5%"], d["ci_97.5%"] - d.beta], fmt="none", ecolor="#333", capsize=3)
    ax.axvline(0, color="#555", lw=0.8)
    ax.set_yticks(y, d.nhom)
    ax.set_xlabel("Hệ số đường dẫn β (khoảng tin cậy bootstrap 95%)")
    ax.set_title("Ảnh hưởng của 10 nhóm nguyên nhân lên mức độ chậm trễ (Aceh)\nđỏ: có ý nghĩa p < 0,05")
    fig.tight_layout()
    fig.savefig(FIG / "aceh_he_so.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
