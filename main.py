#calling rest api using flask
from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL
import requests
import json
import yaml

app = Flask(__name__)

#Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/posts',methods=['GET'])
def index():
  req = requests.get('https://jsonplaceholder.typicode.com/posts')
  data = json.loads(req.content)
  return render_template('index.html',data=data)

@app.route('/comments',methods=['GET'])
def comments():
  req = requests.get('https://jsonplaceholder.typicode.com/comments')
  data = json.loads(req.content)
  return render_template('comments.html',data=data)

@app.route('/users',methods=['GET'])
def users():
  req = requests.get('https://jsonplaceholder.typicode.com/users')
  data = json.loads(req.content)
  return render_template('users.html',data=data)

@app.route('/new',methods=['GET','POST'])
def new_post():
  if request.method == 'POST':
    postDetails=request.form
    title = postDetails['title']
    body = postDetails['body']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO posts(title,body) VALUES(%s,%s)",(title,body))
    mysql.connection.commit()
    return 'Successfully added'
  elif request.method == 'GET':
    return render_template('new_post.html')




if __name__ == '__main__':
  app.run(debug=True)