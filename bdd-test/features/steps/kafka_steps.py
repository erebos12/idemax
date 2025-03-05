from kafka import KafkaProducer
import json
from hamcrest import *


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


@when('kafka - sending json to broker "{broker:String}" and topic "{topic:String}"')
def sending_json_to_kafka(context, broker, topic):
    assert_that(context.json, is_not(None))
    producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=json_serializer
    )
    producer.send(topic, context.json)
    producer.flush()
    producer.close()
