# Ghi chú 04 – Các điểm mâu thuẫn, nghi vấn trong bài báo

Ghi lại để dùng cho phần phản biện (Chương 4) và để trả lời khi bị hỏi "bài báo có hạn chế gì". Mỗi điểm ghi kèm vị trí trong bài để kiểm tra lại.

## A. Về phương pháp

1. **Định nghĩa W trong công thức RII sai** (mục 3.2.2). W là tổng điểm chứ không phải trung bình. Đã kiểm chứng bằng CL1: 0.675 × 0.821 = 0.554 (xem ghi chú 02).

2. **Công thức GoF in thiếu dấu căn** (mục 4.3.6e). In là "R2 × AVE2", trong khi đúng phải là GoF = √(R² × AVE). Con số 0.638 thì tính đúng.

3. **Dùng GoF để kết luận mô hình phù hợp.** Henseler & Sarstedt (2013), chính là tài liệu [73] tác giả trích, đã chỉ ra GoF không phân biệt được mô hình đúng và mô hình sai trong PLS-SEM. Hair và cộng sự (2019) cũng khuyên không dùng.

4. **Không báo cáo HTMT**, chỉ dùng Fornell–Larcker và cross-loading. Theo Henseler, Ringle & Sarstedt (2015), Fornell–Larcker hay bỏ sót vấn đề về giá trị phân biệt. Các tương quan giữa nhóm trong Bảng 9 khá cao (nhiều cặp 0.75–0.87), nên rất cần kiểm tra HTMT.

5. **Cross-loading rất cao.** Ví dụ trong Bảng 10, câu EC1 có loading 0.886 với EC nhưng 0.809 với PO. Nhiều câu tải lên nhóm khác ở mức 0.7. Nghĩa là các nhóm rủi ro chồng lấn nhau khá nhiều.

6. **Không rõ 13 hệ số của các nhóm bậc 1 được ước lượng ra sao.** Mô hình có 2 bậc: 13 nhóm → nội bộ/bên ngoài → thành công, nên không có đường thẳng từ CL tới "thành công". Lúc đầu mình đoán β của từng nhóm = trọng số lên nhóm bậc 2 × β bậc 2. Nhưng tính thử (26/10) thì không khớp: bên nội bộ có tỷ lệ vượt 1 (MR 1.06), bên ngoài chỉ 0.23–0.35. Điểm chắc chắn là độ lệch chuẩn suy ra (β/t) của 13 nhóm chỉ 0.003–0.006, nhỏ hơn 10–20 lần so với 2 nhóm bậc 2 (0.064). Bài không giải thích. Cần đọc Sarstedt và cộng sự (2019) về higher-order constructs.

7. **Mọi giả thuyết đều p < 0.01**, kể cả nhóm có β nhỏ (CN 0.097). Với mô hình kiểu ở mục 6 thì gần như chắc chắn sẽ "có ý nghĩa", nên kiểm định này không nói lên nhiều điều.

8. **Kết luận nói "đã kiểm định bằng G*Power"** (mục 7), nhưng phần phương pháp không hề nhắc tới G*Power hay cách tính cỡ mẫu.

## B. Mâu thuẫn giữa các phần trong bài

9. **H5 vừa bị bác bỏ vừa được ủng hộ.** Mục 5.1 viết "SEM analysis does not support Hypothesis 5" (đấu thầu, hợp đồng). Nhưng Bảng 11 cho TC: β = 0.143, p < 0.001, và câu ngay sau lại nói "liên hệ đáng kể".

10. **Giá trị t trong phần thảo luận khác Bảng 11.** Phần thảo luận ghi CO t = 32.359, EC 44.850, PO 42.486, LP 33.260, EN 30.052, SE 40.252, FM 36.786. Không số nào khớp với Bảng 11.

11. **Q² bị gán lộn.** Mục 5.3 nói Q² của mô hình nội bộ là 0.527, bên ngoài 0.590. Kết luận lại nói 0.369 (ảnh hưởng rủi ro), 0.590 (nội bộ), 0.527 (bên ngoài). Đã kiểm chứng (26/10): SSO/314 = số câu của biến, nên dòng 0.590 có 20 câu (bên ngoài), dòng 0.527 có 31 câu (nội bộ). **Mục 5.3 đúng, Kết luận sai.** Dòng 0.369 có 4 câu, chứng tỏ biến kết quả thật sự đã bỏ 1 câu.

12. **Có H14, H15 nhưng không định nghĩa.** Mục 5.3 nhắc "H1 tới H7 và H14", "H8 tới H13 và H15", trong khi mục 2.2 chỉ có H1–H13. Đoán là H14 = nội bộ → thành công, H15 = bên ngoài → thành công.

