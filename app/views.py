from app import app
from flask import render_template,request
import feedparser
import jinja2
import os
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
@app.route('/')
@app.route('/index')
def search():

    return render_template('index.html')

@app.route('/searchRSS',methods=['POST'])

def search_results():
    feed = feedparser.parse("http://news.google.com/news?hl=en&gl=in&q="+request.form['query']+"&um=1&output=rss" )
    print feed['feed']
    posts = []
    for i in range(0,len(feed['entries'])):
        posts.append({
            'title': feed['entries'][i].title,
            'date': feed['entries'][i].updated,
            'description': strip_tags(feed['entries'][i].description)

        })
    print  posts
    return render_template('index.html', posts=posts)