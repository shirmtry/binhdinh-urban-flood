# -*- coding: utf-8 -*-
"""Ngập úng đô thị Quy Nhơn – Bình Định 2026.
Tác giả: HTK · Hotline/Zalo: 0396241674 · Email: htk.contact@gmail.com
Cập nhật: 09/11/2026
"""
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Dữ liệu mô phỏng – cập nhật 09/11/2026
# 15 điểm ngập úng đô thị Quy Nhơn.
# x, y: toạ độ trên bản đồ SVG (viewBox 800x560)
# runoff: hệ số dòng chảy mặt (0-1), drain_mm: khả năng thoát nước (mm/2h)
# depth_cm: mực ngập quan trắc mô phỏng hiện tại (cm)
POINTS = [
    {"id": "nguyen-thai-hoc", "name": "Nguyễn Thái Học", "ward": "Phường Trần Phú",
     "x": 300, "y": 330, "runoff": 0.85, "drain_mm": 40, "depth_cm": 55},
    {"id": "tay-son", "name": "Tây Sơn (đoạn chợ Đầm)", "ward": "Phường Nguyễn Văn Cừ",
     "x": 205, "y": 260, "runoff": 0.80, "drain_mm": 45, "depth_cm": 48},
    {"id": "le-hong-phong", "name": "Lê Hồng Phong", "ward": "Phường Trần Hưng Đạo",
     "x": 420, "y": 300, "runoff": 0.82, "drain_mm": 42, "depth_cm": 52},
    {"id": "tran-hung-dao", "name": "Trần Hưng Đạo", "ward": "Phường Trần Hưng Đạo",
     "x": 500, "y": 360, "runoff": 0.65, "drain_mm": 60, "depth_cm": 25},
    {"id": "ngo-may", "name": "Ngô Mây", "ward": "Phường Ngô Mây",
     "x": 350, "y": 230, "runoff": 0.75, "drain_mm": 50, "depth_cm": 35},
    {"id": "ly-thuong-kiet", "name": "Lý Thường Kiệt", "ward": "Phường Trần Phú",
     "x": 280, "y": 400, "runoff": 0.70, "drain_mm": 55, "depth_cm": 28},
    {"id": "nguyen-hue", "name": "Nguyễn Huệ", "ward": "Phường Trần Hưng Đạo",
     "x": 460, "y": 240, "runoff": 0.60, "drain_mm": 65, "depth_cm": 15},
    {"id": "hai-ba-trung", "name": "Hai Bà Trưng", "ward": "Phường Lê Hồng Phong",
     "x": 380, "y": 420, "runoff": 0.72, "drain_mm": 52, "depth_cm": 30},
    {"id": "dong-da", "name": "Đống Đa", "ward": "Phường Đống Đa",
     "x": 230, "y": 170, "runoff": 0.78, "drain_mm": 46, "depth_cm": 40},
    {"id": "phan-boi-chau", "name": "Phan Bội Châu", "ward": "Phường Hải Cảng",
     "x": 540, "y": 200, "runoff": 0.55, "drain_mm": 70, "depth_cm": 10},
    {"id": "tang-bat-ho", "name": "Tăng Bạt Hổ", "ward": "Phường Lê Hồng Phong",
     "x": 430, "y": 150, "runoff": 0.68, "drain_mm": 58, "depth_cm": 20},
    {"id": "bach-dang", "name": "Bạch Đằng (bến cảng)", "ward": "Phường Hải Cảng",
     "x": 620, "y": 280, "runoff": 0.50, "drain_mm": 80, "depth_cm": 8},
    {"id": "nguyen-tat-thanh", "name": "Nguyễn Tất Thành", "ward": "Phường Đống Đa",
     "x": 160, "y": 110, "runoff": 0.62, "drain_mm": 62, "depth_cm": 12},
    {"id": "an-duong-vuong", "name": "An Dương Vương", "ward": "Phường Nguyễn Văn Cừ",
     "x": 130, "y": 330, "runoff": 0.74, "drain_mm": 48, "depth_cm": 33},
    {"id": "xuan-dieu", "name": "Xuân Diệu (ven biển)", "ward": "Phường Trần Phú",
     "x": 560, "y": 450, "runoff": 0.45, "drain_mm": 90, "depth_cm": 5},
]

