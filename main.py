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
    #defines the blog class for the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(750))

    def __init__(self, title, body):
        self.title = title
        self.body = body


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
        new_blog = Blog(title, body)
        
        
        # redirects to post after post is successfully made
        if len(title) > 0 and len(body) > 0:
            db.session.add(new_blog)
            db.session.commit()
            new_blog_id = new_blog.id
            blog = Blog.query.get(new_blog_id)
            url = "/blog?id=" + str(new_blog_id)
            return redirect(url)

        # redirects back to form with error if user leaves field blank
        elif len(title) == 0 and len(body) > 0:
            flash('Please fill in a title for your blog.', 'error')
            return render_template('newpost.html', body=body)

        elif len(title) > 0 and len(body) == 0:
            flash('Please fill in the body for your blog.', 'error')
            return render_template('newpost.html', title=title)
    
    else:
        return render_template('newpost.html')
            

@app.route('/', methods=['POST','GET'])
def index():
    # redirects to page with all blogs displayed
    return redirect('/blog')

if __name__ == '__main__':
    app.run()