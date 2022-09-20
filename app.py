
from asyncio.windows_events import NULL
from re import S
import json
from flask import Flask,render_template,request,jsonify,flash,redirect,session
from flask_pymongo import PyMongo
from password_strength import PasswordPolicy
from password_strength import PasswordStats
from flask_session import Session
from flask_bcrypt import Bcrypt


app = Flask(__name__)

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    strength=0.66 # need a password that scores at least 0.5 with its entropy bits
)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = '@#$%^&*('
app.config['MONGO_URI']="mongodb://localhost/books"

sessionv = Session(app)

bcrypt = Bcrypt(app)


mongo=PyMongo(app)

db=mongo.db.users 
db2=mongo.db.Book
db3=mongo.db.forum

k=db2.insert_one({

})


@app.route('/', methods=['POST','GET'])
def login():
    global userid
    if request.method == "POST":

        new_email = request.form['email']
        password = request.form['psw']


        res = db.find({"email": new_email},{"_id":1,"password":1})
        l = list(res)

        if len(l) != 0 and bcrypt.check_password_hash(l[0]["password"],password):

            session["email"] = new_email
            userid = l[0]["_id"]
            flash(f"You are successfully logged in!",'success')
            return redirect("/homepage")

        else:

            flash(f"Invalid Email ID or Password",'danger')
            return redirect("/")

    return render_template("login.html")

@app.route('/homepage')
def home():
    return render_template('Homepage.html')



@app.route('/registration', methods=['GET','POST'])
def Register():
    return render_template('registartion.html')

@app.route('/send_data',methods=['POST','GET'])
def get_data():
    new_password=request.form['psw']
    # stats = PasswordStats(new_password)
    # checkpolicy = policy.test(new_password)
    # haspassword=bcrypt.hashpw(new_password.encode('utf-8'),bcrypt.gensalt())
    haspassword=bcrypt.generate_password_hash(new_password)
    id =db.insert_one({
        'email':request.form['email'],
        'name':request.form['name'],
        'password':haspassword,
        'age':request.form['age'],
        'Fav_b':request.form['Fav_b'],
        'Fav_a':request.form['Fav_a']

        })      
    return redirect('/')

@app.route('/review',methods=['POST','GET'])
def review():
    # kk=[]
    # kip=[]
    if request.method == "POST":
        #bo_title=request.form['name']
        #print(bo_title)
        rate_k=request.form['rat']
        print(rate_k)
        shi=float(rate_k)
        print(type(shi))
    #     idk=db2.find({'title':bo_title})
    #     ratingvar=list(db2.find({'title':bo_title},{'average_rating':1,'_id':0}))
    #     print(ratingvar)
        
    #     k=db2.find({'title':bo_title},{'average_rating':1,'ratings_count':1,'_id':0})
    
    #     for i in k:
    #         avg=i['average_rating']
    #         print(avg)
        #print(avg)
        #print(cou)
        #   tot=avg*cou
    #rate_k="43.23"
        # print(shi)
        # print(type(shi))
        # print(float(shi))
        # print(type(shi))
        #new=int(float(rate_k))
        #print(new)
        #dev=int(rate_k)
        # tot=tot+rate_k
        # cou=cou+1
        # final=tot/cou

        # gar=db2.update_one({'title':bo_title,'average_count':final})
        # print(gar)
        

        
        # for i in idk:
        #   kk.append(i)   

       
    return render_template('review.html')

@app.route('/forum')
def forum():
    kd=[]
    ss=db3.find()
    for i in ss:
        kd.append(i)
    print(kd)
    return render_template('forum.html',kd=kd)

@app.route('/posting', methods=['POST','GET'])
def post():
    if request.method == "POST":
        kk=db3.insert_one({

        'name':request.form['name'],
        'title':request.form['title'],
        'content' :request.form['content']

        })

    return render_template('forum_form.html')

@app.route('/forum/<bookID>', methods=['POST','GET'])
def b_review(bookID):
    ks=[]
    oops=db3.find({'bookID':bookID})
    
    for i in oops:
        ks.append(i)
    return render_template('/review.html',ks=ks)
        

# @app.route('/profile',methods=['POST','GET'])
# def prof():


if(__name__=='__main__'):

    app.run(port=2000,debug=True)