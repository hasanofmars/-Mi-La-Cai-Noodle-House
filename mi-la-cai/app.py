from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

# ── Menu Data ──────────────────────────────────────────────
menu_items = {
    "Appetizers": [
        {"name": "Crispy Fried Pork Egg Rolls", "price": 7.95, "desc": "Golden-fried pork and vegetable rolls served with nuoc cham", "tags": []},
        {"name": "Fresh Spring Rolls", "price": 6.95, "desc": "Shrimp, vermicelli, herbs & lettuce wrapped in rice paper", "tags": ["gluten-free"]},
        {"name": "Potstickers", "price": 8.95, "desc": "Pan-seared pork & vegetable dumplings with soy-ginger dip", "tags": []},
        {"name": "Cream Cheese Wontons", "price": 7.50, "desc": "Crispy wontons filled with cream cheese & crab", "tags": ["vegetarian"]},
        {"name": "Edamame", "price": 5.95, "desc": "Steamed soy beans tossed with sea salt", "tags": ["vegan", "gluten-free"]},
    ],
    "Pho & Noodle Soups": [
        {"name": "Beef Pho", "price": 12.95, "desc": "Rich beef broth with rice noodles, sliced rare beef, brisket & herbs", "tags": ["gluten-free"]},
        {"name": "Chicken Pho", "price": 11.95, "desc": "Aromatic chicken broth with shredded chicken & rice noodles", "tags": ["gluten-free"]},
        {"name": "Vegetable Pho", "price": 10.95, "desc": "Hearty vegetable broth with tofu, mushrooms & fresh greens", "tags": ["vegan", "gluten-free"]},
        {"name": "Wonton Egg Noodle Soup", "price": 12.50, "desc": "Pork & shrimp wontons in savory broth with egg noodles", "tags": []},
    ],
    "Vietnamese Entrees": [
        {"name": "Lemongrass Chicken", "price": 13.95, "desc": "Wok-seared chicken with lemongrass, chili & onions over jasmine rice", "tags": ["gluten-free"]},
        {"name": "Shaking Beef", "price": 16.95, "desc": "Tender cubed filet mignon wok-tossed with garlic & black pepper", "tags": ["gluten-free"]},
        {"name": "Caramelized Clay Pot Fish", "price": 14.95, "desc": "Catfish simmered in caramel sauce with black pepper & ginger", "tags": ["gluten-free"]},
        {"name": "Vermicelli Bowl", "price": 12.95, "desc": "Grilled pork, egg roll, fresh herbs & vermicelli over greens", "tags": []},
    ],
    "Chinese Comfort Dishes": [
        {"name": "Walnut Shrimp", "price": 15.95, "desc": "Crispy honey-glazed shrimp with candied walnuts", "tags": []},
        {"name": "House Stir-Fried Beef", "price": 14.95, "desc": "Tender beef strips wok-fried with seasonal vegetables", "tags": []},
        {"name": "Kung Pao Chicken", "price": 13.50, "desc": "Spicy Sichuan-style chicken with peanuts & dried chilis", "tags": []},
        {"name": "Sweet & Sour Pork", "price": 12.95, "desc": "Crispy battered pork in tangy sweet-sour sauce with pineapple", "tags": []},
        {"name": "Mapo Tofu", "price": 11.95, "desc": "Silken tofu in spicy Sichuan peppercorn sauce", "tags": ["vegan"]},
    ],
    "Vegetarian & Vegan": [
        {"name": "Buddha's Delight", "price": 12.95, "desc": "Mixed seasonal vegetables & tofu in light garlic sauce", "tags": ["vegan", "gluten-free"]},
        {"name": "Tofu Vermicelli Bowl", "price": 11.95, "desc": "Crispy lemongrass tofu with vermicelli, herbs & greens", "tags": ["vegan"]},
        {"name": "Vegetable Fried Rice", "price": 10.95, "desc": "Wok-fried jasmine rice with egg & garden vegetables", "tags": ["vegetarian"]},
    ],
    "Drinks": [
        {"name": "Vietnamese Iced Coffee", "price": 4.50, "desc": "Strong dark roast with sweetened condensed milk over ice", "tags": []},
        {"name": "Thai Iced Tea", "price": 4.50, "desc": "Creamy sweet tea with spices & condensed milk", "tags": []},
        {"name": "Fresh Limeade", "price": 3.95, "desc": "House-made with fresh-squeezed limes & cane sugar", "tags": ["vegan", "gluten-free"]},
        {"name": "Jasmine Hot Tea", "price": 2.95, "desc": "Fragrant loose-leaf jasmine green tea", "tags": ["vegan", "gluten-free"]},
        {"name": "Beer & Wine", "price": 5.00, "desc": "Rotating selection of domestic & imported beers and wines", "tags": []},
    ],
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html", menu_items=menu_items)


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
