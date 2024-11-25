FROM python:3.12

WORKDIR /view_app

COPY . /view_app

RUN pip3 install flask==3.0.3
RUN pip3 install pymongo
RUN pip3 install redis
RUN python3 service.py

CMD ["python3", "app.py"]

#EXPOSE 5000
