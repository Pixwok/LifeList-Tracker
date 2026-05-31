# LifeList Tracker
LifeList Tracker est une application web pour suivre ses objectifs et les actions à effectuer pour les atteindres.

## Envireonnement de dev
Créer un fichier .env pour initialiser votre base de données.
```
POSTGRES_PASSWORD: my_password
POSTGRES_USER: db_user
POSTGRES_DB: lifelist 
POSTGRES_TZ: Europe/Paris
POSTGRES_PGTZ: Europe/Paris
```

Création des conteneurs + build
```
docker compose -f docker-compose-dev.yml
```