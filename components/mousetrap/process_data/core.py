import time


def process_data(data: list):

    time.sleep(1)  # Simulate a long running process

    # Calculate the average lat and average long from the data
    lats = [float(x[0]) for x in data]
    average_lat = sum(lats) / len(lats)
    longs = [float(x[1]) for x in data]
    average_long = sum(longs) / len(longs)

    # The most northerly datapoint
    most_northerly_lat = max(lats)
    most_northerly_index = lats.index(most_northerly_lat)
    most_northerly = data[most_northerly_index]

    # Package up into processed data
    result = {"centroid": (average_lat, average_long), "most_northerly": most_northerly}

    return result
