PROJECT_NAME = "Auth Service"

# Цвета
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m

.PHONY: help run

# Справка по командам
help:
	@echo "$(YELLOW)Команды для $(PROJECT_NAME):$(NC)"
	@echo " $(GREEN)make run$(NC)              - Запуск проекта"

# Запуск проекта
run:
	@echo "$(GREEN) Запуск проекта...$(NC)"
	uvicorn src.main:app --reload
