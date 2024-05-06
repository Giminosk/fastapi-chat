D = docker
DC = docker compose
EXEC = docker exec -it
ENV = --env-file .env
APP_YAML = docker_compose/app.yaml

.PHONY: app-up
app-up:
	${DC} -f ${APP_YAML} ${ENV} up --build -d 

.PHONY: app-down
app-down:
	${DC} -f ${APP_YAML} down