from datetime import datetime
import json
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

# ── JSON Data Helpers ─────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "admin_data.json")

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Auth Decorator ────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# ── Menu Data ──────────────────────────────────────────────
menu_items = {
    "Appetizers 🥟": [
        {"name": "Crispy Fried Pork Egg Rolls", "price": 7.95, "desc": "Golden-fried pork and vegetable rolls served with nuoc cham", "tags": [], "badge": "🔥 Bestseller", "spice": 0, "img": "/static/img/menu/crispy-fried-pork-egg-rolls.jpg"},
        {"name": "Fresh Spring Rolls", "price": 6.95, "desc": "Shrimp, vermicelli, herbs & lettuce wrapped in rice paper", "tags": ["gluten-free"], "badge": "", "spice": 0, "img": "/static/img/menu/fresh-spring-rolls.jpg"},
        {"name": "Potstickers", "price": 8.95, "desc": "Pan-seared pork & vegetable dumplings with soy-ginger dip", "tags": [], "badge": "⭐ Popular", "spice": 0, "img": "/static/img/menu/potstickers.jpg"},
        {"name": "Cream Cheese Wontons", "price": 7.50, "desc": "Crispy wontons filled with cream cheese & crab", "tags": ["vegetarian"], "badge": "", "spice": 0, "img": "/static/img/menu/cream-cheese-wontons.jpg"},
        {"name": "Edamame", "price": 5.95, "desc": "Steamed soy beans tossed with sea salt", "tags": ["vegan", "gluten-free"], "badge": "", "spice": 0, "img": "/static/img/menu/edamame.jpg"},
    ],
    "Pho & Noodle Soups 🍜": [
        {"name": "Beef Pho", "price": 12.95, "desc": "Rich beef broth with rice noodles, sliced rare beef, brisket & herbs", "tags": ["gluten-free"], "badge": "👑 Signature", "spice": 1, "img": "/static/img/menu/beef-pho.jpg"},
        {"name": "Chicken Pho", "price": 11.95, "desc": "Aromatic chicken broth with shredded chicken & rice noodles", "tags": ["gluten-free"], "badge": "", "spice": 0, "img": "/static/img/menu/chicken-pho.jpg"},
        {"name": "Vegetable Pho", "price": 10.95, "desc": "Hearty vegetable broth with tofu, mushrooms & fresh greens", "tags": ["vegan", "gluten-free"], "badge": "🌱 Healthy", "spice": 0, "img": "/static/img/menu/vegetable-pho.jpg"},
        {"name": "Wonton Egg Noodle Soup", "price": 12.50, "desc": "Pork & shrimp wontons in savory broth with egg noodles", "tags": [], "badge": "⭐ Popular", "spice": 0, "img": "/static/img/menu/wonton-egg-noodle-soup.jpg"},
    ],
    "Vietnamese Entrees 🇻🇳": [
        {"name": "Lemongrass Chicken", "price": 13.95, "desc": "Wok-seared chicken with lemongrass, chili & onions over jasmine rice", "tags": ["gluten-free"], "badge": "", "spice": 2, "img": "/static/img/menu/lemongrass-chicken.jpg"},
        {"name": "Shaking Beef", "price": 16.95, "desc": "Tender cubed filet mignon wok-tossed with garlic & black pepper", "tags": ["gluten-free"], "badge": "🔥 Bestseller", "spice": 0, "img": "/static/img/menu/shaking-beef.jpg"},
        {"name": "Caramelized Clay Pot Fish", "price": 14.95, "desc": "Catfish simmered in caramel sauce with black pepper & ginger", "tags": ["gluten-free"], "badge": "", "spice": 1, "img": "/static/img/menu/caramelized-clay-pot-fish.jpg"},
        {"name": "Vermicelli Bowl", "price": 12.95, "desc": "Grilled pork, egg roll, fresh herbs & vermicelli over greens", "tags": [], "badge": "⭐ Popular", "spice": 1, "img": "/static/img/menu/vermicelli-bowl.jpg"},
    ],
    "Chinese Comfort Dishes 🥡": [
        {"name": "Walnut Shrimp", "price": 15.95, "desc": "Crispy honey-glazed shrimp with candied walnuts", "tags": [], "badge": "👑 Signature", "spice": 0, "img": "/static/img/menu/walnut-shrimp.jpg"},
        {"name": "House Stir-Fried Beef", "price": 14.95, "desc": "Tender beef strips wok-fried with seasonal vegetables", "tags": [], "badge": "🔥 Bestseller", "spice": 1, "img": "/static/img/menu/house-stir-fried-beef.jpg"},
        {"name": "Kung Pao Chicken", "price": 13.50, "desc": "Spicy Sichuan-style chicken with peanuts & dried chilis", "tags": [], "badge": "🌶️ Spicy", "spice": 3, "img": "/static/img/menu/kung-pao-chicken.jpg"},
        {"name": "Sweet & Sour Pork", "price": 12.95, "desc": "Crispy battered pork in tangy sweet-sour sauce with pineapple", "tags": [], "badge": "", "spice": 0, "img": "/static/img/menu/sweet-sour-pork.jpg"},
        {"name": "Mapo Tofu", "price": 11.95, "desc": "Silken tofu in spicy Sichuan peppercorn sauce", "tags": ["vegan"], "badge": "🌶️ Spicy", "spice": 3, "img": "/static/img/menu/mapo-tofu.jpg"},
    ],
    "Vegetarian & Vegan 🥬": [
        {"name": "Buddha's Delight", "price": 12.95, "desc": "Mixed seasonal vegetables & tofu in light garlic sauce", "tags": ["vegan", "gluten-free"], "badge": "🌱 Healthy", "spice": 0, "img": "/static/img/menu/buddhas-delight.jpg"},
        {"name": "Tofu Vermicelli Bowl", "price": 11.95, "desc": "Crispy lemongrass tofu with vermicelli, herbs & greens", "tags": ["vegan"], "badge": "", "spice": 1, "img": "/static/img/menu/tofu-vermicelli-bowl.jpg"},
        {"name": "Vegetable Fried Rice", "price": 10.95, "desc": "Wok-fried jasmine rice with egg & garden vegetables", "tags": ["vegetarian"], "badge": "⭐ Popular", "spice": 0, "img": "/static/img/menu/vegetable-fried-rice.jpg"},
    ],
    "Drinks 🍹": [
        {"name": "Vietnamese Iced Coffee", "price": 4.50, "desc": "Strong dark roast with sweetened condensed milk over ice", "tags": [], "badge": "👑 Signature", "spice": 0, "img": "/static/img/menu/vietnamese-iced-coffee.jpg"},
        {"name": "Thai Iced Tea", "price": 4.50, "desc": "Creamy sweet tea with spices & condensed milk", "tags": [], "badge": "⭐ Popular", "spice": 0, "img": "/static/img/menu/thai-iced-tea.jpg"},
        {"name": "Fresh Limeade", "price": 3.95, "desc": "House-made with fresh-squeezed limes & cane sugar", "tags": ["vegan", "gluten-free"], "badge": "", "spice": 0, "img": "/static/img/menu/fresh-limeade.jpg"},
        {"name": "Jasmine Hot Tea", "price": 2.95, "desc": "Fragrant loose-leaf jasmine green tea", "tags": ["vegan", "gluten-free"], "badge": "", "spice": 0, "img": "/static/img/menu/jasmine-hot-tea.jpg"},
        {"name": "Beer & Wine", "price": 5.00, "desc": "Rotating selection of domestic & imported beers and wines", "tags": [], "badge": "", "spice": 0, "img": "/static/img/menu/beer-wine.jpg"},
    ],
}

