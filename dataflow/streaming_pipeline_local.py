import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
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
            data = json.loads(element.decode('utf-8'))
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
            yield data

def run():
    # Enable streaming mode for DirectRunner
    options = PipelineOptions([
        "--runner=DirectRunner",
        "--project=real-time-sentiment-analytics",
        "--streaming"
    ])
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        (p
         | "ReadPubSub" >> beam.io.ReadFromPubSub(topic="projects/real-time-sentiment-analytics/topics/chat-topic")
         | "AnalyzeSentiment" >> beam.ParDo(AnalyzeSentiment())
         | "PrintResults" >> beam.Map(print))

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
