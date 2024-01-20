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

if __name__ == "__main__":
    app.run(host = "localhost", port = 8000, debug = True) 
    db.create_all() 
    app.app_context().push() 