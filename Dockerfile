FROM python:slim

MAINTAINER Pitik Dmitry

#RUN apt-get update
#RUN apt-get install python3-setuptools
#RUN easy_install3 pip

ADD ./ /my_application
ADD ./http-test /var/www/html/http-test

# Get pip to download and install requirements:
#RUN python3 -m pip install -r /my_application/requirements.txt
RUN pip install -r /my_application/requirements.txt

EXPOSE 80

WORKDIR /my_application

#CMD python main.py
CMD [ "python3", "./main.py" ]
