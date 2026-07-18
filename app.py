from flask import Flask, render_template, jsonify, request, redirect, session
from db import get_db_connection
import mysql.connector
from reportlab.pdfgen import canvas
import pandas as pd
from flask import send_file
from openpyxl import Workbook
from io import BytesIO
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import sqlite3
from functools import wraps

import os
import mysql.connector

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'admin_id' not in session:
            return redirect('/admin_login')

        return f(*args, **kwargs)

    return decorated_function




# Home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


# Get All Restaurants
@app.route('/restaurants')
def get_restaurants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT *
                   FROM restaurants
                   """)

    restaurants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'restaurants.html',
        restaurants=restaurants
    )



# Restaurant Details
@app.route('/restaurant/<int:id>')
def restaurant_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT *
                   FROM restaurants
                   WHERE restaurant_id = %s
                   """, (id,))

    restaurant = cursor.fetchone()

    return render_template(
        "restaurant_details.html",
        restaurant=restaurant
    )



# Add Restaurant Page
@app.route('/add')
def add_page():
    return render_template('add_restaurant.html')


# Save Restaurant
@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO restaurants
        (
            restaurant_name,
            city,
            cuisine,
            rating,
            cost_for_two,
            image_url
        )
        VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (
        request.form['restaurant_name'],
        request.form['city'],
        request.form['cuisine'],
        request.form['rating'],
        request.form['cost_for_two'],
        request.form['image_url']
    ))

    conn.commit()
    conn.close()

    return redirect('/user_dashboard')


# Delete Restaurant
@app.route('/delete/<int:id>')
def delete_restaurant(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM restaurants WHERE restaurant_id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/home')


# Edit Restaurant
@app.route('/edit/<int:id>')
def edit_page(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM restaurants WHERE restaurant_id=%s",
        (id,)
    )

    restaurant = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_restaurant.html',
        restaurant=restaurant
    )


