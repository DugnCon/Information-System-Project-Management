# Kế hoạch làm báo cáo giữa kỳ

Bài báo: Kassem (2022), Risk Management Assessment in Oil and Gas Construction Projects Using PLS-SEM, tạp chí Gases 2(2), tr. 33–60.

Hạn nộp: thứ Tư 04/11/2026. Bắt đầu: Chủ nhật 18/10/2026, tức là còn 18 ngày.

Ngày nào cũng có việc và ngày nào cũng có ít nhất một commit. Commit cái gì thì phải đúng là cái đã làm hôm đó.

---

## Mấy điều phải nhớ trước khi làm

Cô chấm theo slide 52: nội dung 2.5, tái hiện thực nghiệm 2.5, ví dụ thực tế + mở rộng 2, thuyết trình 2, phản biện nhóm khác 1. Phần tái hiện thực nghiệm nặng điểm ngang phần lý thuyết nên không được để đến cuối mới làm.

Slide 54: mẫu KLTN, tối thiểu 20 trang ruột, xuất 1 file PDF (nên dùng LaTeX). Chữ trong bảng và hình phải là tiếng Việt. Công thức phải gõ lại và đánh số bên lề phải. Có trích dẫn đầy đủ, không lấy Wikipedia. Phải có phụ lục khai báo công cụ hỗ trợ đã dùng.

Tác giả không công bố dữ liệu gốc, chỉ ghi "liên hệ tác giả khi có yêu cầu hợp lý". Nên mình làm hai hướng song song:
- Hướng 1: lấy các con số đã in trong bài và tự tính lại xem có khớp không.
- Hướng 2: tự tạo bộ dữ liệu giả lập 314 phiếu rồi chạy lại toàn bộ quy trình. Trong báo cáo phải ghi rõ đây là dữ liệu mô phỏng.

Song song đó gửi mail xin dữ liệu thật. Có thì tốt, không có cũng không sao.

Công cụ chọn R + gói seminr để chạy PLS-SEM vì miễn phí, có bootstrapping và có HTMT (bài báo không báo cáo HTMT, mình thêm vào được thì đó là điểm mở rộng). Phần RII, PIM, vẽ biểu đồ làm bằng Python cho quen tay.

Những chỗ mình thấy đáng nghi trong bài báo, ghi lại để dùng cho phần phản biện:
- Bảng 11 có 15 đường dẫn nhưng phần giả thuyết chỉ có H1–H13. Phần thảo luận lại nhắc tới H14.
- Độ lệch chuẩn bootstrap chỉ 0.003–0.006 và giả thuyết nào cũng p < 0.001, đẹp quá mức bình thường.
- Bài dùng GoF để kết luận mô hình phù hợp, trong khi chính tài liệu [73] mà tác giả trích (Henseler & Sarstedt 2013) nói GoF không dùng được cho PLS.
- Có đoạn văn bị lặp nguyên văn, hình bị chồng chữ. Mấy lỗi này cho thấy khâu biên tập không kỹ.

---

## Lịch từng ngày

**CN 18/10 – T2 19/10** – Khởi động (thực tế bắt đầu repo ngày 19/10)
Tạo repo, đẩy PLAN.md, README.md và các thư mục trống (docs, data, src, results, report, slides). Đọc lướt toàn bộ bài báo một lượt, chưa cần hiểu hết. Gửi mail xin dữ liệu cho tác giả (mukhtarkas@gmail.com), lưu nội dung mail vào docs.
Commit: khởi tạo repo và kế hoạch

**T2 19/10** – Đọc phần 1, 2
Đọc kỹ phần Introduction và Research Background. Ghi chú bằng tiếng Việt vào docs/notes/01-tong-quan.md: bài toán là gì, tại sao lại là Yemen, 13 giả thuyết nói gì. Bắt đầu làm bảng thuật ngữ Anh–Việt.
Commit: ghi chú phần tổng quan, bảng thuật ngữ

