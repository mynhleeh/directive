---
trigger: glob
globs: "**/*"
description: "Quy chuẩn cơ học về đặt tên, phân tầng, phân cấp dấu và quản lý tệp/thư mục trong không gian lưu trữ số."
---

# File & Folder Organization Rules

Tài liệu này xác lập các nguyên tắc cơ học, phi ngữ cảnh và trung lập để quản lý toàn bộ hệ thống tệp và thư mục. Quy tắc áp dụng đồng bộ cho cả tác nhân tự động (AI) lẫn con người trong quá trình tạo mới, di chuyển hoặc chuẩn hóa tài nguyên.

---

## 1. NGUYÊN LÝ CỐT LÕI (CORE AXIOMS)

1. **Phân cấp dấu rõ ràng (Delimiter Hierarchy)**: Dấu gạch ngang `-` phân cách ranh giới ngữ nghĩa lớn giữa các phần; dấu gạch dưới `_` gắn kết các từ thành tố trong cùng một phần.
2. **Ưu tiên tiếng Anh đi đôi với bảo tồn định danh (Context-Aware Language)**: Ưu tiên tiếng Anh làm tiêu chuẩn quốc tế hóa; cho phép giữ nguyên tên bản địa dạng ASCII không dấu khi dịch thuật làm mất tính nhận diện thực tế của đối tượng.
3. **Đóng gói phân tầng (Strict Encapsulation)**: Không để tệp tài nguyên trôi nổi tại thư mục gốc của một đơn vị công việc nếu tệp đó thuộc về một nhóm chức năng cụ thể.
4. **Cơ học và đếm được (Deterministic Predictability)**: Mọi quy tắc về ký tự, dấu phân cách, độ sâu và định dạng ngày tháng phải có ranh giới Đạt / Không Đạt (Pass/Fail) cơ học, không phụ thuộc cảm tính.

---

## 2. QUY CHUẨN ĐẶT TÊN CƠ HỌC & HỆ THỐNG PHÂN CẤP DẤU

### 2.1. Quy tắc phân cấp ký tự (Delimiter Hierarchy)

Để tối ưu hóa khả năng đọc của con người và khả năng phân tích chuỗi (parsing) của mã lệnh/AI, hệ thống tên gọi tuân thủ 2 cấp độ dấu:

- **Cấp độ vĩ mô (Macro Delimiter - `-`)**: Dấu gạch ngang dùng để phân tách **giữa các phần ngữ nghĩa độc lập** (ví dụ giữa: `[Tiền tố/Thời gian]` - `[Tên thực thể]` - `[Phân loại]` - `[Hậu tố]`).
- **Cấp độ vi mô (Micro Delimiter - `_`)**: Dấu gạch dưới dùng để liên kết **các từ cấu thành nội dung bên trong một phần** khi tên có từ 2 phần trở lên.

```
Cấu trúc tổng quát (≥ 2 phần):
[part_one]-[part_two]-[part_three]
  ▲         ▲         ▲
  │         │         └─ Nội dung bên trong dùng snake_case (_)
  └─────────┴─────────── Ngăn cách giữa các phần dùng kebab-case (-)
```

#### Bảng quy tắc phân nhánh theo số lượng thành phần:

| Số lượng phần ngữ nghĩa | Cú pháp áp dụng | Quy ước dấu | Ví dụ trung lập |
|---|---|---|---|
| **Đơn thành phần (1 part)**<br>*(Thường là tên môn, tên chủ đề, danh mục)* | `kebab-case` thuần túy | Chỉ dùng dấu gạch ngang `-` nối các từ | `discrete-math`<br>`presentation-skills`<br>`digital-electronics`<br>`phap-luat-dai-cuong` |
| **Đa thành phần ($\ge 2$ parts)**<br>*(Có tiền tố thứ tự, ngày tháng, loại tệp, hậu tố)* | Lai ghép phân cấp<br>`kebab-case` ngoài<br>`snake_case` trong | Dấu `-` ngăn giữa các phần;<br>Dấu `_` nối từ trong mỗi phần | `01-system_architecture`<br>`2026_03_31-quarterly_review`<br>`component_a-test_suite`<br>`module_alpha-lecture_notes` |

