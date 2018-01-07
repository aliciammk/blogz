from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz-app@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    #defines the blog class for the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(750))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.user = user

class User(db.Model):
    #defines the user for the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password


#@app.before_request
#def require_login():
    #allowed_routes = ['login', 'register']
    #if request.endpoint not in allowed_routes and 'email' not in session:
        #return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')


    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        existing_user = User.query.filter_by(username=username).first()
        #validates user password  
        if len(username) == 0:
            flash('Please enter a username.', 'error')
        elif len(password) == 0:
            flash('Please enter a password.', 'error')
        elif len(verify) == 0:
            flash('Please verify password.', 'error')
        elif password != verify:
           flash('Passwords do not match.', 'error')
        elif not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash('Duplicate user.', 'error')

    return render_template('register.html')


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    #displays single blog entry
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('entry.html', blog=blog, title="Blog Entry")
    #displays all blogs on one page
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', title="Build a blog", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    # creates a new post
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(title, body, user)
        
        # redirects to post after post is successfully made
        if len(title) > 0 and len(body) > 0:
            db.session.add(new_blog)
            db.session.commit()
            new_blog_id = new_blog.id
            blog = Blog.query.get(new_blog_id)
            url = "/blog?id=" + str(new_blog_id)
            return redirect(url)

        # redirects back to form with error if user leaves field blank
        elif len(title) == 0:
            flash('Please fill in a title for your blog.', 'error')
            return render_template('newpost.html', body=body)

        elif len(body) == 0:
            flash('Please fill in the body for your blog.', 'error')
            return render_template('newpost.html', title=title) 

    return render_template('newpost.html')
            

@app.route('/', methods=['POST','GET'])
def index():
    # redirects to page with all blogs displayed
    return redirect('/blog')

if __name__ == '__main__':
    app.run()