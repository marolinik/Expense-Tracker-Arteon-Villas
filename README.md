# Arteon Villas Expense Tracker

A web application for tracking and managing shared expenses for Arteon Villas, built with Flask and PostgreSQL.

## Features

- **User Authentication**: Secure login system with password hashing
- **Forced Password Change**: Users must change their initial password on first login
- **Expense Management**: Add, view, and track expenses with notes
- **Cost Splitting**: Automatically calculates cost per person (split between 4 people)
- **Admin Panel**: Admin users can settle all expenses
- **Status Tracking**: Expenses can be marked as settled or unsettled
- **Responsive Design**: Modern UI with Bootstrap 5

## Initial Users

The application comes with 4 pre-configured users:

1. **Jovan Obradovic** (Admin)
   - Email: hookloop1@yahoo.com
   - Initial Password: password1

2. **Marko Markovic**
   - Email: marolinik@gmail.com
   - Initial Password: password2

3. **Marko Jovanović**
   - Email: fonmarko@gmail.com
   - Initial Password: password3

4. **Zoran Radisavljevic**
   - Email: zoran.radisavljevic@egzakta.com
   - Initial Password: password4

**Note**: All users will be required to change their password on first login.

## Deployment Options

### Cloud Deployment (Render)

For easy cloud deployment with free PostgreSQL database, see:
- **[DEPLOYMENT_GUIDE_RENDER.md](DEPLOYMENT_GUIDE_RENDER.md)** - Complete guide for deploying on Render
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Quick checklist for deployment

The application is pre-configured for one-click deployment on Render using the included `render.yaml` blueprint.

### Local Development

Follow the instructions below for local setup and development.

## Prerequisites (Local Development)

1. **PostgreSQL Database Server**
   - Install PostgreSQL from https://www.postgresql.org/download/
   - Make sure PostgreSQL service is running
   - Default port: 5432

2. **Python 3.7+**

## Installation (Local Development)

1. **Clone the repository** (or extract the files to your project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Database Connection**:
   - Copy `env.example` to `.env`:
     ```bash
     copy env.example .env
     ```
   - Edit `.env` and update the DATABASE_URL with your PostgreSQL credentials:
     ```
     DATABASE_URL=postgresql://postgres:your_password@localhost:5432/arteon_villas_expenses
     ```

6. **Set up PostgreSQL Database** (Recommended method):
   ```bash
   python setup_postgres.py
   ```
   This script will automatically:
   - Create the database if it doesn't exist
   - Test the connection
   - Prepare everything for the application

   Alternatively, you can create the database manually:
   ```bash
   # Connect to PostgreSQL as superuser
   psql -U postgres
   
   # Create the database
   CREATE DATABASE arteon_villas_expenses;
   
   # Exit psql
   \q
   ```

7. **Initialize the database tables and users**:
   ```bash
   python init_db.py
   ```

8. **Run the application**:
   ```bash
   python run.py
   ```

9. **Access the application**:
   Open your web browser and go to `http://localhost:5000`

## Database Configuration

The application uses PostgreSQL. The connection string format is:
```
postgresql://username:password@host:port/database_name
```

You can configure the database connection in three ways:
1. Set the `DATABASE_URL` environment variable
2. Create a `.env` file with the `DATABASE_URL` variable
3. Modify the default in `config.py` (not recommended for production)

### Example .env file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/arteon_villas_expenses
```

## Usage

### First Login
1. Go to the login page
2. Enter your email and initial password
3. You'll be redirected to change your password
4. Set a new password and continue to the dashboard

### Adding Expenses
1. On the dashboard, fill in the expense form:
   - Enter the amount in EUR
   - Add a description/note
2. Click "Add Expense"
3. The expense will appear in the table below

### Viewing Expenses
- All expenses are visible to all users
- The dashboard shows:
  - Total expenses
  - Cost per person (total ÷ 4)
  - List of all expenses with details

### Admin Functions
Only Jovan Obradovic has admin access:
1. Click "Admin" in the navigation bar
2. View all expenses and summaries
3. Click "Settle All Expenses" to mark all unsettled expenses as settled

## Project Structure

```
arteon-villas-expense-tracker/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models.py           # Database models
│   ├── forms.py            # WTForms definitions
│   ├── routes.py           # Application routes
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── change_password.html
│   │   ├── dashboard.html
│   │   └── admin.html
│   └── static/             # Static files (CSS, JS)
├── run.py                  # Application entry point
├── config.py               # Configuration settings
├── init_db.py              # Database initialization script
├── setup_postgres.py       # PostgreSQL database setup helper
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for deployment
├── render.yaml             # Render deployment configuration
├── build.sh                # Build script for deployment
├── env.example             # Example environment variables
├── .gitignore             # Git ignore file
├── DEPLOYMENT_GUIDE_RENDER.md  # Render deployment guide
├── DEPLOYMENT_CHECKLIST.md     # Deployment checklist
└── README.md              # This file
```

## Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session management is handled by Flask-Login
- CSRF protection is enabled via Flask-WTF
- The SECRET_KEY should be changed in production
- Never commit `.env` files with real credentials

## Troubleshooting

1. **Database Connection Error**: 
   - Ensure PostgreSQL is running: `pg_ctl status` or check services
   - Check your database credentials in `.env`
   - Verify the database exists: `psql -U postgres -l`
   - Run `python setup_postgres.py` to create the database automatically

2. **Port already in use**: If port 5000 is busy, you can change it in `run.py`

3. **psycopg2 Installation Issues** (Windows):
   - If you have issues installing psycopg2, try: `pip install psycopg2-binary`

4. **Login issues**: Make sure you're using the correct email format

5. **"relation does not exist" error**: Run `python init_db.py` to create the tables

## Future Enhancements

- Export expenses to CSV/PDF
- Individual expense editing/deletion
- Monthly/yearly expense reports
- Email notifications for settlements
- Multi-currency support 