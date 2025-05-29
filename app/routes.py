from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Expense
from app.forms import LoginForm, ChangePasswordForm, ExpenseForm, EditExpenseForm
from sqlalchemy import func
from decimal import Decimal

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
    total_expenses = float(sum(expense.amount_eur for expense in expenses))
    cost_per_person = total_expenses / 4 if total_expenses > 0 else 0
    
    # Calculate expenses by user
    user_expenses = db.session.query(
        User.full_name,
        func.coalesce(func.sum(Expense.amount_eur), 0).label('total_paid'),
        func.count(Expense.id).label('expense_count')
    ).outerjoin(
        Expense, User.id == Expense.user_id
    ).group_by(
        User.id, User.full_name
    ).all()
    
    # Calculate balance for each user
    user_balances = []
    for user_name, total_paid, expense_count in user_expenses:
        # Convert to float, handling Decimal and None
        total_paid_float = float(total_paid) if total_paid else 0
        balance = total_paid_float - cost_per_person
        
        user_balances.append({
            'name': user_name,
            'total_paid': total_paid_float,
            'expense_count': expense_count or 0,
            'balance': balance,
            'owes': -balance if balance < 0 else 0,
            'owed': balance if balance > 0 else 0
        })
    
    # Sort by total paid (descending)
    user_balances.sort(key=lambda x: x['total_paid'], reverse=True)
    
    return render_template('dashboard.html', 
                         form=form, 
                         expenses=expenses,
                         total_expenses=total_expenses,
                         cost_per_person=cost_per_person,
                         user_balances=user_balances)

@main.route('/admin')
@login_required
@admin_required
def admin():
    expenses = Expense.query.order_by(Expense.date_entered.desc()).all()
    total_expenses = float(sum(expense.amount_eur for expense in expenses))
    cost_per_person = total_expenses / 4 if total_expenses > 0 else 0
    
    # Calculate expenses by user
    user_expenses = db.session.query(
        User.full_name,
        func.coalesce(func.sum(Expense.amount_eur), 0).label('total_paid'),
        func.count(Expense.id).label('expense_count')
    ).outerjoin(
        Expense, User.id == Expense.user_id
    ).group_by(
        User.id, User.full_name
    ).all()
    
    # Calculate balance for each user
    user_balances = []
    for user_name, total_paid, expense_count in user_expenses:
        # Convert to float, handling Decimal and None
        total_paid_float = float(total_paid) if total_paid else 0
        balance = total_paid_float - cost_per_person
        
        user_balances.append({
            'name': user_name,
            'total_paid': total_paid_float,
            'expense_count': expense_count or 0,
            'balance': balance,
            'owes': -balance if balance < 0 else 0,
            'owed': balance if balance > 0 else 0
        })
    
    # Sort by total paid (descending)
    user_balances.sort(key=lambda x: x['total_paid'], reverse=True)
    
    return render_template('admin.html',
                         expenses=expenses,
                         total_expenses=total_expenses,
                         cost_per_person=cost_per_person,
                         user_balances=user_balances)

@main.route('/settle-expenses', methods=['POST'])
@login_required
@admin_required
def settle_expenses():
    Expense.query.filter_by(status='unsettled').update({'status': 'settled'})
    db.session.commit()
    flash('All expenses have been settled!', 'success')
    return redirect(url_for('main.admin'))

@main.route('/settle-expense/<int:expense_id>', methods=['POST'])
@login_required
@admin_required
def settle_individual_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.status == 'unsettled':
        expense.status = 'settled'
        db.session.commit()
        flash(f'Expense of €{expense.amount_eur} has been settled!', 'success')
    else:
        flash('This expense is already settled.', 'info')
    return redirect(request.referrer or url_for('main.admin'))

@main.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user can edit this expense (only their own expenses)
    if expense.user_id != current_user.id and not current_user.is_admin:
        flash('You can only edit your own expenses.', 'error')
        return redirect(url_for('main.dashboard'))
    
    form = EditExpenseForm()
    
    if form.validate_on_submit():
        expense.amount_eur = form.amount_eur.data
        expense.note = form.note.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.expense_id.data = expense.id
        form.amount_eur.data = expense.amount_eur
        form.note.data = expense.note
    
    return render_template('edit_expense.html', form=form, expense=expense)

@main.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if user can delete this expense (only their own expenses or admin)
    if expense.user_id != current_user.id and not current_user.is_admin:
        flash('You can only delete your own expenses.', 'error')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(request.referrer or url_for('main.dashboard'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login')) 