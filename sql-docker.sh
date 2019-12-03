# Backup
docker exec postgres /usr/bin/mysqldump -u postgres --password=password ordina-pubquiz > backup.sql

# Restore
cat backup.sql | docker exec -i postgres /var/lib/postgreql -U postgres --password=password ordina-pubquiz
