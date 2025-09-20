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
	@echo " $(GREEN)make format$(NC)           - Форматирование кода Black + сортировка импортов (Ruff)"
	@echo " $(GREEN)make lint$(NC)             - Линтинг кода (Ruff, PEP8)"

# Запуск проекта
run:
	@echo "$(GREEN) Запуск проекта...$(NC)"
	uvicorn src.main:app --reload

# Форматирование кода
format:
	@echo "$(GREEN) Форматирование Black...$(NC)"
	poetry run black .
	@echo "$(GREEN) Сортировка импортов (Ruff isort)...$(NC)"
	poetry run ruff check --select I --fix .

# Линтинг кода (PEP8 + базовые проверки)
lint:
	@echo "$(GREEN) Линтинг Ruff...$(NC)"
	poetry run ruff check .