# Update Restaurant
@app.route('/update/<int:id>', methods=['POST'])
def update_restaurant(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE restaurants
        SET restaurant_name=%s,
            city=%s,
            cuisine=%s,
            rating=%s,
            cost_for_two=%s,
            image_url=%s
        WHERE restaurant_id=%s
    """,
    (
        request.form['restaurant_name'],
        request.form['city'],
        request.form['cuisine'],
        request.form['rating'],
        request.form['cost_for_two'],
        request.form['image_url'],
        id
    ))

    conn.commit()
    conn.close()

    return redirect('/user_dashboard')


# Search Restaurant

@app.route('/dashboard')
def dashboard():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        # =====================
        # Restaurant KPIs
        # =====================

        cursor.execute("SELECT COUNT(*) total_restaurants FROM restaurants")
        total_restaurants = cursor.fetchone()['total_restaurants']

        cursor.execute("SELECT AVG(rating) avg_rating FROM restaurants")
        avg_rating = cursor.fetchone()['avg_rating']

        cursor.execute("SELECT MAX(rating) highest_rating FROM restaurants")
        highest_rating = cursor.fetchone()['highest_rating']

        cursor.execute("SELECT COUNT(DISTINCT city) total_cities FROM restaurants")
        total_cities = cursor.fetchone()['total_cities']

        # =====================
        # Orders KPI
        # =====================

        cursor.execute("SELECT COUNT(*) total_orders FROM orders")
        total_orders = cursor.fetchone()['total_orders']

        cursor.execute("""
                       SELECT COUNT(*) delivered_orders
                       FROM orders
                       WHERE order_status = 'Delivered'
                       """)
        delivered_orders = cursor.fetchone()['delivered_orders']

        cursor.execute("""
                       SELECT COUNT(*) cancelled_orders
                       FROM orders
                       WHERE order_status = 'Cancelled'
                       """)
        cancelled_orders = cursor.fetchone()['cancelled_orders']

        cursor.execute("""
                       SELECT COUNT(*) pending_orders
                       FROM orders
                       WHERE order_status = 'Order Placed'
                       """)
        pending_orders = cursor.fetchone()['pending_orders']

        # =====================
        # Users KPI
        # =====================

        cursor.execute("SELECT COUNT(*) total_users FROM users")
        total_users = cursor.fetchone()['total_users']

        # =====================
        # Revenue KPI
        # =====================

        cursor.execute("""
                       SELECT IFNULL(SUM(amount), 0) revenue
                       FROM payments
                       WHERE payment_status = 'Success'
                       """)
        revenue = cursor.fetchone()['revenue']

        cursor.execute("""
                       SELECT IFNULL(SUM(amount), 0) today_revenue
                       FROM payments
                       WHERE DATE (payment_date)=CURDATE()
                         AND payment_status='Success'
                       """)
        today_revenue = cursor.fetchone()['today_revenue']

        cursor.execute("""
                       SELECT IFNULL(AVG(total_amount), 0) avg_order_value
                       FROM orders
                       """)
        avg_order_value = cursor.fetchone()['avg_order_value']

        # =====================
        # Extra KPIs
        # =====================

        cursor.execute("SELECT COUNT(*) total_payments FROM payments")
        total_payments = cursor.fetchone()['total_payments']

        cursor.execute("SELECT COUNT(*) total_reviews FROM reviews")
        total_reviews = cursor.fetchone()['total_reviews']

        cursor.execute("SELECT COUNT(*) total_favorites FROM favorites")
        total_favorites = cursor.fetchone()['total_favorites']

        cursor.execute("SELECT COUNT(*) total_menu_items FROM menu_items")
        total_menu_items = cursor.fetchone()['total_menu_items']

        # =====================
        # Cuisine Chart
        # =====================

        cursor.execute("""
                       SELECT cuisine, COUNT(*) total
                       FROM restaurants
                       GROUP BY cuisine
                       """)

        cuisine_data = cursor.fetchall()

        labels = []
        values = []

        for row in cuisine_data:
            labels.append(row['cuisine'])
            values.append(row['total'])

        # =====================
        # Top Selling Items
        # =====================

        cursor.execute("""
                       SELECT m.item_name,
                              SUM(oi.quantity) total_qty
                       FROM order_items oi
                                JOIN menu_items m
                                     ON oi.item_id = m.item_id
                       GROUP BY m.item_name
                       ORDER BY total_qty DESC LIMIT 5
                       """)

        top_items = cursor.fetchall()

        item_labels = []
        item_values = []

        for row in top_items:
            item_labels.append(row['item_name'])
            item_values.append(row['total_qty'])

        # =====================
        # Order Status
        # =====================

        cursor.execute("""
                       SELECT order_status,
                              COUNT(*) total
                       FROM orders
                       GROUP BY order_status
                       """)

        status_data = cursor.fetchall()

        status_labels = []
        status_values = []

        for row in status_data:
            status_labels.append(row['order_status'])
            status_values.append(row['total'])

        # =====================
        # Monthly Revenue
        # =====================

        cursor.execute("""
                       SELECT DATE_FORMAT(payment_date, '%Y-%m') month,
                              SUM(amount) revenue
                       FROM payments
                       WHERE payment_status = 'Success'
                       GROUP BY month
                       ORDER BY month
                       """)

        monthly_data = cursor.fetchall()

        months = []
        revenues = []

        for row in monthly_data:
            months.append(row['month'])
            revenues.append(float(row['revenue']))

        # =====================
        # Top Restaurants
        # =====================

        cursor.execute("""
                       SELECT r.restaurant_name,
                              COUNT(o.order_id) total_orders
                       FROM orders o
                                JOIN restaurants r
                                     ON o.restaurant_id = r.restaurant_id
                       GROUP BY r.restaurant_name
                       ORDER BY total_orders DESC LIMIT 5
                       """)

        top_restaurants = cursor.fetchall()

        restaurant_labels = []
        restaurant_values = []

        for row in top_restaurants:
            restaurant_labels.append(row['restaurant_name'])
            restaurant_values.append(row['total_orders'])

        # =====================
        # Top Customers
        # =====================

        cursor.execute("""
                       SELECT u.name,
                              COUNT(o.order_id) total_orders
                       FROM orders o
                                JOIN users u
                                     ON o.user_id = u.user_id
                       GROUP BY u.name
                       ORDER BY total_orders DESC LIMIT 5
                       """)

        top_customers = cursor.fetchall()

        customer_labels = []
        customer_values = []

        for row in top_customers:
            customer_labels.append(row['name'])
            customer_values.append(row['total_orders'])

        # =====================
        # Payment Status
        # =====================

        cursor.execute("""
                       SELECT payment_status,
                              COUNT(*) total
                       FROM payments
                       GROUP BY payment_status
                       """)

        payment_data = cursor.fetchall()

        payment_labels = []
        payment_values = []

        for row in payment_data:
            payment_labels.append(row['payment_status'])
            payment_values.append(row['total'])

        # =====================
        # Recent Orders
        # =====================

        cursor.execute("""
                       SELECT order_id,
                              order_status,
                              total_amount,
                              order_date
                       FROM orders
                       ORDER BY order_date DESC LIMIT 10
                       """)

        recent_orders = cursor.fetchall()

        print("restaurant_labels =", restaurant_labels)
        print("customer_labels =", customer_labels)
        print("payment_labels =", payment_labels)
        print("months =", months)
        cursor.execute("""
                       SELECT order_id,
                              order_status,
                              total_amount,
                              order_date
                       FROM orders
                       ORDER BY order_date DESC LIMIT 10
                       """)

        recent_orders = cursor.fetchall()
        # Orders by date

        cursor.execute("""
                       SELECT DATE (order_date) as day, COUNT(*) as total
                       FROM orders
                       GROUP BY day
                       ORDER BY day
                       """)

        orders_data = cursor.fetchall()

        order_dates = [str(row['day']) for row in orders_data]
        order_counts = [row['total'] for row in orders_data]
        cursor.execute("""
                       SELECT DATE (payment_date) as day, SUM(amount) as revenue
                       FROM payments
                       GROUP BY day
                       ORDER BY day
                       """)

        revenue_data = cursor.fetchall()

        revenue_dates = [str(row['day']) for row in revenue_data]
        revenues = [float(row['revenue']) for row in revenue_data]

        cursor.execute("""
                       SELECT order_status,
                              COUNT(*) total
                       FROM orders
                       GROUP BY order_status
                       """)

        status_data = cursor.fetchall()

        status_labels = [row['order_status'] for row in status_data]
        status_values = [row['total'] for row in status_data]

        cursor.execute("""
                       SELECT rating,
                              COUNT(*) total
                       FROM reviews
                       GROUP BY rating
                       ORDER BY rating
                       """)

        rating_data = cursor.fetchall()

        rating_labels = [str(row['rating']) for row in rating_data]
        rating_values = [row['total'] for row in rating_data]
        cursor.close()
        conn.close()

        return render_template(
            'dashboard.html',

            total_restaurants=total_restaurants,
            avg_rating=avg_rating,
            highest_rating=highest_rating,
            total_cities=total_cities,

            total_orders=total_orders,
            delivered_orders=delivered_orders,
            cancelled_orders=cancelled_orders,
            pending_orders=pending_orders,

            total_users=total_users,
            revenue=revenue,
            today_revenue=today_revenue,
            avg_order_value=avg_order_value,

            total_payments=total_payments,
            total_reviews=total_reviews,
            total_favorites=total_favorites,
            total_menu_items=total_menu_items,

            labels=labels,
            values=values,

            item_labels=item_labels,
            item_values=item_values,

            status_labels=status_labels,
            status_values=status_values,

            months=months,
            revenues=revenues,

            top_restaurants=top_restaurants,
            restaurant_labels=restaurant_labels,
            restaurant_values=restaurant_values,

            customer_labels=customer_labels,
            customer_values=customer_values,

            payment_labels=payment_labels,
            payment_values=payment_values,

            recent_orders=recent_orders,
            order_dates=order_dates,
            order_counts=order_counts,

            revenue_dates=revenue_dates,


            rating_labels=rating_labels,
            rating_values=rating_values
        )


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT m.item_id,
                          m.item_name,
                          m.price,
                          c.category_name,
                          r.restaurant_name
                   FROM menu_items m
                            LEFT JOIN categories c
                                      ON m.category_id = c.category_id
                            LEFT JOIN restaurants r
                                      ON m.restaurant_id = r.restaurant_id
                   WHERE m.restaurant_id = %s
                   """, (restaurant_id,))

    items = cursor.fetchall()

    cursor.execute("""
                   SELECT category_name
                   FROM categories
                   """)
    categories = cursor.fetchall()

    print("Restaurant ID =", restaurant_id)
    print("Items Found =", len(items))

    conn.close()

    return render_template(
        'menu.html',
        items=items,
        categories=categories,
        search=""
    )
