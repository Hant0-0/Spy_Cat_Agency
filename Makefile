docker-compose-dev:
	docker-compose -f deployment/development/docker-compose-dev.yaml down
	docker-compose -f deployment/development/docker-compose-dev.yaml up --build -d