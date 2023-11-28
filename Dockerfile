FROM python:3.10-slim-bullseye AS builder

WORKDIR app
COPY . .

RUN apt-get update && apt-get upgrade -y
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

FROM python:3.10-slim-bullseye AS deployer

WORKDIR app
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
