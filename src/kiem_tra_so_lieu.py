"""Kiểm tra lại các số liệu đã công bố trong bài báo Kassem (2022).

Đọc các bảng đã gõ lại trong data/published, tính lại những gì tính lại được
(RII, PIM, AVE, CR, Fornell-Larcker, Q2, GoF, f2) và so với số trong bài.

Chạy:  python src/kiem_tra_so_lieu.py
Kết quả: results/tables/*.csv, results/figures/*.png, results/kiem-tra-so-lieu.md
"""
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "published"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
N = 314          # số phiếu hợp lệ
TOL = 0.0015     # sai số làm tròn chấp nhận được (số in 3 chữ số thập phân)

MUC = ["VL", "L", "M", "H", "VH"]
MUC_SO = {m: i + 1 for i, m in enumerate(MUC)}

bao_cao = []     # các dòng markdown cho file tổng hợp


def ghi(dong=""):
    bao_cao.append(dong)


def khop(a, b, tol=TOL):
    return "khớp" if abs(a - b) <= tol else "LỆCH"


def rii_sang_muc(rii):
    """Quy đổi RII sang 5 mức theo thang chia đều hay dùng:
    0-0.2 VL, 0.2-0.4 L, 0.4-0.6 M, 0.6-0.8 H, 0.8-1 VH."""
    return MUC[min(int(rii / 0.2), 4)]


# ---------------------------------------------------------------- RII
def kiem_tra_rii():
    df = pd.read_csv(DATA / "bang7_rii_top10.csv")
    df["rii_tong_tinh_lai"] = (df.rii_tac_dong * df.rii_xac_suat).round(4)
    df["chenh_lech"] = (df.rii_tong_tinh_lai - df.rii_tong).round(4)
    df["ket_qua"] = [khop(a, b) for a, b in zip(df.rii_tong_tinh_lai, df.rii_tong)]
    df["hang_tinh_lai"] = df.rii_tong_tinh_lai.rank(ascending=False, method="min").astype(int)
    df.to_csv(TABLES / "rii_tinh_lai.csv", index=False)

    ghi("## 1. RII tổng = RII tác động × RII xác suất (Bảng 7)")
    ghi()
    ghi(df[["ma", "rii_tac_dong", "rii_xac_suat", "rii_tong", "rii_tong_tinh_lai",
            "ket_qua", "hang_tong", "hang_tinh_lai"]].to_markdown(index=False))
    ghi()
    so_khop = (df.ket_qua == "khớp").sum()
    ghi(f"{so_khop}/{len(df)} dòng khớp trong sai số làm tròn. "
        f"Thứ hạng tính lại {'giống' if (df.hang_tong == df.hang_tinh_lai).all() else 'KHÁC'} thứ hạng trong bài.")
    ghi()
    return df


# ---------------------------------------------------------------- PIM
def kiem_tra_pim(rii):
    pim = pd.read_csv(DATA / "bang6_pim_top10.csv")
    pim["diem_pim"] = pim.tac_dong.map(MUC_SO) * pim.xac_suat.map(MUC_SO)

    # so mức trong Bảng 6 với mức suy ra từ RII ở Bảng 7 (cho các rủi ro có mã)
    gop = pim.merge(rii[["ma", "rii_tac_dong", "rii_xac_suat", "hang_tong"]], on="ma", how="left")
    gop["tac_dong_tu_rii"] = gop.rii_tac_dong.map(lambda x: rii_sang_muc(x) if pd.notna(x) else "")
    gop["xac_suat_tu_rii"] = gop.rii_xac_suat.map(lambda x: rii_sang_muc(x) if pd.notna(x) else "")
    co_ma = gop[gop.ma.notna()].copy()
    co_ma["nhat_quan"] = np.where(
        (co_ma.tac_dong == co_ma.tac_dong_tu_rii) & (co_ma.xac_suat == co_ma.xac_suat_tu_rii),
        "có", "KHÔNG")
    gop.to_csv(TABLES / "pim_so_voi_rii.csv", index=False)

    ghi("## 2. Ma trận PIM (Bảng 6) so với RII (Bảng 7)")
    ghi()
    ghi("Quy đổi RII sang mức theo thang chia đều 0.2 (giả định của mình, bài báo không nói cách quy đổi).")
    ghi()
    ghi(co_ma[["hang", "ma", "tac_dong", "xac_suat", "rii_tac_dong", "rii_xac_suat",
               "tac_dong_tu_rii", "xac_suat_tu_rii", "nhat_quan", "hang_tong"]]
        .rename(columns={"hang": "hang_pim", "hang_tong": "hang_rii"}).to_markdown(index=False))
    ghi()
    ghi(f"{(co_ma.nhat_quan == 'có').sum()}/{len(co_ma)} rủi ro có mức trong Bảng 6 khớp với RII ở Bảng 7. "
        "Thứ hạng giữa hai cách cũng khác nhau, ví dụ CL2 'Chính phủ bất ổn' đứng đầu RII nhưng không có trong top 10 PIM.")
    ghi()

    ve_ma_tran_pim(pim)
    return gop


