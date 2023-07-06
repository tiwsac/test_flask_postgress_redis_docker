from app import app
from routes import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5008, use_reloader=True)

