# Qoresto-Food-Delivery-Analytics-System

Enterprise-grade Food Delivery \& Restaurant Analytics Platform built with Flask, Python, MySQL, HTML, CSS, JavaScript and Chart.js.





🍽️ Qoresto – Food Delivery \& Restaurant Analytics System





















🚀 Project Overview



Qoresto is a full-stack Food Delivery and Restaurant Analytics Platform inspired by modern food delivery applications.



The system enables customers to browse restaurants, order food, manage carts, track orders, submit ratings, and receive recommendations. It also provides a powerful Admin Dashboard with business analytics, sales reports, customer insights, and restaurant performance tracking.



This project demonstrates real-world implementation of:



Full Stack Web Development

Database Design

Business Analytics

Data Visualization

Customer Management

Restaurant Management

Order Processing

Reporting Systems

📸 Project Screens

Customer Module



✔ Home Page

✔ Restaurant Listing

✔ Restaurant Details

✔ Menu Management

✔ Cart Management

✔ Checkout System

✔ Order Tracking

✔ Order History

✔ Customer Profile

✔ Favorites

✔ Ratings \& Reviews



Admin Module



✔ Admin Login

✔ Admin Dashboard

✔ Restaurant Management

✔ User Management

✔ Orders Management

✔ Revenue Reports

✔ Customer Reports

✔ Restaurant Reports

✔ Reviews Analysis

✔ Analytics Dashboard



✨ Key Features

👤 Customer Features

Authentication

User Registration

User Login

Session Management

Profile Editing

Restaurant Browsing

Search Restaurants

Filter by Category

View Restaurant Details

Restaurant Ratings

Food Ordering

Dynamic Menu System

Add to Cart

Update Cart

Checkout Process

Order Placement

Order Management

Track Orders

View Order History

Reorder Previous Orders

Cancel Orders

Reviews \& Ratings

Submit Ratings

Write Reviews

View Customer Feedback

Personalized Experience

Favorite Restaurants

Food Recommendations

🏢 Admin Features

Dashboard KPIs

Total Revenue

Total Orders

Total Customers

Total Restaurants

Restaurant Management

Add Restaurant

Edit Restaurant

Delete Restaurant

Manage Restaurant Information

Order Analytics

Orders by Status

Daily Orders

Monthly Orders

Revenue Tracking

Customer Analytics

Customer Growth

Top Customers

Customer Reports

Restaurant Analytics

Top Performing Restaurants

Revenue Contribution

Restaurant Ratings

Review Analytics

Average Ratings

Customer Feedback Analysis

📊 Advanced Analytics Dashboard



The analytics dashboard includes interactive visualizations powered by Chart.js.



Revenue Analytics

Daily Revenue Trend

Monthly Revenue Trend

Revenue by Restaurant

Customer Analytics

New Customer Growth

Customer Activity Analysis

Restaurant Analytics

Top Restaurants

Restaurant Performance Comparison

Order Analytics

Order Status Distribution

Orders by Day

Orders by Month

🛠️ Technology Stack

Frontend

HTML5

CSS3

JavaScript

Chart.js

Responsive UI Design

Backend

Python

Flask Framework

Database

MySQL

Libraries

Flask

MySQL Connector

Werkzeug

Pandas

NumPy

🗄️ Database Design

Main Tables

Users

user\_id

username

email

password

Restaurants

restaurant\_id

restaurant\_name

city

cuisine

rating

Categories

category\_id

category\_name

Menu Items

item\_id

item\_name

price

category\_id

Orders

order\_id

user\_id

restaurant\_id

total\_amount

order\_status

Order Items

order\_item\_id

order\_id

item\_id

Payments

payment\_id

order\_id

payment\_method

Reviews

review\_id

user\_id

restaurant\_id

rating

review\_text

Admins

admin\_id

username

password

📂 Project Structure

Qoresto-Food-Delivery-Analytics-System/

│

├── app.py

├── db.py

├── requirements.txt

│

├── static/

│   ├── style.css

│   ├── script.js

│   ├── dashboard.js

│   └── displayRestaurants.js

│

├── templates/

│   ├── index.html

│   ├── login.html

│   ├── register.html

│   ├── restaurants.html

│   ├── menu.html

│   ├── cart.html

│   ├── checkout.html

│   ├── my\_orders.html

│   ├── track\_order.html

│   ├── admin.html

│   ├── analytics.html

│   └── more templates...

│

├── Qoresto\_report.xlsx

├── zomato\_report.xlsx

│

└── README.md

⚙️ Installation Guide

Clone Repository

git clone https://github.com/Sathishoffcial/Qoresto-Food-Delivery-Analytics-System.git

cd Qoresto-Food-Delivery-Analytics-System

Create Virtual Environment

python -m venv venv

Windows

venv\\Scripts\\activate

Linux/Mac

source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Configure Database



Create MySQL database:



CREATE DATABASE zomato\_db;



Update database credentials inside:



def get\_db\_connection():

&#x20;   return mysql.connector.connect(

&#x20;       host="localhost",

&#x20;       user="root",

&#x20;       password="YOUR\_PASSWORD",

&#x20;       database="zomato\_db"

&#x20;   )

Run Application

python app.py



Open:



http://127.0.0.1:5000

📈 Business Insights Generated



The system provides:



Revenue Analysis

Customer Growth Analysis

Restaurant Performance Tracking

Food Item Popularity

Customer Rating Analysis

Sales Trends

Order Trends

Business KPI Monitoring

🎯 Learning Outcomes



This project helped develop skills in:



Flask Development

MySQL Database Design

RESTful Routing

Authentication Systems

Dashboard Development

Data Analytics

Chart.js Visualization

SQL Query Optimization

Full Stack Development

Business Intelligence Reporting

🔮 Future Enhancements

AI Food Recommendation Engine

Online Payment Gateway Integration

Email Notifications

SMS Notifications

Real-time Order Tracking

Restaurant Owner Portal

Mobile Application

Cloud Deployment (AWS/Azure/GCP)

Machine Learning Sales Forecasting

Predictive Customer Analytics

👨‍💻 Author

Sathish A



📧 Email: sathishoff007@gmail.com



🔗 LinkedIn: www.linkedin.com/in/sathish-a-626a28323



💻 GitHub: https://github.com/Sathishoffcial

&#x20;  

&#x20;  contact number:+91 8682016989



⭐ Project Highlights



✔ 45+ HTML Templates

✔ Full CRUD Operations

✔ Authentication System

✔ Food Ordering Workflow

✔ Restaurant Management

✔ Analytics Dashboard

✔ Reporting System

✔ MySQL Integration

✔ Responsive UI Design

✔ Real-world Business Use Case



If you found this project useful, please ⭐ the repository and connect with me on LinkedIn. 🚀

