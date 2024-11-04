from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Get debug and port settings from environment variables
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=app.config['DEBUG'])
