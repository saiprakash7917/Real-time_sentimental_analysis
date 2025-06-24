import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import logging

try:
    from google.cloud import language_v1
except ImportError as e:
    logging.error("Failed to import google.cloud.language_v1. Install with: pip install google-cloud-language")
    raise e

class AnalyzeSentiment(beam.DoFn):
    def setup(self):
        self.client = language_v1.LanguageServiceClient()

    def process(self, element):
        try:
            if isinstance(element, str):
                data = json.loads(element)
            else:
                data = element
                
            document = language_v1.Document(
                content=data["message"], 
                type_=language_v1.Document.Type.PLAIN_TEXT
            )
            resp = self.client.analyze_sentiment(
                request={"document": document}
            )
            data.update({
                "score": resp.document_sentiment.score,
                "magnitude": resp.document_sentiment.magnitude
            })
            print(f"Processed: {data}")
            yield data
        except Exception as e:
            logging.error(f"Error processing element: {e}")
            yield element

def run():
    # Test data (same as your publisher)
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
         | "AnalyzeSentiment" >> beam.ParDo(AnalyzeSentiment())
         | "PrintResults" >> beam.Map(print))

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
