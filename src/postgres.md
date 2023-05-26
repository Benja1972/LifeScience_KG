## On Linux

Update and install PostgreSQL 10.4

``
sudo apt-get update
sudo apt-get install postgresql-10.4
``
By default, the postgres user has no password and can hence only connect if ran by the postgres system user. The following command will assign it:

	sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
	sudo -u postgres psql -c "CREATE DATABASE testdb;"
Start the PostgreSQL server
	sudo service postgresql start
Stop the PostgreSQL server:
	sudo service postgresql stop


https://www.postgresqltutorial.com/install-postgresql-linux/


# to get acess to dump 
(base) seg@seg-pc:~/==RYBALKO==/ALPHA10X/RD_Projects/Projects/KG_KnowledgeGraphs/DrugCentral$ chmod a+x data/
(base) seg@seg-pc:~/==RYBALKO==/ALPHA10X/RD_Projects/Projects/KG_KnowledgeGraphs/DrugCentral$ chmod a+r data/drugcentral.dump.010_05_2021.sql
(base) seg@seg-pc:~/==RYBALKO==/ALPHA10X/RD_Projects/Projects/KG_KnowledgeGraphs/DrugCentral$ chmod a+rx ../

# mangaro
https://medium.com/@Iraj/installing-and-running-postgresql-on-manjaro-os-10210cdefbd6

# create database
$ su postgres
$ psql
postgres=# create database clinicaltrials;

# restore dump to database 
[sergei-alpha10x data]# pg_restore -U postgres --dbname=clinicaltrials --verbose /home/sergei/ALPHA10X/RD_Projects/KG_KnowledgeGraphs/LSKG_NEO4J/data/ClinicalTrials/CDEK_project/cdek-public-2019-01-24.dump
 
# To change a password !!! PASWORGD changed
ALTER USER postgres PASSWORD 'postgres';



# To run pgAdmin [pgAdmin](https://www.pgadmin.org/download/pgadmin-4-python/)

$ source pgadmin4/bin/activate
(pgadmin4) $ pip install pgadmin4
...
(pgadmin4) $ pgadmin4

http://127.0.0.1:5050/browser/#
