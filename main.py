from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:cheese123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
# rewrite this to be a blog with id, title, body
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(750))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def blog():
# TODO rewrite to display a page that shows a singular blog post

    return render_template('blog.html', blog=blog)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
# TODO rewrite so this page allows user to submit new post
# TODO include error if either the blog body or title are left empty, keeping content entered content
        
    #blog_title = request.form['title']
    #blog_body = request.form['body']
    #new_blog = Blog(blog_title, blog_body)
    #db.session.add(new_blog)
    #db.session.commit()

    return render_template('newpost.html')


@app.route('/', methods=['POST','GET'])
def index():
# render a page that shows all the blogs
    return render_template('blog.html', title="Build a blog",)

if __name__ == '__main__':
    app.run()