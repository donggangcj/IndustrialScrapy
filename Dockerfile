FROM python:3.6
ENV PATH /usr/local/bin:$PATH \
    MONGODB_URI='mongodb://localhost:27017' MONGODB_DATABASE='industry'
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ['python3','manager.py']

