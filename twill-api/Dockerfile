FROM python:3.9-slim-bullseye as base

RUN apt-get update && apt-get install -y pkgconf libhdf5-dev curl linux-libc-dev && apt-get clean
ENV POETRY_HOME=/etc/poetry
ENV PATH="/etc/poetry/bin:$PATH"
RUN curl -sSLfo poetry-install.py https://install.python-poetry.org \
    && python poetry-install.py --version 1.1.12

WORKDIR /app

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
