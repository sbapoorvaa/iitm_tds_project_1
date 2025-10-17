import os
from flask import Flask
from flask_cors import CORS 
from api.v1.task import task_bp
from api.v1.evaluation import evaluation_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(task_bp, url_prefix="/api/v1")
app.register_blueprint(evaluation_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    # Use PORT environment variable provided by Render, fallback to 5000
    port = int(os.environ.get("PORT", 5000))
    # Do not use debug=True in production; Render logs will capture output
    app.run(host="0.0.0.0", port=port, debug=True)