def ve_ma_tran_pim(pim):
    diem = np.outer(np.arange(1, 6), np.arange(1, 6))  # hàng = xác suất, cột = tác động
    vung = np.where(diem >= 15, 2, np.where(diem >= 8, 1, 0))
    mau = matplotlib.colors.ListedColormap(["#9bd39b", "#f5d76e", "#ef8a7a"])

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(vung, cmap=mau, origin="lower")
    for i in range(5):
        for j in range(5):
            ax.text(j, i - 0.35, str(diem[i, j]), ha="center", va="center", fontsize=8, color="#555")
    o = {}
    for _, r in pim.iterrows():
        o.setdefault((MUC_SO[r.xac_suat] - 1, MUC_SO[r.tac_dong] - 1), []).append(str(r.hang))
    for (i, j), ds in o.items():
        ax.text(j, i + 0.05, ", ".join(ds), ha="center", va="center", fontsize=10, weight="bold")
    ax.set_xticks(range(5), ["Rất thấp", "Thấp", "Trung bình", "Cao", "Rất cao"])
    ax.set_yticks(range(5), ["Rất thấp", "Thấp", "Trung bình", "Cao", "Rất cao"])
    ax.set_xlabel("Mức tác động")
    ax.set_ylabel("Mức xác suất")
    ax.set_title("Vị trí top 10 rủi ro trên ma trận xác suất – tác động\n(số in đậm = thứ hạng trong Bảng 6)")
    fig.tight_layout()
    fig.savefig(FIGURES / "ma_tran_pim_top10.png", dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------- mô hình đo lường
def ave_cr(loading):
    l = np.asarray(loading)
    ave = np.mean(l ** 2)
    cr = l.sum() ** 2 / (l.sum() ** 2 + np.sum(1 - l ** 2))
    return ave, cr


def kiem_tra_do_luong():
    ld = pd.read_csv(DATA / "bang8_loading.csv")
    cs = pd.read_csv(DATA / "bang8_chi_so_nhom.csv").set_index("nhom")

    dong = []
    for nhom, g in ld.groupby("nhom", sort=False):
        ave, cr = ave_cr(g.loading)
        dong.append({"nhom": nhom, "so_cau": len(g), "loading_min": g.loading.min(),
                     "ave_bai_bao": cs.at[nhom, "ave"], "ave_tinh_lai": round(ave, 3),
                     "ave": khop(ave, cs.at[nhom, "ave"]),
                     "cr_bai_bao": cs.at[nhom, "cr"], "cr_tinh_lai": round(cr, 3),
                     "cr": khop(cr, cs.at[nhom, "cr"])})
    df = pd.DataFrame(dong)
    df.to_csv(TABLES / "ave_cr_tinh_lai.csv", index=False)

    ghi("## 3. AVE và CR tính lại từ loading (Bảng 8)")
    ghi()
    ghi("AVE = trung bình bình phương loading; CR = (Σλ)² / ((Σλ)² + Σ(1 − λ²)).")
    ghi()
    ghi(df.to_markdown(index=False))
    ghi()

    # biến kết quả EF: thử bỏ từng câu xem có ra AVE 0.549 không
    ef = ld[ld.nhom == "EF"].set_index("cau").loading
    thu = []
    for bo in [None] + list(ef.index):
        con = ef.drop(bo) if bo else ef
        ave, cr = ave_cr(con)
        thu.append({"bo_cau": bo or "(không bỏ)", "so_cau": len(con),
                    "ave": round(ave, 3), "cr": round(cr, 3)})
    thu = pd.DataFrame(thu)
    thu.to_csv(TABLES / "ef_thu_bo_cau.csv", index=False)
    ghi("Riêng biến kết quả EF (bài báo: AVE 0.549, CR 0.826), thử bỏ từng câu:")
    ghi()
    ghi(thu.to_markdown(index=False))
    ghi()
    ghi("Không phương án nào cho ra đúng AVE 0.549, kể cả khi bỏ EF3 như tác giả nói.")
    ghi()
    return df


def kiem_tra_fornell_larcker():
    fl = pd.read_csv(DATA / "bang9_fornell_larcker.csv", index_col=0)
    cs = pd.read_csv(DATA / "bang8_chi_so_nhom.csv").set_index("nhom")
    M = fl.values.copy()
    M = np.where(np.isnan(M), M.T, M)          # đối xứng hoá
    ten = list(fl.index)

    dong = []
    for i, n in enumerate(ten):
        tuong_quan = np.delete(M[i], i)
        doi_tac = np.delete(np.array(ten), i)
        j = int(np.argmax(tuong_quan))
        dong.append({"nhom": n, "can_ave_bang9": M[i, i],
                     "can_ave_tu_bang8": round(np.sqrt(cs.at[n, "ave"]), 3),
                     "tuong_quan_max": tuong_quan[j], "voi_nhom": doi_tac[j],
                     "khoang_cach": round(M[i, i] - tuong_quan[j], 3),
                     "dat": "đạt" if M[i, i] > tuong_quan[j] else "KHÔNG ĐẠT"})
    df = pd.DataFrame(dong)
    df.to_csv(TABLES / "fornell_larcker_kiem_tra.csv", index=False)

    tri = M[np.tril_indices(len(ten), -1)]
    ghi("## 4. Fornell–Larcker (Bảng 9)")
    ghi()
    ghi("Bản PDF in Bảng 9 theo từng đường chéo; ma trận đã được dựng lại trong data/published/bang9_fornell_larcker.csv.")
    ghi()
    ghi(df.to_markdown(index=False))
    ghi()
    ghi(f"Tương quan giữa các nhóm: trung bình {tri.mean():.3f}, lớn nhất {tri.max():.3f}; "
        f"{(tri > 0.85).sum()}/{len(tri)} cặp > 0.85 và {(tri > 0.80).sum()}/{len(tri)} cặp > 0.80.")
    hong = df[df.dat != "đạt"]
    sat = df[(df.dat == "đạt") & (df.khoang_cach < 0.03)]
    if len(hong):
        ghi("**Không đạt** ở: " + ", ".join(f"{r.nhom} (tương quan với {r.voi_nhom} = {r.tuong_quan_max:.3f} "
                                             f"> √AVE = {r.can_ave_bang9:.3f})" for r in hong.itertuples())
            + ". Bài báo lại kết luận tất cả đều đạt.")
    ghi("Sát ngưỡng (chênh < 0.03): " + ", ".join(f"{r.nhom} ({r.khoang_cach:+.3f})" for r in sat.itertuples()) + ".")
    ghi()
    ghi("Tương quan giữa biến tiềm ẩn đã cao như vậy thì HTMT (tính từ tương quan giữa các câu hỏi, không bị suy giảm) "
        "nhiều khả năng còn cao hơn, có thể vượt ngưỡng 0.85. Không tính được HTMT vì thiếu dữ liệu gốc.")
    ghi()
    return df


# ---------------------------------------------------------------- mô hình cấu trúc
def kiem_tra_cau_truc(ave_df):
    p = pd.read_csv(DATA / "bang11_duong_dan.csv")
    p["do_lech_chuan_suy_ra"] = (p.beta / p.t).round(4)
    p.to_csv(TABLES / "duong_dan_do_lech_chuan.csv", index=False)

    ghi("## 5. Hệ số đường dẫn (Bảng 11)")
    ghi()
    ghi("Độ lệch chuẩn bootstrap suy ra = β / t.")
    ghi()
    ghi(p.to_markdown(index=False))
    ghi()
    nhom = p[~p.tu.isin(["INT", "EXT"])]
    ghi(f"13 nhóm bậc 1 có độ lệch chuẩn chỉ {nhom.do_lech_chuan_suy_ra.min():.4f}–"
        f"{nhom.do_lech_chuan_suy_ra.max():.4f}, nhỏ hơn khoảng 10–20 lần so với hai nhóm bậc 2 (≈ 0.064). "
        "Với mẫu 314 phiếu, đường dẫn trực tiếp thông thường hiếm khi có sai số nhỏ như vậy.")
    ghi()

    noi_bo = ["CL", "CO", "CN", "FD", "TC", "RM", "MR"]
    ben_ngoai = ["EC", "PO", "LP", "EN", "SE", "FM"]
    b = p.set_index("tu").beta
    ghi("Thử giả thuyết 'β của nhóm bậc 1 = trọng số lên nhóm bậc 2 × β của nhóm bậc 2':")
    ghi()
    ghi(f"- Nội bộ: β_nhóm / 0.200 = " + ", ".join(f"{k} {b[k] / b['INT']:.2f}" for k in noi_bo))
    ghi(f"- Bên ngoài: β_nhóm / 0.673 = " + ", ".join(f"{k} {b[k] / b['EXT']:.2f}" for k in ben_ngoai))
    ghi()
    tl_nb = b[noi_bo] / b["INT"]
    tl_bn = b[ben_ngoai] / b["EXT"]
    ghi(f"Bên nội bộ có tỷ lệ lớn nhất {tl_nb.max():.2f} ({tl_nb.idxmax()}), vượt 1 nên không thể là loading; "
        f"bên ngoài thì tỷ lệ chỉ {tl_bn.min():.2f}–{tl_bn.max():.2f}, quá nhỏ cho một loading. "
        "Vậy giả thuyết đơn giản này không giải thích được. Bài báo không nói rõ "
        "13 hệ số này được ước lượng thế nào, nên không kiểm chứng được.")
    ghi()

    # Q2
    q = pd.read_csv(DATA / "bang14_q2.csv")
    q["q2_tinh_lai"] = (1 - q.sse / q.sso).round(3)
    q["so_cau_suy_ra"] = (q.sso / N).round(2)
    q["bien_suy_ra"] = q.so_cau_suy_ra.map({4.0: "EF (4 câu, đã bỏ 1)", 20.0: "Bên ngoài (20 câu)",
                                            31.0: "Nội bộ (31 câu)"})
    q["ket_qua"] = [khop(a, b) for a, b in zip(q.q2_tinh_lai, q.q2)]
    q.to_csv(TABLES / "q2_tinh_lai.csv", index=False)
    ghi("## 6. Q² = 1 − SSE/SSO (Bảng 14)")
    ghi()
    ghi(q.to_markdown(index=False))
    ghi()
    ghi("SSO = số phiếu × số câu hỏi của biến, nên chia SSO cho 314 sẽ biết mỗi dòng là biến nào. "
        "Bảng 14 không ghi tên dòng rõ ràng; suy ra: 0.369 là EF (chỉ còn 4 câu, khớp việc bỏ EF3), "
        "0.590 là rủi ro bên ngoài, 0.527 là rủi ro nội bộ. Vậy mục 5.3 nói đúng, còn phần Kết luận "
        "(nội bộ 0.590, bên ngoài 0.527) bị nhầm.")
    ghi()

    # GoF
    r2 = 0.720
    ghi("## 7. GoF = √(R² × AVE trung bình)")
    ghi()
    ghi(f"√(0.720 × 0.566) = {np.sqrt(r2 * 0.566):.3f} → khớp với 0.638 bài báo công bố.")
    ghi()
    cs = pd.read_csv(DATA / "bang8_chi_so_nhom.csv").set_index("nhom").ave
    ung_vien = {"13 nhóm bậc 1": cs.iloc[:13].mean(),
                "13 nhóm bậc 1 + EF": cs.iloc[:14].mean(),
                "INT + EXT": cs[["INT", "EXT"]].mean(),
                "INT + EXT + EF": cs[["INT", "EXT", "EF"]].mean(),
                "INT + EF": cs[["INT", "EF"]].mean(),
                "EXT + EF": cs[["EXT", "EF"]].mean()}
    ghi("Bài không nói 0.566 là trung bình AVE của những biến nào. Thử các cách lấy trung bình:")
    ghi()
    for k, v in ung_vien.items():
        ghi(f"- {k}: {v:.3f} → GoF = {np.sqrt(r2 * v):.3f}")
    ghi()
    ghi("Không cách nào ra đúng 0.566. Nếu lấy trung bình 13 nhóm bậc 1 (cách thường dùng) thì GoF ≈ 0.735.")
    ghi()

    # f2
    ghi("## 8. f² và R² khi bỏ từng biến")
    ghi()
    ghi("f² = (R²_có − R²_bỏ) / (1 − R²_có) ⇒ R²_bỏ = R²_có − f² × (1 − R²_có).")
    ghi()
    for ten, f2 in [("rủi ro nội bộ", 0.042), ("rủi ro bên ngoài", 0.471)]:
        ghi(f"- Bỏ {ten} (f² = {f2}): R² còn {r2 - f2 * (1 - r2):.3f}")
    ghi()
    ghi("Bỏ rủi ro bên ngoài mà R² vẫn còn 0.588 nghĩa là riêng rủi ro nội bộ đã giải thích được ~59%. "
        "Như vậy hai nhóm chồng lấn nhau rất nhiều, phù hợp với tương quan cao ở Bảng 9.")
    ghi()


def ve_rii(rii):
    df = rii.sort_values("rii_tong")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    y = np.arange(len(df))
    ax.barh(y - 0.2, df.rii_tac_dong, height=0.4, label="RII tác động", color="#4c78a8")
    ax.barh(y + 0.2, df.rii_xac_suat, height=0.4, label="RII xác suất", color="#f58518")
    ax.scatter(df.rii_tong, y, color="black", zorder=3, label="RII tổng (tác động × xác suất)")
    ax.set_yticks(y, [f"{m} – {t}" for m, t in zip(df.ma, df.rui_ro)])
    ax.set_xlim(0, 1)
    ax.set_xlabel("Giá trị RII")
    ax.set_title("Top 10 rủi ro theo RII (số liệu Bảng 7)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.12), ncol=3, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURES / "rii_top10.png", dpi=200)
    plt.close(fig)


def main():
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    ghi("# Kết quả kiểm tra lại số liệu đã công bố")
    ghi()
    ghi("File này do `src/kiem_tra_so_lieu.py` sinh ra. Sai số chấp nhận: ±0.0015 (làm tròn 3 chữ số).")
    ghi()
    rii = kiem_tra_rii()
    kiem_tra_pim(rii)
    ave = kiem_tra_do_luong()
    kiem_tra_fornell_larcker()
    kiem_tra_cau_truc(ave)
    ve_rii(rii)

    (ROOT / "results" / "kiem-tra-so-lieu.md").write_text("\n".join(bao_cao), encoding="utf-8")
    print("\n".join(bao_cao))


if __name__ == "__main__":
    main()