LEVELS = {
    0: {"label": "Không ngập", "color": "#2e9e5b"},
    1: {"label": "Ngập nhẹ", "color": "#e6b800"},
    2: {"label": "Ngập vừa", "color": "#e8760c"},
    3: {"label": "Ngập nặng", "color": "#d92626"},
}


def flood_level(depth_cm):
    """Phân cấp ngập: 0 <10cm, 1: 10-29cm, 2: 30-49cm, 3 >=50cm."""
    if depth_cm >= 50:
        return 3
    if depth_cm >= 30:
        return 2
    if depth_cm >= 10:
        return 1
    return 0


def predict_depth(point, rain_mm):
    """Công thức mô phỏng: nước dâng = mưa * hệ số dòng chảy - thoát nước.

    depth_cm = max(0, (rain_mm * runoff - drain_mm)) * 1.1
    (mưa trong 2 giờ, quy đổi xấp xỉ 1mm đọng ≈ 1.1cm tại điểm trũng)
    """
    depth = max(0.0, rain_mm * point["runoff"] - point["drain_mm"]) * 1.1
    return round(depth, 1)


def point_payload():
    data = []
    for p in POINTS:
        item = dict(p)
        lv = flood_level(p["depth_cm"])
        item["level"] = lv
        item["levelLabel"] = LEVELS[lv]["label"]
        item["color"] = LEVELS[lv]["color"]
        data.append(item)
    return data


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/map')
def flood_map():
    return render_template('map.html', points=point_payload(), levels=LEVELS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/points')
def api_points():
    return jsonify({
        "city": "Quy Nhơn",
        "province": "Bình Định",
        "note": "Dữ liệu mô phỏng – cập nhật 09/11/2026",
        "updatedAt": "09/11/2026 08:00",
        "points": point_payload(),
    })


@app.route('/api/predict', methods=['GET', 'POST'])
def api_predict():
    if request.method == 'POST':
        payload = request.get_json(silent=True) or {}
        raw = payload.get('rain_mm', payload.get('rain', 0))
    else:
        raw = request.args.get('rain_mm', request.args.get('rain', 0))
    try:
        rain_mm = float(raw)
    except (TypeError, ValueError):
        return jsonify({"ok": False, "error": "Lượng mưa không hợp lệ (cần số mm)."}), 400
    if rain_mm < 0 or rain_mm > 1000:
        return jsonify({"ok": False, "error": "Lượng mưa phải trong khoảng 0–1000 mm."}), 400

    results = []
    for p in POINTS:
        depth = predict_depth(p, rain_mm)
        lv = flood_level(depth)
        results.append({
            "id": p["id"], "name": p["name"], "ward": p["ward"],
            "depthCm": depth, "level": lv,
            "levelLabel": LEVELS[lv]["label"], "color": LEVELS[lv]["color"],
        })
    results.sort(key=lambda r: r["depthCm"], reverse=True)
    return jsonify({
        "ok": True,
        "rainMm": rain_mm,
        "durationHours": 2,
        "formula": "depth_cm = max(0, mưa_mm × hệ_số_dòng_chảy − thoát_nước_mm) × 1.1",
        "note": "Dữ liệu mô phỏng – cập nhật 09/11/2026",
        "results": results,
    })


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class VercelPathMiddleware:
    """Vercel rewrite '/(.*)' -> '/api/index/$1' đưa prefix /api/index vào PATH_INFO.

    Middleware khôi phục đường dẫn gốc để Flask định tuyến đúng
    (hoạt động cả local lẫn Vercel, không side-effect khi import).
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        prefix = '/api/index'
        if path == prefix or path.startswith(prefix + '/'):
            rest = path[len(prefix):]
            environ['PATH_INFO'] = rest if rest else '/'
        return self.wsgi_app(environ, start_response)


app.wsgi_app = VercelPathMiddleware(app.wsgi_app)


if __name__ == '__main__':
    app.run(debug=True)