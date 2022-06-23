import smtplib
import random

import timeago, datetime
import flask
from question import Quiz
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///advises.db'
app.config['TESTING'] = False

db = SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return  Register.query.filter_by(id=user_id).first()


class Register(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    stats = db.Column(db.String(120))
    posts = db.relationship('Blog', backref='register')

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('register.id'))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    what_i_have_been_through = db.Column(db.String(400))
    what_i_did_to_overcome = db.Column(db.String(400))
    tips = db.Column(db.String(400))
    time = db.Column(db.String(100))
db.create_all()

@app.route('/',methods=['POST','GET'])
def home():
    on=current_user.is_authenticated
    return render_template("index.html",on=on)

@app.route('/AppHome',methods=['POST','GET'])
def AppHome():
    if (current_user.is_authenticated):
        quotes=["If you want to achieve greatness stop asking for permission.",
                "Be yourself; everyone else is already taken.",
                "Be the change that you wish to see in the world.",
                "It is never too late to be what you might have been.",
                "I have very strong feelings about how you lead your life. You always look ahead, you never look back",
                "You’re off to great places, today is your day. Your mountain is waiting, so get on your way.",
                "You always pass failure on the way to success.",
                "No one is perfect - that’s why pencils have erasers.",
                "Keep your face to the sunshine and you cannot see a shadow.",
                "Positive thinking will let you do everything better than negative thinking will.",
                "When you are enthusiastic about what you do, you feel this positive energy. It’s very simple.",
                "Winning is fun, but those moments that you can touch someone’s life in a very positive way are better.",
                "We become what we think about",
                "Eighty percent of success is showing up.",
                "Your time is limited, so don’t waste it living someone else’s life.",
                "Winning isn’t everything, but wanting to win is",
                "Either you run the day, or the day runs you.",
                "Ask and it will be given to you; search, and you will find; knock and the door will be opened for you.",
                "Believe you can and you’re halfway there.",
                " Fall seven times and stand up eight. ",
                " Happiness is not something readymade.  It comes from your own actions.",
                " Challenges are what make life interesting and overcoming them is what makes life meaningful."]
        quote=random.choice(quotes)

        return render_template('AppHome.html',name=current_user.name.title(),quote=quote)
    else:
        return flask.redirect('/login')

