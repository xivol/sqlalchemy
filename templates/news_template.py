from flask import Flask
from flask import render_template
from data.news import News

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index1.html', news_image=News.news_img, news_title=News.title, news_text=News.content,
                           news_date=News.created_date)