### 2.2. Định dạng số đếm và thứ tự (Sequencing)
- Mọi dãy số thứ tự phải được đệm số không (Zero-padded) để đảm bảo tính sắp xếp tự nhiên trên hệ thống tệp:
  - Chuỗi dưới 100 phần tử: Dùng tối thiểu 2 chữ số (`01`, `02`, `03`, ... `99`).
  - Chuỗi từ 100 phần tử trở lên: Dùng tối thiểu 3 chữ số (`001`, `002`, ... `999`).
- Áp dụng quy tắc phân cấp dấu khi ghép với nội dung:
  - Định dạng: `nn-<noi_dung_phan_hai>` (ví dụ: `01-introduction_overview.md`, `02-core_analysis.pdf`).

### 2.3. Định dạng thời gian (Temporal Tokens)
- Mốc thời gian được coi là **một phần ngữ nghĩa độc lập**:
  - Khi mốc thời gian đứng độc lập: tuân thủ ISO 8601 (`YYYY-MM-DD`).
  - Khi mốc thời gian là một phần trong tên tệp đa thành phần, các đơn vị ngày/tháng/năm liên kết bằng `_` để tạo thành một khối liền, phân cách với phần tiếp theo bằng `-`:
    - Định dạng: `YYYY_MM_DD-<ten_noi_dung>` (ví dụ: `2026_03_31-annual_summary_report.pdf`).
    - Hoặc mốc tháng: `YYYY_MM-<ten_noi_dung>` (ví dụ: `2026_03-quarterly_review`).

### 2.4. Bảng ký tự hợp lệ tuyệt đối
- **Cho phép**: Chữ cái thường `a-z`, số `0-9`, dấu `-`, dấu `_`, và dấu `.` (chỉ dùng cho phần mở rộng).
- **Cấm tuyệt đối**:
  - Khoảng trắng (Space).
  - Chữ cái in hoa (`A-Z`).
  - Ký tự đặc biệt: `@`, `#`, `$`, `%`, `&`, `*`, `(`, `)`, `+`, `=`, `[`, `]`, `{`, `}`.
  - Ký tự Unicode có dấu (toàn bộ phải chuyển về ASCII không dấu).

---

## 3. CHÍNH SÁCH NGÔN NGỮ NHẬN DIỆN NGỮ CẢNH (LANGUAGE POLICY)

Để đảm bảo tính chuẩn hóa học thuật/kỹ thuật mà không làm mất liên kết với hồ sơ gốc thực tế, chính sách ngôn ngữ tuân thủ 2 bậc ưu tiên:

```
[Bậc 1: Mặc định] Tiếng Anh kỹ thuật chuẩn (English-first)
       │
       ▼ (Ngoại lệ nhận diện)
[Bậc 2: Ngoại lệ] Tiếng Việt không dấu (ASCII Vietnamese) khi việc dịch sang tiếng Anh
                  làm suy giảm tính nhận diện hoặc sai lệch tên hồ sơ chính thức.
```

### 3.1. Bậc 1: Ưu tiên tiếng Anh (Default Standard)
- Áp dụng bắt buộc cho:
  - 100% tên các thư mục chức năng Cấp 3 (ví dụ: `docs/`, `references/`, `slides/`, `assessments/`, `templates/`, `reports/`, `images/`).
  - Các môn học, dự án, công nghệ mang tính phổ quát quốc tế (ví dụ: `computer-architecture`, `discrete-math`, `probability-statistics`, `digital-electronics`).
  - Các chỉ số trạng thái, loại dữ liệu kỹ thuật.

### 3.2. Bậc 2: Bảo tồn định danh nguyên ngữ (Identity Preservation)
- Áp dụng khi:
  - Tên môn học, văn bản, chứng từ mang tính thể chế, pháp lý, chính trị hoặc chương trình nội địa đặc thù mà nếu dịch sang tiếng Anh sẽ làm mất tính nhận diện thực tế khi đối chiếu văn bằng/hồ sơ (Recognition Loss).
  - *Nguyên tắc bắt buộc*: Chuyển đổi 100% sang ký tự **ASCII không dấu**, viết thường, tuân thủ đúng quy tắc phân cấp dấu ở Mục 2.
  - *Ví dụ đối chiếu*:
    - Giữ nguyên bản địa không dấu: `phap-luat-dai-cuong`, `triet-hoc-mac-lenin`, `ky-nang-lam-viec-nhom`.
    - Dùng tiếng Anh chuẩn: `algebra`, `calculus-01`, `physics`.

