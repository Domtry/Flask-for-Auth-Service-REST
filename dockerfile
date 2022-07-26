FROM python:3.9
RUN mkdir /usr/src/app/
COPY nginx.conf /etc/nginx/conf.d
COPY . /usr/src/app/
WORKDIR /usr/src/app/
RUN pip install -r requirements.txt
EXPOSE 5000
RUN cd /usr/src/app/