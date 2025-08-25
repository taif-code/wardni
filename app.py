from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "wardni-secret"

# --- mock data ---
shipments = [
    {"id": "T-10234", "origin": "الطائف", "destination": "جدة", "temp": 9.8, "status": "في الطريق"},
    {"id": "T-10235", "origin": "جدة", "destination": "الرياض", "temp": 12.4, "status": "مؤجلة"},
    {"id": "T-10236", "origin": "الطائف", "destination": "الرياض", "temp": 8.9, "status": "في الطريق"},
    {"id": "T-10237", "origin": "الطائف", "destination": "جدة", "temp": 10.2, "status": "تم التسليم"},
]
suppliers = [
    {"id": 1, "name": "مزارع ورد الطائف", "location": "الهدا - الطائف", "rating": 4.8},
    {"id": 2, "name": "مزرعة الورود الحديثة", "location": "الشفا - الطائف", "rating": 4.6},
    {"id": 3, "name": "ورد الطائف العضوي", "location": "السيل - الطائف", "rating": 4.7},
]

@app.context_processor
def inject_globals():
    return dict(app_name="وردني", brand_dark_pink="#7A2048", brand_light_pink="#F0D0DB", brand_dark_blue="#0E2A47")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # demo: just redirect
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    in_transit = [s for s in shipments if ("الطريق" in s["status"]) or ("in" in s["status"].lower())]
    avg_temp = round(sum(s["temp"] for s in shipments) / len(shipments), 1)
    alerts = [f"تنبيه: ارتفاع درجة حرارة الشحنة {shipments[0]['id']}." ]
    chart = [{"day": d, "success": v} for d, v in enumerate([12,9,14,11,16,13,18], start=1)]
    return render_template("dashboard.html", shipments=shipments, in_transit=in_transit, avg_temp=avg_temp, alerts=alerts, chart=chart)

@app.route("/track", methods=["GET", "POST"])
def track():
    status = None
    code = request.form.get("code") if request.method == "POST" else "T-10234"
    if code:
        found = next((s for s in shipments if s["id"].lower() == code.lower()), None)
        if found:
            status = f"{found['origin']} → {found['destination']} • {found['status']} • {found['temp']}°C"
        else:
            status = "—"
    return render_template("track.html", code=code or "", status=status)

@app.route("/shipments", methods=["GET", "POST"])
def shipments_page():
    if request.method == "POST":
        new = {
            "id": request.form.get("id") or f"T-{10000+len(shipments)}",
            "origin": request.form.get("origin") or "الطائف",
            "destination": request.form.get("destination") or "الرياض",
            "temp": float(request.form.get("temp") or 10),
            "status": request.form.get("status") or "في الطريق",
        }
        shipments.insert(0, new)
        flash("تم إنشاء الشحنة", "ok")
        return redirect(url_for("shipments_page"))
    return render_template("shipments.html", shipments=shipments)

@app.route("/suppliers")
def suppliers_page():
    return render_template("suppliers.html", suppliers=suppliers)

@app.route("/users", methods=["GET", "POST"])
def users_page():
    # simple demo - not storing users persistently
    if request.method == "POST":
        flash("تمت الإضافة (تجريبي).", "ok")
        return redirect(url_for("users_page"))
    demo_users = [
        {"id": 1, "name": "Admin", "role": "Admin", "email": "admin@wardni.sa"},
        {"id": 2, "name": "Operator", "role": "User", "email": "op@wardni.sa"},
    ]
    return render_template("users.html", users=demo_users)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)


