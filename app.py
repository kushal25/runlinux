from flask import Flask, render_template, json, request, Response, jsonify
from flask.ext.pymongo import PyMongo
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
import subprocess

app = Flask(__name__)

# app.config['MONGO_HOST'] = '127.10.85.2'
# app.config['MONGO_PORT'] = 27017
# app.config['MONGO_DBNAME'] = 'runlinux'
app.config['MONGO_URI'] = 'mongodb://127.10.85.2:27017/runlinux'
app.config['MONGO_USERNAME'] = 'admin'
app.config['MONGO_PASSWORD'] = 'dp53nstHebqE'
mongo = PyMongo(app, config_prefix='MONGO')

# mongo = PyMongo(app) #for local MongDB


# from pymongo import Connection
# connection = Connection()
# db = connection.runlinux

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

@app.route('/command', methods=['POST'])
def command():   
	 if request.headers['Content-Type'] == 'application/json':	 			 	  
		  json = request.json	 	 
		  _linuxCommand = json.get("linuxCommand")		 
		   # validate the received values
		  if _linuxCommand:
		  	comm = _linuxCommand.split(' ')
			p = subprocess.Popen(comm,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
			out,err = p.communicate()
			js = {'commandResponse' : out}
			return jsonify(js)
		  else:
		  	return jsonify({'commandResponse' : 'Enter the required fields'})
	 else:
		return jsonify({'commandResponse' : 'Cannot Find JSON type'})

@app.route('/signUp',methods=['POST'])
def signUp():	
	if request.headers['Content-Type'] == 'application/json':
		json = request.json			
		_name = json.get("inputName")
		_email = json.get("inputEmail")
		_password = json.get("inputPassword")
		reqJson = {"name" : _name,"email" : _email, "password" : _password}		
		if _email and _password and _name:		
			res = mongo.db.linuxCommand.find({'email' : _email})								
			if(res.count()>0):			
				return jsonify({'commandResponse' : 'user already exists'})
			else:						
				abc = mongo.db.linuxCommand.save(reqJson)			
				return jsonify({'commandResponse' : 'user successfully registered','flag' : 1})			
		else:
			return jsonify({'commandResponse' : 'Enter the required fields'})
	else:
	 	return jsonify({'commandResponse' : 'Cannot Find JSON type'})


@app.route('/signIn',methods=['POST'])
def signIn(): 		 
	 if request.headers['Content-Type'] == 'application/json':	 			 	  
		  json = request.json	 	 	
		  _email = json.get("inputEmail")
		  _password = json.get("inputPassword")		  		
		  if _email and _password:
			res = mongo.db.linuxCommand.find({'email' : _email})
			if(res.count()>0):
				if(res[0].get("email") == _email and res[0].get("password") == _password):
					return jsonify({'commandResponse' : 'user loggedin successfully', 'flag' : 1})
				else:
					return jsonify({'commandResponse' : 'Incorrect Credentials'})
			else:
				return jsonify({'commandResponse' : 'No User Found'})
		  else:
			return jsonify({'commandResponse' : 'Enter the required fields'})
	 else:
		return jsonify({'commandResponse' : 'Cannot Find JSON type'})

@app.route('/logout', methods=['GET'])
def logout():   
	return render_template('signin.html')       

if __name__ == "__main__":
	app.run()
