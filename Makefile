BASE_DOCKER_COMPOSE = -f docker/docker-compose.yml
ENV_FILE =  ./.docker.env
LOCAL_ENV_FILE =  ./.env

.PHONY: create_env
create_env: ## Just touching env files
	touch $(ENV_FILE)
	touch $(LOCAL_ENV_FILE)

.PHONY: up
up: create_env ## up local services
	@docker compose --env-file $(ENV_FILE) $(BASE_DOCKER_COMPOSE) up $(service) -d

.PHONY: down
down: ## down local services
	@docker compose --env-file $(ENV_FILE) $(BASE_DOCKER_COMPOSE) down

.PHONY: logs
logs: ## logs local services
	@docker compose --env-file $(ENV_FILE) $(BASE_DOCKER_COMPOSE) logs $(service) -f

.PHONY: restart
restart: down up ## logs local services

.PHONY: build
build: create_env ## build local services
	@docker compose --env-file $(ENV_FILE) $(BASE_DOCKER_COMPOSE) build $(service)

.PHONY: uninstall
uninstall: create_env ## uninstall all services
	@docker compose --env-file $(ENV_FILE) $(BASE_DOCKER_COMPOSE) down --remove-orphans --volumes
