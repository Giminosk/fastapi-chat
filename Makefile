D = docker
DC = docker compose
EXEC = docker exec -it
ENV = --env-file .env
APP_YAML = docker_compose/app.yaml
DB_YAML = docker_compose/db.yaml
ALL_YAML = docker_compose/all.yaml
BROKER_YAML = docker_compose/kafka.yaml

.PHONY: app-up
app-up:
	${DC} -f ${APP_YAML} ${ENV} up --build

.PHONY: app-down
app-down:
	${DC} -f ${APP_YAML} down

.PHONY: db-up
db-up:
	${DC} -f ${DB_YAML} ${ENV} up

.PHONY: db-down
db-down:
	${DC} -f ${DB_YAML} down

.PHONY: broker-up
broker-up:
	${DC} -f ${BROKER_YAML} ${ENV} up

.PHONY: broker-down
broker-down:
	${DC} -f ${BROKER_YAML} down


.PHONY: all-up
all-up:
	${DC} -f ${ALL_YAML} ${ENV} up --build

.PHONY: all-down
all-down:
	${DC} -f ${ALL_YAML} down
