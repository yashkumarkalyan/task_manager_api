from app import db, app  # Import the 'app' instance

# Create an application context
with app.app_context():
    # Create the database tables based on your defined models
    db.create_all()
