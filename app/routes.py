from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Expense
from app.forms import LoginForm, ChangePasswordForm, ExpenseForm

main = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need to be an admin to access this page.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            if user.force_password_change:
                return redirect(url_for('main.change_password'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if not current_user.force_password_change:
        return redirect(url_for('main.dashboard'))
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        current_user.force_password_change = False
        db.session.commit()
        flash('Your password has been changed successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('change_password.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount_eur=form.amount_eur.data,
            note=form.note.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Get all expenses
    expenses = Expense.query.order_by(Expense.date_entered.desc()).all()
    
    # Calculate totals
    total_expenses = sum(expense.amount_eur for expense in expenses)
    cost_per_person = total_expenses / 4 if total_expenses > 0 else 0
    
    return render_template('dashboard.html', 
                         form=form, 
                         expenses=expenses,
                         total_expenses=total_expenses,
                         cost_per_person=cost_per_person)

@main.route('/admin')
@login_required
@admin_required
def admin():
    expenses = Expense.query.order_by(Expense.date_entered.desc()).all()
    total_expenses = sum(expense.amount_eur for expense in expenses)
    cost_per_person = total_expenses / 4 if total_expenses > 0 else 0
    
    return render_template('admin.html',
                         expenses=expenses,
                         total_expenses=total_expenses,
                         cost_per_person=cost_per_person)

@main.route('/settle-expenses', methods=['POST'])
@login_required
@admin_required
def settle_expenses():
    Expense.query.filter_by(status='unsettled').update({'status': 'settled'})
    db.session.commit()
    flash('All expenses have been settled!', 'success')
    return redirect(url_for('main.admin'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login')) 