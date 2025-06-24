import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import json
from google.cloud import language_v1
from datetime import datetime

class AnalyzeSentiment(beam.DoFn):
    def setup(self):
        self.client = language_v1.LanguageServiceClient()

    def process(self, element):
        data = json.loads(element.decode('utf-8'))
        resp = self.client.analyze_sentiment(document={"content": data["message"], "type_": language_v1.Document.Type.PLAIN_TEXT})
        data.update({
            "score": resp.document_sentiment.score,
            "magnitude": resp.document_sentiment.magnitude,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Fixed timestamp format
        })
        yield data

def run():
    options = PipelineOptions([
        "--runner=DataflowRunner",
        "--project=real-time-sentiment-analytics",
        "--region=us-central1",
        "--staging_location=gs://real-time-sentiment-analytics-pipeline/staging",
        "--temp_location=gs://real-time-sentiment-analytics-pipeline/temp",
        "--streaming"
    ])
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        (p
         | "ReadPubSub" >> beam.io.ReadFromPubSub(topic="projects/real-time-sentiment-analytics/topics/chat-topic")
         | "AnalyzeSentiment" >> beam.ParDo(AnalyzeSentiment())
         | "WriteBQ" >> beam.io.WriteToBigQuery(
               "real-time-sentiment-analytics:sentiment_results.raw",
               schema="user:STRING, message:STRING, orderId:STRING, score:FLOAT, magnitude:FLOAT, timestamp:TIMESTAMP",
               write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

if __name__ == "__main__":
    run()
