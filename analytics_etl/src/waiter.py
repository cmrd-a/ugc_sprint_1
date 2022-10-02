import time

from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError

from logger import get_logger
from settings import setting

logger = get_logger(__name__)


def wait_and_init():
    ch_client = Client(host=setting.ch_server, user=setting.ch_user, password=setting.ch_password)
    while True:
        try:
            kc = KafkaConsumer(
                "views",
                bootstrap_servers=[setting.kafka_server],
                group_id="analytics-etl",
            )
            ch_client.execute("CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster")
            ch_client.execute(
                "CREATE TABLE IF NOT EXISTS movies.views ON CLUSTER company_cluster (id UUID, "
                "user_id Int64, film_id UUID, film_position_ms Int64, event_dt datetime64 ) "
                "Engine=MergeTree() ORDER BY event_dt"
            )
            ch_client.disconnect()
            kc.close()
            break
        except (Error, KafkaError) as e:
            logger.error(f"{e}\n retry in 2 seconds")
            time.sleep(2)


if __name__ == "__main__":
    wait_and_init()
