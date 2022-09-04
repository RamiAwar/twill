FROM python:3.10.6-slim-bullseye

RUN apt-get update && apt-get install -y pkgconf libhdf5-dev curl linux-libc-dev && apt-get clean

# TODO: Add trivy scan
# CVE-2022-2509
RUN apt-get install --upgrade -y libgnutls30
RUN apt-get install --upgrade -y libpq-dev

ENV POETRY_HOME=/etc/poetry
ENV PATH="/etc/poetry/bin:$PATH"
RUN curl -sSLfo poetry-install.py https://install.python-poetry.org \
    && python poetry-install.py --version 1.1.12

COPY twill-core /twill-core

WORKDIR /app
COPY twill-api/poetry.lock twill-api/pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY twill-api/app /app
WORKDIR /
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]