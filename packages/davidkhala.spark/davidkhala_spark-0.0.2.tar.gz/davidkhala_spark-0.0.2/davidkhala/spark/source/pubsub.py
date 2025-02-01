from pyspark.sql import SparkSession, DataFrame

from davidkhala.spark.gcp import AuthOptions


class PubSub:
    auth: AuthOptions
    spark: SparkSession

    def start(self, topic_id, subscription_id) -> DataFrame:
        # Set up the streaming DataFrame to listen to the Pub/Sub topic
        pubsub_df = (self.spark.readStream
                     .option("subscriptionId", subscription_id)
                     .option("topicId", topic_id)
                     .options(**self.auth)
                     .load(format="pubsub"))
        assert pubsub_df.isStreaming == True
        return pubsub_df
