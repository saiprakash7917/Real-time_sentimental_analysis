from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when, current_timestamp, window, date_format

if __name__ == "__main__":
    spark = SparkSession.builder.appName("SentimentTrends").getOrCreate()
    
    # Read data from BigQuery
    df = spark.read.format("bigquery").option("table", "real-time-sentiment-analytics.sentiment_results.raw").load()
    
    print("=== DEBUG: Original data ===")
    print(f"Total records: {df.count()}")
    df.show(5)
    
    # Fix NULL timestamps by using current timestamp
    df_with_timestamp = df.withColumn(
        "fixed_timestamp", 
        when(col("timestamp").isNull(), current_timestamp()).otherwise(col("timestamp"))
    )
    
    print("=== DEBUG: Data with fixed timestamps ===")
    df_with_timestamp.select("user", "message", "score", "fixed_timestamp").show(5)
    
    # Now create hourly trends using the fixed timestamp
    trends = df_with_timestamp.groupBy(
        window(col("fixed_timestamp"), "1 hour")
    ).agg(
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
    
    print("=== DEBUG: Final results ===")
    trends_flattened.show()
    
    # Write to CSV
    trends_flattened.write.mode("overwrite").csv("gs://real-time-sentiment-analytics-pipeline/trends/", header=True)
    
    print("Sentiment trends analysis completed successfully!")