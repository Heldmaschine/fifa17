from app import mdb


class Post(mdb.Document):
    title = mdb.StringField()
    text = mdb.StringField()
    author = mdb.StringField()
    category = mdb.IntField()


class Comment(mdb.Document):
    text = mdb.StringField()
    author = mdb.StringField()
    post = mdb.DocumentField(Post)
