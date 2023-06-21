.PHONY: up-local
up-local:
	@docker-compose -f docker-compose.yaml up

.PHONY: down-local
down-local:
	@docker-compose -f docker-compose.yaml down

.PHONY: uninstall-local
uninstall-local:
	@docker-compose -f docker-compose.yaml down --remove-orphans --volumes
