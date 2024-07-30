FROM python:3.12.3-slim as builder
WORKDIR /app
ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt install -y --no-install-recommends gcc

COPY requirements/prod .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r prod

#final stage
FROM python:3.12.3-slim
WORKDIR /app
ENV PYTHONPATH=/externals:
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*