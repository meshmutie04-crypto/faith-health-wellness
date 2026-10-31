from flask import (
    Flask, render_template, request, abort,
    session, redirect, url_for, flash
)
import urllib.parse

app = Flask(__name__)
app.secret_key = "faith-health-wellness-secret-2026"

# ------------------------------------------------------------
# PRODUCT DATA
# ------------------------------------------------------------
products = [
    {"code": "A014", "name": "Chrysanthemum Tea", "category": "Weight Management", "retail": 2760, "dist": 2300, "benefit": "Supports weight management and detox."},
    {"code": "A034", "name": "Peanut Sprout", "category": "Sleep Aid", "retail": 4860, "dist": 4050, "benefit": "Promotes restful sleep and relaxation."},
    {"code": "A066", "name": "Vitality Coffee", "category": "Men's Reproductive Health", "retail": 2100, "dist": 1750, "benefit": "Boosts men's vitality and reproductive health."},
    {"code": "A053", "name": "Chitosan", "category": "Men's Reproductive Health", "retail": 4080, "dist": 3400, "benefit": "Supports men's reproductive system and energy."},
    {"code": "A032", "name": "Saw Palmetto Polypeptide Capsule", "category": "Men's Reproductive Health", "retail": 4080, "dist": 3400, "benefit": "Promotes prostate health and male wellness."},
    {"code": "A043", "name": "Gyrophora Tea", "category": "Immune Boosters", "retail": 3480, "dist": 2900, "benefit": "Strengthens immune system and overall wellness."},
    {"code": "A045", "name": "Cordyceps Tea", "category": "Immune Boosters", "retail": 3480, "dist": 2900, "benefit": "Enhances immunity and energy levels."},
    {"code": "A060", "name": "Broken Ganoderma Capsules", "category": "Immune Boosters", "retail": 4860, "dist": 4050, "benefit": "Powerful immune support and antioxidant."},
    {"code": "A067", "name": "Reishi Coffee", "category": "Immune Boosters", "retail": 2460, "dist": 2050, "benefit": "Immunity-boosting coffee for daily wellness."},
    {"code": "A069", "name": "Cordyceps Coffee", "category": "Immune Boosters", "retail": 2460, "dist": 2050, "benefit": "Energy and immune support in every cup."},
    {"code": "A003", "name": "Isomalto", "category": "Digestive Health", "retail": 10560, "dist": 8800, "benefit": "Promotes healthy digestion and gut flora."},
    {"code": "A036", "name": "Toothpaste", "category": "Daily Usage", "retail": 912, "dist": 760, "benefit": "Natural oral care for daily freshness."},
    {"code": "A022", "name": "Fish Oil", "category": "Cerebrovascular Health", "retail": 4080, "dist": 3400, "benefit": "Supports brain and cardiovascular health."},
    {"code": "A044", "name": "Ginkgo Tea", "category": "Cerebrovascular Health", "retail": 3480, "dist": 2900, "benefit": "Improves memory and cerebrovascular health."},
    {"code": "A013", "name": "Antilipemic Tea", "category": "Cardiovascular Health", "retail": 2760, "dist": 2300, "benefit": "Helps maintain healthy cholesterol levels."},
    {"code": "A027", "name": "Propolis", "category": "Cardiovascular Health", "retail": 4080, "dist": 3400, "benefit": "Supports heart health and immunity."},
    {"code": "A059", "name": "Lecithin Soft Capsules", "category": "Cardiovascular Health", "retail": 4080, "dist": 3400, "benefit": "Promotes cardiovascular wellness."},
    {"code": "A029", "name": "Spirulina Tablets", "category": "Cardiovascular Health", "retail": 4080, "dist": 3400, "benefit": "Nutrient-rich superfood for heart health."},
    {"code": "A033", "name": "Salviae Miltiorrhizae", "category": "Cardiovascular Health", "retail": 4860, "dist": 4050, "benefit": "Supports healthy circulation and heart function."},
    {"code": "A056", "name": "Glucosamine Capsule", "category": "Bone & Joint Health", "retail": 4080, "dist": 3400, "benefit": "Supports joint flexibility and bone strength."},
    {"code": "A058", "name": "Natural Liquid Calcium Soft Capsules", "category": "Bone & Joint Health", "retail": 4080, "dist": 3400, "benefit": "Promotes strong bones and healthy joints."},
    {"code": "A023", "name": "NMN", "category": "Anti-Aging", "retail": 14700, "dist": 12200, "benefit": "Advanced anti-aging and cellular rejuvenation."},
]

