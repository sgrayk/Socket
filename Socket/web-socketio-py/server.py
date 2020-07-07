
#Requirement: install Flask and Flask-socketio
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Templates include pages: login, info, 404
app = Flask(__name__, static_folder='./templates', template_folder='./templates') # point to current folder

app.config[ 'SECRET_KEY' ] = 'secret!'; # SECRET_KEY is generated to keep client-side sessions secure, we can generate random key  
socketio = SocketIO(app);


#Default route to load login page
@app.route('/')
def index_login():
  return render_template('/login/index.html')

#If login success, redirect to info page 
@app.route('/info')
def index_info():
  return render_template('/members/index.html') # include info of us

#if login fail, turn to 404 page 
@app.errorhandler(404)
def page_not_found(e):
  socketio.emit('error', '404')
  return render_template('/404/index.html'), 404 

# Handle when user connect to server
@socketio.on('conn')
def handle_login(json):
  print('Client: ' + str(json))

# When user send form login
@socketio.on('login')
#get user_name and password from user
def handle_login(data):
  user_name = data['data']['user_name']
  password = data['data']['password']

  # Check if login success
  if user_name == "admin" and password == "admin":
    socketio.emit('redirect', 'info') 
  else:
    socketio.emit('redirect', 404)

# Start server: python server.py
if __name__ == '__main__':
    socketio.run(app)