@app.route('/reviews/<int:restaurant_id>')
def reviews_page(restaurant_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT review_id,
               rating,
               review_text
        FROM reviews
        WHERE restaurant_id=%s
    """, (restaurant_id,))

    reviews = cursor.fetchall()

    conn.close()

    return render_template(
        'reviews.html',
        reviews=reviews,
        restaurant_id=restaurant_id
    )
@app.route('/add_review/<int:restaurant_id>', methods=['POST'])
def add_review(restaurant_id):

    rating = request.form['rating']
    review_text = request.form['review_text']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews
        (
            user_id,
            restaurant_id,
            rating,
            review_text
        )
        VALUES (%s,%s,%s,%s)
    """,
    (
        1,
        restaurant_id,
        rating,
        review_text
    ))

    conn.commit()
    conn.close()

    return redirect(f'/reviews/{restaurant_id}')

@app.route('/reviews')
def reviews():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            review_id,
            users.name,
            restaurants.restaurant_name,
            reviews.rating,
            reviews.review_text
        FROM reviews

        JOIN users
        ON reviews.user_id = users.user_id

        JOIN restaurants
        ON reviews.restaurant_id = restaurants.restaurant_id
    """)

    reviews = cursor.fetchall()

    conn.close()

    return render_template(
        'reviews.html',
        reviews=reviews
    )
@app.route('/users')
def users():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return render_template(
        'users.html',
        users=users
    )

@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/admin_login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_restaurants FROM restaurants")
    total_restaurants = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_orders FROM orders")
    total_orders = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_reviews FROM reviews")
    total_reviews = cursor.fetchone()

    # Replace total_amount with your actual revenue column name
    cursor.execute("""
        SELECT SUM(amount) AS total_revenue
        FROM payments
    """)
    total_revenue = cursor.fetchone()
    cursor.execute("""
                   SELECT u.name,
                          COUNT(o.order_id) total_orders
                   FROM orders o
                            JOIN users u
                                 ON o.user_id = u.user_id
                   GROUP BY u.name
                   ORDER BY total_orders DESC LIMIT 5
                   """)

    top_customers = cursor.fetchall()
    cursor.execute("""
                   SELECT r.restaurant_name,
                          SUM(o.total_amount) revenue
                   FROM orders o
                            JOIN restaurants r
                                 ON o.restaurant_id = r.restaurant_id
                   GROUP BY r.restaurant_name
                   ORDER BY revenue DESC LIMIT 5
                   """)

    top_revenue_restaurants = cursor.fetchall()
    restaurant_names = []
    restaurant_revenues = []

    for row in top_revenue_restaurants:
        restaurant_names.append(row['restaurant_name'])
        restaurant_revenues.append(float(row['revenue'] or 0))
    cursor.close()
    conn.close()

    return render_template(
        'admin.html',
        total_users=total_users,
        total_restaurants=total_restaurants,
        total_orders=total_orders,
        total_reviews=total_reviews,
        total_revenue=total_revenue,
        top_customers=top_customers,
        restaurant_names=restaurant_names,
        restaurant_labels=restaurant_names,
        restaurant_revenues=restaurant_revenues

    )

from flask import render_template, request

@app.route('/orders')
@login_required
def orders():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    search = request.args.get('search')

    if search:

        cursor.execute("""
            SELECT
                orders.order_id,
                users.name,
                restaurants.restaurant_name,
                orders.order_status,
                orders.order_date
            FROM orders
            JOIN users
                ON orders.user_id = users.user_id
            JOIN restaurants
                ON orders.restaurant_id = restaurants.restaurant_id
            WHERE users.name LIKE %s
        """, ('%' + search + '%',))

    else:

        cursor.execute("""
            SELECT
                orders.order_id,
                users.name,
                restaurants.restaurant_name,
                orders.order_status,
                orders.order_date
            FROM orders
            JOIN users
                ON orders.user_id = users.user_id
            JOIN restaurants
                ON orders.restaurant_id = restaurants.restaurant_id
        """)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'orders.html',
        orders=orders
    )
@app.route('/menu')
def menu():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT m.item_id,
                          m.item_name,
                          m.price,
                          r.restaurant_name
                   FROM menu_items m
                            JOIN restaurants r
                                 ON m.restaurant_id = r.restaurant_id
                   """)

    items = cursor.fetchall()

    conn.close()

    return render_template(
        "menu.html",
        items=items,
        categories=[],
        search=""
    )

