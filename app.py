# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, g

app = Flask(__name__)
app.secret_key = "wardni-secret"

# ----------------- i18n -----------------
SUPPORTED_LANGS = {"ar", "en"}
DEFAULT_LANG = "ar"

STR = {
    "ar": {
        "app_name": "وردني",
        # navbar
        "dashboard": "لوحة التحكم",
        "shipments": "الشحنات",
        "suppliers": "الموردون",
        "track": "تتبّع شحنة",
        "users": "المستخدمون",
        "login": "تسجيل الدخول",
        # home / common
        "start": "ابدأ",
        "trackShipment": "تتبّع الشحنة",
        # dashboard
        "shipmentsInTransit": "شحنات قيد النقل",
        "avgTemp": "متوسط الحرارة",
        "alerts": "تنبيهات",
        "reports": "التقارير",
        "last7days": "عدد الشحنات الناجحة (آخر 7 أيام)",
        # shipments page
        "manageShipments": "إدارة الشحنات",
        "id": "المعرف",
        "route": "المسار",
        "temperature": "الحرارة",
        "station_col": "المحطة/المرحلة",
        "status": "الحالة",
        "createShipment": "إنشاء شحنة جديدة",
        "createdShipmentOk": "تم إنشاء الشحنة",
        # track page
        "trackTitle": "تتبّع الشحنة",
        "enterTracking": "أدخل رقم التتبّع",
        "trackBtn": "تتبّع",
        "legsTitle": "مراحل الشحنة",
        "notFound": "—",
        # suppliers
        "suppliersTitle": "الموردون",
        "createFromSupplier": "إنشاء شحنة",
        # users
        "usersTitle": "إدارة المستخدمين",
        "name": "الاسم",
        "role": "الدور",
        "email": "البريد الإلكتروني",
        "add": "إضافة",
        "addedOk": "تمت الإضافة (تجريبي).",
        # login
        "email_label": "البريد الإلكتروني",
        "password_label": "كلمة المرور",
        "signIn": "دخول",
        # chatbot
        "botMsg1": "مرحبًا! تقدر تكتب رقم الشحنة وأعطيك حالتها.",
        "botMsg2": "أو تسأل عن الموردين المتاحين.",
        # misc
        "delivered": "تم التسليم",
        "inTransit": "في الطريق",
        "statusLine": "{origin} → {destination} • الحالة: {status}",
        "statusLineWithStation": "{origin} → {destination} • الحالة: {status} • {station}",
        "statusLineWithTemp": "{origin} → {destination} • {status} • {temp}°C",
        "tempUnit": "°م",
        "alertHighTemp": "تنبيه: ارتفاع درجة حرارة الشحنة {sid}.",
        "lang_ar": "العربية",
        "lang_en": "English",
        "heroTitle": "منصة خفيفة لإدارة سلاسل الإمداد للورد الطائفي",
        "heroDesc": "واجهة بسيطة تشبه ERP/SAP لكن أسهل — تتبّع الشحنات، راقب الحرارة، وتواصل مع المورّدين بسهولة.",
        "city_taif": "الطائف",
        "city_jeddah": "جدة",
        "city_riyadh": "الرياض",


    },
    "en": {
        "app_name": "Wardni",
        # navbar
        "dashboard": "Dashboard",
        "shipments": "Shipments",
        "suppliers": "Suppliers",
        "track": "Track",
        "users": "Users",
        "login": "Login",
        # home / common
        "start": "Get Started",
        "trackShipment": "Track Shipment",
        # dashboard
        "shipmentsInTransit": "Shipments In Transit",
        "avgTemp": "Average Temperature",
        "alerts": "Alerts",
        "reports": "Reports",
        "last7days": "Successful Shipments (Last 7 days)",
        # shipments page
        "manageShipments": "Manage Shipments",
        "id": "ID",
        "route": "Route",
        "temperature": "Temp",
        "station_col": "Station/Stage",
        "status": "Status",
        "createShipment": "Create New Shipment",
        "createdShipmentOk": "Shipment created.",
        # track page
        "trackTitle": "Track Shipment",
        "enterTracking": "Enter Tracking Number",
        "trackBtn": "Track",
        "legsTitle": "Shipment Legs",
        "notFound": "—",
        # suppliers
        "suppliersTitle": "Suppliers",
        "createFromSupplier": "Create Shipment",
        # users
        "usersTitle": "Users",
        "name": "Name",
        "role": "Role",
        "email": "Email",
        "add": "Add",
        "addedOk": "Added (demo).",
        # login
        "email_label": "Email",
        "password_label": "Password",
        "signIn": "Sign In",
        # chatbot
        "botMsg1": "Hi! Send a tracking number to get its status.",
        "botMsg2": "Or ask about available suppliers.",
        # misc
        "delivered": "Delivered",
        "inTransit": "In Transit",
        "statusLine": "{origin} → {destination} • Status: {status}",
        "statusLineWithStation": "{origin} → {destination} • Status: {status} • {station}",
        "statusLineWithTemp": "{origin} → {destination} • {status} • {temp}°C",
        "tempUnit": "°C",
        "alertHighTemp": "Alert: high temperature for shipment {sid}.",
        "lang_ar": "العربية",
        "lang_en": "English",
        "heroTitle": "A lightweight platform for managing Taif rose supply chains",
        "heroDesc": "A simple interface similar to ERP/SAP but easier — track shipments, monitor temperature, and connect with suppliers effortlessly.",
        "city_taif": "Taif",
        "city_jeddah": "Jeddah",
        "city_riyadh": "Riyadh",


    },
}

