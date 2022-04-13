FROM postgres:latest

ENV POSTGRES_PASSWORD=mc_data_123
ENV POSTGRES_USER=mcdata
ENV POSTGRES_DB=database
COPY create_table.sql /docker-entrypoint-initdb.d/create_fixtures.sql