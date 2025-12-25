from flask import Flask
from auth import auth_bp
from quiz import quiz_bp
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(quiz_bp, url_prefix="/quiz")

@app.route("/")
def index():
    from flask import session, redirect
    if "username" in session:
        return redirect("/quiz/home")
    return redirect("/auth/login")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
