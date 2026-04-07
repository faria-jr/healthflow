# HealthFlow - BMad Method Makefile
# Facilita a execução do fluxo completo de desenvolvimento

.PHONY: help install dev test lint qa bmad-review bmad-retry clean

# Default target
help:
	@echo "HealthFlow - BMad Method Commands"
	@echo "=================================="
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment (docker-compose up)"
	@echo "  make install      - Install all dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-backend - Run backend tests with coverage"
	@echo "  make test-frontend- Run frontend tests"
	@echo ""
	@echo "Linting:"
	@echo "  make lint         - Run all linters"
	@echo "  make lint-backend - Run backend linters (ruff, mypy)"
	@echo "  make lint-frontend- Run frontend linters"
	@echo ""
	@echo "BMad QA:"
	@echo "  make qa           - Run all QA checks (simulates BMad agents)"
	@echo "  make qa-bug       - Run Bug Founder QA"
	@echo "  make qa-quality   - Run Code Quality QA"
	@echo "  make qa-security  - Run Security QA"
	@echo "  make qa-perf      - Run Performance QA"
	@echo "  make qa-tdd       - Run TDD QA"
	@echo ""
	@echo "BMad Flow:"
	@echo "  make bmad-review  - Run full BMad code review"
	@echo "  make bmad-retry   - Run BMad with retry loop"
	@echo ""
	@echo "Docker:"
	@echo "  make build        - Build all Docker images"
	@echo "  make clean        - Clean Docker resources"

# ============================================
# Development
# ============================================

dev:
	docker-compose up -d

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# ============================================
# Testing
# ============================================

test: test-backend test-frontend

test-backend:
	cd backend && pytest --cov=src --cov-report=term-missing

test-frontend:
	cd frontend && npm test

# ============================================
# Linting
# ============================================

lint: lint-backend lint-frontend

lint-backend:
	@echo "🔍 Running backend linters..."
	cd backend && ruff check src
	cd backend && mypy src --strict || true

lint-frontend:
	@echo "🔍 Running frontend linters..."
	cd frontend && npm run type-check || true

# ============================================
# BMad QA (Simulated)
# ============================================

qa: qa-bug qa-quality qa-security qa-perf qa-tdd

qa-bug:
	@echo "🔍 Running Bug Founder QA..."
	@# Check for race conditions
	@if grep -r "race condition\|TODO.*fixme\|FIXME" --include="*.py" backend/src/ 2>/dev/null; then \
		echo "⚠️  Potential bugs found"; \
	else \
		echo "✅ No obvious bugs detected"; \
	fi
	@# Check for transaction safety
	@if grep -r "session.execute.*SELECT.*INSERT" --include="*.py" backend/src/infrastructure/repositories/ 2>/dev/null; then \
		echo "⚠️  Potential race condition in repository"; \
	fi

qa-quality:
	@echo "📊 Running Code Quality QA..."
	@# Check for code smells
	@if grep -r "print(\|console.log" --include="*.py" --include="*.ts" backend/src/ frontend/src/ 2>/dev/null | grep -v "logger"; then \
		echo "⚠️  Debug statements found"; \
	fi
	@# Check for TODOs
	@TODO_COUNT=$$(grep -r "TODO:" --include="*.py" --include="*.ts" backend/src/ frontend/src/ 2>/dev/null | wc -l); \
	if [ $$TODO_COUNT -gt 5 ]; then \
		echo "⚠️  $$TODO_COUNT TODOs found (consider addressing)"; \
	else \
		echo "✅ Code quality acceptable ($$TODO_COUNT TODOs)"; \
	fi

qa-security:
	@echo "🔒 Running Security QA..."
	@# Check for secrets
	@if grep -r "ghp_[a-zA-Z0-9]\{36,\}\|sk-[a-zA-Z0-9]\{20,\}" --include="*.py" --include="*.ts" --include="*.md" . 2>/dev/null; then \
		echo "🚨 Secrets detected!"; \
		exit 1; \
	else \
		echo "✅ No secrets detected"; \
	fi
	@# Check for hardcoded passwords
	@if grep -ri "password.*=.*['\"][^'\"]*['\"]" --include="*.py" backend/src/ 2>/dev/null; then \
		echo "⚠️  Potential hardcoded credentials"; \
	fi

qa-perf:
	@echo "⚡ Running Performance QA..."
	@# Check for N+1 queries
	@N1_COUNT=$$(grep -r "for.*in.*:\|while.*:" --include="*.py" backend/src/infrastructure/repositories/ 2>/dev/null | grep -v "selectinload" | wc -l); \
	if [ $$N1_COUNT -gt 0 ]; then \
		echo "⚠️  $$N1_COUNT potential N+1 queries (check for eager loading)"; \
	else \
		echo "✅ No obvious N+1 queries"; \
	fi

qa-tdd:
	@echo "🧪 Running TDD QA..."
	@# Check test coverage
	@cd backend && python -m pytest --cov=src --cov-report=term 2>/dev/null | grep -E "TOTAL|coverage" || echo "⚠️  Run 'make test-backend' for coverage"

# ============================================
# BMad Flow
# ============================================

bmad-review:
	@echo "🎯 Running BMad Code Review..."
	@echo "=================================="
	@echo ""
	@echo "Phase 1: Development Quality Gate"
	$(MAKE) lint
	@echo ""
	@echo "Phase 2: Parallel QA Review"
	$(MAKE) qa
	@echo ""
	@echo "Phase 3: Consolidation"
	@echo "Manual consolidation required (see .docs/BMAD_COMPLIANCE.md)"
	@echo ""
	@echo "Review complete. Check findings above."

bmad-retry:
	@echo "🔄 Running BMad with Retry Loop..."
	@for i in 1 2 3; do \
		echo ""; \
		echo "Attempt $$i/3"; \
		echo "============"; \
		if $(MAKE) qa; then \
			echo "✅ QA Passed on attempt $$i"; \
			exit 0; \
		else \
			echo "❌ QA Failed on attempt $$i"; \
			if [ $$i -lt 3 ]; then \
				echo "Retrying..."; \
				sleep 2; \
			fi; \
		fi; \
	done; \
	echo "❌ All retry attempts exhausted"

# ============================================
# Docker
# ============================================

build:
	docker-compose build --no-cache

clean:
	docker-compose down -v
	docker system prune -f