# ------------------------------------------------------------
# CATEGORY METADATA (Includes 'slug' for URLs)
# ------------------------------------------------------------
category_meta = [
    {"name": "Immune Boosters", "slug": "immune-boosters", "icon": "fa-shield-virus",
     "description": "Strengthen your body's natural defenses with our immune-supporting teas, coffees, and capsules."},
    {"name": "Cardiovascular Health", "slug": "cardiovascular-health", "icon": "fa-heart-pulse",
     "description": "Support a healthy heart, circulation, and cholesterol levels with these targeted formulas."},
    {"name": "Bone & Joint Health", "slug": "bone-and-joint-health", "icon": "fa-bone",
     "description": "Maintain strong bones, flexible joints, and comfortable movement at every age."},
    {"name": "Men's Reproductive Health", "slug": "mens-reproductive-health", "icon": "fa-mars",
     "description": "Vitality, prostate support, and reproductive wellness formulated specifically for men."},
    {"name": "Cerebrovascular Health", "slug": "cerebrovascular-health", "icon": "fa-brain",
     "description": "Support memory, focus, and healthy blood flow to the brain."},
    {"name": "Digestive Health", "slug": "digestive-health", "icon": "fa-leaf",
     "description": "Promote gut balance, healthy digestion, and a flourishing microbiome."},
    {"name": "Weight Management", "slug": "weight-management", "icon": "fa-weight-scale",
     "description": "Gentle support for healthy weight goals and gentle daily detox."},
    {"name": "Sleep Aid", "slug": "sleep-aid", "icon": "fa-moon",
     "description": "Encourage restful, deep sleep so your body can restore itself."},
    {"name": "Daily Usage", "slug": "daily-usage", "icon": "fa-tooth",
     "description": "Everyday essentials for oral care and personal freshness."},
    {"name": "Anti-Aging", "slug": "anti-aging", "icon": "fa-hourglass-half",
     "description": "Advanced cellular support for healthy aging and long-term vitality."},
]

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def get_categories():
    present = {p["category"] for p in products}
    return [c for c in category_meta if c["name"] in present]

def group_products():
    grouped = {}
    for cat in get_categories():
        grouped[cat["name"]] = [p for p in products if p["category"] == cat["name"]]
    return grouped

def find_category_by_slug(slug):
    return next((c for c in category_meta if c["slug"] == slug), None)

def find_product(code):
    return next((p for p in products if p["code"] == code), None)

def get_cart():
    return session.get("cart", {})

def cart_items():
    cart = get_cart()
    items = []
    for code, qty in cart.items():
        p = find_product(code)
        if p:
            items.append({"product": p, "qty": qty, "subtotal": p["retail"] * qty})
    return items

def cart_totals():
    items = cart_items()
    total = sum(i["subtotal"] for i in items)
    count = sum(i["qty"] for i in items)
    return items, total, count

@app.context_processor
def inject_cart_count():
    cart = get_cart()
    return {"cart_count": sum(cart.values()) if cart else 0}

# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------
@app.route("/")
def home():
    cats = get_categories()
    for c in cats:
        c["count"] = len([p for p in products if p["category"] == c["name"]])
    return render_template("index.html", categories=cats, products=products)

@app.route("/products")
def products_page():
    return render_template("products.html", grouped=group_products(), categories=get_categories())

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = []
    if q:
        q_lower = q.lower()
        results = [
            p for p in products
            if q_lower in p["name"].lower()
            or q_lower in p["code"].lower()
            or q_lower in p["category"].lower()
            or q_lower in p["benefit"].lower()
        ]
    return render_template("search.html", query=q, results=results, categories=get_categories())

@app.route("/category/<slug>")
def category_page(slug):
    cat = find_category_by_slug(slug)
    if not cat:
        abort(404)
    cat_products = [p for p in products if p["category"] == cat["name"]]
    return render_template("category.html", category=cat, products=cat_products, categories=get_categories())

@app.route("/product/<code>")
def product_detail(code):
    product = find_product(code)
    if not product:
        abort(404)
    return render_template("product_detail.html", product=product)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/join")
def join():
    return render_template("join.html", products=products, categories=get_categories())

