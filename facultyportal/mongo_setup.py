import mongoengine
import pymongo

alias_core = 'core'
mdb = 'profile'

# data = dict(
#     username='admin',
#     password='pass',
#     host='http://127.0.0.1',
#     port='5000',
#     authentication_source='admin',
#     authentication_mechanism='SCRAM-SHA-1',
#     ssl=True,
#     ssl_cert_reqs=ssl.CERT_NONE
# )

# def global_init():
#     mongoengine.register_connection(alias=alias_core, name=mdb)

class MongodbProfile:
    def __init__(self):
        self.connect()

    def connect(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mdb = myclient["faculty_profile"]
        self.mycol = mdb["profile"]

    def createProfile(self, email):
        self.mycol.insert_one({'email':email})

    def getProfile(self, email):
        return self.mycol.find_one({'email':email})

    def updateBio(self, email, bio):
        myquery = { "email": email }
        newvalues = { "$set": { "bio": bio } }

        self.mycol.update_one(myquery, newvalues)

    def addPublication(self, email, title, content):
        myquery = { "email": email }
        newvalues = { "$push": { "pubs": {'title':title, 'content':content} } }

        self.mycol.update_one(myquery, newvalues)

    def updatePublication(self, email, title, content):
        myquery = { "email": email, 'pubs.title': title }
        newvalues = { "$set": { "pubs.$.title": title, "pubs.$.content": content } }

        self.mycol.update_one(myquery, newvalues)

    def getPublication(self, email, title):
        return self.mycol.find_one({'email':email},
                {'_id':0, 'pubs': {'$elemMatch':{'title':title}}})

    def deletePublication(self, email, title):
        myquery = { "email": email }
        newvalues = { "$pull": { "pubs": {'title':title} } }

        self.mycol.update_one(myquery, newvalues)