MENU_FILE = os.path.join(os.path.dirname(__file__), "menu_data.json")

def load_menu():
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return menu_items

def save_menu(data):
    with open(MENU_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/")
def home():
    data = load_data()
    return render_template("index.html", data=data)


@app.route("/menu")
def menu():
    return render_template("menu.html", menu_items=load_menu())


@app.route("/contact")
def contact():
    data = load_data()
    return render_template("contact.html", data=data)


# ══════════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ══════════════════════════════════════════════════════════════

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        data = load_data()
        admin = data.get("admin", {})
        if request.form["username"] == admin.get("username") and request.form["password"] == admin.get("password"):
            session["admin_logged_in"] = True
            flash("Welcome back!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out", "info")
    return redirect(url_for("admin_login"))


@app.route("/admin/")
@login_required
def admin_dashboard():
    data = load_data()
    return render_template("admin/dashboard.html", data=data)


@app.route("/admin/edit/site", methods=["GET", "POST"])
@login_required
def admin_edit_site():
    data = load_data()
    if request.method == "POST":
        data["site"] = {
            "name": request.form["name"],
            "tagline": request.form["tagline"],
            "address": request.form["address"],
            "phone": request.form["phone"],
            "phone_link": request.form["phone_link"],
            "email": request.form["email"],
            "rating": request.form["rating"],
            "reviews": request.form["reviews"],
            "since": request.form["since"],
            "description": request.form["description"]
        }
        save_data(data)
        flash("Site info updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_site.html", data=data)


@app.route("/admin/edit/hero", methods=["GET", "POST"])
@login_required
def admin_edit_hero():
    data = load_data()
    if request.method == "POST":
        data["hero"] = {
            "badge_text": request.form["badge_text"],
            "badge_detail": request.form["badge_detail"],
            "badge_year": request.form["badge_year"],
            "subtitle": request.form["subtitle"],
            "title_line1": request.form["title_line1"],
            "title_line2_prefix": request.form["title_line2_prefix"],
            "title_line2_accent": request.form["title_line2_accent"],
            "description": request.form["description"],
            "cta_primary": request.form["cta_primary"],
            "cta_secondary": request.form["cta_secondary"],
            "tags": [{"icon": t.split("|")[0], "text": t.split("|")[1], "color": t.split("|")[2]} for t in request.form.getlist("tags")]
        }
        save_data(data)
        flash("Hero section updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_hero.html", data=data)


@app.route("/admin/edit/stats", methods=["GET", "POST"])
@login_required
def admin_edit_stats():
    data = load_data()
    if request.method == "POST":
        stats = []
        for i in range(len(request.form.getlist("num"))):
            stats.append({
                "num": request.form.getlist("num")[i],
                "suf": request.form.getlist("suf")[i],
                "label": request.form.getlist("label")[i],
                "icon": request.form.getlist("icon")[i]
            })
        data["stats"] = stats
        save_data(data)
        flash("Stats updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_stats.html", data=data)


@app.route("/admin/edit/menu", methods=["GET", "POST"])
@login_required
def admin_edit_menu():
    if request.method == "POST":
        categories = request.form.getlist("category")
        names = request.form.getlist("name")
        prices = request.form.getlist("price")
        descs = request.form.getlist("desc")
        badges = request.form.getlist("badge")
        spices = request.form.getlist("spice")
        tags_list = request.form.getlist("tags")
        imgs = request.form.getlist("img")
        
        menu = {}
        current_cat = None
        for i in range(len(names)):
            cat = categories[i]
            if cat:
                current_cat = cat
                menu[current_cat] = []
            if current_cat and names[i]:
                menu[current_cat].append({
                    "name": names[i],
                    "price": float(prices[i]) if prices[i] else 0,
                    "desc": descs[i],
                    "tags": [t.strip() for t in tags_list[i].split(",") if t.strip()] if i < len(tags_list) else [],
                    "badge": badges[i] if i < len(badges) else "",
                    "spice": int(spices[i]) if i < len(spices) and spices[i] else 0,
                    "img": imgs[i] if i < len(imgs) and imgs[i] else ""
                })
        save_menu(menu)
        flash("Menu updated!", "success")
        return redirect(url_for("admin_dashboard"))
    
    menu = load_menu()
    return render_template("admin/edit_menu.html", menu=menu, categories=list(menu.keys()))


@app.route("/admin/edit/story", methods=["GET", "POST"])
@login_required
def admin_edit_story():
    data = load_data()
    if request.method == "POST":
        data["story"] = {
            "section_title": request.form["section_title"],
            "title_line1": request.form["title_line1"],
            "title_line2": request.form["title_line2"],
            "paragraphs": [p for p in request.form.getlist("paragraphs") if p],
            "features": [{"icon": f.split("||")[0], "color": f.split("||")[1], "text": f.split("||")[2]} for f in request.form.getlist("features")],
            "cta_text": request.form["cta_text"],
            "award_text": request.form["award_text"],
            "award_subtext": request.form["award_subtext"],
            "image": request.form["image"]
        }
        save_data(data)
        flash("Story section updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_story.html", data=data)


@app.route("/admin/edit/testimonials", methods=["GET", "POST"])
@login_required
def admin_edit_testimonials():
    data = load_data()
    if request.method == "POST":
        testimonials = []
        for i in range(len(request.form.getlist("name"))):
            testimonials.append({
                "stars": request.form.getlist("stars")[i],
                "quote": request.form.getlist("quote")[i],
                "name": request.form.getlist("name")[i],
                "initial": request.form.getlist("initial")[i],
                "gradient": request.form.getlist("gradient")[i]
            })
        data["testimonials"] = testimonials
        save_data(data)
        flash("Testimonials updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_testimonials.html", data=data)


@app.route("/admin/edit/gallery", methods=["GET", "POST"])
@login_required
def admin_edit_gallery():
    data = load_data()
    if request.method == "POST":
        gallery = []
        for i in range(len(request.form.getlist("img"))):
            gallery.append({
                "img": request.form.getlist("img")[i],
                "caption": request.form.getlist("caption")[i],
                "span": request.form.getlist("span")[i]
            })
        data["gallery"] = gallery
        save_data(data)
        flash("Gallery updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_gallery.html", data=data)


@app.route("/admin/edit/hours", methods=["GET", "POST"])
@login_required
def admin_edit_hours():
    data = load_data()
    if request.method == "POST":
        hours = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            hours[day] = request.form.get(day, "")
        data["hours"] = hours
        save_data(data)
        flash("Hours updated!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/edit_hours.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
