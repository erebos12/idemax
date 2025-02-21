.PHONY: help start stop it

help: ## this help
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

start: ## rebuild and run idemax with Redis
		docker-compose up --build --remove-orphans

stop: ## stop and clean orphan containers
		docker-compose down --remove-orphans

it: stop ## docker compose - execute all BDD tests (including API tests)
	docker-compose -f docker-compose.yml -f docker-compose-only-tests.yml build || exit 1
	docker-compose -f docker-compose.yml -f docker-compose-only-tests.yml run bdd-test || exit 1
	docker-compose -f docker-compose.yml -f docker-compose-only-tests.yml down --remove-orphans