**T3 20/10** – Đọc phần 3, phương pháp
Hiểu cho được RII và ma trận PIM. Tự lấy một ví dụ nhỏ (5 người chấm 1 rủi ro) rồi tính RII bằng tay, chụp hoặc gõ lại vào ghi chú. Với SEM/PLS-SEM, hôm nay chỉ cần hiểu biến tiềm ẩn, biến quan sát, mô hình đo lường và mô hình cấu trúc là gì.
Commit: ghi chú phương pháp RII, PIM, SEM

**T4 21/10** – Đọc phần 4–7, kết quả
Đọc bảng kết quả, ghi từng chỉ số (Cronbach, AVE, CR, R², f², Q², GoF) có nghĩa là gì và ngưỡng bao nhiêu. Ghi các điểm đáng nghi ở trên vào docs/notes/03-nhan-xet.md. Tìm và tải các tài liệu chính: PMBOK 7, ISO 31000:2018, sách A Primer on PLS-SEM (Hair và cộng sự), Henseler 2015 về HTMT.
Commit: ghi chú kết quả và danh sách tài liệu tham khảo

**T5 22/10** – Dựng khung báo cáo + nhập số liệu
Lấy mẫu KLTN của trường, dựng khung LaTeX gồm bìa, lời cam đoan, mục lục và 4 chương trống. Gõ bảng 6, 7 của bài báo thành file CSV trong data/published.
Commit: khung LaTeX, dữ liệu bảng 6 và 7

**T6 23/10** – Tính lại số liệu đã công bố (hướng 1)
Gõ tiếp các bảng 8, 9, 12, 13, 14. Viết script src/kiem_tra_so_lieu.py để tính lại RII tổng, xếp hạng, vùng PIM, GoF = √(R² × AVE), Q² = 1 − SSE/SSO, và kiểm tra Fornell–Larcker. Ghi lại chỗ nào khớp, chỗ nào lệch.
Commit: script kiểm tra lại số liệu bài báo

**T7 24/10** – Viết Chương 1
Viết về dự án và thành công dự án (thời gian, chi phí, chất lượng), rủi ro và quy trình quản lý rủi ro theo PMBOK và ISO 31000, đặc thù dự án dầu khí, các kỹ thuật quản lý rủi ro (dịch Bảng 1). Mục tiêu khoảng 5 trang.
Commit: viết chương 1

**CN 25/10** – Sơ đồ + đầu Chương 2
Vẽ sơ đồ tư duy toàn bộ chủ đề bằng draw.io (yêu cầu bắt buộc về biểu diễn trực quan). Vẽ lại mô hình 13 giả thuyết bằng tiếng Việt. Viết 2.1 RII và 2.2 PIM, có công thức đánh số.
Commit: sơ đồ tư duy, sơ đồ mô hình, mục 2.1–2.2

**T2 26/10** – Viết phần PLS-SEM
Viết 2.3 (SEM, so sánh CB-SEM với PLS-SEM), 2.4 (cách PLS-SEM chạy, bootstrapping, bảng tổng hợp chỉ số và ngưỡng), 2.5 (mô hình nghiên cứu của bài). Đây là phần khó nhất về lý thuyết, viết tới đâu phải giải thích được tới đó.
Commit: mục 2.3–2.5

**T3 27/10** – Dữ liệu mô phỏng (hướng 2)
Viết src/mo_phong.py sinh 314 phiếu Likert 1–5 cho 13 nhóm rủi ro và biến thành công dự án, có tương quan giữa các câu cùng nhóm. Chạy thống kê mô tả, Cronbach, RII, PIM. Vẽ ma trận nhiệt PIM.
Commit: sinh dữ liệu mô phỏng, chạy Cronbach/RII/PIM

