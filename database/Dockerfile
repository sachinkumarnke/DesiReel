FROM postgres:15-alpine

# Create a directory for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Add any initialization scripts if needed
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432