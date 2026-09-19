import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# Create the Flask application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

class Movetype (db.Model):
    __tablename__ = "move_types"

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=false, unique=true)
   description = db.Column(db.Text)

class Services (db.Model):
    __tablename__ = "services"

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    duration_minutes = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(30))
    country_of_origin = db.Column(db.String(80), nullable=False, default="Brazil")
    move_type_id = db.Column(db.Integer, db.ForeignKey("move_types.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)    

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="scheduled")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    

reasons = [
    {
        "name": "Safety & Security",
        "icon": "🛡️",
        "description": "Ireland is one of the safest countries in Europe, with low crime rates and a welcoming, friendly society that makes "
        "newcomers feel at home quickly.",
        "highlights": [
            "Low crime rates",
            "Friendly local communities",
            "Stable political environment",
            "Strong social cohesion",
        ],
    },
    {
        "name": "Strong Job Market",
        "icon": "💼",
        "description": "With major tech, pharma and financial companies based in Ireland, finding a well-paid job is very achievable "
        "especially in Dublin and Cork.",
        "highlights": [
            "Big companies European HQ",
            "Low unemployment rate",
            "Competitive salaries" "Higher minimum wage",
        ],
    },
    {
        "name": "English Speaking Country",
        "icon": "🗣️",
        "description": "As an English-speaking nation, adapting to daily life, work and communication is much easier compared to other "
        "European countries.",
        "highlights": [
            "English as official language",
            "No language barrier at work",
            "Large international community",
            "Easy integration",
            "Access to global opportunities",
        ],
    },
    {
        "name": "Education System",
        "icon": "🎓",
        "description": "Ireland has a world-class education system with highly ranked universities, making it a great place for families "
        "with children or those looking to study further.",
        "highlights": [
            "Great Universities",
            "Strong primary and secondary schools",
            "International student friendly",
        ],
    },
    {
        "name": "Gateway to Europe",
        "icon": "✈️",
        "description": "Living in Ireland gives you easy access to travel across Europe. Weekend trips to Paris, Lisbon or Barcelona are just"
        " a short flight away.",
        "highlights": [
            "Dublin Airport — 180+ destinations",
            "Ryanair and Aer Lingus hubs",
            "EU member state",
            "Easy Schengen access",
        ],
    },
    {
        "name": "Quality of Life",
        "icon": "🌿",
        "description": "From clean air and green landscapes to excellent healthcare and social services, Ireland offers a high standard of "
        "living for those who settle here.",
        "highlights": [
            "Public healthcare through HSE",
            "Clean natural environment",
            "Strong work-life balance",
            "Flexible working culture",
            "Green spaces and outdoor lifestyle",
        ],
    },
]

tips = [
    "Open a bank account as soon as possible — AIB and Bank of Ireland are the most accessible for newcomers.",
    "Register with a GP (General Practitioner) shortly after arriving to access public healthcare through the HSE.",
    "Apply for your PPS Number (Personal Public Service Number) early — you will need it for work, taxes and public services.",
    "The Leap Card is the easiest and cheapest way to use public transport in Dublin — buses, trams and trains all in one card.",
    "Renting in Dublin is competitive and expensive — start your search before arriving and use Daft.ie as your main platform.",
    "Ireland operates on the PAYE tax system — make sure your employer registers you correctly to avoid overpaying tax.",
    "The weather in Ireland is unpredictable year-round — always carry a light waterproof jacket regardless of the season.",
    "Join local Facebook groups and community apps like Nextdoor to connect with other expats and find practical advice from people who have been through the same experience.",
]

# Each route maps a URL to a function that returns a page


# Home page - renders the main landing page
@app.route("/")
def home():
    return render_template("home.html")


# About page - renders the about me page
@app.route("/about")
def about():
    return render_template("about.html")


# Reasons page - passes the full reasons list to the template
@app.route("/reasons")
def reasons_page():
    return render_template("reasons.html", reasons=reasons)


# Reason detail - dynamic route that receives a name parameter
# Searches the reasons list for a matching name
# Returns 404 if no match is found
@app.route("/reason_detail/<name>")
def reason_detail(name):
    reason = next((r for r in reasons if r["name"].lower() == name.lower()), None)
    if reason is None:
        return "Reason not found", 404
    return render_template("reason_detail.html", reason=reason)


@app.route("/tips")
def tips_page():
    return render_template("tips.html", tips=tips)


# Contact page - handles both GET and POST requests
# GET: renders the empty form
# POST: processes the form data and validates input
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # Validate that all fields are filled in
        if not name or not email or not message:
            error = "Please fill in all fields."
            return render_template("contact.html", error=error)

        # If validation passes, show success message
        success = f"Thank you, {name}! Your message has been received."
        return render_template("contact.html", success=success)

    return render_template("contact.html")


# Run the app in debug mode during development
if __name__ == "__main__":
    app.run(debug=False)
