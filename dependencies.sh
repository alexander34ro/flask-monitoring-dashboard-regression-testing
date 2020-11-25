# Get pip3
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements.txt

# Launch
gunicorn wsgi:app --bind 0.0.0.0:8000
