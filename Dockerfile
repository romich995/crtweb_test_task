FROM python:3.8
WORKDIR /code

COPY requirements.txt .

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY src .

COPY logging.yaml .
