# from tkinter.tix import COLUMN, INTEGER
from sqlalchemy import Column, Integer, String, DateTime, false, null
from base import Base
import datetime

class Blog(Base):
    """ Blog """
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True)
    trans_id = Column(String(250), nullable=False)
    blog_id = Column(String(250), nullable=False)
    title = Column(String(100), nullable=False)
    snippet = Column(String(250), nullable=False)
    blogBody = Column(String(250), nullable=False)
    userName = Column(String(250), nullable=False)
    postNumbers = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, trans_id, blog_id, title, snippet, blogBody, userName, postNumbers, date):
        """ Initializes blogs """
        self.trans_id = trans_id
        self.blog_id = blog_id
        self.title = title
        self.snippet = snippet
        self.blogBody = blogBody
        self.userName = userName
        self.postNumbers = postNumbers
        self.date = datetime.datetime.now()
    
    def to_dict(self):
        """ Dictionary for blogs """
        dict = {}
        dict['id'] = self.id
        dict['trans_id'] = self.trans_id
        dict['blog_id'] = self.blog_id
        dict['title'] = self.title
        dict['snippet'] = self.snippet
        dict['blogBody'] = self.blogBody
        dict['userName'] = self.userName
        dict['postNumbers'] = self.postNumbers
        dict['date'] = self.date

        return dict
