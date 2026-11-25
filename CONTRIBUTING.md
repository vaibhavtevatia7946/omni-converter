# Contributing to OmniConvert

Thank you for your interest in contributing to **OmniConvert**! We welcome all contributions from bug fixes to feature requests.

---

## 🛠️ Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/vaibhavtevatia7946/omni-converter.git
   cd omni-converter
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the test suite:
   ```bash
   python test_converter.py
   ```

5. Start the local development server:
   ```bash
   ./run.sh
   # Or directly:
   uvicorn main:app --reload --port 8000
   ```

---

## 🚀 Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with clear messages.
3. Ensure all unit tests pass (`python test_converter.py`).
4. Push to your branch and open a Pull Request.

---

## 📜 Code of Conduct
Please be polite, respectful, and constructive in all interactions.
