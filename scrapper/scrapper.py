from bs4 import BeautifulSoup
import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/sqlite/test.db'
db = SQLAlchemy(app)

class NewsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    link = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()

def scrapper():
    #上下文？
    with app.app_context():
        url = "https://news.hqu.edu.cn/hdyw.htm"
        response = requests.get(url)
        html_content = response.content.decode('utf-8')
        soup = BeautifulSoup(html_content, 'lxml')
        news_list = soup.find_all('a')

        for news in news_list:
            title = news.text
            link = news['href']
            link = 'https://news.hqu.edu.cn/' + link
            existing_news = NewsData.query.filter_by(link=link).first()
            if existing_news is None:
                news_data = NewsData(title=title, link=link)
                db.session.add(news_data)
                
        db.session.commit()

if __name__ == "__main__":
    scrapper()