FROM postgres

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD 111
ENV POSTGRES_DB bobdb

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
