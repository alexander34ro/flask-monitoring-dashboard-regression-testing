from flask import Flask, send_from_directory, current_app
import flask_monitoringdashboard as dashboard
import time, datetime, os, psutil

# Remove Database
DB_Name = "flask_monitoringdashboard.db"
os.remove(DB_Name)

### FMD Setup
app = Flask(__name__)
dashboard.bind(app)

# Mining CPU Data
def CPU():
    cpu = psutil.cpu_percent()
    print(f"{datetime.datetime.now()} | CPU: {cpu}")
    return cpu


every_second_schedule = {'seconds': 5}

dashboard.add_graph("CPU Usage", CPU,
                    "interval", **every_second_schedule)

### Regressions
# CPU Heavy Regression
def Fibonacci(n):
    if n == 1: return 0
    elif n == 2: return 1
    else: return Fibonacci(n - 1) + Fibonacci(n - 2)

def CPU_Heavy_Regression():
    print(Fibonacci(28))

# CPU Light Regression
def CPU_Light_Regression():
    time.sleep(1)

### Main
@app.route('/')
def Main():
    CPU_Heavy_Regression()
    return "Executed main body."

### Refresh DB
def Download_File():
    file_handle = open(DB_Name, 'rb')

    def stream_and_remove_file():
        yield from file_handle
        file_handle.close()
        os.remove(DB_Name)

    return current_app.response_class(
        stream_and_remove_file(),
        headers = {
            'Content-Disposition': 'attachment',
            'filename': 'db_copy.db',
            'mimetype': 'db'
        }
    )

@app.route('/db')
def Download_DB():
    return Download_File()

if __name__ == '__main__':
    app.run()