---

## 4. KIẾN TRÚC PHÂN TẦNG 4 CẤP (4-TIER HIERARCHY)

Một không gian lưu trữ chuẩn mực không được vượt quá **4 cấp độ sâu** tính từ gốc thư mục làm việc:

```
Level 0: [Workspace Root]
  └── Level 1: [Domain Namespace]          (Ví dụ: engineering/ hoặc archives/)
        └── Level 2: [Scope / Entity]      (Ví dụ: discrete-math/ hoặc project_alpha-phase_01/)
              └── Level 3: [Category Pool] (Ví dụ: docs/ hoặc references/ - Bắt buộc số nhiều)
                    └── Level 4: [Target]  (Ví dụ: 01-system_overview.md)
```

- **Cấp 1 - Miền dữ liệu (Domain Namespace)**: Đơn vị độc lập lớn nhất (ví dụ: `academics`, `operations`, `certifications`).
- **Cấp 2 - Thực thể phạm vi (Scope Unit)**: Đơn vị học phần, môn học, dự án hoặc sự kiện độc lập.
- **Cấp 3 - Nhóm chức năng (Functional Category)**: Phân loại mục đích của tài nguyên. Bắt buộc dùng **danh từ tiếng Anh số nhiều** (xem Mục 5).
- **Cấp 4 - Tệp tài nguyên (Target Artifact)**: Tệp dữ liệu thực tế mang nội dung.

---

## 5. MA TRẬN PHÂN LOẠI DANH TỪ SỐ NHIỀU & SỐ ÍT (FUNCTIONAL POOLS)

Toàn bộ các thư mục chức năng ở Cấp 3 bắt buộc chuẩn hóa bằng tiếng Anh theo danh từ số nhiều:

| Danh mục chuẩn hóa | Quy tắc | Phạm vi tài liệu chứa bên trong |
|---|---|---|
| `docs/` | Số nhiều | Tài liệu thuyết minh, hướng dẫn, biên bản, ghi chú tổng hợp |
| `references/` | Số nhiều | Giáo trình, sách tham khảo bên thứ ba, tài liệu tiêu chuẩn ngoài |
| `slides/` hoặc `presentations/` | Số nhiều | Bản trình chiếu, bài thuyết trình bài giảng |
| `assessments/` hoặc `exams/` | Số nhiều | Đề thi, đề kiểm tra định kỳ, đáp án, barem điểm |
| `exercises/` hoặc `assignments/`| Số nhiều | Bài tập tự luyện, bài tập lớn, bài tập thực hành |
| `images/` hoặc `media/` | Số nhiều | Ảnh chụp minh họa, sơ đồ, video, biểu đồ |
| `templates/` | Số nhiều | Khung biểu mẫu chuẩn, sườn tài liệu tái sử dụng |
| `reports/` | Số nhiều | Báo cáo định kỳ, báo cáo nghiệm thu, bản tóm tắt tiến độ |
| `data/` hoặc `datasets/` | Tập hợp | Dữ liệu bảng tính thô, tệp số liệu đo đạc thực nghiệm |
| `archive/` | Số ít | Nhóm dữ liệu lịch sử đã kết thúc hoàn toàn vòng đời sử dụng |

---

## 6. NGUYÊN TẮC VỆ SINH THƯ MỤC GỐC (ROOT HYGIENE)

1. **Quy tắc trần 1 tệp chỉ mục (Max-1 Index Rule)**:
   Tại gốc của mỗi Scope Unit (Cấp 2), chỉ cho phép tồn tại tối đa **01 tệp chỉ mục/tổng quan** (ví dụ: `overview.md` hoặc `index.md`).
2. **Cấm tài sản trôi nổi (No Floating Assets)**:
   - Toàn bộ tệp hình ảnh (`.png`, `.jpg`), tệp tài liệu xử lý (`.docx`, `.xlsx`, `.pptx`, `.pdf`) và tệp media (`.mp3`, `.mp4`) bắt buộc phải nằm trong các thư mục chức năng Cấp 3 tương ứng (`docs/`, `references/`, `images/`...).
   - Nghiêm cấm đặt tệp thô trực tiếp tại thư mục gốc Cấp 2 bên cạnh các thư mục con.
