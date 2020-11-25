# Update apt
sudo apt-get update

# Get pip3
sudo apt-get install python3-pip
pip3 install -r requirements.txt

# Get gunicorn
sudo apt-get install gunicorn

# Launch
gunicorn wsgi:app --bind 0.0.0.0:8000
