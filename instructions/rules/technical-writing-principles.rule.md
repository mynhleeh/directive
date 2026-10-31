---
trigger: glob
globs: "**/*.md, **/*.qmd, **/*.markdown"
description: "Bộ quy chuẩn 10 cương lĩnh phổ quát và khung kiểm định cơ học 2 lớp triệt tiêu văn phong AI cho mọi thể loại tài liệu kỹ thuật."
---

# Universal Technical Writing & Engineering Documentation Principles (Quy Chuẩn Biên Soạn Tài Liệu Kỹ Thuật Phổ Quát & Kỷ Luật Kiểm Soát AI)

Tài liệu này xác lập bộ quy chuẩn kỹ thuật bắt buộc áp dụng cho toàn bộ các thể loại tài liệu kỹ thuật định dạng Markdown trong kho lưu trữ. Phạm vi áp dụng bao trùm từ đặc tả yêu cầu, thiết kế hệ thống, bản ghi quyết định kiến trúc, đề xuất kỹ thuật (RFC), báo cáo thử nghiệm thực nghiệm, báo cáo điều tra sự cố (Postmortem/RCA), đặc tả giao diện lập trình cho đến cẩm nang vận hành hệ thống. Mọi tác nhân tự động hoặc kỹ sư khi tạo mới, cập nhật, tái cấu trúc hoặc nghiệm thu tài liệu bắt buộc phải tuân thủ nghiêm ngặt các điều khoản cơ học dưới đây nhằm triệt tiêu hoàn toàn các lỗi cố hữu của mô hình ngôn ngữ lớn: phong cách diễn đạt sáo rỗng, nhầm lẫn tầng trừu tượng, xung đột cú pháp bảng biểu, hoa mỹ học thuật giả tạo và mô hình hóa hình thức thiếu thực tế.

---

## 1. Bản Chất, Triết Lý Nền Tảng và Phổ Áp Dụng

### 1.1. Tính bất biến của quy chuẩn
Quy chuẩn này đóng vai trò hợp đồng kỹ thuật bất biến giữa người phát triển và mô hình ngôn ngữ. Mọi nội dung tài liệu kỹ thuật sinh ra phải đáp ứng đầy đủ các tiêu chuẩn cấu trúc, tính nhất quán ngữ nghĩa và cú pháp định lượng được xác định trong văn bản này. Tài liệu kỹ thuật không được phép vi phạm bất kỳ cổng kiểm định nào trong bảng kiểm định cơ học.

### 1.2. Triết lý Weak-Model-First và ranh giới đếm được
Mọi quy tắc trong tài liệu này được thiết kế theo nguyên lý cơ học và đếm được. Các ranh giới Đạt hoặc Không Đạt (Pass/Fail) dựa trên số đếm cụ thể, biểu thức chính quy và sự hiện diện của các mã định danh có cấu trúc. Hệ thống kiểm soát chất lượng không phụ thuộc vào cảm tính, văn phong chủ quan hay khả năng suy luận ngầm của mô hình ngôn ngữ. Một mô hình ngôn ngữ có năng lực tối thiểu cũng có thể thực thi và kiểm tra tính tuân thủ bằng các phép so khớp chuỗi cơ học.

### 1.3. Phổ áp dụng 8 thể loại tài liệu kỹ thuật chuẩn công nghiệp
Quy chuẩn áp dụng cho tất cả các tệp tài liệu văn bản kỹ thuật có phần mở rộng `.md`, `.qmd`, `.markdown` trong kho lưu trữ, được chuẩn hóa thành 8 thể loại chính:
1. **Tài liệu Đặc tả Yêu cầu (Software / Product Requirements Specification - SRS / PRD)**: Định nghĩa phạm vi bài toán, mục tiêu nghiệp vụ, ranh giới hệ thống, tác nhân ngoài, quy tắc nghiệp vụ bất biến và tiêu chí nghiệm thu định lượng.
2. **Tài liệu Thiết kế Kiến trúc & Hệ thống (Software / System Design Description - SDD / Arch Spec)**: Đặc tả cấu trúc thành phần, phân tầng, mô hình tương tác, giao thức kết nối, mô hình dữ liệu và phân tích điểm gãy tải.
3. **Bản ghi Quyết định Kiến trúc (Architecture Decision Records - ADR)**: Ghi lại bối cảnh kỹ thuật, các giải pháp thay thế đã đánh giá, nguyên nhân lựa chọn, các điểm đánh đổi chấp nhận và hệ quả kỹ thuật phát sinh.
4. **Đề xuất Kỹ thuật & Bản thảo Thiết kế (Request for Comments / Engineering Proposals - RFC)**: Đề xuất giải pháp hoặc thay đổi kỹ thuật mới, trưng cầu ý kiến phản biện từ cộng đồng kỹ sư trước khi phê duyệt triển khai.
5. **Báo cáo Kỹ thuật & Thực nghiệm (Technical Reports / Benchmarks / Evaluations)**: Báo cáo kết quả thử nghiệm tải, đo lường hiệu năng, khảo nghiệm giải pháp công nghệ hoặc đánh giá an ninh bảo mật.
6. **Báo cáo Phân tích Sự cố & Hậu kiểm (Incident Postmortems / Root Cause Analysis - RCA)**: Điều tra sự cố vận hành sản xuất, chuỗi thời gian diễn biến (Timeline), phân tích nguyên nhân gốc rễ và kế hoạch hành động khắc phục.
7. **Đặc tả Giao diện & Hợp đồng Dữ liệu (API Specifications / Data Schema Contracts)**: Đặc tả kỹ thuật chi tiết về các điểm cuối giao tiếp, cấu trúc gói tin, ràng buộc biên, định dạng dữ liệu và mã lỗi chuẩn.
8. **Cẩm nang Vận hành & Quy trình Thao tác Chuẩn (Runbooks / How-to Guides / SOP)**: Chuỗi mệnh lệnh thực thi tuần tự cho triển khai, cấu hình, sao lưu hoặc phục hồi dịch vụ kèm bước kiểm chứng và quy trình rollback.

---

## 2. Mười Cương Lĩnh Biên Soạn Phổ Quát

### 2.1 [U1]: Kỷ luật Ranh giới Mục đích & Tầng Trừu tượng (Purpose & Abstraction Layer Discipline)

Mọi tài liệu kỹ thuật phải xác định rõ mục đích tồn tại duy nhất và duy trì tính thuần khiết của tầng trừu tượng tương ứng:

1. Ranh giới tầng trừu tượng theo loại tài liệu:
- **Tầng Bài toán & Yêu cầu (SRS/PRD)**: Tập trung vào mục tiêu của người dùng và doanh nghiệp (CÁI GÌ - WHAT). Cấm tuyệt đối rò rỉ chi tiết thiết kế giải pháp (như cấu trúc lớp nội bộ, mẫu thiết kế GoF, kiến trúc phân tầng mã nguồn, tên bảng cơ sở dữ liệu vật lý) hoặc chi tiết mã nguồn vi mô (tên hàm của một thư viện ngôn ngữ lập trình cụ thể, tên các lớp ngoại lệ mã nguồn). Mọi lỗi và điều kiện biên phải được mô tả độc lập công nghệ dưới dạng thông điệp nghiệp vụ.
- **Tầng Giải pháp & Kiến trúc (SDD/Arch Spec)**: Tập trung vào cách thức hiện thực hóa (NHƯ THẾ NÀO - HOW). Cấm sao chép lại nguyên văn mô tả yêu cầu nghiệp vụ chi tiết; mọi thành phần kiến trúc bắt buộc phải dẫn chiếu bằng mã định danh yêu cầu.
- **Tầng Đánh giá & Báo cáo Thực nghiệm (Tech Report/Benchmark)**: Tập trung vào dữ liệu đo kiểm thực tế, giả thuyết kiểm thử, phương pháp luận thực nghiệm và kết luận phân tích. Cấm biến báo cáo thực nghiệm thành tài liệu quảng cáo giải pháp hoặc thuyết trình lý thuyết giáo trình.
- **Tầng Hậu kiểm Sự cố (Postmortem/RCA)**: Tập trung vào chuỗi dữ kiện thời gian khách quan, phân tích nguyên nhân gốc rễ (5 Whys / Fishbone) và biện pháp phòng ngừa. Cấm đưa ra các nhận định cảm tính quy kết cá nhân hoặc lý thuyết trừu tượng ngoài phạm vi sự cố.

