from flask import Flask, send_from_directory, request, g, jsonify
import flask_monitoringdashboard as dashboard
import sqlite3, time, datetime, os, psutil, random
import json

### FMD Setup
app = Flask(__name__)
dashboard.bind(app)

DB_Name = 'flask_monitoringdashboard.db'
Regression_Level = int(os.environ.get('REGRESSION_LEVEL', 0))
Regression_Magnitude = int(os.environ.get('REGRESSION_MAGNITUDE', 1))
data = []
last_cpu_read = 0.0

# Mining CPU Data
def CPU():
    cpu = psutil.cpu_percent(interval=None, percpu=False)
    print(f"{datetime.datetime.now()} | CPU: {cpu}")
    
    global last_cpu_read
    last_cpu_read = cpu
    
    return cpu


every_second_schedule = {'seconds': 10}
dashboard.add_graph('CPU Usage', CPU, 'interval', **every_second_schedule)

### Regressions
# CPU Heavy Regression
def Fibonacci(n):
    if n == 1: return 0
    elif n == 2: return 1
    else: return Fibonacci(n - 1) + Fibonacci(n - 2)

def CPU_Heavy_Regression():
    if Regression_Magnitude == 1: Fibonacci(26)
    elif Regression_Magnitude == 2: Fibonacci(28)
    elif Regression_Magnitude == 3: Fibonacci(30)
    elif Regression_Magnitude == 4: Fibonacci(31)

# CPU Light Regression
def CPU_Light_Regression():
    time.sleep(0.1)

# Main Regression
def Regression():
    if (Regression_Level == 0):
        pass
    if (Regression_Level == 1):
        CPU_Light_Regression()
    if (Regression_Level == 2):
        CPU_Heavy_Regression()
    if (Regression_Level == 3):
        CPU_Light_Regression()
        CPU_Heavy_Regression()


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
    g.request_end_time = None
    g.request_time_2 = None

@app.teardown_request
def teardown_request(exc):
    g.request_end_time = time.time()
    g.request_time_2 = "%.5fs" % (g.request_end_time - g.request_start_time)
    request_latency = float(g.request_time_2[:-1])
    cpu_usage = psutil.cpu_percent(interval=request_latency, percpu=False)
    print('CPU Usage measured at teardown: ' + str(cpu_usage))
    print('Request time measured at teardown: ' + str(g.request_time_2))

@app.route('/set_regression_level/<level>')
def Set_Regression_Level(level=0):
    global Regression_Level
    Regression_Level = int(level)
    return 'Regression_Level set to ' + str(Regression_Level) + '.\n'

@app.route('/set_regression_magnitude/<level>')
def Set_Regression_Magnitude(level=0):
    global Regression_Magnitude
    Regression_Magnitude = int(level)
    return 'Regression_Magnitude set to ' + str(Regression_Magnitude) + '.\n'

### Main
@app.route('/')
def Main():
    db = sqlite3.connect(DB_Name)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM CustomGraphData')
    resultset = cursor.fetchall()

    Fibonacci(28)

    Regression()

    r, gr, b = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
    rgb = str(r) + str(gr) + str(b)

    db.close()

    request_latency = float(g.request_time()[:-1])
    cpu_usage = psutil.cpu_percent(interval=request_latency, percpu=False)
    data.append({"request_latency": request_latency, "cpu_usage": cpu_usage})

    text  = '<h1>Main</h1>'
    text += '<p>Executed main body in ' + str(request_latency) + '</p>'
    text += '<p>Executed main body in ' + str(g.request_time_2) + '</p>'
    text += '<p>Executed main body in ' + str(g.request_end_time) + '</p>'
    text += '<p>CPU usage: ' + str(cpu_usage) + '%</p>'
    text += '<p>FMD CPU usage: ' + str(last_cpu_read) + '%</p>'
    text += '<div style="background-color: #' + rgb + ';padding: 4px"></div>'
    text += '<code style="background-color: #ddd;padding: 5px 20px;display: block;border-radius: 0 0 10px 10px;">'
    text += '<p>Number of records: ' + str(len(resultset)) + '</p>'
    text += '<p>Regression Level: ' + str(Regression_Level) + '</p>'
    text += '<p>Regression Magnitude: ' + str(Regression_Magnitude) + '</p>'
    text += '</code>'
    return text

### Refresh DB
@app.route('/get_db')
def Download_DB():
    return send_from_directory(directory='', filename=DB_Name, as_attachment=True)

### Refresh DB
@app.route('/get_json')
def Download_JSON():
    return jsonify(data)

@app.route('/clear_db')
def Clear_DB():
    db = sqlite3.connect(DB_Name)
    cursor = db.cursor()
    cursor.execute('DELETE FROM CustomGraphData')
    db.commit()
    cursor.execute('DELETE FROM Request')
    db.commit()
    db.close()

    data = []

    return 'Custom Graph Data cleared.'

if __name__ == '__main__':
    app.run()
