# migrate_db.py
from app import create_app
from extensions import db
from sqlalchemy import text

def migrate_database():
    app = create_app()
    
    with app.app_context():
        # Check if reset_token column exists
        try:
            result = db.session.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'reset_token' not in columns:
                print("Adding reset_token column...")
                db.session.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR(100)"))
                
            if 'reset_token_expires' not in columns:
                print("Adding reset_token_expires column...")
                db.session.execute(text("ALTER TABLE users ADD COLUMN reset_token_expires DATETIME"))
                
            db.session.commit()
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Migration error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database() 