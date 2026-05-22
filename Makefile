.PHONY: install run migrations migrate superuser shell collectstatic fixtures \
        up down build logs restart \
        dmigrations dmigrate dsuperuser dshell dcollectstatic dfixtures \
        fresh dfresh

DC = docker compose
WEB = $(DC) exec web

# ─── Lokaal (zonder Docker) ──────────────────────────────────────────────────

install:
	pip install -r requirements/dev.txt

run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

collectstatic:
	python manage.py collectstatic --no-input

## Demo-pagina's en blokken-testinhoud aanmaken
fixtures:
	python manage.py build_fixtures

## Demo-inhoud aanmaken en bestaande inhoud eerst verwijderen
fixtures-leeg:
	python manage.py build_fixtures --leeg

## Alles in één keer: installeer, migreer en start lokaal
fresh:
	$(MAKE) install
	$(MAKE) migrate
	$(MAKE) run

# ─── Docker ──────────────────────────────────────────────────────────────────

## Containers bouwen en starten (met logs)
up:
	$(DC) up

## Containers starten op de achtergrond
upd:
	$(DC) up -d

## Containers stoppen
down:
	$(DC) down

## Containers stoppen en volumes verwijderen (wist de database!)
down-v:
	$(DC) down -v

## Image(s) herbouwen
build:
	$(DC) build

## Logs volgen van de web container
logs:
	$(DC) logs -f web

## Web container herstarten
restart:
	$(DC) restart web

## Django shell in de container
dshell:
	$(WEB) python manage.py shell

## Migraties aanmaken in de container
dmigrations:
	$(WEB) python manage.py makemigrations

## Migraties uitvoeren in de container
dmigrate:
	$(WEB) python manage.py migrate

## Supergebruiker aanmaken in de container
dsuperuser:
	$(WEB) python manage.py createsuperuser

## Statische bestanden verzamelen in de container
dcollectstatic:
	$(WEB) python manage.py collectstatic --no-input

## Demo-pagina's aanmaken in de container
dfixtures:
	$(WEB) python manage.py build_fixtures

## Demo-inhoud aanmaken en bestaande inhoud eerst verwijderen (container)
dfixtures-leeg:
	$(WEB) python manage.py build_fixtures --leeg

## Alles in één keer: build, start op achtergrond, migreer
dfresh:
	$(MAKE) build
	$(MAKE) upd
	$(MAKE) dmigrate