@app.route('/payments')
@admin_required
def payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT *
                   FROM payments
                   ORDER BY payment_id DESC
                   """)
    payments = cursor.fetchall()

    cursor.execute("""
                   SELECT SUM(amount) AS revenue
                   FROM payments
                   WHERE payment_status = 'Success'
                   """)
    revenue = cursor.fetchone()['revenue']

    cursor.close()
    conn.close()

    return render_template(
        'payments.html',
        payments=payments,
        revenue=revenue
    )
@app.route('/payment-success', methods=['GET', 'POST'])
def payment_success():

    import random
    order_id = "ORD" + str(random.randint(100000, 999999))

    cart_items = session.get('cart', [])
    total_amount = session.get('total', 0)

    # convert items to string (simple way)
    items_str = str(cart_items)

    # insert into DB
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="nithish@004",
        database="qoresto"
    )
    cursor = conn.cursor()

    query = """
    INSERT INTO payments
(order_id, payment_method, amount, payment_status)
VALUES (%s,%s,%s,'Success')"""

    values = (
        order_id,
        "Guest User",
        total_amount
    )

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    session.pop('cart', None)

    return render_template("order_success.html", order_id=order_id, total=total_amount)

@app.route('/my-orders')
@login_required
def my_orders():
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT *
                   FROM orders
                   WHERE user_id = %s
                   ORDER BY order_date DESC
                   """, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "my_orders.html",
        orders=orders
    )




