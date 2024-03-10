FROM python:3.10.13

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /Backend
COPY . .

EXPOSE 5000

ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "--app=Backend/manage", "run"]