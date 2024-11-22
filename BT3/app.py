from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/QuanLyNhaHang'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Dish(db.Model):
    __tablename__ = 'monan'
    id = db.Column(db.Integer, primary_key=True)
    tenmon = db.Column(db.String(100), nullable=False)
    dongia = db.Column(db.Float, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), nullable=False)
    dish_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)

class Table(db.Model):
    __tablename__ = 'tables'
    table_number = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.String(20), default='Trống')
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Menu routes
@app.route('/menu')
def menu():
    dishes = Dish.query.all()
    return render_template('menu.html', dishes=dishes)

@app.route('/add_dish', methods=['POST'])
def add_dish():
    try:
        name = request.form['name']
        price = float(request.form['price'])
        
        dish = Dish(tenmon=name, dongia=price)
        db.session.add(dish)
        db.session.commit()
        
        flash('Món ăn đã được thêm thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('menu'))

@app.route('/delete_dish/<int:id>')
def delete_dish(id):
    try:
        dish = Dish.query.get_or_404(id)
        db.session.delete(dish)
        db.session.commit()
        flash('Món ăn đã được xóa thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('menu'))

# Order routes
@app.route('/orders')
def orders():
    orders = Order.query.order_by(Order.order_time.desc()).all()
    dishes = Dish.query.all()
    tables = Table.query.all()
    return render_template('orders.html', orders=orders, dishes=dishes, tables=tables)

@app.route('/add_order', methods=['POST'])
def add_order():
    try:
        table = request.form['table']
        dish_name = request.form['dish']
        quantity = int(request.form['quantity'])
        
        # Get dish price
        dish = Dish.query.filter_by(tenmon=dish_name).first()
        if not dish:
            raise ValueError("Món ăn không tồn tại")
            
        total_price = dish.dongia * quantity
        
        # Create order
        order = Order(
            table_number=table,
            dish_name=dish_name,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(order)
        
        # Update table status
        table_obj = Table.query.get(table)
        if table_obj:
            table_obj.status = 'Đang phục vụ'
            table_obj.last_update = datetime.utcnow()
        else:
            table_obj = Table(table_number=table, status='Đang phục vụ')
            db.session.add(table_obj)
        
        db.session.commit()
        flash('Đơn hàng đã được thêm thành công!', 'success')
        
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('orders'))

@app.route('/complete_order/<int:id>')
def complete_order(id):
    try:
        order = Order.query.get_or_404(id)
        
        # Check if this is the last order for the table
        remaining_orders = Order.query.filter_by(table_number=order.table_number).count()
        if remaining_orders <= 1:  # Including this order
            table = Table.query.get(order.table_number)
            if table:
                table.status = 'Trống'
                table.last_update = datetime.utcnow()
        
        db.session.delete(order)
        db.session.commit()
        flash('Đơn hàng đã được thanh toán thành công!', 'success')
        
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('orders'))

# Table routes
@app.route('/tables')
def tables():
    tables = Table.query.all()
    return render_template('tables.html', tables=tables)

@app.route('/toggle_table/<table_number>')
def toggle_table(table_number):
    try:
        table = Table.query.get(table_number)
        if not table:
            table = Table(table_number=table_number)
            db.session.add(table)
        
        # Check if table has active orders
        has_orders = Order.query.filter_by(table_number=table_number).count() > 0
        
        if table.status == 'Đang phục vụ':
            if has_orders:
                flash('Không thể đổi trạng thái bàn khi còn đơn hàng!', 'error')
                return redirect(url_for('tables'))
            table.status = 'Trống'
        else:
            table.status = 'Đang phục vụ'
        
        table.last_update = datetime.utcnow()
        db.session.commit()
        flash('Đã cập nhật trạng thái bàn!', 'success')
        
    except Exception as e:
        flash(f'Lỗi: {str(e)}', 'error')
    
    return redirect(url_for('tables'))

# Helper route for formatting currency
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "0"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)