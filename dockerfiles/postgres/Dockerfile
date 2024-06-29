FROM postgres:16-alpine
LABEL authors="Oleh Dziuba"


COPY ./init.sql /docker-entrypoint-initdb.d/create_tables.sql
COPY ./uuid_v7/extension/* /usr/local/share/postgresql/extension/
COPY ./uuid_v7/lib/pg_uuidv7.so /usr/local/lib/postgresql/pg_uuidv7.so

