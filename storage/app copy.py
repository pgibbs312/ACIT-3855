import connexion
from connexion import NoContent
import mysql.connector
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from blog import Blog
from user import User
import logging
import logging.config
import yaml
import datetime
# from flask import request


logger = logging.getLogger('basicLogger')
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
with open("app_conf.yml", 'r') as f:
    parsed_conf = yaml.load(f, Loader=yaml.FullLoader)
    DB_ENGINE = create_engine(f'mysql+pymysql://{parsed_conf["datastore"]["user"]}:{parsed_conf["datastore"]["password"]}@{parsed_conf["datastore"]["hostname"]}:{parsed_conf["datastore"]["port"]}/{parsed_conf["datastore"]["db"]}')
    Base.metadata.bind = DB_ENGINE
    DB_SESSION = sessionmaker(bind=DB_ENGINE)


def addBlog(body):
    """ Receives a score """
    logger.info(f'Stored event addBlog request received with a trace id of {body["trans_id"]}')
    session = DB_SESSION()
    logger.info(f'Connecting to DB. Hostname: {parsed_conf["datastore"]["hostname"]}, Port: {parsed_conf["datastore"]["port"]}')
    print(f'date is: {body["date"]}')
    blog = Blog(
        body["trans_id"],
        body['blog_id'],
        body['title'],
        body['snippet'],
        body["blogBody"],
        body['userName'],
        body['postNumbers'],
        body['date']
    )
    session.add(blog)
    session.commit()
    session.close()
    logger.debug(f'Stored Event: addBlog id {body["trans_id"]} with a status code 201')
    return NoContent, 201                        

def addUser(body):
    """ Receives a user """
    logger.info(f'Stored event: addUser request received with a trace id: {body["trans_id"]}')
    session = DB_SESSION()
    user = User(
        body["trans_id"],
        body['user_id'],
        body['age'],
        body['email'],
        body['friends'],
        body['name'],
        body['password'],
        body['phoneNumber'],
        body['timeStamp']
    )
    session.add(user)
    session.commit()
    session.close()
    logger.debug(f'Stored event: addUser with trace id: {body["trans_id"]}')
    return NoContent, 201

def get_blogs(timestamp):
    """ Gets new website blogs added after the timestamp """
    session = DB_SESSION()
    #timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    #timestamp_datetime = datetime.datetime.strptime(timestamp, "%yyy-%MM-%ddT%HH:%mm:%ss.SSSZ")
    print(f'timestamp: {timestamp}')
    blog_data = session.query(Blog).filter(Blog.date >= timestamp)
    result_list = []

    for i in blog_data:
        result_list.append(i.to_dict())

    session.close()
    logger.info("Query for website blogs added after %s returns %d results" %(timestamp, len(result_list)))
    print(f'Blog response: {result_list}')
    return result_list, 200

def get_users(timestamp):
    """ Gets new website users added after the timestamp """
    print(timestamp)
    session = DB_SESSION()
    # timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    #timestamp_datetime = datetime.datetime.strptime(timestamp, "%yyy-%MM-%ddT%HH:%mm:%ss.SSSZ")
    user_data = session.query(User).filter(User.timeStamp >= timestamp)
    result_list = []

    for i in user_data:
        result_list.append(i.to_dict())
    session.close()
    print(f'user response: {result_list}')
    logger.info("Query for website users added after %s returns %d results" %(timestamp, len(result_list)))

    return result_list, 200
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("gibbons.peter312-Web-API-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8090)