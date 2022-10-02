black:
	black . --line-length 120

prod_up:
	docker compose -f docker-compose-databases.yml -f docker-compose-analytics.yml -f docker-compose-prod.yml up -d --build

prod_down:
	docker compose -f docker-compose-databases.yml -f docker-compose-analytics.yml -f docker-compose-prod.yml down

dev_up:
	docker compose -f docker-compose-databases.yml -f docker-compose-dev.yml up -d

dev_down:
	docker compose -f docker-compose-databases.yml -f docker-compose-dev.yml down

tests_up:
	docker compose -f tests/functional/docker-compose.yml up

tests_down:
	docker compose -f tests/functional/docker-compose.yml down

analyticts_up:
	docker compose -f docker-compose-analytics.yml up -d

analyticts_down:
	docker compose -f docker-compose-analytics.yml down


auth_debug:
	flask --app auth/src/Auth.app --debug run