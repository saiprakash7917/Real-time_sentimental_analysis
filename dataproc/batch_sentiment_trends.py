from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window, date_format, count

if __name__ == "__main__":
    spark = SparkSession.builder.appName("SentimentTrends").getOrCreate()
    
    # Read data from BigQuery
    df = spark.read.format("bigquery").option("table", "real-time-sentiment-analytics.sentiment_results.raw").load()
    
    # Create hourly trends with flattened window columns
    trends = df.groupBy(window(col("timestamp"), "1 hour")).agg(
        avg("score").alias("avg_score"),
        avg("magnitude").alias("avg_magnitude"),
        count("*").alias("message_count")
    )
    
    # Flatten the window struct for CSV compatibility
    trends_flattened = trends.select(
        date_format(col("window.start"), "yyyy-MM-dd HH:mm:ss").alias("window_start"),
        date_format(col("window.end"), "yyyy-MM-dd HH:mm:ss").alias("window_end"),
        col("avg_score"),
        col("avg_magnitude"),
        col("message_count")
    )
    
    # Write to CSV
    trends_flattened.write.mode("overwrite").csv("gs://real-time-sentiment-analytics-pipeline/trends/", header=True)
    
    print("Sentiment trends analysis completed successfully!")
