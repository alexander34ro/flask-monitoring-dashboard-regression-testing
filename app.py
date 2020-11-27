from flask import Flask, send_from_directory
import flask_monitoringdashboard as dashboard
import sqlite3, time, datetime, os, psutil

### FMD Setup
app = Flask(__name__)
dashboard.bind(app)

DB_Name = 'flask_monitoringdashboard.db'
Regression_Level = int(os.environ.get('REGRESSION_LEVEL', 0))

# Mining CPU Data
def CPU():
    cpu = psutil.cpu_percent()
    print(f"{datetime.datetime.now()} | CPU: {cpu}")
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
    Fibonacci(25)

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

@app.route('/set_regression_level/<level>')
def Set_Regression_Level(level=0):
    global Regression_Level
    Regression_Level = int(level)
    return 'Regression_Level set to ' + str(Regression_Level) + '.\n'

### Main
@app.route('/')
def Main():
    db = sqlite3.connect(DB_Name)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM CustomGraphData')
    resultset = cursor.fetchall()

    Fibonacci(30)

    Regression()

    db.close()
    text  = 'Main\n'
    text += 'Executed main body.\n'
    text += 'Number of records: ' + str(len(resultset)) + '.\n'
    text += 'Regression Level: ' + str(Regression_Level) + '.\n'
    return text

### Refresh DB
@app.route('/get_db')
def Download_DB():
    return send_from_directory(directory='', filename=DB_Name, as_attachment=True)

@app.route('/clear_db')
def Clear_DB():
    db = sqlite3.connect(DB_Name)
    cursor = db.cursor()
    cursor.execute('DELETE FROM CustomGraphData')
    db.commit()
    cursor.execute('DELETE FROM Request')
    db.commit()
    db.close()
    return 'Custom Graph Data cleared.'

if __name__ == '__main__':
    app.run()
