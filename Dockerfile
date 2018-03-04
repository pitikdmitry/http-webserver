
FROM ubuntu

MAINTAINER Pitik Dmitry

RUN apt-get update

RUN apt-get install -y python3.5 python3-pip

ADD ./ /my_application
ADD ./http-test-suite /var/www/html/

# Get pip to download and install requirements:
RUN python3.5 -m pip install -r /my_application/requirements.txt

EXPOSE 80

WORKDIR /my_application

#CMD python main.py
CMD [ "python3.5", "./main.py" ]
