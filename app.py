from flask import Flask
from auth import auth_bp
from quiz import quiz_bp

app = Flask(__name__)
app.secret_key = "your-secret-key"

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz")

if __name__ == "__main__":
    app.run(debug=True)