2. Triệt tiêu hội chứng giáo trình hóa (Zero Textbook Syndrome):
Tài liệu kỹ thuật phục vụ mục đích bàn giao công việc giữa các kỹ sư và hội đồng chuyên môn thẩm định. Cấm viết theo phong cách giáo trình giảng dạy nhập môn đại học.
Cấm chèn các đoạn văn giảng giải phương pháp luận chung chung, thuyết trình định luật tâm lý học trừu tượng (như định luật Miller $7 \pm 2$, định luật Hick, định luật Conway), hoặc liệt kê danh sách nguyên lý triết học trước sơ đồ hoặc bảng dữ liệu. Tác giả phải đi thẳng vào bảng số liệu, thông số cấu hình, sơ đồ kỹ thuật và phân tích nghiệp vụ thực tế.

### 2.2 [U2]: Định vị Độc giả & Khung Chức năng Diataxis Mở Rộng (Audience Orientation & Functional Diataxis)

Tài liệu kỹ thuật phải phân loại chính xác nội dung vào đúng 4 góc phần tư của khung tài liệu Diataxis, phục vụ đúng nhu cầu nhận thức của độc giả tại từng ngữ cảnh:

1. Bốn góc phần tư chức năng:
- **Tutorials (Định hướng học tập)**: Dẫn dắt người đọc hoàn thành một chuỗi thao tác thực nghiệm từ trạng thái ban đầu đến khi tạo ra một kết quả mẫu hoạt động được. Văn phong dẫn dắt từng bước, giải thích kết quả tức thì.
- **How-to Guides / Runbooks (Định hướng mục tiêu thực tế)**: Cung cấp chuỗi chỉ dẫn chính xác để giải quyết một bài toán nghiệp vụ, triển khai hạ tầng hoặc khắc phục sự cố cụ thể đã phát sinh. Văn phong trực diện, mệnh lệnh, tập trung thao tác, giả định người đọc đã nắm vững khái niệm nền tảng.
- **Reference (Định hướng thông tin tra cứu)**: Cung cấp mô tả kỹ thuật chuẩn xác, đầy đủ và khô khan về các tham số, cấu hình, chữ ký hàm, điểm cuối API, mã lỗi và ràng buộc dữ liệu. Tuyệt đối không chứa lời bình luận hay hướng dẫn cài đặt bên ngoài.
- **Explanation / Technical Reports (Định hướng thấu hiểu kiến trúc & thực nghiệm)**: Làm rõ bối cảnh kỹ thuật, lý do lựa chọn công nghệ, phân tích đánh đổi kiến trúc hoặc công bố kết quả phân tích thực nghiệm sâu. Văn phong phân tích đa chiều, khách quan và khoa học.

2. Quy tắc phân tách Diataxis:
Cấm trộn lẫn nội dung của các góc phần tư trong cùng một đề mục. Không nhét bảng tham chiếu mã lỗi API vào giữa bài hướng dẫn học tập Tutorials; không chèn phân tích triết lý kiến trúc vào giữa tài liệu hướng dẫn vận hành How-to Guides / Runbooks.

3. Chuẩn mực văn phong kỹ sư chuyên nghiệp (Google Developer Documentation):
- **Giọng văn**: Giữ vai trò đồng nghiệp am hiểu chuyên môn (Knowledgeable Colleague). Thể hiện sự tôn trọng, chuyên nghiệp và khách quan, tránh giọng điệu kẻ cả hoặc giảng giải đạo lý.
- **Thể chủ động (Active Voice)**: Luôn đặt chủ ngữ thực hiện hành động ở vị trí rõ ràng. Tránh câu bị động làm ẩn đi tác nhân gây ra hành động (Ví dụ chuẩn: `Hệ thống xác thực mã khóa API trước khi chuyển tiếp yêu cầu`).
- **Thể mệnh lệnh (Imperative Mood) trong hướng dẫn thao tác**: Mọi câu chỉ dẫn quy trình phải bắt đầu bằng động từ hành động trực tiếp (Ví dụ chuẩn: `Khởi tạo phân vùng lưu trữ`, `Kiểm tra mã trạng thái trả về`).

### 2.3 [U3]: Kỷ luật Ngôn ngữ Đơn nhất & Triệt Tiêu Văn Phong Máy Cơ Học (Linguistic Purity & Anti-AI Tells)

1. Kỷ luật ngôn ngữ đơn nhất:
Trong tài liệu viết bằng ngôn ngữ mục tiêu (ví dụ tiếng Việt), cấm tuyệt đối việc chèn thuật ngữ tiếng Anh tương đương vào trong dấu ngoặc đơn ngay sau từ dịch.
- Ví dụ vi phạm: `Tổng quan (Overview)`, `Yêu cầu (Requirement)`, `Phân hệ (Subsystem)`, `Cấu hình (Configuration)`.
- Chuẩn hóa: Viết thuần ngôn ngữ mục tiêu rõ ràng: `Tổng quan`, `Yêu cầu`, `Phân hệ`, `Cấu hình`.
- Ngoại lệ: Bảng thuật ngữ chuyên dụng có cột ngôn ngữ gốc độc lập, hoặc các danh từ riêng chỉ công nghệ, giao thức chuẩn quốc tế không có từ dịch tương đương: `Kafka`, `Docker`, `PostgreSQL`, `gRPC`, `OAuth 2.0`.

2. Cấm tuyệt đối dấu gạch ngang dài làm ngắt câu:
Mô hình ngôn ngữ thường lạm dụng dấu gạch ngang dài (em-dash `—`) hoặc hai dấu gạch ngang liên tiếp (`--`) làm dấu ngắt câu hoặc giải thích ý phụ một cách lười biếng.
- Quy định cơ học: Số lượng ký tự `—` hoặc chuỗi `--` đóng vai trò gạch ngang ngắt câu, nằm ngoài mọi khối mã nội tuyến (inline code) và khối mã fenced, trong toàn bộ văn bản phải bằng 0.
- Chuẩn hóa: Thay thế bằng dấu chấm câu để tách câu đơn mạch lạc, dùng dấu phẩy, dùng dấu hai chấm để giải thích hoặc tái cấu trúc lại câu. (Lưu ý: Không cấm đường kẻ ngang bảng `|---|` hoặc cờ lệnh dòng lệnh `--verbose`).
- Ngoại lệ duy nhất: Ký tự em-dash nằm bên trong một khối mã nội tuyến (đánh dấu bằng cặp dấu backtick đơn `` `...` ``) dùng để bảo toàn nguyên văn tên riêng của một nguồn bên ngoài (ấn phẩm, tiêu chuẩn, tài liệu tham chiếu có em-dash trong tên chính thức) không tính vào ngưỡng cấm. Ví dụ trung lập: `` `Chuẩn tham chiếu XYZ — Ấn bản lần 2` `` được chấp nhận vì em-dash nằm trong khối mã nội tuyến; câu văn thân bài `Hệ thống xử lý nhanh — đáng tin cậy` vẫn vi phạm vì em-dash nằm ngoài khối mã.

3. Cấm mẫu câu tương phản giả (Not X but Y):
Cấm các mẫu câu sáo rỗng dạng: "Không chỉ là X mà còn là Y", "Không đơn thuần là X mà là Y", "Không dừng lại ở việc X mà còn mở ra Y".
Trình bày trực tiếp năng lực kỹ thuật, thông số đo đếm hoặc ràng buộc thực tế trong câu khẳng định ngắn gọn.

