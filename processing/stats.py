from sqlalchemy import Column, Integer, String, DateTime
from base import Base
class Stats(Base):
    """ Processing Statistics """
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_users = Column(Integer, nullable=False)
    number_posts = Column(Integer, nullable=False)
    average_posts = Column(Integer, nullable=False)
    most_posts = Column(String, nullable =False)
    least_posts = Column(String, nullable=False)
    # average_friends = Column(Integer, nullable=False)
    last_updated = Column(String, nullable=False)

    def __init__(self, num_users, number_posts, average_posts, most_posts, least_posts, last_updated):
        self.num_users = num_users
        self.number_posts = number_posts
        self.most_posts = most_posts
        self.least_posts = least_posts
        self.average_posts = average_posts
        # self.average_friends = average_friends
        self.last_updated = last_updated
    
    def to_dict(self):
        dict = {}
        dict['num_users'] = self.num_users
        dict['number_posts'] = self.number_posts
        dict['most_posts'] = self.most_posts
        dict['least_posts'] = self.least_posts
        dict['average_posts'] = self.average_posts
        # dict['average_friends'] = self.average_friends
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")

        return dict