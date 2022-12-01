from email import header
from time import strftime
from unittest import result
import connexion
from connexion import NoContent
from flask import session
from pymysql import NULL

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import logging.config
import datetime
import requests
import uuid
import sqlite3
from stats import Stats

logger = logging.getLogger('basicLogger')
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open("app_conf.yml", 'r') as f:
    app_config = yaml.safe_load(f.read())

DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def populate_stats():
    logger.info('Start Periodic Processing')
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    time = str(time)
    id = str(uuid.uuid4())

    query = get_time()
    # if len(query) == 0:
    #     last_update = query[-1]
    # else:
    #     last_update = datetime.datetime.now()
    #     print('true')

    # Get score and user data
    last_updated = query
    print(f'time: {last_updated}')
    blog_request = requests.get(f'http://localhost:8090/website/blog?timestamp={last_updated}')
    #user_data = requests.get(f'http://localhost:8090/website/user?timestamp={last_updated}')
    blog_data = blog_request.json()
    #user_data = user_data.json()
    session = DB_SESSION()
    num_users = 0
    number_posts = 0

    most_posts = 0
    least_posts = 0

    total_friends = 0
    count = 0

    # Forloop for Blog data
    if len(blog_data) != 0:
        for i in blog_data:
            if most_posts > i["postNumbers"]:
                most_posts = i["postNumbers"]
            if least_posts < i["postNumbers"]:
                least_posts = i["postNumbers"]
            count += 1
            number_posts += 1
            num_users += 1
    # for i in user_data:
    #     print(f'i is: {i}')
    #     logger.info(f'processing event with trans_id: {i["trans_id"]}')
    #     if most_posts < i["postNumbers"]:
    #         most_posts = i["postNumbers"]
    #     if least_posts > i["postNumbers"]:
    #         least_posts = i["postNumbers"]
    #     count += 1
    # for i in user_data["postNumbers"]:
    #     number_posts += 1
    # for i in user_data["friends"]:   #fixme
    #     total_friends += 1
    
    # calculating averages
    average_posts = num_users/number_posts
    #average_friends = num_users/total_friends
    

    if blog_request.status_code != 200:
        logger.error(f'bad request with status code: {blog_request.status_code}')
    else:
        logger.info(f'received {num_users} of requests with status code: {blog_request.status_code}')
    # if user_data.status_code != 200:
    #     logger.error(f'bad request with status code: {user_data.status_code}')
    # else:
    #     logger.info(f'received {num_users} of requests with status code: {user_data.status_code}')
    
    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    last_updated = str(last_updated)    # could be last_update = str(last_update)
    stats = Stats(
        num_users,
        number_posts,
        most_posts,
        least_posts,
        average_posts,
        last_updated
    )
    session.add(stats)
    session.commit()
    session.close()

    # Log debug message with updated stat values 
    logger.debug(f'Stored event: populate stats with trace id: {id} with status code 201')
    

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_stats,
        'interval',
        seconds=app_config['scheduler']['period_sec']
    )
    sched.start()


def get_stats():
    """ Returns a list of values """
    session = DB_SESSION()
    stats = session.query(Stats)
    result_list = []

    for i in stats:
        result_list.append(i.to_dict())

    session.close()

    return result_list, 200
    
def get_time():

    con = sqlite3.connect('stats.sqlite')
    cur = con.cursor()

    if cur.execute('select * from stats').fetchall() == []:
        last_row = datetime.datetime.now()
        print('true')
        return
    else:
        print('else is true')
        last_row = cur.execute('select * from stats').fetchall()[-1]
    #print(f'last updated @ {last_row}')
    row = []
    for i in last_row:
        row.append(i)
    time = row[-1]
    return time
app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("gibbons.peter312-stats-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)