4. Cấm bộ ba tính từ hoặc vế câu song song cưỡng bức:
Cấm thói quen ghép 3 tính từ hoặc 3 vế câu cân xứng để tạo nhịp điệu giả tạo: "nhanh chóng, linh hoạt và chính xác", "an toàn, hiệu quả và đáng tin cậy", "scalable, robust, and reliable".
Chọn duy nhất 1 từ chuyên môn xác đáng phản ánh bản chất kỹ thuật, hoặc chuyển đổi thành bảng chỉ số định lượng có thể kiểm thử được.

5. Cấm bôi đậm đầu dòng máy móc:
Cấm khuôn mẫu tự động bôi đậm cụm từ đầu tiên ở mọi gạch đầu dòng danh sách trong phần thân văn bản: `- **Tiêu đề:** Nội dung diễn giải`.
Trình bày nội dung dưới dạng câu văn kỹ thuật đầy đủ, bảng dữ liệu chuẩn hóa hoặc tiểu mục đánh số thứ tự khi cần diễn giải cấu trúc phân cấp.

6. Cấm tóm tắt lặp tầng (Fractal Repetition):
Cấm đặt đoạn tóm tắt sơ lược ở đầu mục, diễn giải lại ở giữa mục và chèn thêm đoạn tổng kết lặp lại nguyên văn ý cũ ở cuối mục. Mỗi dữ kiện hoặc yêu cầu kỹ thuật chỉ được trình bày một lần duy nhất tại vị trí phân loại chuẩn xác nhất.

7. Bộ lọc từ vựng AI ba tầng:
- Tầng 1 (Cấm tuyệt đối, tần suất bằng 0): `delve`, `tapestry`, `landscape` (theo nghĩa bóng), `pivotal`, `foster`, `robust` (theo nghĩa bóng mơ hồ), `leverage` (động từ), `seamless`, `groundbreaking`, `game-changer`, `bức tranh tổng thể`, `đòn bẩy`, `toàn diện và sâu sắc`, `trực quan sinh động`, `chìa khóa vàng`.
- Tầng 2 (Cụm từ đệm sáo rỗng bị cấm): `như chúng ta đã biết`, `để đảm bảo tính toàn diện`, `dưới đây là nội dung chi tiết`, `tóm lại hệ thống sẽ mang lại`, `đóng vai trò then chốt`, `là giải pháp tối ưu hàng đầu`.
- Tầng 3 (Giới hạn mật độ từ nối trừu tượng): Các từ nối như `nhằm mục đích`, `qua đó`, `từ đó`, `thông qua việc`, `notably`, `furthermore` không được vượt quá mật độ 2 lần xuất hiện trên mỗi 500 từ.

8. Chuẩn từ khóa quy chuẩn RFC 2119 viết hoa không diễn giải thừa:
Sử dụng trực tiếp các từ khóa quy định mức độ bắt buộc theo chuẩn RFC 2119: `BẮT BUỘC` (`MUST`), `KHÔNG ĐƯỢC PHÉP` (`MUST NOT`), `NÊN` (`SHOULD`), `TÙY CHỌN` (`OPTIONAL`).
Cấm viết câu giảng giải quy ước (ví dụ cấm: `Theo chuẩn RFC 2119, từ BẮT BUỘC ở đây có nghĩa là...`). Đặt từ khóa trực tiếp vào câu quy tắc kỹ thuật.

### 2.4 [U4]: Kỹ Nghệ Định Danh Thực Thể Có Không Gian Tên (Structured Namespaced Identifiers - POLA)

1. Chuẩn hóa vị trí và cấu trúc mã định danh duy nhất:
Mọi phân mục chứa đối tượng có thể truy vết (yêu cầu nghiệp vụ, yêu cầu kỹ thuật, ca sử dụng, quyết định kiến trúc, giả thuyết thực nghiệm, phát hiện đo kiểm, sự cố vận hành, khuyến nghị) bắt buộc phải đặt mã định danh ngay sau số thứ tự đề mục, phân cách bằng dấu hai chấm `:`.
Cú pháp chuẩn: `### X.Y [UID]: [Tiêu đề chuẩn]`

2. Nguyên lý ít gây ngạc nhiên nhất (Principle of Least Astonishment - POLA) & Kỷ luật không gian tên:
Mọi mã định danh thực thể bắt buộc phải chứa không gian tên phân vùng phản ánh cấu trúc phân rã của hệ thống hoặc miền chủ đề: `[TIỀN TỐ LOẠI]-[MIỀN/PHÂN HỆ]-[SỐ THỨ TỰ]`.
- Cấm tuyệt đối đánh mã phẳng tuyến tính vô hồn không có namespace: Cấm dùng các tiền tố phẳng như `ID01`, `REQ01`, `UC01`, `RULE01`, `FIND01`. Đánh mã phẳng là dấu vết của bài tập lý thuyết rập khuôn và mô hình AI sinh danh sách tuần tự thiếu tư duy cấu trúc phân rã hệ thống.
- Bảng tiền tố định danh chuẩn hóa theo ngữ cảnh:
  - Yêu cầu & Quy tắc: `BR-[DOMAIN]-[NN]` (Business Rule), `REQ-[SUBSYS]-[NN]` (Requirement), `UC-[SUBSYS]-[NN]` (Use Case), `US-[SUBSYS]-[NN]` (User Story).
  - Kiến trúc & Quyết định: `CMP-[SUBSYS]-[NN]` (Component), `ADR-[NNN]` (Architecture Decision), `RFC-[NNN]` (Request for Comments).
  - Báo cáo & Thực nghiệm: `HYP-[TOPIC]-[NN]` (Hypothesis), `FIND-[TOPIC]-[NN]` (Finding), `REC-[TOPIC]-[NN]` (Recommendation), `MET-[TOPIC]-[NN]` (Metric).
  - Sự cố & Vận hành: `INC-[DATE]-[NN]` (Incident), `ACT-[TOPIC]-[NN]` (Action Item), `FAIL-[TOPIC]-[NN]` (Failure Mode).
- Quy tắc cấm vị trí: Cấm đặt mã định danh trong dấu ngoặc đơn ở cuối tiêu đề mục (ví dụ cấm: `### 3.1 Cân bằng tải phiên bản (REQ-NET-01)`).

3. Quy tắc tinh gọn tiêu đề cột bảng con:
Khi một bảng được đặt dưới một phân mục đã có định danh và ngữ cảnh rõ ràng, tiêu đề các cột trong bảng phải rút gọn tối đa, cấm lặp lại từ khóa danh mục cha.
- Bảng Tham số API: `| Tham số | Kiểu dữ liệu | Bắt buộc | Ràng buộc | Mặc định |` (Cấm lặp: `| Tên tham số API | Kiểu dữ liệu của tham số |`)
- Bảng Khuyến nghị / Hành động: `| Mã | Hành động | Người phụ trách | Thời hạn | Trạng thái |` (Cấm lặp: `| Mã hành động khuyến nghị |`)
- Bảng Chỉ số kiểm thử: `| Chỉ số | Ngưỡng mục tiêu | Kết quả đo | Đánh giá |`

### 2.5 [U5]: Phòng Vệ Cú pháp Đa Tầng & Kỹ Nghệ Markdown (Syntax Defense & Markdown Engineering)

1. Kỷ luật ký tự phân cách khi nhúng LaTeX trong bảng Markdown:
Trình phân tích Markdown sử dụng ký tự gạch đứng `|` để phân định cột trong bảng. Việc đặt ký tự `|` đơn lẻ bên trong công thức toán `$ ... $` sẽ phá vỡ cấu trúc bảng.
- Quy định cơ học: Số lượng ký tự `|` đơn lẻ bên trong khối toán học nằm trong bảng Markdown phải bằng 0.
- Quy tắc thay thế:
  - Giá trị tuyệt đối hoặc chuẩn vector: Sử dụng `\lvert ... \rvert` hoặc `\vert ... \vert`.
  - Điều kiện tập hợp hoặc xác suất có điều kiện: Sử dụng `\mid`.
  - Ký tự gạch đứng dạng văn bản thuần: Sử dụng thực thể HTML `&#124;`.