@app.route('/admin/orders')
@admin_required
def admin_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT o.order_id,
                          u.name,
                          r.restaurant_name,
                          o.order_status,
                          o.order_date
                   FROM orders o
                            JOIN users u
                                 ON o.user_id = u.user_id
                            JOIN restaurants r
                                 ON o.restaurant_id = r.restaurant_id
                   """)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_orders.html',
        orders=orders
    )
@app.route('/rate_order/<order_id>', methods=['GET', 'POST'])
def rate_order(order_id):
    if request.method == 'POST':
        rating = request.form['rating']
        feedback = request.form['feedback']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT user_id, restaurant_id
                       FROM orders
                       WHERE order_id = %s
                       """, (order_id,))

        order_data = cursor.fetchone()

        user_id = order_data[0]
        restaurant_id = order_data[1]

        cursor.execute("""
                       INSERT INTO reviews
                           (user_id, restaurant_id, rating, review_text)
                       VALUES (%s, %s, %s, %s)
                       """, (
                           user_id,
                           restaurant_id,
                           rating,
                           feedback
                       ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/my-orders')

    return render_template(
        'rate_order.html',
        order_id=order_id
    )

@app.route('/analytics')
def analytics():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)

    # =========================
    # TOP 5 RESTAURANTS
    # =========================
    cursor.execute("""
        SELECT r.restaurant_name,
               COUNT(o.order_id) AS total_orders
        FROM restaurants r
        LEFT JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id, r.restaurant_name
        ORDER BY total_orders DESC
        LIMIT 5
    """)
    top_restaurants = cursor.fetchall()

    # =========================
    # TOTAL ORDERS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total_orders
        FROM orders
    """)
    total_orders = cursor.fetchone()['total_orders']

    # =========================
    # TOTAL REVENUE
    # =========================
    cursor.execute("""
        SELECT SUM(amount) AS total_revenue
        FROM payments
    """)
    revenue_result = cursor.fetchone()
    total_revenue = revenue_result['total_revenue'] or 0

    # =========================
    # ORDERS PER DAY
    # =========================
    cursor.execute("""
        SELECT DATE(order_date) AS order_date,
               COUNT(*) AS total_orders
        FROM orders
        GROUP BY DATE(order_date)
        ORDER BY order_date
    """)

    data = cursor.fetchall()

    labels = [str(row['order_date']) for row in data]
    values = [row['total_orders'] for row in data]

    # =========================
    # TOTAL CUSTOMERS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total_customers
        FROM users
    """)
    total_customers = cursor.fetchone()['total_customers']

    # =========================
    # TOTAL RESTAURANTS
    # =========================
    cursor.execute("""
        SELECT COUNT(*) AS total_restaurants
        FROM restaurants
    """)
    total_restaurants = cursor.fetchone()['total_restaurants']

    # =========================
    # PAYMENT METHOD CHART
    # =========================
    cursor.execute("""
        SELECT payment_method,
               SUM(amount) AS total_amount
        FROM payments
        GROUP BY payment_method
    """)

    payment_data = cursor.fetchall()

    payment_labels = [row['payment_method'] for row in payment_data]
    payment_values = [float(row['total_amount']) for row in payment_data]

    # =========================
    # ORDER STATUS CHART
    # =========================
    cursor.execute("""
        SELECT order_status,
               COUNT(*) AS total
        FROM orders
        GROUP BY order_status
    """)

    status_data = cursor.fetchall()

    status_labels = [row['order_status'] for row in status_data]
    status_values = [row['total'] for row in status_data]

    # =========================
    # REVENUE TREND
    # =========================
    cursor.execute("""
        SELECT DATE(order_date) AS day,
               SUM(p.amount) AS revenue
        FROM orders o
        JOIN payments p
            ON o.order_id = p.order_id
        GROUP BY DATE(order_date)
        ORDER BY day
    """)

    revenue_data = cursor.fetchall()

    revenue_labels = [str(row['day']) for row in revenue_data]
    revenue_values = [float(row['revenue']) for row in revenue_data]
    cursor.execute("""
                   SELECT AVG(amount) AS avg_order
                   FROM payments
                   """)

    avg_order = cursor.fetchone()['avg_order'] or 0
    cursor.close()
    conn.close()

    return render_template(
        'analytics.html',
        total_orders=total_orders,
        total_revenue=total_revenue,
        total_customers=total_customers,
        total_restaurants=total_restaurants,
        labels=labels,
        values=values,
        payment_labels=payment_labels,
        payment_values=payment_values,
        top_restaurants=top_restaurants,
        status_labels=status_labels,
        status_values=status_values,
        revenue_labels=revenue_labels,
        revenue_values=revenue_values,
        avg_order=avg_order
    )
