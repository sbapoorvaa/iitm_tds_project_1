from flask import Flask
from api.v1.task import task_bp
from api.v1.evaluation import evaluation_bp

app = Flask(__name__)
app.register_blueprint(task_bp, url_prefix="/api/v1")
app.register_blueprint(evaluation_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(debug=True)
