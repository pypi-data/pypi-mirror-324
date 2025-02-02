from pyspark.sql import SparkSession, DataFrame


def sample(spark: SparkSession) -> DataFrame:
    from pyspark.sql.functions import current_timestamp
    return (
        spark.readStream.format('rate')
        .option("rowsPerSecond", 1)
        .load()
        .withColumn("timestamp", current_timestamp())
    )

def show(df: DataFrame):
    from pyspark.sql.streaming import StreamingQuery
    assert df.isStreaming
    df.printSchema()
    query: StreamingQuery = (
        df.writeStream
        .foreachBatch(lambda _df, batch_id: _df.show())
        .start()
    )
    return query