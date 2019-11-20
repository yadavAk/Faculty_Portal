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

    def updateBio(self, email, title, content):
        myquery = { "email": email}
        newvalues = { "$set": { "bio": {'title':title, "content": content } }}

        self.mycol.update_one(myquery, newvalues)

    def getBio(self, email, title):
        return self.mycol.find_one({'email':email},
                {'_id':0, 'bio': 1})


    def addPublication(self, email, title, content):
        myquery = { "email": email }
        newvalues = { "$push": { "pubs": {'title':title, 'content':content} } }

        self.mycol.update_one(myquery, newvalues)

    def updatePublication(self, email, old_title, title, content):
        myquery = { "email": email, 'pubs.title': old_title }
        newvalues = { "$set": { "pubs.$.title": title, "pubs.$.content": content } }

        self.mycol.update_one(myquery, newvalues)

    def getPublication(self, email, title):
        return self.mycol.find_one({'email':email},
                {'_id':0, 'pubs': {'$elemMatch':{'title':title}}})

    def deletePublication(self, email, title):
        myquery = { "email": email }
        newvalues = { "$pull": { "pubs": {'title':title} } }

        self.mycol.update_one(myquery, newvalues)
    
    def addAward(self, email, title, content):
        myquery = { "email": email }
        newvalues = { "$push": { "award": {'title':title, 'content':content} } }

        self.mycol.update_one(myquery, newvalues)

    def updateAward(self, email, old_title, title, content):
        myquery = { "email": email, 'award.title': old_title }
        newvalues = { "$set": { "award.$.title": title, "award.$.content": content } }

        self.mycol.update_one(myquery, newvalues)

    def getAward(self, email, title):
        return self.mycol.find_one({'email':email},
                {'_id':0, 'award': {'$elemMatch':{'title':title}}})

    def deleteAward(self, email, title):
        myquery = { "email": email }
        newvalues = { "$pull": { "award": {'title':title} } }

        self.mycol.update_one(myquery, newvalues)


    def addOther(self, email, title, content):
        myquery = { "email": email }
        newvalues = { "$push": { "other": {'title':title, 'content':content} } }

        self.mycol.update_one(myquery, newvalues)

    def updateOther(self, email, old_title, title, content):
        myquery = { "email": email, 'other.title': old_title }
        newvalues = { "$set": { "other.$.title": title, "other.$.content": content } }

        self.mycol.update_one(myquery, newvalues)

    def getOther(self, email, title):
        return self.mycol.find_one({'email':email},
                {'_id':0, 'other': {'$elemMatch':{'title':title}}})

    def deleteOther(self, email, title):
        myquery = { "email": email }
        newvalues = { "$pull": { "other": {'title':title} } }

        self.mycol.update_one(myquery, newvalues)