from app import create_app, db
from app.models import User
import sys

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Test database connection
            db.engine.connect()
            print("✓ Successfully connected to PostgreSQL database")
        except Exception as e:
            print(f"✗ Could not connect to database: {e}")
            print("\nPlease ensure:")
            print("1. PostgreSQL is running")
            print("2. The database 'arteon_villas_expenses' exists")
            print("3. Your DATABASE_URL in .env is correct")
            print("\nTip: Run 'python setup_postgres.py' first to create the database")
            sys.exit(1)
        
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Check if users already exist
            if User.query.first() is None:
                # Create initial users
                users = [
                    {
                        'email': 'hookloop1@yahoo.com',
                        'password': 'password1',
                        'full_name': 'Jovan Obradovic',
                        'is_admin': True
                    },
                    {
                        'email': 'marolinik@gmail.com',
                        'password': 'password2',
                        'full_name': 'Marko Markovic',
                        'is_admin': False
                    },
                    {
                        'email': 'fonmarko@gmail.com',
                        'password': 'password3',
                        'full_name': 'Marko Jovanović',
                        'is_admin': False
                    },
                    {
                        'email': 'zoran.radisavljevic@egzakta.com',
                        'password': 'password4',
                        'full_name': 'Zoran Radisavljevic',
                        'is_admin': False
                    }
                ]
                
                for user_data in users:
                    user = User(
                        email=user_data['email'],
                        full_name=user_data['full_name'],
                        is_admin=user_data['is_admin'],
                        force_password_change=True
                    )
                    user.set_password(user_data['password'])
                    db.session.add(user)
                
                db.session.commit()
                print("\n✓ Database initialized successfully!")
                print("\nInitial users created:")
                for user_data in users:
                    print(f"  - {user_data['full_name']} ({user_data['email']})")
                    if user_data['is_admin']:
                        print("    [ADMIN]")
                print("\nAll users must change their password on first login.")
            else:
                print("\n✓ Database already contains users. Skipping user creation.")
                
        except Exception as e:
            print(f"\n✗ Error initializing database: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    print("Arteon Villas Expense Tracker - Database Initialization")
    print("=" * 55)
    init_database() 