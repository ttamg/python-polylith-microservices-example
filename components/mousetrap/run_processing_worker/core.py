import json

from mousetrap.job_queue import open_channel
from mousetrap.mongo_connection import open_db
from mousetrap.process_data import process_data

LISTEN_QUEUE = "data_processing"

# Open the database connection - needs some error handling normally.
db = open_db()


def callback(ch, method, properties, body):
    """
    Takes the data and calculates the geo centroid and the most
    northerly element.
    Returns these in a dictionary object.
    """
    print("Started data processing job.")

    # Do the data processing
    data = json.loads(body)
    result = process_data(data)

    # Push data to the database
    db.results.insert_one(result)

    # Acknowledge the incoming message to remove it from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Done. Finished processing data.")


def run_processing_worker():
    """Does the worker 2 processing of data."""

    # Get a new channel from the base
    channel = open_channel()

    # Register the callback
    channel.basic_consume(queue=LISTEN_QUEUE, on_message_callback=callback)

    # This is a blocking connection
    channel.start_consuming()