2. Chuẩn hóa khối lệnh mã nguồn và biểu đồ:
Cú pháp mở khối mã nguồn hoặc biểu đồ bắt buộc viết liền sau 3 dấu backticks, không có khoảng trắng giữa backticks và tên ngôn ngữ (```` ```mermaid ````, ```` ```json ````, ```` ```bash ````).
Làm sạch ký tự escape rác: Nghiêm cấm để sót các chuỗi ký tự thoát hiển thị thô như `\n\n`, `\r\n`, `\t` trong tệp tài liệu Markdown.
Cấm HTML-escape thực thể `&amp;`, `&lt;`, `&gt;` trong dòng tiêu đề Markdown (`^#{1,6}\s`). Trình tạo mục lục suy ra slug neo liên kết (anchor) trực tiếp từ văn bản tiêu đề thô; escape các ký tự này làm sai lệch slug so với tiêu đề hiển thị, khiến liên kết mục lục trỏ sai đích dù nội dung có vẻ "sạch" hơn.
- Quy định cơ học: Số dòng heading chứa `&amp;`, `&lt;`, hoặc `&gt;` phải bằng 0.
- Chuẩn hóa: Viết trực tiếp ký tự thô trong tiêu đề (`# Thiết kế API & Cổng dữ liệu`), không escape.

3. Chuẩn khối cảnh báo Admonition của GitHub Flavored Markdown:
Tài liệu chỉ sử dụng 5 loại khối cảnh báo chuẩn hóa theo cú pháp GFM Callout: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`.
Quy tắc bố cục: Cấm lồng ghép nhiều khối cảnh báo vào nhau. Cấm đặt hai khối cảnh báo liên tiếp mà không có nội dung phân cách.

### 2.6 [U6]: Trực Quan Hóa Phân Tầng, Nhất Quán Đa Phương Thức & Hướng Mục Tiêu (Tiered Visuals, Parity & Goal Semantics)

1. Kiến trúc phân tầng hai cấp độ:
Mọi hệ thống kỹ thuật phức tạp phải được phân rã thành hai cấp độ hiển thị tách biệt, cấm dồn tất cả các thành phần vào một sơ đồ duy nhất tạo thành cấu trúc mạng nhện:
- Tầng 1 (Tổng quan kiến trúc / Bối cảnh): Thể hiện ranh giới hệ thống, tương tác giữa tác nhân ngoài và các khối dịch vụ chính hoặc đường ống luồng dữ liệu cấp cao.
- Tầng 2 (Phân rã chi tiết luồng / Thành phần): Mô tả chi tiết nội bộ một phân hệ, sơ đồ tuần tự một giao thức, sơ đồ chuyển đổi trạng thái thực thể hoặc cây nguyên nhân gốc rễ sự cố.

2. Giới hạn tải nhận thức:
Số lượng nút trong một biểu đồ duy nhất không được vượt quá 9 nút. Khi phạm vi mô hình hóa vượt quá 9 nút, tác giả bắt buộc phải phân nhóm thành các cụm hoặc tách thành biểu đồ con phân tầng.

3. Mô hình hóa hướng mục tiêu hoàn chỉnh (Goal-Oriented Modeling):
Mọi đơn vị phân tích hành vi trong sơ đồ quy trình, sơ đồ ca sử dụng hoặc luồng nghiệp vụ phải thể hiện một mục tiêu hoàn chỉnh mang lại giá trị đo lường được:
- Cú pháp chuẩn hóa: `<Động từ hành động> + <Đối tượng trực tiếp>` (Ví dụ: `Quyết toán giao dịch`, `Xác thực chứng chỉ`, `Thu hồi phiên đăng nhập`).
- Triệt tiêu Anti-Pattern "CRUD Entity / God Entity": Cấm tuyệt đối việc gom cụm lười biếng toàn bộ các thao tác cơ bản vào một nút trừu tượng mang tên "Quản lý [Thực thể]" (`Quản lý tài khoản`, `Quản lý người dùng` / `Manage X`).
- Cấm biến sơ đồ thành chuỗi thao tác bấm nút giao diện: Cấm các nút dạng `Bấm nút Lưu`, `Nhập trường dữ liệu`, `Mở màn hình cấu hình`.

4. Kỷ luật ngữ nghĩa quan hệ trên sơ đồ:
Mối quan hệ giữa các nút trên sơ đồ (kể cả biểu đồ luồng, tuần tự hay ca sử dụng) phải phản ánh đúng logic thực tế:
- Cấm dùng quan hệ mở rộng (`<<extend>>` hoặc mũi tên rẽ nhánh tùy chọn) để nối hai kịch bản loại trừ lẫn nhau (mutually exclusive). Hai kịch bản loại trừ nhau phải được mô hình hóa thành hai luồng độc lập.
- Cấm dùng quan hệ bao hàm (`<<include>>`) để biểu diễn thứ tự các bước thao tác tuần tự thông thường.

5. Đồng bộ 100% giữa Sơ đồ và Văn bản (Zero Phantom Entities / Cross-Modal Parity):
Mọi thực thể, khối chức năng, mã ca sử dụng hoặc thành phần kiến trúc xuất hiện trên sơ đồ (kể cả các phân nhánh chi tiết) bắt buộc phải có phần văn bản mô tả, đặc tả hoặc phân tích tương ứng trong thân tài liệu.
Cấm tuyệt đối hiện tượng mô hình AI tự ý "vẽ thêm" các nút, nhánh con trên sơ đồ để lấp đầy hình vẽ mà không có nội dung tương ứng trong văn bản tài liệu.

6. Tính hữu ích thực tế của sơ đồ (Diagram Utility):
Sơ đồ trực quan phải giải quyết một bài toán nhận thức rõ ràng (làm rõ ranh giới phân quyền, luồng dữ liệu, máy trạng thái hoặc điểm gãy sự cố). Cấm vẽ các sơ đồ hình thức vô nghĩa (ví dụ: vẽ sơ đồ kết nối một tác nhân duy nhất tới tất cả các chức năng thực chất chỉ là vẽ lại Menu ứng dụng dạng đồ họa).

7. Công nghệ biểu diễn bản địa Mermaid:
Mọi biểu đồ luồng dữ liệu, kiến trúc thành phần, tuần tự và trạng thái phải được viết trực tiếp bằng mã nguồn Mermaid native trong khối code ```` ```mermaid ```` (`flowchart TD`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`). Tránh nhúng ảnh bitmap đối với tài liệu đang trong chu kỳ bảo trì.

### 2.7 [U7]: Đo Lường Định Lượng & Khép Kín Ma Trận Bằng Chứng (Quantitative Verification & Traceability Closure)

1. Tiêu chí đánh giá và kết luận định lượng:
Mọi yêu cầu phi chức năng, chỉ số chất lượng dịch vụ (SLO/SLA), phát hiện đo kiểm hiệu năng hoặc tiêu chí hoàn thành nhiệm vụ bắt buộc phải được xác lập bằng các con số định lượng kèm ngưỡng dung sai đo được.
Cấm sử dụng các tính từ cảm tính mơ hồ không có khả năng đo kiểm: `nhanh`, `mượt mà`, `bảo mật cao`, `dễ dùng`, `ổn định`, `tối ưu`.
Chuẩn hóa các chỉ số kỹ thuật định lượng:
- Hiệu năng xử lý: `Thời gian phản hồi P99 <= 150ms tại mức tải 2.000 RPS`.
- Tính sẵn sàng: `Tỷ lệ sẵn sàng dịch vụ đạt >= 99.95% tính trên chu kỳ 90 ngày`.
- Mức độ tin cậy dữ liệu: `Dung sai sai số tính toán = 0.00; sai lệch đối soát = 0 đơn vị`.
- Khả năng chịu lỗi: `Thời gian phục hồi dịch vụ (RTO) <= 30 giây; điểm khôi phục dữ liệu (RPO) = 0`.

2. Khép kín ma trận bằng chứng và truy vết hai chiều:
Tài liệu kỹ thuật phải bảo đảm chuỗi mắt xích lập luận khép kín hai chiều 100% phù hợp với loại tài liệu:
- Trong tài liệu đặc tả phần mềm: `Mục tiêu kinh doanh <-> Quy tắc nghiệp vụ <-> Yêu cầu chức năng <-> Kịch bản kiểm thử`.
- Trong báo cáo thử nghiệm / thực nghiệm: `Giả thuyết kiểm thử <-> Tham số môi trường <-> Số liệu đo đạc thực tế <-> Phân tích phương sai <-> Kết luận kiến nghị`.
- Trong báo cáo điều tra sự cố: `Triệu chứng cảnh báo <-> Chuỗi thời gian diễn biến <-> Bằng chứng log/metrics <-> Nguyên nhân gốc rễ <-> Hành động khắc phục`.
Không chấp nhận bất kỳ yêu cầu, phát hiện hay hành động khắc phục nào mồ côi (không có nguồn gốc dữ liệu bảo trợ hoặc không có đầu ra kiểm chứng).

### 2.8 [U8]: Tuyên Ngôn Luận Điểm, Tương Xứng Độ Chặt Chẽ & Hiện Thực Hóa Đánh Đổi (Thesis, Proportional Rigor & Trade-Off Realism)

1. Tuyên ngôn luận điểm kỹ thuật (Technical Thesis Statement):
Mọi tài liệu kiến trúc, đề xuất kỹ thuật (RFC), sách trắng hoặc báo cáo khảo sát hệ thống bắt buộc phải mở đầu bằng một tuyên ngôn luận điểm kỹ thuật ngắn gọn:
Xác định rõ ràng: Tài liệu này bảo vệ giải pháp gì, tối ưu hóa cho bài toán nào, hoạt động trong điều kiện biên tải trọng nào, và chấp nhận những ràng buộc giới hạn nào.

2. Nguyên lý Tương xứng của Độ chặt chẽ (Principle of Proportional Rigor):
Công cụ biểu đạt kỹ thuật và toán học phải tương xứng với bản chất độ phức tạp thực tế của bài toán:
- Triệt tiêu sự chặt chẽ giả tạo (Spurious Precision / Academic Ornamentation): Cấm lạm dụng toán vị từ cấp một ($\forall, \exists, \exists!$), ký hiệu tập hợp hàn lâm hoặc phương trình đại số triệt tiêu tầm thường chỉ để diễn đạt các logic đời thường hiển nhiên. Trình bày trực tiếp bằng câu văn khẳng định ngắn gọn hoặc bảng điều kiện số học.
- Bảo vệ tính chính xác toán học thực thụ: Khi tài liệu giải quyết các bài toán phức tạp thực sự (mô hình hóa rủi ro, phân tích độ phức tạp thuật toán, thiết kế giao thức mật mã, xác minh hình thức formal verification), tác giả bắt buộc phải trình bày công thức toán học và chứng minh chặt chẽ theo chuẩn IEEE/ACM.

3. Hiện thực hóa các điểm đánh đổi kỹ thuật (Trade-Off Realism & Breaking Point):
Cấm mô tả một giải pháp kỹ thuật là hoàn hảo toàn diện, đáp ứng tất cả các tiêu chí mà không có nhược điểm. Mọi đề xuất kiến trúc hoặc giải pháp bắt buộc phải công khai phân tích tối thiểu 3 trục đánh đổi thực tế:
- Độ trễ so với Chi phí bộ nhớ hoặc Băng thông mạng.
- Tính nhất quán dữ liệu so với Tính sẵn sàng vận hành (CAP / PACELC).
- Tốc độ phát triển tính năng so với Độ phức tạp vận hành và Chi phí bảo trì.
Xác định điểm gãy tải (Breaking Point): Ngưỡng tải trọng, dung lượng dữ liệu hoặc kích thước cụm mà tại đó kiến trúc hiện tại sẽ bắt đầu suy giảm hiệu năng và bắt buộc phải tái cấu trúc hoặc nâng cấp.

### 2.9 [U9]: Tính Độc Lập Tự Thân, Ngôi Thứ Ba Khách Quan & Triệt Tiêu Lặp Ngữ Cảnh (Document Self-Containment, Neutral 3rd-Person & Context Deduplication)

Mọi tài liệu kỹ thuật phải là một thực thể độc lập tự bảo chứng, sử dụng ngôi thứ ba khách quan phi cảm xúc và triệt tiêu toàn bộ hiện tượng lặp lại ngữ cảnh dư thừa giữa các phân mục:

1. Kỷ luật tài liệu đứng độc lập tự thân (Document Self-Containment):
Mỗi tài liệu kỹ thuật phải giải quyết trọn vẹn và độc lập bài toán trong phạm vi và tầng trừu tượng được giao.
- Cấm tuyệt đối hiện tượng đùn đẩy trách nhiệm đặc tả sang tài liệu ngoại thân trong phần thân văn bản: Cấm các câu dạng "Chi tiết thuật toán tham khảo tài liệu Thiết kế Chi tiết", "Quy trình này tuân theo tài liệu BRD", "Xem thêm trong tài liệu hướng dẫn sử dụng".
- Quy tắc cô lập mục tham khảo ngoại thân: Tài liệu CHỈ ĐƯỢC PHÉP đề cập đến tài liệu khác khi có yêu cầu tường minh từ người dùng hoặc theo quy chuẩn cấu trúc bắt buộc của thể loại (như mục References trong IEEE SRS). Khi có yêu cầu, toàn bộ các dẫn chiếu phải được cô lập 100% trong mục riêng biệt mang tên `## Tài liệu tham khảo` (References / Normative References). Cấm rò rỉ lời dẫn chiếu rải rác trong các chương mục thân bài.
- Quy định cơ học: Số câu dẫn chiếu tài liệu khác nằm ngoài mục `## Tài liệu tham khảo` phải bằng 0.

2. Ngôi thứ ba khách quan và văn phong kỹ thuật trung tính:
Tài liệu kỹ thuật phản ánh sự vận hành của máy móc và logic hệ thống, không phải bài luận cá nhân hay thông điệp tiếp thị.
- Ngôi thứ ba định danh rõ ràng: 100% chủ ngữ phải là thực thể kỹ thuật danh xưng xác định (`Hệ thống`, `Dịch vụ`, `Mô-đun`, `Bộ điều phối`, `Người vận hành`, `The system`, `The operator`). Riêng tài liệu quy trình thao tác và cẩm nang vận hành (Runbook/SOP) sử dụng thể mệnh lệnh không chủ ngữ (`Khởi tạo phân vùng...`, `Kiểm tra mã trạng thái...`).
- Triệt tiêu đại từ nhân xưng ngôi 1 và ngôi 2: Cấm tuyệt đối việc sử dụng các từ: `chúng tôi`, `chúng ta`, `tôi`, `bạn`, `quý vị`, `we`, `us`, `our`, `I`, `you` ngoài các khối trích dẫn nguyên văn hoặc khối mã nguồn.
- Tính trung tính tuyệt đối: Cấm toàn bộ các tính từ hoặc trạng từ biểu cảm, khen ngợi, phán xét chủ quan (`tuyệt vời`, `ưu việt`, `hoàn hảo`, `đáng tiếc`, `dễ dàng`, `fantastic`, `unfortunately`, `superior`, `convenient`). Mọi đánh giá chất lượng phải được quy đổi thành chỉ số kỹ thuật hoặc cặp trạng thái nhị phân: `Đạt` hoặc `Không Đạt` (Pass/Fail).

3. Kế thừa ngữ cảnh tĩnh và triệt tiêu lặp ngữ cảnh dư thừa (Context Deduplication):
Mô hình AI thường mắc tật lặp lại bối cảnh hệ thống hoặc mục tiêu vĩ mô ở phần mở đầu của mỗi phân mục con.
- Nguyên lý kế thừa ngữ cảnh: Các phân mục con (cấp 2 `## X.Y`, cấp 3 `### X.Y.Z`) mặc định kế thừa 100% bối cảnh đã xác lập ở phân mục cha. Cấm tuyệt đối viết lại tên hệ thống, mục tiêu dự án hay định nghĩa miền bài toán trong phần mở đầu của các đề mục con.
- Cấm câu dẫn đường thừa thãi (Throat-Clearing Preambles): Cấm các câu đệm trước bảng biểu hoặc sơ đồ dạng: `Nhằm đảm bảo bối cảnh đã nêu ở trên, dưới đây là bảng...`, `Trong bối cảnh hệ thống cần mở rộng như đề cập ở mục 1, phân hệ này...`.
- Vào đề trực diện: Mọi phân mục con phải bắt đầu trực tiếp bằng câu khẳng định về thông số kỹ thuật, cấu trúc thực thể, ràng buộc biên hoặc bảng dữ liệu cục bộ.
- Quy định cơ học: Số câu lặp lại bối cảnh hệ thống cha tại các phân mục con phải bằng 0.

### 2.10 [U10]: Kỷ Luật Phân Tích Tác Động Toàn Diện, Chống Hồi Quy & Bảo Toàn Giá Trị Tối Ưu (End-to-End Impact Analysis, Regression Prevention & Value Preservation)

Mọi thao tác sửa đổi, bổ sung thông tin, vá lỗi hoặc tái cấu trúc văn bản kỹ thuật và hệ thống không bao giờ được tiến hành một cách cục bộ, chắp vá:

1. Khảo sát bán kính ảnh hưởng toàn diện (End-to-End Blast Radius Audit):
Khi nhận yêu cầu cập nhật hoặc sửa chữa bất kỳ thông tin nào, tác giả bắt buộc phải truy vết toàn bộ luồng tác động từ đầu đến cuối dự án:
- Truy vết xuyên suốt chuỗi phụ thuộc: Kiểm tra tác động dây chuyền từ mục tiêu nghiệp vụ, yêu cầu chức năng, mô hình dữ liệu, sơ đồ kiến trúc, điểm gãy tải đến kịch bản kiểm thử và các tài liệu liên quan.
- Đánh giá đa chiều: Lập ma trận đánh giá rủi ro kéo theo về hiệu năng vận hành, độ trễ, tính nhất quán logic, tính bảo mật và khả năng tương thích ngược.

2. Kỷ luật bảo toàn giá trị tối ưu và chống suy thoái hồi quy (Value Preservation & Anti-Regression):
Tuyệt đối không để xảy ra tình trạng "càng sửa càng sai" hoặc sửa điểm này làm hỏng điểm khác:
- Bảo tồn thành phần đã tối ưu: Giữ nguyên vẹn toàn bộ các khối kiến trúc tối ưu, các chỉ số định lượng khắt khe, bảng dung sai đo lường và các thuật toán đã hoạt động ổn định. Nghiêm cấm việc hạ thấp tiêu chuẩn kỹ thuật hoặc thay thế thiết kế tối ưu bằng giải pháp sơ sài chỉ để giải quyết một lỗi cục bộ.
- Nâng cấp có chọn lọc: Chỉ tập trung cải tiến, tái cấu trúc hoặc thay thế các điểm cũ, các điểm sai lệch hoặc chưa đáp ứng đúng yêu cầu của người dùng.

3. Cơ chế hội chẩn và thống nhất giải pháp (Deliberative Alignment Gate):
Khi việc sửa đổi tiềm ẩn rủi ro phá vỡ tính nhất quán tổng thể hoặc phát sinh các điểm đánh đổi lớn:
- Chủ động dừng lại để phân tích và lập bảng đối chiếu các phương án khắc phục (ưu điểm, nhược điểm, rủi ro phụ thuộc kéo theo).
- Trình bày công khai các điểm đánh đổi kỹ thuật và thảo luận với người dùng để đạt được sự thống nhất về mặt giải pháp trước khi thực thi việc sửa đổi.
- Quy định cơ học: Số lỗi hồi quy logic hoặc gãy liên kết phụ thuộc phát sinh sau sửa đổi bằng 0; 100% các thành phần tối ưu sẵn có được bảo toàn nguyên vẹn.

---

## 3. Bảng Đối Chiếu Thực Thi Toàn Diện

| Danh mục kiểm soát | Lỗi AI cấm hoặc cần tránh | Chuẩn mực thay thế | Cơ chế đếm được (Pass/Fail) |
|---|---|---|---|
| Ranh giới tầng trừu tượng | Nhồi nhét chi tiết mã nguồn vi mô, tên hàm thư viện, class ngoại lệ vào tài liệu yêu cầu hoặc kiến trúc cấp cao. | Mô tả hành vi độc lập công nghệ; chi tiết cài đặt chuyển sang tài liệu thiết kế module hoặc mã nguồn. | Số từ khóa thiết kế pha sau, hàm mã nguồn hoặc exception trong tài liệu tầng cao bằng 0. |
| Độ tương xứng chặt chẽ | Lạm dụng toán vị từ hình thức ($\forall, \exists!$) hoặc đẳng thức triệt tiêu cho logic đời thường hiển nhiên. | Trình bày trực tiếp quy tắc bằng câu khẳng định kỹ thuật rõ ràng hoặc bảng điều kiện số học. | Số đoạn văn lạm dụng toán vị từ hình thức cho logic thông thường bằng 0. |
| Thuyết giảng lý thuyết | Giảng giải định luật Miller $7 \pm 2$, định luật Conway hoặc nguyên lý giáo trình đại học trước bảng số liệu/sơ đồ. | Trình bày trực tiếp sơ đồ kèm bảng dữ liệu nghiệp vụ và thông số kỹ thuật thực tế. | Số đoạn văn thuyết giảng lý thuyết phương pháp luận bằng 0. |
| Khung Diataxis và giọng văn | Trộn lẫn bảng mã lỗi tra cứu vào bài học nhập môn; dùng câu bị động mơ hồ: Dữ liệu được ghi nhận bởi hệ thống. | Tách bạch 4 góc phần tư Diataxis; dùng câu chủ động: Dịch vụ lưu trữ ghi nhận dữ liệu vào cơ sở dữ liệu. | 100% tài liệu định vị đúng 1 góc phần tư Diataxis; số câu bị động thiếu chủ ngữ bằng 0. |
| Không gian tên định danh | Đánh mã phẳng vô hồn không namespace: ID01, REQ01, UC01, FIND01. | Phân cấp mã định danh theo miền/phân hệ: REQ-NET-01, FIND-PERF-01, ADR-004. | Số mã định danh phẳng không có tiền tố phân hệ/miền bằng 0. |
| Vị trí mã định danh UID | Đặt UID ở cuối tiêu đề trong ngoặc đơn: Tiêu đề mục (REQ-AUTH-01). | Đặt UID ngay sau số thứ tự mục: 3.1 REQ-AUTH-01: Tiêu đề mục. | 100% tiêu đề phân mục có mã định danh tuân thủ cú pháp `### X.Y [UID]: [Tên]`. |
| Mô hình hóa hướng mục tiêu | Đặt tên gom cụm CRUD: Quản lý ví, Quản lý tài khoản, Quản lý giao dịch (Manage X). | Tên thực thể/quy trình là mục tiêu cụ thể: Tạo tài khoản, Chuyển tiền nội bộ, Quyết toán nợ. | Số ca sử dụng hoặc quy trình mang tên "Quản lý..." hoặc "Manage..." bằng 0. |
| Kỷ luật quan hệ sơ đồ | Dùng quan hệ mở rộng để nối hai kịch bản loại trừ nhau; dùng bao hàm cho chuỗi bước tuần tự. | Quan hệ mở rộng chỉ dùng cho nhánh tùy chọn tại extension point; các nhánh loại trừ tách kịch bản độc lập. | Số quan hệ mở rộng áp dụng cho hai luồng loại trừ nhau bằng 0. |
| Đồng bộ Sơ đồ - Văn bản | Tự ý vẽ thêm các nút, nhánh con trên sơ đồ Mermaid mà thân tài liệu không hề mô tả. | 100% nút và mã định danh trên sơ đồ phải có mục mô tả hoặc đặc tả tương ứng trong thân tài liệu. | Số phần tử trên sơ đồ không có văn bản đặc tả tương ứng bằng 0. |
| Đối xứng cơ học 1:1 | Ép đối xứng 1:1 máy móc giữa các phân hệ tĩnh và các luồng hành vi động của người dùng. | Tách bạch cấu trúc tĩnh và hành vi động; quy trình người dùng được phép tương tác xuyên suốt nhiều khối. | Số trường hợp ép đối xứng cơ học 1:1 cấu trúc - hành vi bằng 0. |
| Luồng rẽ nhánh ca quy trình | Luồng rẽ nhánh biến thành menu chuyển sang bấm xem, sửa, xóa chức năng khác. | Luồng rẽ nhánh là nhánh thay thế để đạt cùng mục tiêu hoặc luồng phục hồi lỗi trong hành trình. | Số luồng rẽ nhánh biến thành menu chuyển chức năng CRUD bằng 0. |
| Song ngữ cưỡng bức | Chèn chú thích tiếng Anh song song: Cấu hình (Configuration), Loại (Type), Trạng thái (Status). | Dùng từ ngữ mục tiêu chuẩn xác: Cấu hình, Loại, Trạng thái. | Số cặp ngoặc đơn chứa từ tiếng Anh song hành ngay sau từ tiếng Việt bằng 0. |
| Dấu gạch ngang dài làm ngắt câu | Dùng dấu em-dash hoặc hai dấu gạch ngang liên tiếp để ngắt câu hoặc giải thích ý phụ. | Tách thành các câu đơn bằng dấu chấm câu, dấu phẩy, dấu hai chấm hoặc viết lại câu. Ngoại lệ: em-dash trong khối mã nội tuyến bảo toàn tên riêng nguyên văn của nguồn bên ngoài. | Số ký tự em-dash hoặc chuỗi double hyphen làm dấu ngắt câu, nằm ngoài khối mã nội tuyến/fenced, bằng 0. |
| Escape HTML phá anchor tiêu đề | Escape `&`, `<`, `>` thành `&amp;`, `&lt;`, `&gt;` trong dòng tiêu đề Markdown, làm lệch slug neo liên kết mục lục so với tiêu đề hiển thị. | Viết trực tiếp ký tự thô trong tiêu đề: `# Thiết kế API & Cổng dữ liệu`. | Số dòng heading chứa `&amp;`, `&lt;`, hoặc `&gt;` bằng 0. |
| Mẫu câu tương phản giả | Viết: Hệ thống không chỉ là công cụ lưu trữ mà còn là giải pháp đột phá nâng tầm vận hành. | Trình bày trực diện: Hệ thống lưu trữ và đồng bộ hồ sơ khách hàng giữa các chi nhánh. | Số câu chứa cấu trúc tương phản giả Not X but Y bằng 0. |
| Bộ ba tính từ sáo rỗng | Ghép 3 tính từ đi liền: nhanh chóng, an toàn và minh bạch; accurate, robust, and scalable. | Chọn duy nhất 1 từ kỹ thuật chuẩn xác hoặc lập bảng chỉ số định lượng kiểm thử. | Số cụm 3 tính từ hoặc 3 vế câu song song bằng 0. |
| Bôi đậm đầu dòng tự động | Mọi dòng gạch đầu dòng đều bôi đậm máy móc cụm từ đầu tiên. | Trình bày câu văn kỹ thuật liền mạch hoặc dùng bảng dữ liệu chuẩn hóa. | Số gạch đầu dòng bắt đầu bằng cú pháp bôi đậm bằng 0. |
| Từ vựng AI tầng 1 | Dùng các từ: delve, tapestry, landscape, pivotal, foster, robust, leverage, bức tranh tổng thể, đòn bẩy. | Dùng thuật ngữ kỹ thuật chuyên ngành: phân tích, liên kết, bối cảnh, cơ chế, kiến trúc, kiểm thử. | Quét danh sách từ khóa Tier 1; tần suất xuất hiện bằng 0. |
| Ký tự phân cách trong toán bảng | Đặt ký tự gạch đứng trần trong công thức toán nằm ở bảng Markdown. | Dùng lệnh LaTeX thay thế: `\lvert`, `\rvert` hoặc `\mid`. | Số ký tự gạch đứng trần nằm trong khối toán của bảng Markdown bằng 0. |
| Khối mã lệnh và escape rác | Viết khoảng trắng sau backticks hoặc để sót chuỗi escape hiển thị thô dạng ký tự thoát dòng và tab. | Viết liền mạch không khoảng trắng và làm sạch toàn bộ chuỗi ký tự thoát rác. | Số khối lệnh có khoảng trắng sau backticks bằng 0; số chuỗi escape rác bằng 0. |
| Tiêu đề cột bảng con lặp từ | Lặp lại từ khóa danh mục ở hàng tiêu đề: Mã quy tắc, Tên quy tắc, Nội dung quy tắc. | Rút gọn tiêu đề cột tối đa: Mã, Tên, Nội dung, Ghi chú. | Số cột lặp lại từ khóa danh mục của phân mục cha bằng 0. |
| Biểu đồ chứa nút bấm giao diện | Vẽ quy trình: Bấm nút Lưu, Nhập mật khẩu, Mở màn hình chỉnh sửa. | Quy trình là mục tiêu nghiệp vụ hoàn chỉnh: Ghi nhận giao dịch, Xác thực định danh. | 100% tên bước là động từ nghiệp vụ; số thao tác giao diện bằng 0. |
| Tiêu chí nghiệm thu định tính | Viết tiêu chí chung chung: Hệ thống chạy nhanh, Giao diện thân thiện, Bảo mật tối đa. | Xác định chỉ số định lượng: P95 latency nhỏ hơn hoặc bằng 200ms tại 1.000 RPS. | 100% tiêu chí NFR và DoD có chỉ số định lượng kèm ngưỡng chấp thuận cụ thể. |
| Giải pháp hoàn hảo không đánh đổi | Khẳng định giải pháp hoàn hảo toàn diện, đáp ứng mọi yêu cầu mà không có nhược điểm. | Phân tích tối thiểu 3 trục đánh đổi kỹ thuật thực tế và công khai điểm gãy tải của hệ thống. | Số tài liệu kiến trúc/đề xuất thiếu phần phân tích đánh đổi thực tế bằng 0. |
| Lặp ngữ cảnh dư thừa | Viết đoạn mở đầu lặp lại bối cảnh hệ thống, mục tiêu dự án ở các phân mục con. | Kế thừa ngữ cảnh tĩnh; vào đề trực diện bằng thực thể, thông số hoặc ràng buộc. | Số câu lặp bối cảnh hệ thống cha ở các phân mục con bằng 0. |
| Ngôi xưng và từ ngữ cảm tính | Dùng ngôi 1 (chúng tôi, we), ngôi 2 (bạn, you) hoặc từ ngữ khen ngợi (tuyệt vời, ưu việt). | Dùng ngôi 3 định danh chủ thể kỹ thuật; thể mệnh lệnh cho SOP; từ ngữ trung tính. | Số đại từ ngôi 1/2 bằng 0; số tính từ biểu cảm, tán dương bằng 0. |
| Dẫn chiếu tài liệu ngoại thân | Đùn đẩy "Xem chi tiết tại tài liệu X" trong thân bài; tự ý dẫn chiếu tài liệu ngoài. | Tài liệu đứng độc lập tự thân; chỉ dẫn chiếu tại mục Tài liệu tham khảo khi user yêu cầu. | Số câu dẫn chiếu tài liệu khác ngoài mục Tài liệu tham khảo bằng 0. |
| Vá víu cục bộ & suy thoái hồi quy | Sửa cục bộ gây gãy vỡ phân hệ khác, vứt bỏ điểm tối ưu sẵn có hoặc hạ thấp tiêu chuẩn kỹ thuật. | Quét toàn diện end-to-end, bảo toàn giá trị tối ưu, thống nhất giải pháp với người dùng trước khi sửa. | Số lỗi logic/hồi quy phát sinh sau sửa đổi bằng 0; 100% phần tối ưu được giữ nguyên. |

---

## 4. Bảng Kiểm Định Cơ Học 2 Lớp Thích Ứng Ngữ Cảnh (2-Tier Adaptive Quality Gates)

Mọi tệp tài liệu kỹ thuật sau khi được tạo mới, cập nhật hoặc tái cấu trúc bắt buộc phải vượt qua toàn bộ các cổng kiểm định dưới đây trước khi được nghiệm thu. Hệ thống kiểm định gồm 2 lớp:
- **Lớp 1 (Cổng Bắt Buộc Chung - Universal Core Gates)**: 10 cổng áp dụng cho 100% tài liệu kỹ thuật thuộc mọi thể loại.
- **Lớp 2 (Cổng Kiểm Định Mở Rộng Thích Ứng - Context-Adaptive Extension Gates)**: 4 cổng tự động điều chỉnh tiêu chí kiểm tra tương ứng với thể loại tài liệu đang thẩm định.

### 4.1. Lớp 1: Mười Cổng Bắt Buộc Chung (Universal Core Gates)

- [ ] **Gate U1 (Functional Purpose & Diataxis Consistency)**: Nội dung tài liệu tuân thủ chính xác 1 trong 4 góc phần tư Diataxis; số đoạn văn thuyết giảng lý thuyết hoặc tự bào chữa phương pháp luận bằng 0. (Pass/Fail)
- [ ] **Gate U2 (Single-Language Linguistic Integrity)**: Số cặp ngoặc đơn chứa từ tiếng Anh song hành ngay sau từ tiếng dịch ở tiêu đề và nội dung bằng 0. (Pass/Fail)
- [ ] **Gate U3 (Anti-AI Stylistic Tell Filtration)**: Số dấu em-dash hoặc chuỗi double hyphen nằm ngoài khối mã nội tuyến/fenced bằng 0; số bộ ba tính từ sáo rỗng bằng 0; số mẫu câu tương phản giả Not X but Y bằng 0; số từ vựng AI Tier 1 bằng 0; số gạch đầu dòng bôi đậm đầu dòng bằng 0. (Pass/Fail)
- [ ] **Gate U4 (Table Delimiter & Math Integrity)**: Số ký tự gạch đứng trần bên trong công thức toán học LaTeX trong bảng Markdown bằng 0; sử dụng chuẩn `\lvert ... \rvert`, `\lVert ... \rVert` hoặc `\mid`. (Pass/Fail)
- [ ] **Gate U5 (Code Fence, Callout & Escape Hygiene)**: Số khối lệnh có khoảng trắng sau ba dấu backticks bằng 0; số ký tự thoát rác hiển thị thô bằng 0; số dòng heading chứa thực thể HTML escape của `&`, `<`, `>` bằng 0; các khối cảnh báo tuân thủ chuẩn GitHub Callouts. (Pass/Fail)
- [ ] **Gate U6 (Thesis Statement, Proportional Rigor & Trade-Off Realism)**: Có tuyên ngôn luận điểm kỹ thuật rõ ràng; số biểu thức toán vị từ hoa mỹ cho logic hiển nhiên bằng 0; phân tích tối thiểu 3 trục đánh đổi thực tế; xác định rõ điểm gãy tải hoặc giới hạn phạm vi áp dụng. (Pass/Fail)
- [ ] **Gate U7 (Document Self-Containment & Isolated Reference)**: Tài liệu hoàn chỉnh độc lập; số câu dẫn chiếu đùn đẩy sang tài liệu khác trong thân bài bằng 0; mục Tài liệu tham khảo chỉ hiện diện khi có yêu cầu tường minh từ người dùng và cô lập 100%. (Pass/Fail)
- [ ] **Gate U8 (Strict 3rd-Person Perspective & Neutral Tone)**: Số đại từ ngôi 1 và 2 (`chúng tôi`, `chúng ta`, `tôi`, `bạn`, `quý vị`, `we`, `us`, `our`, `you`) bằng 0; số tính từ biểu cảm, tán dương hoặc phán xét chủ quan bằng 0. (Pass/Fail)
- [ ] **Gate U9 (Context Deduplication & Direct Entry)**: Các phân mục con kế thừa ngữ cảnh tĩnh; số câu tái diễn giải bối cảnh hệ thống vĩ mô hoặc mục tiêu chung của dự án bằng 0; vào đề trực diện bằng thực thể, thông số hoặc ràng buộc. (Pass/Fail)
- [ ] **Gate U10 (End-to-End Impact Analysis & Value Preservation)**: Phân tích đầy đủ bán kính ảnh hưởng xuyên suốt dự án; bảo toàn 100% các điểm tối ưu sẵn có; số lỗi hồi quy logic kéo theo bằng 0; hoàn thành hội chẩn thống nhất giải pháp khi có rủi ro đánh đổi lớn. (Pass/Fail)

### 4.2. Lớp 2: Bốn Cổng Kiểm Định Mở Rộng Thích Ứng (Context-Adaptive Extension Gates)

- [ ] **Gate E1 (Abstraction Layer & Scope Boundary Purity)**:
  - *Đối với SRS/PRD*: Số từ khóa thuộc pha thiết kế chi tiết, hàm ngôn ngữ mã nguồn hoặc class ngoại lệ bằng 0.
  - *Đối với SDD/Arch Spec*: Số đoạn văn sao chép lại yêu cầu nghiệp vụ chi tiết bằng 0; 100% thành phần dẫn chiếu mã định danh yêu cầu.
  - *Đối với Technical Report/Benchmark*: Số kết luận không có số liệu thực nghiệm bảo trợ bằng 0.
  - *Đối với Postmortem/RCA*: Số phán xét quy kết trách nhiệm cá nhân bằng 0; tập trung 100% vào lỗ hổng quy trình và kỹ thuật. (Pass/Fail)
- [ ] **Gate E2 (Structured Namespaced UID Placement & POLA)**:
  - 100% tiêu đề phân mục có thực thể truy vết tuân thủ cú pháp `### X.Y [UID]: [Tên chuẩn]`.
  - 100% mã định danh có tiền tố không gian tên phản ánh phân hệ hoặc miền chủ đề (`REQ-`, `CMP-`, `FIND-`, `REC-`, `INC-`, `ADR-`). Số mã định danh phẳng tuyến tính không namespace (`ID01`, `REQ01`, `UC01`) bằng 0. (Pass/Fail)
- [ ] **Gate E3 (Tiered Visual Modeling, Semantics & Multimodal Parity)**:
  - 100% biểu đồ phức tạp được phân rã hai tầng; số nút trong một biểu đồ duy nhất không vượt quá 9 nút.
  - 100% thực thể hành vi mô hình hóa theo mục tiêu hoàn chỉnh (`<Động từ> + <Đối tượng>`), số thực thể mang tên "Quản lý..." (CRUD) bằng 0.
  - Số quan hệ mở rộng/rẽ nhánh nối các luồng loại trừ nhau bằng 0.
  - **Cross-Modal Parity**: 100% nút hoặc mã định danh trên sơ đồ có phần văn bản đặc tả tương ứng trong thân bài (số thực thể ma bằng 0).
  - Số sơ đồ trang trí vô nghĩa chỉ lặp lại menu giao diện bằng 0. (Pass/Fail)
- [ ] **Gate E4 (Quantitative Evidence & Traceability Closure)**:
  - 100% tiêu chí chấp thuận, chỉ số hiệu năng hoặc kết luận thực nghiệm có ngưỡng số học định lượng kèm dung sai.
  - Chuỗi truy vết khép kín hai chiều 100% phù hợp với loại tài liệu: Yêu cầu <-> Kiểm thử (đối với SRS); Triệu chứng <-> Dữ liệu <-> Nguyên nhân gốc <-> Hành động khắc phục (đối với Postmortem); Giả thuyết <-> Thực nghiệm <-> Kết luận (đối với Tech Report). Số thực thể mồ côi bằng 0. (Pass/Fail)
