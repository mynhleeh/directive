---
lang: vi
title: BÁO CÁO PHÂN TÍCH HỆ THỐNG DỮ LIỆU
subtitle: Thiết kế Cơ sở dữ liệu và Quy trình Xử lý
institution: HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
faculty: KHOA CÔNG NGHỆ THÔNG TIN 1
course: Cơ sở dữ liệu nâng cao [DB-01]
team: "Nhóm 01"
cover-logo: logo.png
cover-style: boxed
members:
  - name: Sinh viên A
    id: B24XXXX001
  - name: Sinh viên B
    id: B24XXXX002
instructor: Giảng viên hướng dẫn
location-year: "Hà Nội, 2026"
---

# 1. Tổng quan kiến trúc

Báo cáo trình bày quy trình chuẩn hóa dữ liệu thông qua hàm `engine.tinh_gia_tri(ma_nhan_vien)` với bảng mã tiếng Việt đầy đủ dấu thanh điệu: ă, â, đ, ê, ô, ơ, ư, ệ, ậ.

> [!WARNING]
> Không bỏ qua bước kiểm tra ký tự thiếu trong file log biên dịch.

## 1.1 Truy vấn và mã nguồn minh họa

```python
# Tính toán điểm đánh giá định kỳ theo từng quý
def compute_score(base_score: float, bonus: float) -> float:
    return base_score + bonus
```

| Mã | Thành phần | Phụ trách<br>`module_id` | Vai trò | Trạng thái |
| --- | --- | --- | --- | --- |
| C1 | Bộ lọc Lua | Hệ thống | Chuẩn hóa tiêu đề, bảng, callout | Hoàn tất |
| C2 | Mẫu Unicode | Xuất bản | Biên dịch song song LuaLaTeX và XeLaTeX | Đã kiểm thử |

![](diagram.pdf)

*Hình 1: Kiến trúc tổng thể*

# Phụ lục A: Kịch bản SQL

## A.1 Bảng dữ liệu mẫu

```sql
-- Khởi tạo bảng chấm công tiếng Việt
SELECT employee_id, full_name FROM EMPLOYEE_PROFILE;
```
