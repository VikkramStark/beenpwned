from flask import Flask, jsonify, request, render_template 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///extended_wordlist.db"
db = SQLAlchemy(app) 

class WordList(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False) 
    word = db.Column(db.String(30), nullable = False, unique = True)    

    def __repr__(self):
        return f"Word<{self.word}>"  
    
class Email(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True) 
    email = db.Column(db.String(50), nullable = False) 

    def __repr__(self):
        return f"<Email {self.email}>" 

class Phone(db.Model):
    id = db.Column(db.Integer, nullable = False, primary_key = True) 
    number = db.Column(db.BigInteger,nullable = False) 
    name = db.Column(db.String(25), nullable = False) 

    def __repr__(self):
        return f"<Phone {self.number} - {self.name}>"   

@app.get("/") 
def home():
    return render_template("index.html");  

@app.post("/password") 
def pwned_passsword():
    # print(request.form) 
    # print(request.data)   
    print(request.json) 
    password = str(request.json.get("password")) 
    print(password) 
    search_password = WordList.query.filter_by(word = password).first() 
    print(f"search_result : {search_password}")     

    if search_password !=None: 
        return jsonify({"found":search_password.word, "breached":True}), 201    
    else:
        return jsonify({"breached":False}), 201 

@app.post("/phone") 
def pwned_number():
    print(request.json) 
    number = request.json.get("number") 
    search_number = Phone.query.filter_by(number = number).first() 
    print("Pwned Number Result:", search_number) 

    if search_number != None:
        return jsonify({"found":number, "name":search_number.name, "breached":True}), 201 
    else:
        return jsonify({"breached":False})   
    
@app.post("/email") 
def pwned_email():
    print(request.json) 
    email = request.json.get("email") 
    search_mail = Email.query.filter_by(email = email).first() 
    print("Pwned Email Result:", search_mail) 
    if search_mail != None:
        return jsonify({"found":email,"breached":True}), 201 
    else:
        return jsonify({"breached":False}), 201  

if __name__ == "__main__":
    app.run(host = "localhost", port = 8000, debug = True) 
    db.create_all() 
    app.app_context().push() 