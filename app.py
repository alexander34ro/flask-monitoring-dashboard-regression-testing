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
    print(Fibonacci(20))

# CPU Light Regression
def CPU_Light_Regression():
    time.sleep(1)

### Main
@app.route('/')
def Main():
    db = sqlite3.connect(DB_Name)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM CustomGraphData')
    resultset = cursor.fetchall()

    if (Regression_Level == 1 or Regression_Level == 3):
        CPU_Light_Regression()
    if (Regression_Level == 2 or Regression_Level == 3):
        CPU_Heavy_Regression()

    db.close()
    return 'Executed main body. Number of records: ' + str(len(resultset))

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
    db.close()
    return 'Custom Graph Data cleared.'

if __name__ == '__main__':
    app.run()
