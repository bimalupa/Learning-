.PHONY: help setup install verify check status clean run test smart-setup

help:
	@echo "🚀 Insurance Claim Processing System - Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make smart-setup    - Smart setup (only installs missing packages)"
	@echo "  make install        - Install all requirements"
	@echo "  make verify         - Verify requirements are installed"
	@echo ""
	@echo "Development:"
	@echo "  make run            - Run the Streamlit application"
	@echo "  make test           - Run test suite"
	@echo ""
	@echo "Maintenance:"
	@echo "  make status         - Show installation status"
	@echo "  make check          - Check missing packages"
	@echo "  make clean          - Clean cache and temporary files"
	@echo ""

smart-setup:
	@echo "🚀 Starting smart setup..."
	@python setup_smart.py

install:
	@echo "📦 Installing all requirements..."
	@pip install -r requirements.txt

verify:
	@echo "🔍 Verifying requirements..."
	@python verify_requirements.py --install

check:
	@echo "🔍 Checking for missing packages..."
	@python verify_requirements.py --check

status:
	@echo "📊 Showing installation status..."
	@python verify_requirements.py --status

run:
	@echo "🚀 Starting application..."
	@streamlit run ui/app.py

test:
	@echo "🧪 Running tests..."
	@python -m pytest test_system.py -v || python test_system.py

clean:
	@echo "🧹 Cleaning up..."
	@rm -f .requirements_cache.json
	@rm -rf __pycache__ .pytest_cache .streamlit
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned up temporary files"

venv:
	@echo "📦 Creating virtual environment..."
	@python -m venv venv
	@echo "✅ Virtual environment created"
	@echo "Activate with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"

deps:
	@echo "📚 Show dependencies..."
	@pip list

freeze:
	@echo "💾 Saving current environment..."
	@pip freeze > requirements_frozen.txt
	@echo "✅ Saved to requirements_frozen.txt"
