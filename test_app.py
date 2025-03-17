from app import app, db

print("Flask application imported successfully!")
print(f"SQLAlchemy database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"Available extensions: {', '.join(app.extensions.keys())}") 