# ==== ترجمة بيانات ديناميكية (حالات + مدن) ====
AR_TO_EN = {
    # حالات
    "تم التسليم": "Delivered",
    "في الطريق": "In Transit",
    "قادم": "Inbound",
    "جاهزة للشحن": "Ready to Ship",
    "مرحلة 1": "Stage 1",
    "مرحلة1": "Stage 1",
    "محطة1": "Station 1",
    # مدن/أماكن
    "مزرعة الطائف": "Taif Farm",
    "الطائف": "Taif",
    "جدة": "Jeddah",
    "الرياض": "Riyadh",
    "الشرقية": "Eastern Province",
}
EN_TO_AR = {v: k for k, v in AR_TO_EN.items()}

# ------------ أدوات لغة ومساعدة ------------
def current_lang():
    return getattr(g, "lang", session.get("lang", DEFAULT_LANG))

def T_key(key, **kwargs):
    lang = current_lang()
    text = STR.get(lang, STR[DEFAULT_LANG]).get(key, key)
    return text.format(**kwargs) if kwargs else text

def to_en(value: str) -> str:
    s = str(value or "")
    return AR_TO_EN.get(s, s)

def to_ar(value: str) -> str:
    s = str(value or "")
    return EN_TO_AR.get(s, s)

def normalize_status_for_match(status: str) -> str:
    """نحوّل الحالة للإنجليزي لتسهيل المقارنة المنطقية داخل الباك."""
    return to_en(status).lower()

# ------------ فلاتر وكونتكست ------------
@app.template_filter('trans')
def trans_filter(value):
    """يحوّل القيم حسب اللغة الحالية (AR/EN)."""
    if value is None:
        return ""
    lang = current_lang()
    s = str(value)
    if lang == "en":
        return AR_TO_EN.get(s, s)
    else:
        return EN_TO_AR.get(s, s)

@app.context_processor
def inject_flags():
    def is_delivered(status):
        s = normalize_status_for_match(status)
        return ("delivered" in s)
    return dict(is_delivered=is_delivered)

@app.context_processor
def inject_i18n():
    lang = current_lang()
    T = STR.get(lang, STR[DEFAULT_LANG])
    direction = "rtl" if lang == "ar" else "ltr"
    # توفير دالة _ للاستخدام داخل القوالب: {{ _('dashboard') }}
    return dict(T=T, lang_code=lang, dir=direction, _=T_key)

# ------------ لغة الطلب ------------
@app.before_request
def set_lang_from_request():
    qlang = request.args.get("lang")
    if qlang in SUPPORTED_LANGS:
        session["lang"] = qlang
    g.lang = session.get("lang", DEFAULT_LANG)

@app.route("/toggle-lang/")
def toggle_lang():
    lang = session.get("lang", DEFAULT_LANG)
    session["lang"] = "en" if lang == "ar" else "ar"
    return redirect(request.referrer or url_for("index"))

