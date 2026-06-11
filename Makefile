.PHONY: install run migrations migrate superuser shell collectstatic runclub-home \
        up down build logs restart \
        dmigrations dmigrate dsuperuser dshell dcollectstatic drunclub-home \
        fresh dfresh

DC = docker compose
WEB = $(DC) exec web

PYTHON = .venv/bin/python
MANAGE = DJANGO_SETTINGS_MODULE=runclub.settings.dev $(PYTHON) manage.py

# ─── Lokaal (zonder Docker) ──────────────────────────────────────────────────

install:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements/dev.txt

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

collectstatic:
	$(MANAGE) collectstatic --no-input

## Bolt Run Club homepage (her)opbouwen
runclub-home:
	$(MANAGE) build_runclub_home

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

## Bolt Run Club homepage (her)opbouwen in de container
drunclub-home:
	$(WEB) python manage.py build_runclub_home

## Alles in één keer: build, start op achtergrond, migreer
dfresh:
	$(MAKE) build
	$(MAKE) upd
	$(MAKE) dmigrate
