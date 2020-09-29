from flask import Flask
import flask_monitoringdashboard as dashboard
import time

app = Flask(__name__)
dashboard.bind(app)


@app.route('/')
def hello_world():
    time.sleep(5)
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
