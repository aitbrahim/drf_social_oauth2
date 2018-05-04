FROM obytes/python:2.7

RUN apk add --update curl \
                     git \
                     jpeg-dev \
		             zlib-dev \
		             libffi-dev \
		             openssl-dev \
                     mariadb-dev \
                     mariadb-client \
                     mariadb-libs

RUN apk add gdal --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted

COPY requirements/common.txt /opt/pip/requirements/common.txt
RUN pip install -r /opt/pip/requirements/common.txt

COPY requirements/development.txt /opt/pip/requirements/development.txt
RUN pip install -r /opt/pip/requirements/development.txt

COPY requirements/test.txt /opt/pip/requirements/test.txt
RUN pip install -r /opt/pip/requirements/test.txt


ADD . /opt/app
WORKDIR /opt/app

EXPOSE 8000

ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]
CMD ["api"]

