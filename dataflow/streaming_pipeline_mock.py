import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import logging
import random

class MockAnalyzeSentiment(beam.DoFn):
    """Mock sentiment analysis for testing without API calls"""
    
    def process(self, element):
        try:
            if isinstance(element, str):
                data = json.loads(element)
            else:
                data = element
            
            # Mock sentiment analysis based on keywords
            message = data["message"].lower()
            if any(word in message for word in ["love", "amazing", "excellent", "recommend"]):
                score = random.uniform(0.5, 1.0)  # Positive
            elif any(word in message for word in ["terrible", "disappointed", "damaged", "not worth"]):
                score = random.uniform(-1.0, -0.5)  # Negative
            else:
                score = random.uniform(-0.2, 0.2)  # Neutral
            
            data.update({
                "score": score,
                "magnitude": abs(score) + random.uniform(0.1, 0.5)
            })
            print(f"Mock Processed: {data}")
            yield data
        except Exception as e:
            logging.error(f"Error processing element: {e}")
            yield element

def run():
    test_messages = [
        {"user": "A", "message": "I love this product!", "orderId": "1001"},
        {"user": "B", "message": "This is terrible.", "orderId": "1002"},
        {"user": "C", "message": "Amazing quality and fast delivery!", "orderId": "1003"},
        {"user": "D", "message": "Not worth the money.", "orderId": "1004"},
        {"user": "E", "message": "Excellent customer service!", "orderId": "1005"},
        {"user": "F", "message": "Product arrived damaged.", "orderId": "1006"},
        {"user": "G", "message": "Highly recommend this!", "orderId": "1007"},
        {"user": "H", "message": "Very disappointed with the purchase.", "orderId": "1008"}
    ]

    options = PipelineOptions([
        "--runner=DirectRunner",
        "--project=real-time-sentiment-analytics"
    ])

    with beam.Pipeline(options=options) as p:
        (p
         | "CreateTestData" >> beam.Create(test_messages)
         | "MockAnalyzeSentiment" >> beam.ParDo(MockAnalyzeSentiment())
         | "PrintResults" >> beam.Map(print))

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
