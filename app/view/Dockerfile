FROM python:3.12

WORKDIR /view_app

COPY . /view_app

RUN pip3 install flask==3.0.3
RUN pip3 install pymongo==4.10.1
RUN pip3 install redis==5.1.1
RUN python3 service.py

CMD ["python3", "app.py"]

#EXPOSE 5000
