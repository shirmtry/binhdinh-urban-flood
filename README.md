# binhdinh-urban-flood — Ngập úng đô thị Quy Nhơn 2026

> Tác giả: **HTK** · Hotline/Zalo: **0396241674** · Email: htk.contact@gmail.com
> Cập nhật: **09/11/2026** — mùa mưa lũ 2026 Bình Định.

## Vấn đề

Tháng 11/2026, bão số 9 và số 10 đổ bộ Quy Nhơn – Phù Cát gây mưa lớn kéo dài trong
**mùa mưa lũ 2026**. Chỉ sau 2 giờ mưa, các tuyến phố trung tâm Quy Nhơn như
**Nguyễn Thái Học, Tây Sơn, Lê Hồng Phong** ngập sâu 40–60cm: giao thông tê liệt,
nhà dân ngập nước, sinh hoạt đảo lộn. Người dân cần công cụ xem nhanh điểm ngập,
dự báo độ ngập theo lượng mưa và chia sẻ thông tin ngập cộng đồng.

## Tính năng

- 🗺️ **Bản đồ SVG 15 điểm ngập** Quy Nhơn, màu theo mức ngập (xanh <10cm, vàng 10–29cm, cam 30–49cm, đỏ ≥50cm).
- 🌧️ **Dự báo ngập theo lượng mưa**: nhập mm mưa/2h → backend Flask tính độ ngập từng điểm qua công thức
  `depth_cm = max(0, mưa_mm × hệ_số_dòng_chảy − thoát_nước_mm) × 1.1` (API `/api/predict`).
- 📣 **Form báo ngập cộng đồng**: lưu localStorage trên trình duyệt, hiển thị danh sách báo cáo, xoá được.
- Trang chủ mô tả vấn đề, trang About bối cảnh mùa lũ 2026, trang 404 có hotline HTK.
- Responsive 375px (mobile) + 1440px (desktop), UI tiếng Việt.
- Toàn bộ là **Dữ liệu mô phỏng – cập nhật 09/11/2026**.

## Công nghệ

- **Python Flask** (serverless trên Vercel, `api/index.py`)
- HTML/CSS/JavaScript thuần, bản đồ SVG, localStorage
- Không database — mock data trong backend

## Cách chạy local

```bash
py -m venv venv
venv/Scripts/python.exe -m pip install -r requirements.txt
venv/Scripts/python.exe api/index.py
# Mở http://127.0.0.1:5000
```

## Routes

| Route | Mô tả |
|---|---|
| `/` | Trang chủ – vấn đề ngập úng Quy Nhơn 2026 |
| `/map` | Bản đồ 15 điểm ngập + dự báo + báo cáo cộng đồng |
| `/about` | Giới thiệu + liên hệ HTK |
| `/api/points` | JSON 15 điểm ngập (mock) |
| `/api/predict` | POST `{"rain_mm": 120}` → dự báo độ ngập từng điểm |

## Deploy

- Vercel (production): xem `deploy_url.txt` — link deploy sẽ được cập nhật tại đây sau khi triển khai.
- GitHub: https://github.com/shirmtry/binhdinh-urban-flood

## 📞 Liên hệ HTK – 0396241674 – 09/11/2026

- Hotline/Zalo: [0396241674](tel:0396241674) · https://zalo.me/0396241674
- Email: htk.contact@gmail.com
- © 2026 HTK · Cập nhật: 09/11/2026