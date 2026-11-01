import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as cot

sys.path.insert(0, str(Path(__file__).resolve().parent))
from du_lieu_that_aceh import NHOM, TEN, doc_du_lieu

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "quan-ly-du-an" / "du-lieu-aceh.xlsx"
FONT = "Arial"
VIEN = Border(*(Side(style="thin", color="BFBFBF"),) * 4)


def tieu_de(ws, hang, ten, rong):
    for i, (t, w) in enumerate(zip(ten, rong), 1):
        c = ws.cell(hang, i, t)
        c.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = VIEN
        ws.column_dimensions[cot(i)].width = w
    ws.row_dimensions[hang].height = 30


def o(ws, r, c, v, fmt=None, dam=False, can="center"):
    x = ws.cell(r, c, v)
    x.font = Font(name=FONT, size=10, bold=dam)
    if fmt:
        x.number_format = fmt
    x.alignment = Alignment(horizontal=can, vertical="center", wrap_text=True)
    x.border = VIEN


def hien_truc(bd):
    bd.x_axis.delete = False
    bd.y_axis.delete = False
    bd.x_axis.title = None
    bd.y_axis.title = None
    if bd.title is not None:
        bd.title.overlay = False
    bd.legend = None
    return bd


def main():
    df = doc_du_lieu()
    n = len(df)
    wb = Workbook()

    ws = wb.active
    ws.title = "Dữ liệu"
    ws["A1"] = ("Dữ liệu gốc: Rauzana (2021), Dataset of Causes of delays in construction projects, Mendeley Data, "
                "doi:10.17632/2wckhrzz5j.1, giấy phép CC BY 4.0. 68 nhà thầu ở Aceh, thang 1–5 (mức ảnh hưởng).")
    ws["A1"].font = Font(name=FONT, size=9, italic=True)
    ws.cell(3, 1, "Phiếu").font = Font(name=FONT, bold=True)
    for j, c in enumerate(df.columns, 2):
        ws.cell(3, j, c).font = Font(name=FONT, bold=True)
        for i, v in enumerate(df[c], 4):
            ws.cell(i, j, int(v))
    for i in range(n):
        ws.cell(4 + i, 1, i + 1)
    dau, cuoi = 4, 3 + n
    cot_cua = {c: cot(j) for j, c in enumerate(df.columns, 2)}
    ws.freeze_panes = "B4"

    tg = wb.create_sheet("Tổng nhóm")
    tg["A1"] = "Tổng điểm của từng phiếu theo nhóm (dùng để tính phương sai tổng trong công thức Cronbach's α)"
    tg["A1"].font = Font(name=FONT, size=9, italic=True)
    nhom = list(NHOM) + ["Y"]
    cau = {g: [c for c in df.columns if c.split(".")[0] == g] for g in NHOM}
    cau["Y"] = ["Y1", "Y2", "Y3", "Y4"]
    for k, g in enumerate(nhom, 2):
        tg.cell(3, k, g).font = Font(name=FONT, bold=True)
        for i in range(dau, cuoi + 1):
            tg.cell(i, k, "=" + "+".join(f"'Dữ liệu'!{cot_cua[c]}{i}" for c in cau[g]))
    cot_tong = {g: cot(k) for k, g in enumerate(nhom, 2)}

    ws = wb.create_sheet("RII")
    ws["A1"] = "RII = trung bình điểm / 5 (= tổng điểm / (5 × n)). Tổng điểm và hạng để đối chiếu với bài gốc (X8.5 = 327)."
    ws["A1"].font = Font(name=FONT, size=9, italic=True)
    tieu_de(ws, 3, ["Mã", "Nhóm", "Yếu tố", "Tổng điểm", "RII", "Hạng", "Phương sai"], [7, 14, 44, 10, 9, 7, 10])
    yeu_to = [c for c in df.columns if c.startswith("X")]
    for k, c in enumerate(yeu_to):
        r = 4 + k
        vung = f"'Dữ liệu'!{cot_cua[c]}{dau}:{cot_cua[c]}{cuoi}"
        o(ws, r, 1, c)
        o(ws, r, 2, NHOM[c.split(".")[0]])
        o(ws, r, 3, TEN[c], can="left")
        o(ws, r, 4, f"=SUM({vung})", fmt="0")
        o(ws, r, 5, f"=AVERAGE({vung})/5", fmt="0.000")
        o(ws, r, 6, f"=RANK(E{r},$E$4:$E${3 + len(yeu_to)})")
        o(ws, r, 7, f"=VAR({vung})", fmt="0.000")
    for k, c in enumerate(cau["Y"]):
        r = 4 + len(yeu_to) + k
        vung = f"'Dữ liệu'!{cot_cua[c]}{dau}:{cot_cua[c]}{cuoi}"
        o(ws, r, 1, c)
        o(ws, r, 2, "Y")
        o(ws, r, 3, "Biến kết quả (bài gốc không định nghĩa)", can="left")
        o(ws, r, 7, f"=VAR({vung})", fmt="0.000")
    het = 3 + len(yeu_to) + 4
    ws.freeze_panes = "D4"

    cr = wb.create_sheet("Cronbach-Nhóm")
    cr["A1"] = "α = k/(k−1) × (1 − Σ phương sai từng câu / phương sai tổng điểm). Bài gốc: Chính trị 0,638; Lao động 0,944."
    cr["A1"].font = Font(name=FONT, size=9, italic=True)
    tieu_de(cr, 3, ["Mã", "Nhóm", "Số câu k", "Σ phương sai câu", "Phương sai tổng", "Cronbach's α", "RII trung bình"],
            [7, 16, 9, 14, 14, 12, 13])
    for k, g in enumerate(nhom):
        r = 4 + k
        ten = NHOM.get(g, "Y")
        o(cr, r, 1, g)
        o(cr, r, 2, ten)
        o(cr, r, 3, f'=COUNTIF(RII!$B$4:$B${het},B{r})')
        o(cr, r, 4, f'=SUMIF(RII!$B$4:$B${het},B{r},RII!$G$4:$G${het})', fmt="0.000")
        o(cr, r, 5, f"=VAR('Tổng nhóm'!{cot_tong[g]}{dau}:{cot_tong[g]}{cuoi})", fmt="0.000")
        o(cr, r, 6, f"=C{r}/(C{r}-1)*(1-D{r}/E{r})", fmt="0.000", dam=True)
        o(cr, r, 7, f'=IFERROR(AVERAGEIF(RII!$B$4:$B${het},B{r},RII!$E$4:$E${het}),"")', fmt="0.000")
    bd = BarChart()
    bd.type = "bar"
    bd.title = "RII trung bình theo nhóm nguyên nhân chậm trễ (Aceh)"
    bd.add_data(Reference(cr, min_col=7, min_row=3, max_row=3 + len(NHOM)), titles_from_data=True)
    bd.set_categories(Reference(cr, min_col=2, min_row=4, max_row=3 + len(NHOM)))
    bd.y_axis.scaling.min, bd.y_axis.scaling.max = 0.8, 1.0
    bd.height, bd.width = 9, 16
    cr.add_chart(hien_truc(bd), "I3")
    wb.move_sheet("Cronbach-Nhóm", offset=-3)
    wb.move_sheet("RII", offset=-2)
    wb.save(OUT)
    print("Đã tạo", OUT)


if __name__ == "__main__":
    main()
