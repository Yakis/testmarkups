import falcon
import pymongo
import json
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import datetime as dt
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

client = pymongo.MongoClient("localhost:27017")
db = client["favorites"]
markup_collection = db["markups"]
article_collection = db["articles"]


class Markups(object):

    def on_post(self, req, resp):
        doc = req.media
        doc['timestamp'] = dt.datetime.now().astimezone().isoformat()
        logging.info(doc)
        x = markup_collection.insert_one(doc)
        if x.inserted_id:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_403


    def on_get(self, req, resp):
        obj_list = []
        resp.status = falcon.HTTP_200 
        for x in markup_collection.find():
            obj_list.insert(0, x)
        resp.body = json.dumps(obj_list, sort_keys=True, indent=4, default=json_util.default)


    def on_delete(self, req, resp, id):
        logging.info('Deleted %s markup', id)
        myquery = {'_id': ObjectId(id)}
        markup_collection.delete_one(myquery)
        resp.status = falcon.HTTP_200



class Articles(object):

    def on_post(self, req, resp):
        doc = req.media
        doc['timestamp'] = dt.datetime.now().astimezone().isoformat()
        logging.info(doc)
        x = article_collection.insert_one(doc)
        if x.inserted_id:
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_403


    def on_get(self, req, resp):
        obj_list = []
        resp.status = falcon.HTTP_200 
        for x in article_collection.find():
            obj_list.insert(0, x)
        resp.body = json.dumps(obj_list, sort_keys=True, indent=4, default=json_util.default)


    def on_delete(self, req, resp, id):
        logging.info('Deleted %s article', id)
        myquery = {'id': id}
        article_collection.delete_one(myquery)
        resp.status = falcon.HTTP_200


app = falcon.App()

markups = Markups()
articles = Articles()

app.add_route('/markups/{id}', markups)
app.add_route('/markups', markups)
app.add_route('/favorites/{id}', articles)
app.add_route('/favorites', articles)
