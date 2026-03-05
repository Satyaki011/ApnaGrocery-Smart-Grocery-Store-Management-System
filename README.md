ApnaGrocery is a web-based grocery store management system designed to help small shops manage their products, suppliers, inventory, and sales from a single dashboard.
This project is built using Python Flask and provides a clean interface for handling everyday store operations efficiently.
The goal of this project is to create a simple but powerful management system for grocery businesses and to practice full-stack web development using Flask.

🚀 Features
📊 Dashboard
The dashboard gives a quick overview of store activity:
Low stock alerts
Revenue tracking
Store activity overview
Quick navigation to store management tools

📦 Product Management
Manage all grocery items easily.
Add new products
Update product details
Track inventory stock
Monitor product availability

🚚 Supplier Management
Keep track of suppliers and purchase information.
Add supplier details
Store supplier contact number
Record purchase items
Track purchase prices

💰 Sales Tracking
Monitor daily store sales.
Record product sales
Track revenue
Analyze product movement

🤖 AI Assistant
Includes an experimental AI assistant module for generating insights and helping analyze store data.

🛠️ Tech Stack
Backend
Python
Flask
SQLAlchemy

Frontend
HTML
CSS
JavaScript

Database
SQLite

Tools
VS Code
Git
GitHub

📂 Project Structure
grosary_app
│
├── models
│   ├── __init__.py
│
├── routes
│   ├── auth.py
│   ├── products.py
│   ├── sales.py
│   └── suppliers.py
│
├── templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── suppliers.html
│   └── sales.html
│
├── static
│   └── css
│       └── style.css
│
├── app.py
├── config.py
├── requirements.txt
└── create_admin.py
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/apnagrocery.git
2️⃣ Go to project directory
cd apnagrocery
3️⃣ Create virtual environment
python -m venv venv
4️⃣ Activate virtual environment

Mac / Linux

source venv/bin/activate

Windows

venv\Scripts\activate
5️⃣ Install dependencies
pip install -r requirements.txt
6️⃣ Run the application
python app.py
7️⃣ Open in browser
http://127.0.0.1:5000
🎯 Project Purpose

This project was created to:
Practice Flask full-stack development
Build a real-world inventory system
Learn database integration
Create a modern dashboard UI

🔮 Future Improvements

Planned features:
Barcode scanner support
Payment system integration
Advanced analytics dashboard
Mobile responsive design
Multi-user role system

👨‍💻 Author
Satyaki
Computer Science Student
Developer | Builder | Learner
