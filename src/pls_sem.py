"""Cài đặt PLS-SEM (mô hình đo lường kết quả – Mode A, lược đồ trọng số đường dẫn).

Các bước giống mục 2.5.1 của báo cáo:
  1. khởi tạo trọng số ngoài = 1
  2. xấp xỉ ngoài: Y_j = X_j w_j (chuẩn hoá)
  3. xấp xỉ trong: Z_j = Σ e_ji Y_i (lược đồ đường dẫn)
  4. cập nhật trọng số Mode A: w_j = cov(X_j, Z_j)
  5. lặp tới khi thay đổi < 1e-7
  6. loading = corr(x, Y), hệ số đường dẫn = OLS giữa các biến tiềm ẩn

Ngoài ra: AVE, CR, Cronbach's α, Fornell–Larcker, HTMT, R², f², Q² (blindfolding), GoF, bootstrapping.
"""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd


def _chuan_hoa(a):
    a = np.asarray(a, dtype=float)
    sd = a.std(axis=0, ddof=0)
    sd[sd == 0] = 1.0
    return (a - a.mean(axis=0)) / sd


def _ols(y, X):
    """Hệ số hồi quy chuẩn hoá của y theo các cột của X."""
    return np.linalg.lstsq(X, y, rcond=None)[0]


@dataclass
class KetQua:
    diem: pd.DataFrame                 # điểm biến tiềm ẩn (chuẩn hoá)
    trong_so: dict                     # trọng số ngoài theo khối
    loading: pd.DataFrame              # khoi, cau, loading
    he_so: pd.DataFrame                # tu, den, beta
    r2: pd.Series
    so_vong_lap: int
    hoi_tu: bool
    tong_hieu_ung: pd.DataFrame = field(default=None)