13. **Lẫn nội bộ với bên ngoài.** Mục 4.3.6a viết "nhóm bị ảnh hưởng mạnh nhất bởi rủi ro bên ngoài là quản lý dự án, khả thi và thiết kế, nguồn lực". Ba nhóm này là **nội bộ**.

14. **R² = 0.720 lúc "cao" lúc "trung bình".** Bảng 12 ghi "High". Mục 5.3 phần nội bộ ghi "medium… gần với mức cao 0.67", tức là 0.72 > 0.67 mà vẫn gọi là trung bình.

15. **Loading biến kết quả.** Mục 5.3 nói "mọi loading > 0.7", nhưng Bảng 8 có 0.595 và 0.591. Tác giả nói bỏ EF3, nhưng vẫn in đủ 5 câu.

16. **EF3 xếp hạng 6 trên tổng số 5.** EF2 và EF3 cùng điểm trung bình 2.755.

17. **Mã không thống nhất.** Mục 5.1 gọi "CT3" trong khi Bảng 7 là "TC3". FM3 được gọi là "trong nhóm an ninh". FD4, FD5 được gọi là "trong nhóm tư vấn".

18. **β nhỏ mà vẫn gọi là "liên hệ mạnh".** CN 0.097 được mô tả là "strong link".

19. **Số người theo kinh nghiệm** cộng lại chỉ được 269/314. 45 người còn lại không được nhắc tới.

## B2. Phát hiện khi tính lại số liệu (26/10, chi tiết ở results/kiem-tra-so-lieu.md)

24. **Fornell–Larcker KHÔNG đạt ở nhóm RM.** Tương quan RM–MR = 0.845 > √AVE(RM) = 0.833. Bài báo kết luận tất cả đều đạt. CL cũng chỉ hơn ngưỡng 0.002. Đây là phát hiện mạnh nhất, vì chỉ cần dùng chính số liệu trong bài là thấy.

25. **AVE của biến kết quả không khớp với loading.** Từ 5 loading in trong Bảng 8 tính ra AVE 0.494, dưới ngưỡng 0.5. Bài in 0.549. Thử bỏ từng câu thì AVE cao nhất cũng chỉ 0.531, không lần nào ra 0.549.

26. **Không rõ AVE 0.566 trong công thức GoF lấy từ đâu.** Đã thử 6 cách lấy trung bình AVE, không cách nào ra 0.566. Nếu lấy trung bình 13 nhóm bậc 1 thì GoF ≈ 0.735.

27. **Mức tác động/xác suất ở Bảng 6 không khớp với RII ở Bảng 7.** Quy đổi RII theo thang chia đều 0.2 thì chỉ 3/6 rủi ro khớp. Ví dụ FD4 có RII tác động 0.717 và xác suất 0.793 (đều mức Cao), nhưng Bảng 6 ghi Rất cao – Rất cao. Lưu ý: cách quy đổi là giả định của mình, vì bài không nói.

28. **Những gì khớp:** RII tổng = tác động × xác suất (10/10 dòng), AVE và CR của 13 nhóm (13/13), √AVE trên đường chéo Bảng 9, Q² (3/3), con số GoF 0.638. Phần tính toán cơ bản đúng, chỗ có vấn đề là cách diễn giải và các chỉ số tổng hợp.

## C. Về trình bày và nguồn

20. Đoạn văn mục 2.3 và cuối mục 5.3 bị lặp nguyên văn. Nhiều hình, tiêu đề bị chồng chữ (ví dụ Hình 1, 4, 8, mục 3.1). Có dòng "FOR PEER REVIEW" còn sót trong bản chính thức.
21. Tài liệu [45] (cảm biến kiểm tra đường sắt) được trích cho nội dung "dự án lọc dầu ở Ấn Độ". Không liên quan.
22. Bảng 5, 6, 7 lấy từ các bài trước của chính nhóm tác giả ([38], [66]), nên phần "mới" của bài này chủ yếu chỉ là mô hình PLS-SEM.
23. Dữ liệu không công khai, nên người đọc không tự kiểm chứng được.

## Ý mình muốn nói khi thuyết trình

Không phải để "chê" bài báo. Ý chính: kết luận tổng quát (rủi ro bên ngoài như chính trị, kinh tế, an ninh lấn át rủi ro nội bộ ở Yemen) thì hợp lý với bối cảnh có chiến tranh. Nhưng các con số chi tiết không đủ tin cậy để dùng nguyên xi, vì vậy phần tái hiện của mình sẽ:
- tính lại những gì tính lại được từ số liệu đã công bố;
- chạy lại trên dữ liệu mô phỏng có thêm HTMT, và làm mô hình bậc 2 cho đúng cách.