@app.route('/export_orders_excel')
def export_orders_excel():


    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT o.order_id,
                          o.user_id,
                          u.name AS customer_name,
                          u.email,
                          u.phone,

                          r.restaurant_id,
                          r.restaurant_name,
                          r.city,
                          r.cuisine,

                          mi.item_name,

                          oi.quantity,
                          oi.price,

                          o.discount_amount,

                          o.total_amount,

                          p.payment_id,
                          p.payment_method,
                          p.payment_status,

                          o.order_status,
                          o.order_date,
                          o.estimated_delivery_time,

                          rv.rating,
                          rv.review_text

                   FROM orders o

                            LEFT JOIN users u
                                      ON o.user_id = u.user_id

                            LEFT JOIN restaurants r
                                      ON o.restaurant_id = r.restaurant_id

                            LEFT JOIN payments p
                                      ON o.order_id = p.order_id

                            LEFT JOIN order_items oi
                                      ON o.order_id = oi.order_id

                            LEFT JOIN menu_items mi
                                      ON oi.item_id = mi.item_id

                            LEFT JOIN reviews rv
                                      ON rv.user_id = o.user_id
                                          AND rv.restaurant_id = o.restaurant_id

                   ORDER BY o.order_id DESC
                   """)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    # Header Row
    ws.append([
        "Order ID",
        "User ID",
        "Customer Name",
        "Email",
        "Phone",
        "Restaurant ID",
        "Restaurant Name",
        "City",
        "Cuisine",
        "Item Name",
        "Quantity",
        "Price",
        "Discount Amount",
        "Total Amount",
        "Payment ID",
        "Payment Method",
        "Payment Status",
        "Order Status",
        "Order Date",
        "Estimated Delivery Time",
        "Rating",
        "Review"
    ])

    # Data Rows
    for order in orders:
        ws.append([

            order.get('order_id', ''),
            order.get('user_id', ''),

            order.get('customer_name', ''),
            order.get('email', ''),
            order.get('phone', ''),

            order.get('restaurant_id', ''),
            order.get('restaurant_name', ''),
            order.get('city', ''),
            order.get('cuisine', ''),

            order.get('item_name', ''),

            order.get('quantity', ''),
            order.get('price', ''),

            order.get('discount_amount', ''),

            order.get('total_amount', ''),

            order.get('payment_id', ''),
            order.get('payment_method', ''),
            order.get('payment_status', ''),

            order.get('order_status', ''),

            str(order.get('order_date', '')),
            str(order.get('estimated_delivery_time', '')),

            order.get('rating', ''),
            order.get('review_text', '')
        ])

    file = BytesIO()
    wb.save(file)
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="orders.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['user_id']
        session['name'] = user['name']

        return redirect('/home')

    return "Invalid Email or Password"

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT *
                       FROM admins
                       WHERE username = %s
                       """, (username,))

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin and admin['password'] == password:
            session['admin_id'] = admin['admin_id']

            return redirect('/admin_dashboard')

        return "Invalid Admin Login"

    return render_template('admin_login.html')
@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    # Replace with session user later

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cart(user_id,item_id,quantity)
        VALUES(%s,%s,1)
    """, (user_id, item_id))

    conn.commit()
    conn.close()

    return redirect('/menu')
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            c.cart_id,
            m.item_name,
            m.price,
            c.quantity,
            (m.price * c.quantity) AS total
        FROM cart c
        JOIN menu_items m
            ON c.item_id = m.item_id
        WHERE c.user_id = %s
    """, (user_id,))

    cart_items = cursor.fetchall()

    conn.close()
    total_amount = sum(item['total'] for item in cart_items)

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total_amount=total_amount
    )
@app.route('/remove_cart/<int:cart_id>')
def remove_cart(cart_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE cart_id=%s",
        (cart_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/cart')
@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT c.cart_id,
                          m.item_name,
                          m.price,
                          c.quantity,
                          (m.price * c.quantity) AS total
                   FROM cart c
                            JOIN menu_items m
                                 ON c.item_id = m.item_id
                   WHERE c.user_id = %s
                   """, (session['user_id'],))

    cart_items = cursor.fetchall()

    total_amount = sum(item['total'] for item in cart_items)

    cursor.close()
    conn.close()

    return render_template(
        'checkout.html',
        cart_items=cart_items,
        total_amount=total_amount
    )

@app.route('/invoice/<int:order_id>')
def invoice(order_id):

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Invoice")

    pdf.drawString(100, 800, "Qoresto Invoice")
    pdf.drawString(100, 770, f"Order ID: {order_id}")

    pdf.drawString(100, 740, "Thank you for ordering!")

    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"invoice_{order_id}.pdf",
        mimetype='application/pdf'
    )
@app.route('/recommendations')
def recommendations():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.restaurant_name,
            COUNT(o.order_id) AS total_orders
        FROM restaurants r
        LEFT JOIN orders o
        ON r.restaurant_id = o.restaurant_id
        GROUP BY r.restaurant_id
        ORDER BY total_orders DESC
    """)

    restaurants = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'recommendations.html',
        restaurants=restaurants
    )
