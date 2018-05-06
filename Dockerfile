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

COPY requirements/base.txt /opt/pip/requirements/base.txt
RUN pip install -r /opt/pip/requirements/base.txt


ADD . /opt/app
WORKDIR /opt/app

EXPOSE 8000

ENTRYPOINT ["/opt/app/docker-entrypoint.sh"]
CMD ["api", "migrate-first"]

