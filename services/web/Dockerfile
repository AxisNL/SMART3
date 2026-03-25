#
FROM library/python:3.13-slim
RUN apt update

ENV DEBUG=TRUE
ENV PYTHONPATH=/app/

#COPY app/tel-dc-01.cer /usr/local/share/ca-certificates/tel-dc-01.crt
#RUN chmod 644 /usr/local/share/ca-certificates/tel-dc-01.crt && update-ca-certificates

# install nginx
RUN apt-get install nginx vim curl -y --no-install-recommends
# RUN apt-get install build-essential python3-dev libldap2-dev ldap-utils libsasl2-dev -y

# create the folder and the root CA
RUN mkdir -p /app
COPY start-server.sh /app/start-server.sh
RUN chmod +x /app/start-server.sh

COPY requirements.txt /app/requirements.txt
COPY nginx.default /app/

WORKDIR /app
RUN python3 -m venv venv
RUN /app/venv/bin/pip install wheel
RUN /app/venv/bin/pip install -r requirements.txt --retries 60 --timeout 100

# copy app
COPY app/app /app/app
#COPY app/ui /app/ui
#COPY app/static /app/static
COPY app/manage.py /app/manage.py

RUN mkdir /app/db

WORKDIR /app/

COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://127.0.0.1:8000/accounts/login/?next=/ -H 'User-Agent: healthcheck' || exit 1

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/app/start-server.sh"]
