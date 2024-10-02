FROM python:3.10-slim
LABEL maintainer="Ruslan Akhmarov"

ENV PYTHONUNBUFFERED="true"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-c", "python:vkcc_auto.config.gunicorn", "vkcc_auto:create_app()"]