3. **Loại bỏ tệp rác hệ thống & shortcut**:
   - Nghiêm cấm lưu trữ các tệp shortcut hệ điều hành cục bộ (như `.lnk`).
   - Tự động xóa hoặc bỏ qua các tệp cấu hình hiển thị môi trường (như `desktop.ini`, `.DS_Store`, `Thumbs.db`).

---

## 7. BẢNG ĐỐI CHIẾU VI PHẠM & CÁCH SỬA ĐỔI

| ❌ Cũ / Vi phạm | ✅ Chuẩn hóa mới | Giải thích kỹ thuật |
|---|---|---|
| `calculus_01` (dùng `_` cho đơn phần) | `calculus-01` | Đơn thành phần: dùng `kebab-case` thuần túy. |
| `2022_10_30-modern-cultural-achievements` | `2022_10_30-modern_cultural_achievements` | Đa thành phần: phần 1 là ngày (`2022_10_30`), phần 2 là nội dung nối bằng `_` (`modern_cultural_achievements`), ngăn cách giữa 2 phần bằng `-`. |
| `day_29-test-voice_01.mp3` | `day_29-voice_test_01.mp3` | Đa thành phần: `day_29` (phần 1) - `voice_test_01` (phần 2). |
| `pháp-luật-đại-cương/` (có dấu) | `phap-luat-dai-cuong/` | Giữ nguyên nhận diện tiếng Việt nhưng chuyển sang ASCII không dấu, dùng `kebab-case` cho tên đơn phần. |
| `General-Law/` (dịch gượng ép làm mất nhận diện) | `phap-luat-dai-cuong/` | Ngoại lệ bảo tồn định danh: giữ tiếng Việt không dấu để tiện tra cứu hồ sơ gốc. |
| `reference/` cạnh `references/` | Luôn là `references/` | Thống nhất danh từ số nhiều cho thư mục tài liệu tham khảo. |
| `essay/` cạnh `exercises/` | `exercises/` hoặc `assignments/` | Đưa các bài luận nhỏ vào nhóm bài tập chuẩn hóa dạng số nhiều. |
| `desktop.ini`, `file.lnk` | *(Đã xóa)* | Loại bỏ tệp rác hệ thống không chứa giá trị nội dung. |

---

## 8. BỘ KIỂM TRA ĐIỀU KIỆN NGHIỆM THU (VERIFICATION CHECKLIST)

Mọi thay đổi hoặc bổ sung thư mục/tệp mới phải vượt qua 6 cổng kiểm định cơ học:

- [ ] **Gate 1 - Delimiter Rule**:
  - Tên đơn thành phần chỉ dùng duy nhất dấu `-` (`kebab-case`).
  - Tên đa thành phần ($\ge 2$ phần) dùng `-` ngăn cách giữa các phần và dùng `_` liên kết các từ bên trong từng phần.
- [ ] **Gate 2 - Language & ASCII Check**:
  - Không có ký tự có dấu, ký tự viết hoa hoặc khoảng trắng.
  - Sử dụng tiếng Anh mặc định; chỉ dùng tiếng Việt không dấu cho các thực thể đặc thù cần bảo tồn nhận diện.
- [ ] **Gate 3 - Depth Check**: Không có bất kỳ tệp dữ liệu nào vượt quá Cấp 4.
- [ ] **Gate 4 - Root Hygiene Check**: Thư mục phạm vi (Cấp 2) không chứa tệp media/tài liệu trôi nổi ở gốc, chỉ cho phép tối đa 01 tệp chỉ mục.
- [ ] **Gate 5 - Plurality Check**: 100% thư mục chức năng Cấp 3 tuân thủ danh từ tiếng Anh số nhiều trong Ma trận Mục 5.
- [ ] **Gate 6 - Date Format Check**: Mốc thời gian đa phần tuân thủ `YYYY_MM_DD-<noi_dung>` hoặc `YYYY_MM-<noi_dung>`.