@app.route('/howitworks',methods=['POST','GET'])
def HIW():
    return render_template("howitworks.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if(current_user.is_authenticated):
        return flask.redirect('/AppHome')

    else:
        if(request.method=="GET"):
            return render_template("sign.html")
        else:
            try:
                new=Register(name=request.form.get("name"),email=request.form.get("email"),password=request.form.get("psd"))
                db.session.add(new)
                db.session.commit()
                return flask.redirect('/AppHome')
            except exc.IntegrityError:
                return flask.render_template('prithvipage1.html')

@app.route('/report',methods=['POST','GET'])
def report():
    if(current_user.is_authenticated):
        return render_template("invalid.html")
    else:
        return flask.redirect('/login')

@app.route('/relax',methods=['POST','GET'])
def relax():
    if(current_user.is_authenticated):
        return render_template("relax.html")
    else:
        return flask.redirect('/login')

@app.route('/post',methods=['POST','GET'])

def post():
    if (current_user.is_authenticated):
        if(request.method=="GET"):
            return render_template("addpost.html")
        else:
            userid = current_user.id
            name = current_user.name
            email = current_user.email
            what_i_have_been_through = request.form.get("wihbt")
            what_i_did = request.form.get("wid")
            tips = request.form.get("tips")
            new=Blog(
                userid=userid,
                name=name,
                email=email,
                what_i_have_been_through=what_i_have_been_through,
                what_i_did_to_overcome=what_i_did,
                tips=tips,
                time=datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
            )
            db.session.add(new)
            db.session.commit()

        return flask.redirect('/view-posts')

    else:
        return flask.redirect('/login')
@app.route('/view-posts',methods=['POST','GET'])

def viewps():
    if (current_user.is_authenticated):
        if(request.method=="GET"):
            Blogs = Blog.query.all()
            BLOG=[]
            for blog in Blogs:
                dit={}
                dit["id"]=blog.id
                dit["name"]=blog.name.strip().title()
                dit["what_i_have_been_through"]= blog.what_i_have_been_through.strip().title()
                now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
                dit["time"]=timeago.format(blog.time.split(".")[0], now)
                BLOG.append(dit)


            return render_template("viewBLogs.html",Blogs=BLOG)
    else:
        return flask.redirect('/login')

@app.route('/view/<int:id>',methods=['POST','GET'])

def view(id):
    if(request.method=="GET"):
        blog= Blog.query.filter_by(id=id).first()

        dit={}
        dit["name"]=blog.name.strip().title()
        dit["email"] = blog.email.strip()
        dit["what_i_have_been_through"]= blog.what_i_have_been_through.strip().title()
        dit["what_i_did_to_overcome"]= blog.what_i_did_to_overcome.strip().title()
        dit["tips"]= blog.tips.strip()
        now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
        dit["time"]=timeago.format(blog.time.split(".")[0], now)
        return render_template("viewPost.html",Blog=dit)

@app.route('/login',methods=['POST','GET'])
def login():

    if(current_user.is_authenticated):
        return flask.redirect('/AppHome')
    else:
        if(request.method=="GET"):
            return render_template("mainlogin.html")
        else:
            email=request.form.get("email")
            psd=request.form.get("psd")
            user=Register.query.filter_by(email=email).first()
            if(user):
                if(user.password==psd):
                    login_user(user)
                    print(current_user.name)
                    return flask.redirect('/AppHome')
                else:
                    return "invalid details"
            else:
                return "invalid details"

@app.route('/selftest',methods=['POST','GET'])
def selftest():
    if (current_user.is_authenticated):
        if(request.method=="GET"):
            quiz=Quiz()

            return render_template('Selftest.html',questions=quiz.getQuestions())
        else:
            q="question"
            quiz = Quiz()
            answers=[]
            for i in range(1,len(quiz.getQuestions())+1):
                answers.append(request.form.get(q+str(i)))
            marks=quiz.checkanswer(answers)

            admin = Register.query.filter_by(id=current_user.id).first()
            admin.stats = marks
            db.session.commit()

            motive=[
                "Meditation, which is a mind and body practice where you learn to focus your attention and awareness.",
                "Practicing gratitude, which means being thankful for the good things in your life. It's helpful to do this every day, either by thinking about what you are grateful for or writing it down in a journal.",
                "It's important to try to have a positive outlook; some ways to do that include finding balance between positive and negative emotions.",
                "Developing coping skills, which are methods you use to deal with stressful situations."
                ]
            return render_template('marks.html',marks=marks,motive=random.choice(motive))
    else:
        return flask.redirect('login')

@app.route("/sendmail/<Email>",methods=['POST','GET'])
def test(Email):

    email = "medvicementalhealth@gmail.com"
    password = "medvice.com"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        sub=request.form.get('subject')
        body=request.form.get('body')

        connection.sendmail(from_addr=email, to_addrs=Email.split('-')[0],msg=f"Subject:'From Medvice '{sub}\n\n{'Hello there from Medvice '}\n{body}\n Contact this Person by {Email.split('-')[1]}")
    return render_template('sucesssmail.html')


@app.route('/profile')
def profile():
    if (current_user.is_authenticated):
        values={"stats":current_user.stats,"noofblog":str(Blog.query.filter_by(userid = current_user.id).count())}

        return render_template('profile.html',values=values)
    else:
        return flask.redirect('login')

@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect('/')


@app.route('/music',methods=['POST','GET'])
def music():
    if (current_user.is_authenticated):
        return render_template('main.html')
    else:
        return flask.redirect('/login')


app.run(debug=True)