import fastapi
from mousetrap.mongo_connection import open_db
from mousetrap.start_fetch_worker import start_fetch_job

app = fastapi.FastAPI()


@app.get("/")
def get_latest_data_record() -> dict:
    """Gets the latest processed data record."""

    db = open_db()

    record = db.results.find_one(sort=[("_id", -1)])

    if record:
        # Drop the Mongo ID field
        if "_id" in record:
            del record["_id"]
        return record

    else:
        # Empty database
        return {}


@app.post("/refresh")
def refresh_data() -> dict:
    """Starts a background data refresh job."""

    start_fetch_job()

    return {"status": "ok"}
