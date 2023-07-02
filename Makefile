.PHONY: up-local
up-local:
	@touch ./.docker.env
	@docker-compose -f docker-compose.override.yml -f dev.docker-compose.yml up

.PHONY: build-local
build-local:
	@touch ./.docker.env
	@docker-compose -f docker-compose.override.yml -f dev.docker-compose.yml build --force-rm

.PHONY: down-local
down-local:
	@docker-compose -f docker-compose.override.yml -f dev.docker-compose.yml down

.PHONY: uninstall-local
uninstall-local:
	@docker-compose -f docker-compose.override.yml -f dev.docker-compose.yml down --remove-orphans --volumes
