from urllib import response
import uuid
import connexion
import yaml
import logging
import logging.config
from connexion import NoContent
import datetime
import json
import requests
from flask import request
from pykafka import KafkaClient, Producer

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

def addBlog(body):
    id = str(uuid.uuid4())
    body['trans_id'] = id
    payload = body
    headers = {'Content-Type': 'application/json'}
    logger.info(f'Stored event addBlog request with a trace id of {id}')
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}: {app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "addBlog",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": payload
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    return 201

def addUser(body):

    id = str(uuid.uuid4())
    body['trans_id'] = id
    logger.info(f'Stored event addUser request with a trace id of {id}')
    payload = body
    headers = {'Content-Type': 'application/json'}
    client = KafkaClient(hosts=f'{app_config["events"]["hostname"]}: {app_config["events"]["port"]}')
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "addUser",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": payload
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    return 201
    


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("gibbons.peter312-Web-API-1.0.0-resolved.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8080)
