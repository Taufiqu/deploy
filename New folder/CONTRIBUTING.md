# 🤝 Contributing Guidelines

Terima kasih atas minat Anda untuk berkontribusi pada Proyek Pajak Backend! Dokumen ini berisi panduan untuk membantu Anda memberikan kontribusi yang efektif.

## 📋 Daftar Isi

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Process](#contributing-process)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## 🌟 Code of Conduct

Proyek ini mengikuti kode etik yang ramah dan inklusif. Dengan berpartisipasi, Anda setuju untuk:

- Menggunakan bahasa yang ramah dan inklusif
- Menghormati sudut pandang dan pengalaman yang berbeda
- Menerima kritik konstruktif dengan baik
- Fokus pada yang terbaik untuk komunitas
- Menunjukkan empati terhadap anggota komunitas lainnya

## 🚀 Getting Started

### Cara Berkontribusi

Ada beberapa cara untuk berkontribusi:

1. **Reporting Bugs**: Laporkan bug yang Anda temukan
2. **Feature Requests**: Usulkan fitur atau perbaikan baru
3. **Code Contributions**: Submit pull request untuk perbaikan atau fitur
4. **Documentation**: Perbaiki atau tambahkan dokumentasi
5. **Testing**: Bantu testing dan quality assurance

### Skill yang Dibutuhkan

- **Python**: Flask, SQLAlchemy, pytest
- **Database**: PostgreSQL, Supabase
- **OCR**: EasyOCR, Tesseract
- **API**: REST API design
- **Frontend** (optional): HTML, CSS, JavaScript
- **DevOps** (optional): Docker, CI/CD

## 🔧 Development Setup

### 1. Fork Repository

```bash
# Fork repository di GitHub
# Clone fork Anda
git clone https://github.com/YOUR_USERNAME/proyek-pajak-backend-clean.git
cd proyek-pajak-backend-clean

# Add upstream remote
git remote add upstream https://github.com/Taufiqu/proyek-pajak-backend-clean.git
```

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your local configuration
# Gunakan database lokal atau Supabase test instance
```

### 4. Database Setup

```bash
# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run migrations (if any)
python -m alembic upgrade head
```

### 5. Run Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### 6. Start Development Server

```bash
python app.py
```

## 🔄 Contributing Process

### 1. Choose an Issue

- Lihat [Issues](https://github.com/Taufiqu/proyek-pajak-backend-clean/issues) untuk task yang tersedia
- Pilih issue dengan label `good first issue` untuk pemula
- Comment di issue untuk menunjukkan minat Anda

### 2. Create Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# atau
git checkout -b bugfix/issue-number
```

### 3. Make Changes

- Ikuti [code style guidelines](#code-style)
- Tulis tests untuk kode baru
- Update dokumentasi jika diperlukan
- Commit changes dengan message yang jelas

### 4. Test Your Changes

```bash
# Run tests
python -m pytest

# Run linting
flake8 .
black --check .
isort --check-only .

# Test manually
python app.py
# Test API endpoints
```

### 5. Submit Pull Request

```bash
# Push changes
git push origin feature/your-feature-name

# Create pull request di GitHub
# Berikan deskripsi yang jelas tentang perubahan
```

## 🎨 Code Style

### Python Style Guide

Project menggunakan:
- **PEP 8** untuk Python code style
- **Black** untuk code formatting
- **isort** untuk import sorting
- **flake8** untuk linting

### Setup Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Code Formatting

```bash
# Format code with black
black .

# Sort imports
isort .

# Check linting
flake8 .
```

### Configuration Files

`.flake8`:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = venv, migrations, __pycache__
```

`pyproject.toml`:
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | migrations
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "John Doe"
def process_invoice():
    pass

# Classes: PascalCase
class InvoiceProcessor:
    pass

# Constants: UPPER_CASE
DATABASE_URL = "postgresql://..."

# Private methods: _underscore_prefix
def _internal_method():
    pass
```

## 🧪 Testing

### Test Structure

```
tests/
├── unit/               # Unit tests
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/        # Integration tests
│   ├── test_api.py
│   └── test_database.py
├── fixtures/           # Test fixtures
│   ├── sample_invoice.pdf
│   └── sample_data.json
└── conftest.py        # pytest configuration
```

### Writing Tests

```python
# test_example.py
import pytest
from app import app, db
from models import PPNMasukan

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_save_invoice(client):
    # Test data
    invoice_data = {
        'jenis': 'masukan',
        'no_faktur': '010.000-24.00000001',
        'tanggal': '2024-01-15',
        'nama_lawan_transaksi': 'PT. Test',
        'dpp': 100000,
        'ppn': 11000
    }
    
    # Send request
    response = client.post('/api/save', json=invoice_data)
    
    # Assert response
    assert response.status_code == 200
    assert response.json['success'] == True
    
    # Assert database
    invoice = PPNMasukan.query.first()
    assert invoice.no_faktur == '010.000-24.00000001'
```

### Test Commands

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_models.py

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run tests with verbose output
python -m pytest -v

# Run tests matching pattern
python -m pytest -k "test_save"
```

## 📝 Submitting Changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Commit Message Format

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**
```
feat(api): add bukti setor export endpoint

Add new endpoint to export bukti setor data to Excel format.
Includes filtering by date range and kode setor.

Closes #123

fix(ocr): improve number detection accuracy

Improve regex pattern for detecting monetary values in OCR results.
Handle edge cases with comma and period separators.

Fixes #456
```

### Review Process

1. **Automated Checks**: CI/CD pipeline akan menjalankan tests dan linting
2. **Code Review**: Maintainer akan review code Anda
3. **Feedback**: Implementasikan feedback jika ada
4. **Approval**: Setelah disetujui, PR akan di-merge

## 🐛 Reporting Issues

### Bug Reports

Gunakan template berikut untuk melaporkan bug:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g. Windows 10]
- Python version: [e.g. 3.9.0]
- Browser: [e.g. Chrome 90]

## Screenshots
Add screenshots if applicable

## Additional Context
Any other context about the problem
```

### Feature Requests

```markdown
## Feature Description
Clear description of the feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this be implemented?

## Alternatives Considered
Other solutions you've considered

## Additional Context
Any other context or screenshots
```

## 📚 Documentation

### Types of Documentation

1. **Code Comments**: Untuk complex logic
2. **Docstrings**: Untuk functions dan classes
3. **API Documentation**: Untuk endpoints
4. **README**: Untuk project overview
5. **Wiki**: Untuk detailed guides

### Documentation Style

```python
def process_invoice(file_path: str, jenis: str) -> dict:
    """
    Process invoice file using OCR and extract data.
    
    Args:
        file_path: Path to the invoice file
        jenis: Type of invoice ('masukan' or 'keluaran')
    
    Returns:
        Dictionary containing extracted invoice data
    
    Raises:
        ValueError: If jenis is not valid
        FileNotFoundError: If file doesn't exist
    """
    pass
```

## 🏗️ Project Structure

### Adding New Features

1. **API Endpoints**: Add to appropriate route file
2. **Business Logic**: Add to services/ directory
3. **Database Models**: Add to models.py
4. **Utilities**: Add to utils/ directory
5. **Tests**: Add corresponding test files

### Module Organization

```
feature_name/
├── __init__.py
├── routes.py          # API endpoints
├── services/          # Business logic
│   ├── __init__.py
│   ├── processor.py
│   └── validator.py
├── utils/             # Utilities
│   ├── __init__.py
│   └── helpers.py
└── tests/             # Tests
    ├── __init__.py
    ├── test_routes.py
    └── test_services.py
```

## 🔍 Code Review Guidelines

### For Contributors

- **Keep PRs small**: Easier to review
- **Write clear descriptions**: Explain what and why
- **Add tests**: Ensure functionality works
- **Update documentation**: Keep docs current
- **Respond to feedback**: Address review comments

### For Reviewers

- **Be constructive**: Provide helpful feedback
- **Check functionality**: Does it work as expected?
- **Review tests**: Are they comprehensive?
- **Consider maintainability**: Is code easy to maintain?
- **Approve when ready**: Don't delay unnecessarily

## 🎯 Getting Help

### Where to Ask Questions

1. **GitHub Issues**: For bugs and feature requests
2. **GitHub Discussions**: For general questions
3. **Code Comments**: For specific implementation questions

### Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Supabase Documentation](https://supabase.com/docs)

## 🏆 Recognition

Contributors akan diakui melalui:
- **Contributors section** di README
- **Changelog** untuk setiap release
- **GitHub contributors** page
- **Special thanks** untuk kontribusi besar

## 📊 Development Metrics

Track progress dengan:
- **Code coverage**: Target 80%+
- **Test passing rate**: 100%
- **Documentation coverage**: Semua public APIs
- **Issue resolution time**: < 7 days untuk bugs

---

**🙏 Terima kasih** atas kontribusi Anda! Setiap kontribusi, besar atau kecil, sangat berarti untuk kemajuan proyek ini.
