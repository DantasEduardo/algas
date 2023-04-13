FROM mysql:8
ADD algas.sql /docker-entrypoint-initdb.d

# docker run --name bd -p 3306:3306 -e MYSQL_ROOT_PASSWORD=urubu100 -d mysql
