from flask import Flask, render_template, json, request, Response, jsonify
from flask.ext.pymongo import PyMongo
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
import subprocess

app = Flask(__name__)

# app.config['MONGO_HOST'] = '127.10.85.2'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'runlinux'
# app.config['MONGO_URI'] = 'mongodb://127.10.85.2:27017/runlinux'
# app.config['MONGO_USERNAME'] = 'admin'
# app.config['MONGO_PASSWORD'] = 'dp53nstHebqE'
# mongo = PyMongo(app, config_prefix='MONGO')
mongo = PyMongo(app) #for local MongDB


from pymongo import Connection
connection = Connection()
print(connection.database_names())	
db = connection.runlinux
collection = db.linuxCommand

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/linuxCommand')
def linuxCommand():
    return render_template('linuxCommand.html')    

@app.route('/signUp',methods=['POST'])
def signUp():
 
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
        '''return redirect(url_for('linuxCommand'))'''
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/signIn',methods=['POST'])
def signIn(): 	
	 if request.headers['Content-Type'] == 'text/plain':
	 	return "Text Message: " + request.data
	 elif request.headers['Content-Type'] == 'application/json':	 			 	  
	 	  json = request.json;		 	 
	 	  _linuxCommand = json.get("linuxCommand")
	 	  _email = json.get("inputEmail")
	 	  _password = json.get("inputPassword")
	 	  
	 	  # validate the received values
	 	  if _email and _password and _linuxCommand:	 	  		 		 	 
	 	  	p = subprocess.Popen(_linuxCommand,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdin=subprocess.PIPE)
	 	  	out,err = p.communicate()	 	  		  	 	 
	 	  	js = {'commandResponse' : out}          	 	  	  
	 	  	return jsonify(js)	 	  
		  else:
		  	return json.dumps({'html':'<span>Enter the required fields</span>'})
	 else:
	 	return "WTF"

@app.route('/logout')
def logout():   
    return redirect(url_for('main'))        

if __name__ == "__main__":
	app.run()