@app.route('/top_items')
def top_items():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.item_name,
            COUNT(*) AS total_orders
        FROM cart c
        JOIN menu_items m
            ON c.item_id = m.item_id
        GROUP BY m.item_id
        ORDER BY total_orders DESC
        LIMIT 10
    """)

    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'top_items.html',
        items=items
    )
@app.route('/revenue_report')
def revenue_report():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            DATE(payment_date) AS day,
            SUM(amount) AS revenue
        FROM payments
        GROUP BY DATE(payment_date)
        ORDER BY day
    """)

    revenue = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'revenue_report.html',
        revenue=revenue
    )
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id = %s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'profile.html',
        user=user
    )
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        hashed = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return "Email already registered. Please login."

        cursor.execute("""
                       INSERT INTO users
                       (name,
                        email,
                        password,
                        phone,
                        address)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (
                           name,
                           email,
                           hashed,  # store hashed password
                           phone,
                           address
                       ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()

    return redirect('/login')
@app.route('/add_favorite/<int:restaurant_id>')
def add_favorite(restaurant_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorites(
            user_id,
            restaurant_id
        )
        VALUES(%s,%s)
    """, (user_id, restaurant_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/favorites')
@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT r.restaurant_id,
                          r.restaurant_name,
                          r.cuisine,
                          r.city,
                          r.rating,
                          r.cost_for_two,
                          r.image_url
                   FROM favorites f
                            JOIN restaurants r
                                 ON f.restaurant_id = r.restaurant_id
                   WHERE f.user_id = %s
                   """, (user_id,))

    favorites = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'favorites.html',
        favorites=favorites
    )
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session['user_id']   # later replace with session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']

        cursor.execute("""
            UPDATE users
            SET name=%s,
                phone=%s,
                address=%s
            WHERE user_id=%s
        """, (name, phone, address, user_id))

        conn.commit()
        conn.close()

        return redirect('/profile')

    cursor.execute("""
        SELECT *
        FROM users
        WHERE user_id=%s
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_profile.html',
        user=user
    )
@app.route('/search')
def search():

    keyword = request.args.get('keyword')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM restaurants
        WHERE restaurant_name LIKE %s
    """, ('%' + keyword + '%',))

    restaurants = cursor.fetchall()

    conn.close()

    return render_template(
        'search_results.html',
        restaurants=restaurants,
        keyword=keyword
    )
@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/reorder/<int:order_id>')
@login_required
def reorder(order_id):

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT restaurant_id
        FROM orders
        WHERE order_id=%s
    """, (order_id,))

    order = cursor.fetchone()

    if not order:
        return "Order not found"

    return redirect(f"/menu/{order['restaurant_id']}")



