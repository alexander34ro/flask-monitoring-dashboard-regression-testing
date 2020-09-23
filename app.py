from flask import Flask, jsonify
import flask_monitoringdashboard as dashboard
import gunicorn

app = Flask(__name__)
dashboard.bind(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
