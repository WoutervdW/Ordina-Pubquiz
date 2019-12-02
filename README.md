# Ordina-Pubquiz

1. Read hand-written pub quiz answers
2. Mark answers. 
3. Show team scores online.

#docker installation
https://www.docker.com/products/docker-desktop

#run
docker-compose build
docker-compose up

#storing data
# Backup
docker exec -t <container_name> pg_dumpall -c -U postgres > backup.sql
# Restore
type backup.sql < docker exec -i <container_name> /var/lib/postgresql -u postgres --password=password ordina-pubquiz
