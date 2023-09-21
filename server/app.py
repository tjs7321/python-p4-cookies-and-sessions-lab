#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_restful import Api, Resource
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Clear(Resource):
    def get(self):
        session['page_views'] = 0
        return {'message': '200: Successfully cleared session data.'}, 200

api.add_resource(Clear, '/clear')

class Articles(Resource):

    def get(self):

        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200
    
api.add_resource(Articles, '/articles')

class ArticleByID(Resource):

    def get(self, id):

        session['page_views'] = session.get('page_views') or 0
        session['page_views'] += 1
        article = Article.query.filter_by(id=id).first().to_dict()
        if session['page_views'] <= 3:
            return article, 200
        return {'message':'Maximum pageview limit reached'}, 401

api.add_resource(ArticleByID, '/articles/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
