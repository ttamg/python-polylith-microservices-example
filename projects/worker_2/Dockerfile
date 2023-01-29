FROM python:3.11-slim

ARG wheel=worker_2-0.1.0-py3-none-any.whl

WORKDIR /code
COPY ./dist/$wheel /code/$wheel

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir /code/$wheel

CMD ["python", "-m", "mousetrap.run_processing_worker.start"]