@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):

    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE orders
        SET order_status=%s
        WHERE order_id=%s
    """, (status, order_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin_orders')

@app.route('/cancel_order/<int:order_id>')
@login_required
def cancel_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update order status
    cursor.execute("""
                   UPDATE orders
                   SET order_status='Cancelled'
                   WHERE order_id = %s
                   """, (order_id,))

    # Update payment status
    cursor.execute("""
                   UPDATE payments
                   SET payment_status='Cancelled'
                   WHERE order_id = %s
                   """, (order_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/my-orders')


@app.route('/favorite/<int:restaurant_id>')
def favorite(restaurant_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO favorites(user_id, restaurant_id)
        VALUES(%s,%s)
    """, (session['user_id'], restaurant_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/home')


@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    payment_method = request.form['payment_method']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get cart items
    cursor.execute("""
                   SELECT m.item_id,
                          c.quantity,
                          m.price,
                          m.restaurant_id
                   FROM cart c
                            JOIN menu_items m
                                 ON c.item_id = m.item_id
                   WHERE c.user_id = %s
                   """, (user_id,))

    cart_items = cursor.fetchall()

    if not cart_items:
        return "Cart is Empty"

    restaurant_id = cart_items[0]['restaurant_id']

    # Calculate total amount
    total_amount = 0

    for item in cart_items:
        total_amount += item['quantity'] * item['price']

    # Create Order
    cursor.execute("""
                   INSERT INTO orders
                   (user_id,
                    restaurant_id,
                    order_status,
                    total_amount)
                   VALUES (%s,
                           %s,
                           %s,
                           %s)
                   """, (
                       user_id,
                       restaurant_id,
                       'Order Placed',
                       total_amount
                   ))

    conn.commit()

    order_id = cursor.lastrowid

    # Save Order Items
    for item in cart_items:
        cursor.execute("""
                       INSERT INTO order_items
                       (order_id,
                        item_id,
                        quantity,
                        price)
                       VALUES (%s,
                               %s,
                               %s,
                               %s)
                       """, (
                           order_id,
                           item['item_id'],
                           item['quantity'],
                           item['price']
                       ))

    conn.commit()

    # Save Payment
    cursor.execute("""
                   INSERT INTO payments
                   (order_id,
                    payment_method,
                    amount,
                    payment_status)
                   VALUES (%s,
                           %s,
                           %s,
                           %s)
                   """, (
                       order_id,
                       payment_method,
                       total_amount,
                       'Success'
                   ))

    conn.commit()

    # Clear Cart
    cursor.execute("""
                   DELETE
                   FROM cart
                   WHERE user_id = %s
                   """, (user_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/my-orders')


@app.route('/order_success/<int:order_id>')
def order_success(order_id):
    return render_template(
        'order_success.html',
        order_id=order_id
    )
@app.route('/toggle_restaurant/<int:restaurant_id>')
def toggle_restaurant(restaurant_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM restaurants
        WHERE restaurant_id=%s
    """,(restaurant_id,))

    current_status = cursor.fetchone()[0]

    new_status = "Closed" if current_status == "Open" else "Open"

    cursor.execute("""
        UPDATE restaurants
        SET status=%s
        WHERE restaurant_id=%s
    """,(new_status, restaurant_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin_dashboard')
@app.route('/track_order/<int:order_id>')
def track_order(order_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT order_status
        FROM orders
        WHERE order_id=%s
    """,(order_id,))

    order = cursor.fetchone()

    conn.close()

    return render_template(
        'track_order.html',
        order=order
    )
@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT o.*,
           r.restaurant_name
    FROM orders o
    JOIN restaurants r
    ON o.restaurant_id=r.restaurant_id
    WHERE o.order_id=%s
    """,(order_id,))

    order = cursor.fetchone()
    cursor.execute("""
                   SELECT m.item_name,
                          oi.quantity,
                          oi.price
                   FROM order_items oi
                            JOIN menu_items m
                                 ON oi.item_id = m.item_id
                   WHERE oi.order_id = %s
                   """, (order_id,))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'order_details.html',
        order=order,
        items=items
    )
@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM orders WHERE order_id=%s",
        (order_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin/orders')
@app.route('/search_orders')
@login_required
def search_orders():

    keyword = request.args.get('keyword')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM orders
    WHERE order_status LIKE %s
    """,('%'+keyword+'%',))

    orders = cursor.fetchall()

    return render_template(
        'my_orders.html',
        orders=orders
    )
@app.route('/api/revenue')
def api_revenue():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT DATE(payment_date) day,
           SUM(amount) revenue
    FROM payments
    GROUP BY DATE(payment_date)
    """)

    data = cursor.fetchall()

    return jsonify(data)
@app.route('/notifications')
@login_required
def notifications():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT *
    FROM notifications
    WHERE user_id=%s
    ORDER BY created_at DESC
    """,(session['user_id'],))

    notifications = cursor.fetchall()

    return render_template(
        'notifications.html',
        notifications=notifications
    )
@app.route('/remove_favorite/<int:restaurant_id>')
@login_required
def remove_favorite(restaurant_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM favorites
    WHERE user_id=%s
    AND restaurant_id=%s
    """,
    (
        session['user_id'],
        restaurant_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/favorites')
@app.route('/upload_profile', methods=['POST'])
@login_required
def upload_profile():
    file = request.files['profile_image']

    if file:
        filename = file.filename

        file.save(
            f"static/uploads/{filename}"
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET profile_image=%s
            WHERE user_id=%s
        """,
        (
            filename,
            session['user_id']
        ))

        conn.commit()

        cursor.close()
        conn.close()

    return redirect('/profile')

@app.route('/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE user_id=%s
    """, (user_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin/users')
@app.route('/export_pdf')
def export_pdf():
    pass
@app.route('/export_excel')
def export_excel():

    conn = get_db_connection()

    df = pd.read_sql("""
        SELECT
            order_id,
            total_amount,
            order_status,
            order_date
        FROM orders
    """, conn)

    file_name = "Qoresto_report.xlsx"

    df.to_excel(file_name, index=False)

    conn.close()

    return send_file(
        file_name,
        as_attachment=True
    )
@app.route('/restaurant_report')
def restaurant_report():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            r.restaurant_name,
            COUNT(o.order_id) AS total_orders,
            SUM(o.total_amount) AS revenue,
            AVG(rv.rating) AS avg_rating
        FROM restaurants r
        LEFT JOIN orders o
            ON r.restaurant_id = o.restaurant_id
        LEFT JOIN reviews rv
            ON r.restaurant_id = rv.restaurant_id
        GROUP BY r.restaurant_id
        ORDER BY revenue DESC
    """)

    report = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'restaurant_report.html',
        report=report
    )
@app.route('/customer_report')
def customer_report():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT u.name,
                              COUNT(o.order_id)   AS total_orders,
                              SUM(o.total_amount) AS total_spent
                       FROM users u
                                LEFT JOIN orders o
                                          ON u.user_id = o.user_id
                       GROUP BY u.user_id
                       ORDER BY total_spent DESC
                       """)

        customers = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            'customer_report.html',
            customers=customers
        )
@app.route('/sql_queries')
def sql_queries():
    return render_template('sql_queries.html')
@app.route('/reports')
def reports():
    return render_template('reports.html')
@app.route('/about_project')
def about_project():
    return render_template('about_project.html')


@app.route('/database_schema')
def database_schema():
    return render_template('database_schema.html')
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/admin/users')
@admin_required
def admin_users():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_users.html",
        users=users
    )


if __name__ == '__main__':
    app.run(debug=True)





