from flask import Flask, render_template, request, make_response, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

def validate_domain():
    host = request.host.split(':')[0]  # Remove port number
    if host != 'blog.cookie-tossing.lab':
        return False
    return True

# In-memory storage for blog posts and comments (for demo purposes) using a Python list that has a dictionary nested inside it
blog_posts = [
    {
        'id': 1,
        'title': 'Hello World',
        'content': 'Welcome to my first blog post!',
        'author': 'Elliot',
        'date': '2024-03-15',
        'comments': []
    },
    {
        'id':2,
        'title': 'Cookie Tossing',
        'content': 'Cookie tossing is a technique that allows an attacker to exfiltrate data from a user by chaining XSS vulnerabilities.',
        'author': 'Sam_Altman',
        'date': '2025-06-17',
        'comments': [] #This is where the comments are stored in a Python list
    }
]

@app.route('/')
def index():
    if not validate_domain():
        return "Access Denied", 403
        
    # Removed automatic cookie setting to make it more vulnerable to cookie tossing
    return render_template('post.html', posts=blog_posts)

@app.route('/add-comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if not validate_domain():
        return "Access Denied", 403
        
    # Vulnerable to XSS - user input is not escaped
    comment = request.form.get('comment', '')
    username = request.form.get('username', 'Anonymous')
    
    # Find the post and add the comment
    for post in blog_posts:
        if post['id'] == post_id:
            post['comments'].append({
                'content': comment,  # Vulnerable: comment is not escaped
                'author': username,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            break
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 