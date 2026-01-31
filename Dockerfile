FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the package from this repository (at the tagged commit)
COPY pyproject.toml setup.py README.md /app/
COPY crossplane /app/crossplane

RUN python -m pip install --no-cache-dir --upgrade pip \
  && python -m pip install --no-cache-dir .

ENTRYPOINT ["crossplane"]