# ------------------------------------------------------------
# CART ROUTES
# ------------------------------------------------------------
@app.route("/cart/add/<code>", methods=["POST"])
def cart_add(code):
    p = find_product(code)
    if not p:
        abort(404)
    cart = get_cart()
    cart[code] = cart.get(code, 0) + 1
    session["cart"] = cart
    flash(f"{p['name']} added to your order.", "success")
    return redirect(request.referrer or url_for("products_page"))

@app.route("/cart/update", methods=["POST"])
def cart_update():
    cart = get_cart()
    for code in list(cart.keys()):
        qty = request.form.get(f"qty_{code}")
        if qty is not None:
            try:
                n = int(qty)
            except ValueError:
                n = 1
            if n <= 0:
                cart.pop(code, None)
            else:
                cart[code] = n
    session["cart"] = cart
    return redirect(url_for("cart_page"))

@app.route("/cart/remove/<code>", methods=["POST"])
def cart_remove(code):
    cart = get_cart()
    cart.pop(code, None)
    session["cart"] = cart
    return redirect(url_for("cart_page"))

@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    session["cart"] = {}
    return redirect(url_for("cart_page"))

@app.route("/cart")
def cart_page():
    items, total, count = cart_totals()
    return render_template("cart.html", items=items, total=total, count=count)

# ------------------------------------------------------------
# CHECKOUT / DELIVERY DETAILS
# ------------------------------------------------------------
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total, count = cart_totals()
    if not items:
        flash("Your order is empty. Please add a product first.", "error")
        return redirect(url_for("products_page"))

    if request.method == "POST":
        data = {
            "name":    request.form.get("name", "").strip(),
            "phone":   request.form.get("phone", "").strip(),
            "email":   request.form.get("email", "").strip(),
            "county":  request.form.get("county", "").strip(),
            "town":    request.form.get("town", "").strip(),
            "address": request.form.get("address", "").strip(),
            "notes":   request.form.get("notes", "").strip(),
        }
        
        delivery_fees = {
            "Mombasa": 250, "Kilifi": 300, "Kwale": 300, "Taita Taveta": 400,
            "Nairobi": 350, "Machakos": 350, "Kajiado": 350, "Kiambu": 350,
            "Nakuru": 400, "Uasin Gishu": 450, "Kisumu": 450,
            "Kisii": 450, "Kakamega": 450, "Nyeri": 400, "Meru": 450
        }
        delivery_fee = delivery_fees.get(data["county"], 500) 
        grand_total = total + delivery_fee

        required = ["name", "phone", "county", "town"]
        missing = [f for f in required if not data[f]]
        if missing:
            flash("Please fill in all required fields.", "error")
            return render_template("checkout.html", items=items, total=total, count=count, form=data)

        lines = []
        lines.append("Hello Madam Faith, I would like to place an order:")
        lines.append("")
        lines.append("*Order Summary*")
        for i in items:
            p = i["product"]
            lines.append(f"- {p['name']} ({p['code']}) x{i['qty']} = KES {i['subtotal']:,}")
        lines.append("")
        lines.append(f"Subtotal: KES {total:,}")
        lines.append(f"Delivery to {data['county']}: KES {delivery_fee:,}") 
        lines.append(f"*GRAND TOTAL: KES {grand_total:,}*") 
        lines.append("")
        lines.append("*Delivery Details*")
        lines.append(f"Name: {data['name']}")
        lines.append(f"Phone: {data['phone']}")
        if data["email"]:
            lines.append(f"Email: {data['email']}")
        lines.append(f"County: {data['county']}")
        lines.append(f"Town/Area: {data['town']}")
        if data["address"]:
            lines.append(f"Address/Landmark: {data['address']}")
        if data["notes"]:
            lines.append(f"Notes: {data['notes']}")
        lines.append("")
        lines.append("Please confirm availability and payment details. Thank you!")

        message = "\n".join(lines)
        wa_url = f"https://wa.me/254743599932?text={urllib.parse.quote(message)}"
        session["cart"] = {}
        
        return render_template("order_sent.html", wa_url=wa_url, data=data, total=grand_total)

    return render_template(
        "checkout.html",
        items=items, total=total, count=count,
        form={"name": "", "phone": "", "email": "", "county": "", "town": "", "address": "", "notes": ""},
    )

# ------------------------------------------------------------
# TEMPLATE FILTER
# ------------------------------------------------------------
@app.template_filter("whatsapp_link")
def whatsapp_link(product_name, product_code):
    text = f"Hello Madam Faith I want to order {product_name} ({product_code})"
    return f"https://wa.me/254743599932?text={urllib.parse.quote(text)}"

# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
