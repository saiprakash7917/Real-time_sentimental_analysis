from google.cloud import pubsub_v1
import json
import time

publisher = pubsub_v1.PublisherClient()
topic = publisher.topic_path("real-time-sentiment-analytics", "chat-topic")

messages = [
    {"user": "A", "message": "I love this product!", "orderId": "1001"},
    {"user": "B", "message": "This is terrible.", "orderId": "1002"},
    {"user": "C", "message": "Amazing quality and fast delivery!", "orderId": "1003"},
    {"user": "D", "message": "Not worth the money.", "orderId": "1004"},
    {"user": "E", "message": "Excellent customer service!", "orderId": "1005"},
    {"user": "F", "message": "Product arrived damaged.", "orderId": "1006"},
    {"user": "G", "message": "Highly recommend this!", "orderId": "1007"},
    {"user": "H", "message": "Very disappointed with the purchase.", "orderId": "1008"}
]

for msg in messages:
    publisher.publish(topic, json.dumps(msg).encode("utf-8"))
    time.sleep(1)
    
print("Published test messages.")
