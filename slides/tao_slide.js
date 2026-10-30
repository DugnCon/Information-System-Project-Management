// Tạo slide thuyết trình báo cáo giữa kỳ (15 slide nội dung + bìa + hỏi đáp).
// Chạy:  NODE_PATH=<thư mục có pptxgenjs> node slides/tao_slide.js
// Số liệu dữ liệu Aceh đọc từ results/tables/aceh_*.csv và results/aceh.md.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..");
const HINH = (f) => path.join(ROOT, "report", "hinh", f);
const KQ = (f) => path.join(ROOT, "results", "figures", f);

// ---------- số liệu Aceh ----------
function docCsv(f) {
  const [dau, ...dong] = fs.readFileSync(path.join(ROOT, "results", "tables", f), "utf8").trim().split(/\r?\n/);
  const cot = dau.split(",");
  return dong.map((d) => Object.fromEntries(d.split(",").map((v, i) => [cot[i], v])));
}
const aceh = (() => {
  const bac2 = docCsv("aceh_he_so_bac2.csv");
  const bac1 = docCsv("aceh_he_so_bac1.csv");
  const rii = docCsv("aceh_rii.csv").slice(0, 3);
  const md = fs.readFileSync(path.join(ROOT, "results", "aceh.md"), "utf8");
  const r2 = md.match(/Mô hình bậc 2[\s\S]*?R²\(Y\) = ([0-9.]+)/)[1];
  return {
    bINT: +bac2[0].beta, bEXT: +bac2[1].beta, tINT: +bac2[0].t, tEXT: +bac2[1].t, r2: +r2,
    yNghia: bac1.filter((r) => +r.p < 0.05).map((r) => r.nhom), rii,
  };
})();
const so = (x, k = 2) => Number(x).toFixed(k).replace(".", ",");

// ---------- chủ đề ----------
const THEME = {
  name: "Rui ro dau khi",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2933", lt1: "FFFFFF", dk2: "3E4C59", lt2: "EEF1F4",
    accent1: "C9761E", accent2: "B03A2E", accent3: "2E7D6B", accent4: "52606D",
    accent5: "E8B04B", accent6: "7B8794", hlink: "C9761E", folHlink: "7B8794",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,33" × 7,5"
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Quản lý rủi ro dự án xây dựng dầu khí bằng PLS-SEM";
const C = pres.SchemeColor;

pres.defineSlideMaster({
  title: "TOI", background: { color: HEX.dk1 },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.3, w: 11.7, h: 1.6,
    fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 11.7, h: 1.6,
    fontSize: 18, color: C.background2, valign: "top" }, text: "" } }],
});
pres.defineSlideMaster({
  title: "TOI_NOI_DUNG", background: { color: HEX.dk1 },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.8, y: 0.6, w: 11.7, h: 1.1,
    fontSize: 36, bold: true, color: C.background1, valign: "middle", align: "left" }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 2.0, w: 11.7, h: 4.6,
    fontSize: 20, color: C.background1, valign: "top" }, text: "" } }],
});
pres.defineSlideMaster({
  title: "NOI_DUNG", background: { color: HEX.lt1 },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9,
    fontSize: 30, bold: true, color: C.text1, valign: "middle" }, text: "" } }],
  slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: "7B8794" },
});

