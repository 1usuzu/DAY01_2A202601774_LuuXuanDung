# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 14h00–18h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.7, 1.2 và 1.8 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Hà Nội."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi? Ở mức nào phản hồi bắt đầu
kém mạch lạc?** (2–3 câu)
> Temperature 0.0 trả lời khô khan. Tăng dần thì văn phong mượt mà và sáng tạo hơn. Khi lên mức 1.8, văn bản trở nên vô nghĩa, bịa đặt và lủng củng.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Hợp đồng: 0.0 (Cần chính xác tuyệt đối, không được bịa đặt).
> Slogan: 0.7 - 1.0 (Cần sáng tạo, linh hoạt, từ ngữ phong phú).

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> GPT-4o: Khoảng $300/ngày (dành cho logic phức tạp, code, suy luận sâu).
> GPT-4o-mini: Khoảng $12/ngày (dành cho chat cơ bản, FAQ, tóm tắt nhẹ).

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích máy học (machine learning) là gì?"** nhưng hai system prompt
khác nhau:
- "Bạn là một nhà thơ, trả lời mọi thứ bằng hình ảnh ví von, tránh thuật ngữ."
- "Bạn là kỹ sư phần mềm senior, trả lời chính xác, có ví dụ code khi phù hợp."

**Hai phản hồi khác nhau như thế nào (giọng văn, độ dài, mức kỹ thuật)?
Từ đó rút ra system prompt điều khiển được những khía cạnh nào của phản hồi?**
(3–4 câu)
> Nhà thơ: dài dòng, bay bổng, dùng từ tượng hình. Kỹ sư: ngắn gọn, đi thẳng vào kỹ thuật, có code.
> Rút ra: System prompt định hình được phong cách (tone), định dạng (format) và mức độ chuyên môn của AI.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Chênh lệch 50% - 100% vì tiếng Việt bị băm nhỏ hơn (1 từ có thể tốn 2 token).
> Dự toán sẽ bị THIẾU tiền vì thực tế số token AI tiêu thụ cao hơn dự tính.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Chatbot (a) và Trợ lý giọng nói (b) cực kỳ cần streaming để người/máy đọc ngay được chữ đầu tiên, giảm độ trễ. Dịch ngầm ban đêm (c) không cần vì không có người ngồi đợi (chỉ quan tâm tổng sản lượng).

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
> Giúp giãn cách lượng request, tránh việc tất cả cùng đập chung 1 lúc làm sập server lần nữa. Kỹ thuật "jitter" thêm vài mili-giây ngẫu nhiên để rải đều hẳn thời gian retry của các client.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> Prompt: "Bạn là trợ giảng, trả lời ngắn gọn."
> (1) Bỏ "trợ giảng": mất đi văn phong thân thiện, nhiệt tình.
> (2) Bỏ "ngắn gọn": bot sẽ trả lời lan man, dài dòng gây tốn token.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Tình huống: Chat tới lượt thứ 5 thì bot quên mất câu hỏi số 1 đang nói về chủ đề gì.
> Khắc phục: Dùng một model nhỏ chạy ngầm tóm tắt lại các đoạn chat cũ rồi dán tóm tắt đó vào System Prompt.

---

## Danh Sách Kiểm Tra Nộp Bài

- [x] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [x] Cả 4 checkpoint pytest đều pass
- [x] Tất cả 9 câu trong file này đã được trả lời
- [x] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
