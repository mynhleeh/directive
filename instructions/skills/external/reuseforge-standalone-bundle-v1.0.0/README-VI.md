# ReuseForge Standalone Bundle v1.0.0 — Hướng dẫn tiếng Việt

Đây là bộ phân phối đầy đủ gồm **9 Skill ReuseForge** chạy theo protocol `reuseforge/1.0`.

## Cài đặt đúng cách

**Không tải file ZIP ngoài cùng lên như một Skill.** File ngoài cùng chứa nhiều Skill.

1. Giải nén `reuseforge-standalone-bundle-v1.0.0.zip`.
2. Mở ChatGPT `/skills`.
3. Vào thư mục `skills/` của gói vừa giải nén.
4. Tải từng file ZIP lên **riêng từng Skill**.
5. Cài đủ 9 Skill để có workflow đầy đủ.

Thứ tự khuyến nghị: Orchestrator -> Project Framer -> Asset Scout -> Candidate Auditor -> Solution Architect -> Project Planner -> Execution Handoff -> Repair Router -> Memory Recovery.

## ReuseForge có cần Solo Builder không?

Không. Bộ này hoạt động độc lập.

Nếu tài khoản có `Solo Builder Dev Orchestrator`, ReuseForge có thể được dùng như subworkflow **Reuse Review** trước DEV Gate C. Đây là tích hợp tùy chọn, không phải dependency.

## Kiểm tra nhanh sau khi cài

Gọi `@ReuseForge Orchestrator` với một dự án nhỏ và yêu cầu “bắt đầu đúng stage, không bỏ qua approval”. Kỳ vọng Orchestrator route sang Project Framer; Project Framer dừng tại Gate A để xin phê duyệt trước khi discovery.

Nếu Asset Scout tìm thấy repo/package, kết quả discovery chưa được xem là phù hợp cho tới khi `reuseforge-candidate-auditor` kiểm chứng.

## Mức bảo đảm của gói

Trước khi đóng gói đã kiểm tra:

- 9/9 Skill PASS validator chính thức.
- 9/9 ZIP PASS integrity và extract -> revalidate.
- 59/59 resource reference nội bộ tồn tại.
- JSON/YAML parse PASS.
- 7 file protocol dùng chung nhất quán giữa 9 Skill.
- Không phát hiện dependency cứng tới Solo Builder/Aki/A2/Orca.

Không thể đảm bảo connector/tool bên ngoài giống nhau trên mọi tài khoản. Web, GitHub, repo access, Codex/OpenCode hoặc external executor phụ thuộc môi trường của người nhận.