let sv = 0;
function slideMoi(tieuDe, ghiChu) {
  const s = pres.addSlide({ masterName: "NOI_DUNG" });
  s.addText(tieuDe, { placeholder: "title" });
  if (ghiChu) s.addNotes(ghiChu);
  sv++;
  return s;
}
function hop(s, x, y, w, h, mau = C.background2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: mau }, line: { type: "none" }, rectRadius: 0.08 });
}
function soLon(s, x, y, w, gia, nhan, mau = C.accent1) {
  hop(s, x, y, w, 1.55);
  s.addText(gia, { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: 0.8, fontSize: 36, bold: true, color: mau, isTextBox: true, margin: 0, fontFace: THEME.headFontFace });
  s.addText(nhan, { x: x + 0.15, y: y + 0.92, w: w - 0.3, h: 0.55, fontSize: 13, color: C.text2, isTextBox: true, margin: 0 });
}
function gach(s, dong, x, y, w, h, co = 16) {
  s.addText(dong.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < dong.length - 1 } })),
    { x, y, w, h, fontSize: co, color: C.text1, paraSpaceAfter: 8, valign: "top", isTextBox: true });
}
// Đặt ảnh vừa khung (x, y, w, h), giữ đúng tỉ lệ, căn giữa. Kích thước ảnh đọc từ phần đầu file PNG.
function anh(s, file, x, y, w, h) {
  const b = fs.readFileSync(file);
  const rong = b.readUInt32BE(16), cao = b.readUInt32BE(20);
  const tl = Math.min(w / rong, h / cao);
  const ww = rong * tl, hh = cao * tl;
  s.addImage({ path: file, x: x + (w - ww) / 2, y: y + (h - hh) / 2, w: ww, h: hh });
}

// ===== 0. Bìa =====
{
  const s = pres.addSlide({ masterName: "TOI" });
  s.addText("Quản lý rủi ro dự án xây dựng dầu khí bằng mô hình PLS-SEM", { placeholder: "title" });
  s.addText("Báo cáo giữa kỳ – Quản lý dự án hệ thống thông tin\nBài báo: Kassem, M.A. (2022). Gases, 2(2), 33–60", { placeholder: "body" });
  s.addNotes("Giới thiệu bản thân và đề tài. Bài báo của Kassem năm 2022 về đánh giá quản lý rủi ro trong dự án xây dựng dầu khí ở Yemen bằng mô hình PLS-SEM.");
}

// ===== 1. Vấn đề và bài báo =====
{
  const s = slideMoi("Bài báo nghiên cứu vấn đề gì", "Dự án dầu khí hay trễ tiến độ và vượt chi phí. Bài báo khảo sát 314 người ở Yemen về 51 yếu tố rủi ro chia 13 nhóm, rồi dùng RII, ma trận xác suất – tác động và PLS-SEM để tìm nhóm rủi ro ảnh hưởng mạnh nhất. Kết quả chính: rủi ro bên ngoài (chính trị, kinh tế, an ninh) ảnh hưởng mạnh hơn rủi ro nội bộ.");
  soLon(s, 0.6, 1.5, 2.85, "314", "người trả lời: chủ đầu tư, nhà thầu, tư vấn");
  soLon(s, 3.65, 1.5, 2.85, "51", "yếu tố rủi ro, chia 13 nhóm");
  soLon(s, 6.7, 1.5, 2.85, "0,72", "R²: mô hình giải thích 72% ảnh hưởng tới thành công");
  soLon(s, 9.75, 1.5, 2.95, "0,673", "β rủi ro bên ngoài, so với 0,200 của nội bộ", C.accent2);
  gach(s, [
    "Bối cảnh: dự án xây dựng dầu khí ở Yemen – thường trễ tiến độ, vượt chi phí, chất lượng kém",
    "Câu hỏi: nhóm rủi ro nào ảnh hưởng mạnh nhất tới thành công của dự án?",
    "Phương pháp: khảo sát Likert 1–5 → Cronbach's α → RII → ma trận PIM → PLS-SEM (SmartPLS 3)",
    "Kết luận của tác giả: rủi ro bên ngoài (chính trị, kinh tế, an ninh) lấn át rủi ro nội bộ",
  ], 0.6, 3.4, 12.1, 3.3);
}