# ----------------------------------------
# --- بيانات تجريبية ---
shipments = [
    {
        "id": "T-20001",
        "origin": "مزرعة الطائف",
        "destination": "جدة",
        "temp": 11.2,
        "status": "تم التسليم",
        "station": None,
        "legs": [{"from": "مزرعة الطائف", "to": "جدة", "status": "تم التسليم"}],
    },
    {
        "id": "T-20002",
        "origin": "الطائف",
        "destination": "الشرقية",
        "temp": 10.8,
        "status": "مرحلة 1",
        "station": "محطة1",
        "legs": [
            {"from": "الطائف", "to": "الرياض", "status": "في الطريق"},
            {"from": "الرياض", "to": "الشرقية", "status": "قادم"},
        ],
    },
    {
        "id": "T-20003",
        "origin": "الشرقية",
        "destination": "الرياض",
        "temp": 12.5,
        "status": "محطة1",
        "station": "محطة1",
        "legs": [{"from": "الشرقية", "to": "الرياض", "status": "جاهزة للشحن"}],
    },
]

# ----------------------------------------
# ------------ الراوتس ------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # مثال فقط
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    # تحديد الشحنات قيد النقل باعتماد توحيد الحالة للإنجليزي
    in_transit = [
        s for s in shipments
        if ("in transit" in normalize_status_for_match(s["status"]))
           or ("stage" in normalize_status_for_match(s["status"]))  # تعتبر مراحل ضمن "قيد النقل"
           or ("station" in normalize_status_for_match(s["status"]))
    ]

    avg_temp = round(sum(s["temp"] for s in shipments) / len(shipments), 1)

    # تنبيه حراري محليّ حسب اللغة
    alerts = [T_key("alertHighTemp", sid=shipments[0]["id"])]

    chart = [{"day": d, "success": v} for d, v in enumerate([12, 9, 14, 11, 16, 13, 18], start=1)]
    return render_template(
        "dashboard.html",
        shipments=shipments,
        in_transit=in_transit,
        avg_temp=avg_temp,
        alerts=alerts,
        chart=chart
    )

@app.route("/track", methods=["GET", "POST"])
def track():
    code = request.form.get("code") if request.method == "POST" else "T-20002"
    found = next((s for s in shipments if s["id"].lower() == (code or "").lower()), None)

    status_line = T_key("notFound")
    legs = []

    if found:
        # نطبّق الترجمة على الحالات/المدن في السطر الظاهر فقط (العرض)، بينما الداتا تبقى كما هي
        origin_disp = (found["origin"])  # سيُترجم في القالب عبر |trans إذا أردت
        dest_disp = (found["destination"])
        status_disp = (found["status"])
        station_disp = found.get("station")

        if found.get("legs"):
            if station_disp:
                status_line = T_key(
                    "statusLineWithStation",
                    origin=origin_disp, destination=dest_disp,
                    status=status_disp, station=station_disp
                )
            else:
                status_line = T_key(
                    "statusLine",
                    origin=origin_disp, destination=dest_disp,
                    status=status_disp
                )
            legs = found["legs"]
        else:
            status_line = T_key(
                "statusLineWithTemp",
                origin=origin_disp, destination=dest_disp,
                status=status_disp, temp=found["temp"]
            )

    return render_template(
        "track.html",
        code=code or "",
        status=status_line,
        legs=legs
    )

@app.route("/shipments", methods=["GET", "POST"])
def shipments_page():
    if request.method == "POST":
        new = {
            "id": request.form.get("id") or f"T-{10000+len(shipments)}",
            "origin": request.form.get("origin") or "الطائف",
            "destination": request.form.get("destination") or "الرياض",
            "temp": float(request.form.get("temp") or 10),
            "status": request.form.get("status") or "في الطريق",
            "station": request.form.get("station") or None,
            "legs": [],
        }
        shipments.insert(0, new)
        flash(T_key("createdShipmentOk"), "ok")
        return redirect(url_for("shipments_page"))

    return render_template("shipments.html", shipments=shipments)

@app.route("/suppliers")
def suppliers_page():
    suppliers = [
        {"id": 1, "name": "مزارع ورد الطائف", "location": "الهدا - الطائف", "rating": 4.8},
        {"id": 2, "name": "مزرعة الورود الحديثة", "location": "الشفا - الطائف", "rating": 4.6},
        {"id": 3, "name": "ورد الطائف العضوي", "location": "السيل - الطائف", "rating": 4.7},
    ]
    return render_template("suppliers.html", suppliers=suppliers)

@app.route("/users", methods=["GET", "POST"])
def users_page():
    if request.method == "POST":
        flash(T_key("addedOk"), "ok")
        return redirect(url_for("users_page"))
    demo_users = [
        {"id": 1, "name": "Admin", "role": "Admin", "email": "admin@wardni.sa"},
        {"id": 2, "name": "Operator", "role": "User", "email": "op@wardni.sa"},
    ]
    return render_template("users.html", users=demo_users)

# ----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
