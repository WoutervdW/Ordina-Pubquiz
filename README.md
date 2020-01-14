# Ordina-Pubquiz

1. Read hand-written pub quiz answers
2. Mark answers. 
3. Show team scores online.

# Docker installation
https://www.docker.com/products/docker-desktop

# Running
* docker-compose build
* docker-compose up

# Storing data

## Backup
docker exec -t <container_name> pg_dumpall -c -U postgres > backup.sql


## Restore
docker exec -i <postgres_container_name> psql -U postgres -d ordina-pubquiz < backup.sql

## Git for large files
https://git-lfs.github.com/