class PLSSEM:
    def __init__(self, khoi: dict, duong_dan: list, max_lap=300, sai_so=1e-7):
        """khoi: {tên biến tiềm ẩn: [tên cột câu hỏi]}; duong_dan: [(từ, đến)]."""
        self.khoi = khoi
        self.ten = list(khoi)
        self.duong_dan = duong_dan
        self.max_lap = max_lap
        self.sai_so = sai_so
        self.truoc = {j: [i for i, k in duong_dan if k == j] for j in self.ten}
        self.sau = {j: [k for i, k in duong_dan if i == j] for j in self.ten}
        self.noi_sinh = [j for j in self.ten if self.truoc[j]]

    # ------------------------------------------------------------ ước lượng
    def uoc_luong(self, du_lieu: pd.DataFrame) -> KetQua:
        X = {j: _chuan_hoa(du_lieu[c].values) for j, c in self.khoi.items()}
        n = len(du_lieu)
        w = {j: np.ones(X[j].shape[1]) for j in self.ten}

        def diem_tu(w):
            Y = {}
            for j in self.ten:
                y = X[j] @ w[j]
                Y[j] = (y - y.mean()) / y.std(ddof=0)
            return Y

        hoi_tu = False
        for vong in range(1, self.max_lap + 1):
            Y = diem_tu(w)
            Ym = np.column_stack([Y[j] for j in self.ten])
            w_moi = {}
            for a, j in enumerate(self.ten):
                Z = np.zeros(n)
                if self.truoc[j]:                                  # tiền nhiệm: hệ số hồi quy
                    P = np.column_stack([Y[i] for i in self.truoc[j]])
                    for i, e in zip(self.truoc[j], _ols(Y[j], P)):
                        Z += e * Y[i]
                for k in self.sau[j]:                              # kế nhiệm: tương quan
                    Z += np.corrcoef(Y[j], Y[k])[0, 1] * Y[k]
                if not self.truoc[j] and not self.sau[j]:
                    Z = Y[j]
                wj = X[j].T @ Z / n                                # Mode A
                y = X[j] @ wj
                w_moi[j] = wj / y.std(ddof=0)
            thay_doi = max(np.abs(w_moi[j] - w[j]).sum() for j in self.ten)
            w = w_moi
            if thay_doi < self.sai_so:
                hoi_tu = True
                break

        Y = diem_tu(w)
        diem = pd.DataFrame(Y)
        ld = []
        for j, cols in self.khoi.items():
            for c, xc in zip(cols, X[j].T):
                ld.append({"khoi": j, "cau": c, "loading": np.corrcoef(xc, Y[j])[0, 1]})
        hs, r2 = [], {}
        for j in self.noi_sinh:
            P = diem[self.truoc[j]].values
            b = _ols(diem[j].values, P)
            r2[j] = 1 - np.sum((diem[j].values - P @ b) ** 2) / np.sum(diem[j].values ** 2)
            hs += [{"tu": i, "den": j, "beta": bi} for i, bi in zip(self.truoc[j], b)]
        kq = KetQua(diem, w, pd.DataFrame(ld), pd.DataFrame(hs), pd.Series(r2), vong, hoi_tu)
        kq.tong_hieu_ung = self.tong_hieu_ung(kq.he_so)
        return kq

    def tong_hieu_ung(self, he_so):
        """Tổng hiệu ứng (trực tiếp + gián tiếp) giữa mọi cặp biến, tính qua ma trận đường dẫn."""
        idx = {j: a for a, j in enumerate(self.ten)}
        B = np.zeros((len(self.ten), len(self.ten)))
        for r in he_so.itertuples():
            B[idx[r.tu], idx[r.den]] = r.beta
        T, luy_thua = np.zeros_like(B), np.eye(len(self.ten))
        for _ in range(len(self.ten)):
            luy_thua = luy_thua @ B
            T += luy_thua
        dong = [{"tu": i, "den": j, "tong": T[idx[i], idx[j]]}
                for i in self.ten for j in self.ten if abs(T[idx[i], idx[j]]) > 1e-12]
        return pd.DataFrame(dong)

    # ------------------------------------------------------------ đánh giá mô hình đo lường
    @staticmethod
    def do_tin_cay(kq: KetQua, du_lieu: pd.DataFrame, khoi: dict):
        dong = []
        for j, cols in khoi.items():
            l = kq.loading[kq.loading.khoi == j].loading.values
            Xj = du_lieu[cols].values.astype(float)
            k = len(cols)
            alpha = k / (k - 1) * (1 - Xj.var(axis=0, ddof=1).sum() / Xj.sum(axis=1).var(ddof=1)) if k > 1 else np.nan
            dong.append({"khoi": j, "so_cau": k, "loading_min": l.min(), "alpha": alpha,
                         "cr": l.sum() ** 2 / (l.sum() ** 2 + np.sum(1 - l ** 2)), "ave": np.mean(l ** 2)})
        return pd.DataFrame(dong).set_index("khoi")

    @staticmethod
    def fornell_larcker(kq: KetQua, ten: list, ave: pd.Series):
        R = kq.diem[ten].corr().values
        np.fill_diagonal(R, np.sqrt(ave[ten].values))
        return pd.DataFrame(R, index=ten, columns=ten)

    @staticmethod
    def htmt(du_lieu: pd.DataFrame, khoi: dict, ten: list):
        """HTMT (Henseler và cộng sự, 2015): trung bình tương quan khác khối / căn tích trung bình cùng khối."""
        C = du_lieu[[c for j in ten for c in khoi[j]]].corr().abs()

        def cung_khoi(j):
            cols = khoi[j]
            m = C.loc[cols, cols].values
            return m[np.triu_indices(len(cols), 1)].mean()

        H = pd.DataFrame(np.nan, index=ten, columns=ten)
        for a, i in enumerate(ten):
            for j in ten[:a]:
                H.loc[i, j] = C.loc[khoi[i], khoi[j]].values.mean() / np.sqrt(cung_khoi(i) * cung_khoi(j))
        return H

    # ------------------------------------------------------------ đánh giá mô hình cấu trúc
    def f2(self, kq: KetQua):
        dong = []
        for j in self.noi_sinh:
            for i in self.truoc[j]:
                con_lai = [p for p in self.truoc[j] if p != i]
                if con_lai:
                    P = kq.diem[con_lai].values
                    b = _ols(kq.diem[j].values, P)
                    r2_bo = 1 - np.sum((kq.diem[j].values - P @ b) ** 2) / np.sum(kq.diem[j].values ** 2)
                else:
                    r2_bo = 0.0
                dong.append({"tu": i, "den": j, "r2_bo": r2_bo, "f2": (kq.r2[j] - r2_bo) / (1 - kq.r2[j])})
        return pd.DataFrame(dong)

    def q2(self, du_lieu: pd.DataFrame, bien: list, D=7):
        """Blindfolding, khoảng cách bỏ D: che lần lượt các ô của khối biến nội sinh, ước lượng lại,
        dự báo phần bị che qua x̂ = λ · Ŷ (Ŷ tính từ các biến tiền nhiệm), Q² = 1 − SSE/SSO."""
        Xs = pd.DataFrame(_chuan_hoa(du_lieu.values), columns=du_lieu.columns)
        kq_bang = []
        for j in bien:
            cols = self.khoi[j]
            n, k = len(Xs), len(cols)
            sse = sso = 0.0
            so_thu_tu = np.arange(n * k).reshape(n, k)
            for d in range(D):
                che = (so_thu_tu % D) == d
                X_che = Xs.copy()
                khoi_che = X_che[cols].values
                tb = np.array([khoi_che[~che[:, c], c].mean() for c in range(k)])
                khoi_che = np.where(che, tb, khoi_che)
                X_che[cols] = khoi_che
                kq = self.uoc_luong(X_che)
                b = kq.he_so[kq.he_so.den == j].set_index("tu").beta
                y_hat = kq.diem[list(b.index)].values @ b.values
                lam = kq.loading[kq.loading.khoi == j].loading.values
                x_hat = np.outer(y_hat, lam)
                that = Xs[cols].values
                sse += np.sum(((that - x_hat) ** 2)[che])
                sso += np.sum((that ** 2)[che])
            kq_bang.append({"bien": j, "so_cau": k, "sso": sso, "sse": sse, "q2": 1 - sse / sso})
        return pd.DataFrame(kq_bang)

    # ------------------------------------------------------------ bootstrapping
    def bootstrap(self, du_lieu: pd.DataFrame, B=5000, seed=1, hien=None):
        rng = np.random.default_rng(seed)
        n = len(du_lieu)
        hs, th = [], []
        for b in range(B):
            mau = du_lieu.iloc[rng.integers(0, n, n)].reset_index(drop=True)
            kq = self.uoc_luong(mau)
            hs.append(kq.he_so.set_index(["tu", "den"]).beta)
            th.append(kq.tong_hieu_ung.set_index(["tu", "den"]).tong)
            if hien and (b + 1) % hien == 0:
                print(f"  bootstrap {b + 1}/{B}")
        return pd.DataFrame(hs), pd.DataFrame(th)


def tom_tat_bootstrap(goc: pd.Series, mau: pd.DataFrame):
    """Sai số chuẩn, t, p (hai phía, xấp xỉ chuẩn) và khoảng tin cậy phân vị 95%."""
    from math import erf, sqrt
    se = mau.std(ddof=1)
    t = goc / se
    p = t.abs().map(lambda v: 2 * (1 - 0.5 * (1 + erf(v / sqrt(2)))))
    return pd.DataFrame({"beta": goc, "se": se, "t": t, "p": p,
                         "ci_2.5%": mau.quantile(0.025), "ci_97.5%": mau.quantile(0.975)})


def gof(ave: pd.Series, r2: pd.Series):
    return float(np.sqrt(ave.mean() * r2.mean()))