**T4 28/10** – Chạy PLS-SEM
Chạy seminr trên dữ liệu mô phỏng. Mô hình đo lường: loading, AVE, CR, Fornell–Larcker, HTMT. Mô hình cấu trúc: bootstrapping 5000 lần, hệ số đường dẫn, R², f². Xuất bảng ra results/tables. Nếu còn sức thì cài bản dùng thử SmartPLS 4 chạy lại và chụp màn hình.
Commit: kết quả PLS-SEM trên dữ liệu mô phỏng

**T5 29/10** – Viết Chương 3
Viết quy trình tái hiện (có lưu đồ), kết quả hướng 1, kết quả hướng 2, bảng so sánh với bài báo và giải thích vì sao khác.
Commit: viết chương 3

**T6 30/10** – Ví dụ thực tế 1
Chọn một dự án dầu khí ở Việt Nam bị chậm tiến độ và đội vốn, ví dụ Nhà máy lọc dầu Nghi Sơn hoặc Nhiệt điện Thái Bình 2. Nguồn lấy từ kết luận thanh tra, báo cáo kiểm toán, báo chính thống và bài của Thuyet, Ogunlana & Dey (2007) về rủi ro dự án dầu khí Việt Nam. Đem rủi ro của dự án đó xếp vào 13 nhóm của bài báo xem có khớp không. Viết 4.1.
Commit: ví dụ thực tế 1

**T7 31/10** – Ví dụ thực tế 2 + mở rộng
Vì môn này là quản lý dự án HTTT nên ví dụ 2 lấy một dự án phần mềm cụ thể. Lập Risk Register, chấm xác suất và tác động, tính RII, đặt vào ma trận PIM. Chạy mô phỏng Monte Carlo cho tiến độ khi có các rủi ro top đầu (RiskyProject hoặc Python). Viết 4.2.
Commit: ví dụ thực tế 2 và Monte Carlo

**CN 01/11** – Mở rộng và phản biện
Viết 4.3 phản biện bài báo (các điểm đáng nghi ở trên, có trích dẫn). Viết 2.6 về ứng dụng, ưu điểm, hạn chế, xu hướng. Đếm số trang, nếu chưa đủ 20 trang ruột thì xem phần nào còn mỏng để bổ sung.
Commit: phần mở rộng, mục 2.6

**T2 02/11** – Hoàn thiện báo cáo
Viết mở đầu, kết luận, tóm tắt. Soát lại: chữ trong hình và bảng đã sang tiếng Việt chưa, công thức đã đánh số chưa, trích dẫn có đủ không. Viết phụ lục khai báo công cụ đã dùng. Xuất PDF.
Commit: bản báo cáo hoàn chỉnh lần 1

**T3 03/11** – Slide và tập nói
Làm tối đa 15 slide nội dung. Tập nói có bấm giờ đủ 15 phút. Soạn sẵn câu trả lời cho mấy câu dễ bị hỏi:
- RII khác điểm trung bình chỗ nào?
- Sao bài lại chọn PLS-SEM mà không chọn CB-SEM?
- R² = 0.72 nghĩa là gì?
- Sao f² của rủi ro bên ngoài lớn gấp 10 lần rủi ro nội bộ?
- Dữ liệu mô phỏng thì chứng minh được gì?
Commit: slide thuyết trình

**T4 04/11** – Nộp
Đọc lại PDF lần cuối, sửa lỗi chính tả, gắn tag v1.0 và nộp bài.
Commit: bản nộp cuối

---

## Nếu bị trễ

Bỏ theo thứ tự này: SmartPLS (giữ seminr là đủ), sau đó Monte Carlo (thay bằng phân tích định tính). Không bỏ hướng 2 (dữ liệu mô phỏng), không bỏ 2 ví dụ thực tế và sơ đồ tư duy, vì mấy phần này có trong barem.

Ghi chú phản biện cho các nhóm khác thì ghi vào docs/phan-bien.md sau mỗi buổi học, không cần đợi xong báo cáo.
