FROM python:3.12-bullseye
WORKDIR app/
COPY requirements req
RUN pip3 install -r req
COPY . .
EXPOSE 5000
CMD ["python3", "app.py"]