// ===== 2. Quản lý rủi ro theo PMBOK =====
{
  const s = slideMoi("Quy trình quản lý rủi ro theo PMBOK và phạm vi bài báo", "PMBOK 6 có 7 quy trình quản lý rủi ro. Bài báo chỉ làm bước nhận diện và hai bước phân tích. Báo cáo của em làm thêm phần lập kế hoạch ứng phó và minh họa giám sát, để chuyển kết quả nghiên cứu thành hành động của người quản lý dự án.");
  const buoc = ["Lập kế hoạch\nquản lý rủi ro", "Nhận diện\nrủi ro", "Phân tích\nđịnh tính", "Phân tích\nđịnh lượng", "Lập kế hoạch\nứng phó", "Thực hiện\nứng phó", "Giám sát\nrủi ro"];
  const loai = ["", "bb", "bb", "bb", "bc", "", "bc"];
  buoc.forEach((t, i) => {
    const x = 0.6 + i * 1.75;
    const mau = loai[i] === "bb" ? C.accent1 : loai[i] === "bc" ? C.accent3 : C.background2;
    s.addShape(pres.shapes.OVAL, { x: x + 0.45, y: 1.6, w: 0.7, h: 0.7, fill: { color: mau }, line: { type: "none" } });
    s.addText(String(i + 1), { x: x + 0.45, y: 1.6, w: 0.7, h: 0.7, fontSize: 20, bold: true, align: "center", valign: "middle", color: loai[i] ? C.background1 : C.text2, isTextBox: true, margin: 0 });
    s.addText(t, { x, y: 2.45, w: 1.6, h: 0.9, fontSize: 13, align: "center", color: C.text1, isTextBox: true, margin: 0 });
  });
  hop(s, 0.6, 3.75, 5.9, 2.0);
  s.addText([{ text: "Bài báo làm (cam)", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Nhận diện 51 yếu tố; RII và ma trận PIM (định tính); PLS-SEM đo ảnh hưởng của nhóm rủi ro (định lượng)", options: { color: C.text1 } }],
    { x: 0.85, y: 3.9, w: 5.4, h: 1.75, fontSize: 16, valign: "top", isTextBox: true });
  hop(s, 6.8, 3.75, 5.9, 2.0);
  s.addText([{ text: "Báo cáo làm thêm (xanh)", options: { bold: true, color: C.accent3, breakLine: true } },
    { text: "Kế hoạch ứng phó cho 10 rủi ro hàng đầu (né tránh, chuyển giao, giảm thiểu, chấp nhận, báo cáo lên trên); chỉ số giám sát CPI, SPI; Monte Carlo để tính dự phòng", options: { color: C.text1 } }],
    { x: 7.05, y: 3.9, w: 5.4, h: 1.75, fontSize: 16, valign: "top", isTextBox: true });
}

// ===== 3. Sơ đồ tư duy =====
{
  const s = slideMoi("Toàn cảnh chủ đề", "Sơ đồ tư duy tóm tắt cả báo cáo: bốn nhánh bên phải là phần hiểu bài báo, ba nhánh bên trái là phần em làm thêm: tái hiện, phản biện và liên hệ thực tế.");
  anh(s, HINH("so_do_tu_duy.png"), 0.6, 1.35, 12.1, 5.9);
}

// ===== 4. RII và PIM =====
{
  const s = slideMoi("Xếp hạng rủi ro: RII và ma trận xác suất – tác động", "RII bằng tổng điểm chia cho 5 nhân số người, nhân phần tác động với phần xác suất. Ví dụ chậm ra quyết định: 0,675 nhân 0,821 bằng 0,554, đúng số trong bài. Ma trận PIM chia vùng đỏ, vàng, xanh để chọn cách ứng phó. Lưu ý: cả 10 rủi ro hàng đầu đều rơi vào vùng đỏ nên ma trận không giúp xếp ưu tiên trong nhóm này.");
  hop(s, 0.6, 1.5, 5.6, 1.75);
  s.addText([{ text: "RII = ΣW / (A × N)", options: { bold: true, fontSize: 24, color: C.accent1, breakLine: true } },
    { text: "RII tổng = RII tác động × RII xác suất", options: { fontSize: 16, breakLine: true } },
    { text: "Ví dụ CL1 – chậm ra quyết định: 0,675 × 0,821 = 0,554", options: { fontSize: 14, color: C.text2 } }],
    { x: 0.85, y: 1.65, w: 5.2, h: 1.8, valign: "top", isTextBox: true, color: C.text1 });
  gach(s, [
    "Top 3 RII: chính phủ bất ổn (0,578), ước tính chi phí sai (0,568), ước tính tiến độ sai (0,556)",
    "Tính lại 10/10 RII tổng khớp với bài báo",
    "Nhưng mức PIM ở Bảng 6 chỉ khớp 3/6 với RII ở Bảng 7",
  ], 0.6, 3.55, 5.6, 3.0, 16);
  anh(s, KQ("ma_tran_pim_top10.png"), 6.6, 1.35, 6.1, 5.6);
}

// ===== 5. PLS-SEM =====
{
  const s = slideMoi("Mô hình PLS-SEM hai bậc của bài báo", "Biến tiềm ẩn như rủi ro chủ đầu tư không đo trực tiếp được, chỉ đo qua câu hỏi. PLS-SEM ước lượng đồng thời mô hình đo lường và mô hình cấu trúc. Mô hình của bài có hai bậc: 13 nhóm gom thành nội bộ và bên ngoài, cùng tác động lên ảnh hưởng tới thành công dự án. Bài chọn PLS-SEM vì dữ liệu Likert không chuẩn và mô hình phức tạp.");
  anh(s, HINH("mo_hinh_nghien_cuu.png"), 0.5, 1.3, 8.4, 5.8);
  gach(s, [
    "Mô hình đo lường: câu hỏi ↔ nhóm (loading, AVE, CR)",
    "Mô hình cấu trúc: nhóm → kết quả (β, R², f², Q²)",
    "Bootstrapping 5000 lần để có t, p",
    "Chọn PLS-SEM vì dữ liệu không chuẩn, mô hình nhiều biến",
    "Lưu ý: biến kết quả đo hậu quả xấu → β dương = dự án kém thành công hơn",
  ], 9.1, 1.5, 3.7, 5.4, 14);
}

// ===== 6. Quy trình tái hiện =====
{
  const s = slideMoi("Tái hiện thực nghiệm khi không có dữ liệu gốc", "Tác giả không công bố dữ liệu. Em tái hiện theo hai hướng: kiểm tra số liệu đã công bố bằng Python và Excel; và chạy lại toàn bộ quy trình trên dữ liệu mô phỏng theo cấu trúc bài báo, với thuật toán PLS-SEM tự cài đặt, đã kiểm chứng với nghiệm giải tích. Ngoài ra em chạy thêm trên một bộ dữ liệu thật công khai.");
  anh(s, HINH("quy_trinh_tai_hien.png"), 0.6, 1.3, 8.0, 4.4);
  hop(s, 8.9, 1.4, 3.85, 3.0);
  s.addText([{ text: "Công cụ", options: { bold: true, color: C.accent1, breakLine: true } },
    { text: "Python (tự cài đặt PLS-SEM, bootstrap, HTMT)", options: { bullet: true, breakLine: true } },
    { text: "Excel (kiểm tra bằng công thức)", options: { bullet: true, breakLine: true } },
    { text: "Kiểm chứng: trùng nghiệm giải tích tới 3×10⁻¹¹", options: { bullet: true } }],
    { x: 9.1, y: 1.55, w: 3.5, h: 2.75, fontSize: 15, valign: "top", color: C.text1, paraSpaceAfter: 6, isTextBox: true });
  s.addText("Thêm hướng 3: chạy quy trình trên dữ liệu thật công khai (68 nhà thầu ở Aceh, Indonesia)", { x: 0.6, y: 6.0, w: 12.1, h: 0.7, fontSize: 16, bold: true, color: C.accent3, isTextBox: true });
}

// ===== 7. Kiểm tra số liệu =====
{
  const s = slideMoi("Kiểm tra số liệu: phần lớn khớp, nhưng có chỗ không đạt", "Em tính lại 9 phép kiểm tra từ chính các bảng của bài. RII, AVE, CR, Q² khớp. Nhưng Fornell–Larcker không đạt ở nhóm nguồn lực vật tư RM: tương quan với quản lý dự án 0,845 lớn hơn căn AVE 0,833, trong khi bài báo nói đạt. AVE của biến kết quả tính ra 0,494 dưới ngưỡng, bài in 0,549. Không tính lại được AVE 0,566 dùng trong GoF.");
  anh(s, KQ("bd_fornell_larcker.png"), 0.5, 1.3, 6.4, 5.8);
  const dong = [["Khớp", "RII 10/10 · AVE, CR 13/13 · Q² 3/3 · R², f² nhất quán", C.accent3],
    ["Không đạt", "Fornell–Larcker ở RM: 0,845 > √AVE 0,833", C.accent2],
    ["Lệch", "AVE biến kết quả: 0,494 (bài in 0,549)", C.accent2],
    ["Nghi vấn", "13 hệ số: SE chỉ 0,003–0,006, t = 26–44", C.accent1]];
  dong.forEach(([nhan, nd, mau], i) => {
    const y = 1.5 + i * 1.35;
    hop(s, 7.2, y, 5.5, 1.15);
    s.addText(nhan, { x: 7.4, y: y + 0.1, w: 5.1, h: 0.4, fontSize: 16, bold: true, color: mau, isTextBox: true, margin: 0 });
    s.addText(nd, { x: 7.4, y: y + 0.5, w: 5.1, h: 0.55, fontSize: 14, color: C.text1, isTextBox: true, margin: 0 });
  });
}

// ===== 8. Mô phỏng =====
{
  const s = slideMoi("Chạy lại trên dữ liệu mô phỏng 314 phiếu", "Dữ liệu sinh theo đúng tham số bài báo công bố. Q² và sai số chuẩn của hai đường bậc 2 trùng gần như tuyệt đối với bài: 0,064. Bên ngoài vẫn mạnh hơn nội bộ. Nhưng 13 hệ số của các nhóm, tính theo cách chuẩn, chỉ 0,03 đến 0,12 với t từ 4,6 đến 7,8; bài in t từ 26 đến 44. HTMT vượt 0,85 ở 3 cặp, trong đó có cặp quản lý dự án – nguồn lực.");
  anh(s, KQ("mp_so_sanh_he_so.png"), 0.5, 1.3, 7.6, 4.3);
  soLon(s, 8.4, 1.4, 2.1, "0,064", "SE bậc 2: trùng bài báo", C.accent3);
  soLon(s, 10.65, 1.4, 2.1, "0,87", "HTMT quản lý DA – nguồn lực", C.accent2);
  soLon(s, 8.4, 3.15, 2.1, "4,6–7,8", "t của 13 nhóm\n(bài báo: 26–44)", C.accent2);
  soLon(s, 10.65, 3.15, 2.1, "0,58", "R² (bài 0,72): suy giảm do sai số đo", C.accent1);
  gach(s, ["Kết luận định tính đứng vững: rủi ro bên ngoài mạnh hơn nội bộ",
    "Kết luận chi tiết H1–H13 không tái hiện được"], 0.6, 5.85, 12.1, 1.2, 16);
}

// ===== 9. Dữ liệu thật Aceh =====
{
  const s = slideMoi("Áp dụng quy trình trên dữ liệu thật công khai", `Bộ dữ liệu của Rauzana trên Mendeley Data, giấy phép CC BY, 68 nhà thầu ở Aceh chấm 60 nguyên nhân chậm trễ. Bài gốc chỉ làm thống kê mô tả; em chạy thêm RII và PLS-SEM như Kassem. Đọc dữ liệu khớp bài gốc. R² chỉ ${so(aceh.r2)}, β nội bộ ${so(aceh.bINT)}, bên ngoài ${so(aceh.bEXT)}. Ở bối cảnh ổn định hơn Yemen, kết quả khác hẳn bài báo.`);
  anh(s, KQ("aceh_rii_top10.png"), 0.5, 1.3, 6.9, 4.2);
  soLon(s, 7.7, 1.4, 2.4, "68 × 60", "nhà thầu × yếu tố (Rauzana, 2021)");
  soLon(s, 10.3, 1.4, 2.4, so(aceh.r2), "R² (Kassem: 0,72)", C.accent2);
  soLon(s, 7.7, 3.15, 2.4, so(aceh.bINT), "β nội bộ", C.accent3);
  soLon(s, 10.3, 3.15, 2.4, so(aceh.bEXT), "β bên ngoài", C.accent1);
  gach(s, [`Top RII: ${aceh.rii.map((r) => r.yeu_to.toLowerCase()).join("; ")}`,
    `Nhóm có ý nghĩa (p < 0,05): ${aceh.yNghia.length ? aceh.yNghia.join(", ") : "không nhóm nào"}`], 0.6, 5.75, 12.1, 1.3, 15);
}

// ===== 10. Thái Bình 2 =====
{
  const s = slideMoi("Ví dụ 1: Nhiệt điện Thái Bình 2 (PVN)", "Theo kết luận thanh tra năm 2020: tổng mức đầu tư tăng 32,7%, khánh thành 4/2023, chậm khoảng 7–8 năm, lãi vay phát sinh gần 82 triệu USD. Nguyên nhân gốc là rủi ro nội bộ: chỉ định thầu sai luật, tổng thầu EPC thiếu năng lực, điều chỉnh hợp đồng sai. Ngược với Yemen nơi rủi ro bên ngoài lấn át.");
  anh(s, KQ("bd_thai_binh_2.png"), 0.5, 1.3, 12.3, 4.5);
  gach(s, ["Nguyên nhân gốc là rủi ro nội bộ: chỉ định thầu sai luật (TC), tổng thầu thiếu năng lực (CO), chủ đầu tư (CL)",
    "Ngược với Yemen: kết quả của bài báo phụ thuộc mạnh vào bối cảnh; khung 13 nhóm thì dùng lại được"], 0.6, 5.95, 12.1, 1.2, 15);
}

// ===== 11. HTTT + Monte Carlo =====
{
  const s = slideMoi("Ví dụ 2: Dự án HTTT – bài học Healthcare.gov và Monte Carlo", "Healthcare.gov năm 2013: chi phí hệ thống tăng từ 56 lên hơn 209 triệu USD theo báo cáo GAO, do yêu cầu thay đổi, giao việc khi chưa rõ yêu cầu, giám sát lỏng. Em dựng dự án cổng dịch vụ mẫu trên MS Project và Excel, rồi mô phỏng Monte Carlo 10.000 lần: kế hoạch 90 ngày gần như không đạt; cần khoảng 128 ngày để có 80% khả năng hoàn thành. Ba rủi ro cần ưu tiên đều là bài học từ Healthcare.gov.");
  anh(s, KQ("mc_phan_phoi.png"), 0.5, 1.3, 7.3, 4.1);
  soLon(s, 8.1, 1.4, 2.25, "×3,7", "chi phí FFM: 56 → 209 triệu USD", C.accent2);
  soLon(s, 10.5, 1.4, 2.25, "0,1%", "xác suất xong đúng kế hoạch 90 ngày", C.accent2);
  soLon(s, 8.1, 3.15, 2.25, "128", "ngày – P80 khi có rủi ro", C.accent1);
  soLon(s, 10.5, 3.15, 2.25, "+38", "ngày dự phòng cần thiết", C.accent3);
  gach(s, ["Ưu tiên: chủ đầu tư thay đổi yêu cầu, tích hợp hệ thống cũ, đội ngũ thiếu kinh nghiệm",
    "Ma trận PIM chưa đủ: R4 ở vùng đỏ nhưng gần như không ảnh hưởng tiến độ (nằm ngoài đường găng)"], 0.6, 5.65, 12.1, 1.4, 15);
}

// ===== 12. Kế hoạch ứng phó =====
{
  const s = slideMoi("Từ phân tích đến hành động: kế hoạch ứng phó", "Cả 10 rủi ro hàng đầu đều ở vùng đỏ, nên cần thêm tiêu chí khả năng kiểm soát. Bốn rủi ro ngoài tầm kiểm soát chỉ có thể chuyển giao, báo cáo lên trên, lập dự phòng. Sáu rủi ro trong tầm kiểm soát, trong đó ba thuộc khả thi và thiết kế, chính là các quy trình lập kế hoạch của môn học.");
  const hang = [["Rủi ro", "Chiến lược", "Hành động chính"],
    ["Ước tính chi phí sai", "Giảm thiểu", "Ước tính 3 điểm, Monte Carlo, dự phòng P80; theo dõi CPI"],
    ["Chậm ra quyết định", "Giảm thiểu", "Ma trận RACI, thời hạn phê duyệt trong hợp đồng"],
    ["Hợp đồng không rõ", "Né tránh", "Mẫu hợp đồng chuẩn (FIDIC), rà soát pháp lý"],
    ["Bất ổn chính trị", "Chuyển giao", "Bảo hiểm rủi ro chính trị, điều khoản ổn định"],
    ["Chiến tranh", "Chuyển giao + chấp nhận", "Điều khoản bất khả kháng, kế hoạch tạm dừng"]];
  s.addTable(hang.map((r, i) => r.map((t) => ({ text: t, options: i === 0 ? { bold: true, color: C.background1, fill: { color: HEX.dk2 } } : {} }))),
    { x: 0.6, y: 1.45, w: 8.2, colW: [2.2, 2.0, 4.0], fontSize: 13, color: C.text1, border: { type: "solid", pt: 0.5, color: "CBD2D9" }, rowH: 0.62, valign: "middle" });
  soLon(s, 9.15, 1.45, 3.55, "10/10", "rủi ro hàng đầu nằm ở vùng đỏ", C.accent2);
  soLon(s, 9.15, 3.2, 3.55, "4/10", "ngoài tầm kiểm soát của dự án", C.accent1);
  s.addText("PM tác động được chủ yếu ở rủi ro nội bộ – nhất là ước tính chi phí, tiến độ, khả thi", { x: 0.6, y: 5.6, w: 12.1, h: 0.8, fontSize: 17, bold: true, color: C.accent3, isTextBox: true });
}

// ===== 13. Công cụ và quản lý dự án báo cáo =====
{
  const s = slideMoi("Công cụ đã dùng và quản lý chính quá trình làm báo cáo", "Mỗi công cụ trả lời một câu hỏi: Excel và PIM cho biết rủi ro nào quan trọng; PLS-SEM cho biết nhóm nào ảnh hưởng tới kết quả; MS Project và Monte Carlo cho biết cần dự phòng bao nhiêu. Em cũng dùng WBS, Gantt, sổ rủi ro để quản lý chính việc làm báo cáo; Gantt cho thấy trễ 22–25/10 và đã làm bù.");
  anh(s, KQ("gantt_bao_cao.png"), 6.6, 1.3, 6.2, 4.3);
  const cc = [["Excel", "RII, ma trận PIM, sổ rủi ro, kiểm tra công thức"],
    ["Python / R", "PLS-SEM, bootstrap, HTMT, mô phỏng – mã nguồn mở"],
    ["SPSS, SmartPLS", "Bài báo dùng – thương mại"],
    ["MS Project", "WBS, đường găng, baseline"],
    ["Monte Carlo", "P80, dự phòng tiến độ, độ nhạy"]];
  cc.forEach(([t, nd], i) => {
    const y = 1.45 + i * 1.0;
    hop(s, 0.6, y, 5.7, 0.85);
    s.addText(t, { x: 0.8, y: y + 0.08, w: 1.9, h: 0.7, fontSize: 15, bold: true, color: C.accent1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(nd, { x: 2.75, y: y + 0.08, w: 3.4, h: 0.7, fontSize: 13, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  });
  s.addText("Excel và Python cho kết quả trùng nhau ở cả 9 phép kiểm tra", { x: 6.6, y: 5.85, w: 6.2, h: 0.6, fontSize: 15, italic: true, color: C.text2, isTextBox: true });
}

// ===== 14. Phản biện =====
{
  const s = slideMoi("Đánh giá phản biện bài báo", "Điểm mạnh: kết hợp nhiều lớp phân tích, mẫu đủ lớn, khung 13 nhóm dùng lại được, phần tính toán cơ bản đúng. Hạn chế: không công bố dữ liệu, giá trị phân biệt không đạt, 13 giả thuyết không tái hiện được, dùng GoF, nhiều lỗi trình bày, cùng một dữ liệu đăng nhiều bài với cỡ mẫu không thống nhất, và chỉ áp dụng cho bối cảnh xung đột.");
  hop(s, 0.6, 1.45, 5.9, 4.3, "E3F1EC");
  s.addText([{ text: "Điểm mạnh", options: { bold: true, fontSize: 20, color: C.accent3, breakLine: true } },
    { text: "Kết hợp RII, PIM và PLS-SEM", options: { bullet: true, breakLine: true } },
    { text: "Mẫu 314 người, đúng đối tượng", options: { bullet: true, breakLine: true } },
    { text: "Khung 13 nhóm rủi ro dùng lại được", options: { bullet: true, breakLine: true } },
    { text: "Tính toán cơ bản đúng, mô hình bậc 2 nhất quán", options: { bullet: true } }],
    { x: 0.85, y: 1.65, w: 5.4, h: 3.9, fontSize: 17, valign: "top", color: C.text1, paraSpaceAfter: 8, isTextBox: true });
  hop(s, 6.8, 1.45, 5.9, 4.3, "F6E3E0");
  s.addText([{ text: "Hạn chế", options: { bold: true, fontSize: 20, color: C.accent2, breakLine: true } },
    { text: "Không công bố dữ liệu", options: { bullet: true, breakLine: true } },
    { text: "Fornell–Larcker không đạt, không báo cáo HTMT", options: { bullet: true, breakLine: true } },
    { text: "13 giả thuyết: t = 26–44 không tái hiện được", options: { bullet: true, breakLine: true } },
    { text: "Dùng GoF; nhiều lỗi trình bày, mâu thuẫn (H5, Q²)", options: { bullet: true, breakLine: true } },
    { text: "Cỡ mẫu không thống nhất giữa các bài (201/314/357)", options: { bullet: true, breakLine: true } },
    { text: "Chỉ đúng cho bối cảnh xung đột ở Yemen", options: { bullet: true } }],
    { x: 7.05, y: 1.65, w: 5.4, h: 3.9, fontSize: 17, valign: "top", color: C.text1, paraSpaceAfter: 8, isTextBox: true });
  s.addText("Dùng được kết luận tổng quát; kết luận cho từng nhóm rủi ro cần kiểm chứng lại trên dữ liệu khác",
    { x: 0.6, y: 6.0, w: 12.1, h: 0.7, fontSize: 17, bold: true, color: C.accent1, isTextBox: true });
}

// ===== 15. Kết luận =====
{
  const s = pres.addSlide({ masterName: "TOI_NOI_DUNG" });
  s.addText("Kết luận", { placeholder: "title" });
  s.addText([
    { text: "Kết luận chính của bài báo đứng vững: ở Yemen, rủi ro bên ngoài lấn át rủi ro nội bộ", options: { bullet: true, breakLine: true } },
    { text: "Kết luận chi tiết cho từng nhóm cần thận trọng: thiếu minh bạch phương pháp, nhiều mâu thuẫn", options: { bullet: true, breakLine: true } },
    { text: "Ở bối cảnh ổn định (Thái Bình 2, Healthcare.gov, Aceh), rủi ro nội bộ mới là nguyên nhân chính", options: { bullet: true, breakLine: true } },
    { text: "Người quản lý dự án cần đi tiếp tới ứng phó và dự phòng – đúng phần bài báo còn thiếu", options: { bullet: true } }],
    { placeholder: "body", paraSpaceAfter: 18 });
  s.addNotes("Tóm lại bốn ý chính. Cảm ơn thầy cô và các bạn đã lắng nghe.");
  sv++;
}

// ===== Hỏi đáp =====
{
  const s = pres.addSlide({ masterName: "TOI" });
  s.addText("Cảm ơn thầy cô và các bạn", { placeholder: "title" });
  s.addText("Câu hỏi và thảo luận\nMã nguồn và dữ liệu: github.com/DugnCon/Information-System-Project-Management", { placeholder: "body" });
}

const OUT = path.join(ROOT, "slides", "thuyet-trinh.pptx");
(async () => {
  await pres.writeFile({ fileName: OUT });
  if (process.env.APPLY_THEME) {                 // đường dẫn tới apply_theme.js để ghi màu chủ đề vào file
    const { applyTheme } = require(process.env.APPLY_THEME);
    await applyTheme(OUT, THEME);
  }
  console.log("Đã tạo", OUT, "–", sv, "slide nội dung (không tính bìa, hỏi đáp)");
})();
