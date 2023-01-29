from mousetrap.job_queue import open_channel

QUEUE = "start_fetch"


def start_fetch_job():
    """Starts the first worker."""

    # Get a new channel from the base
    channel = open_channel()

    # Send an empty message to the queue
    channel.basic_publish(exchange="", routing_key=QUEUE, body="")

    print("New fetch job requested")

    # Close cleanly
    channel.close()
