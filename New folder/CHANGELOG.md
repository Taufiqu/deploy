# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete project documentation
- API documentation with examples
- Deployment guidelines
- Contributing guidelines
- Development setup instructions

### Changed
- Enhanced README with comprehensive information
- Updated environment configuration

### Fixed
- Database connection issues with Supabase
- Port configuration for Windows compatibility

## [1.0.0] - 2024-01-15

### Added
- Initial release of Proyek Pajak Backend
- OCR processing for invoice documents
- Database integration with Supabase
- RESTful API endpoints
- Excel export functionality
- Multi-format support (PDF, JPG, PNG)
- Spell checking for OCR results
- Data validation for invoice numbers and dates

### Features
- **Invoice Processing**: Extract data from tax invoices using OCR
- **Bukti Setor Processing**: Extract data from tax payment receipts
- **Database Storage**: Store processed data in PostgreSQL (Supabase)
- **Export Functionality**: Generate Excel reports
- **API Endpoints**: Complete REST API for all operations
- **File Upload**: Support for PDF and image files
- **Data Validation**: Automatic validation of extracted data

### API Endpoints
- `POST /api/process` - Process invoice files
- `POST /api/save` - Save invoice data
- `GET /api/history` - Get invoice history
- `GET /api/export` - Export to Excel
- `DELETE /api/delete/{jenis}/{id}` - Delete invoice
- `POST /api/bukti_setor/process` - Process bukti setor
- `POST /api/bukti_setor/save` - Save bukti setor data
- `GET /api/bukti_setor/history` - Get bukti setor history
- `GET /api/bukti_setor/export` - Export bukti setor to Excel
- `DELETE /api/bukti_setor/delete/{id}` - Delete bukti setor

### Database Schema
- `ppn_masukan` - Input tax invoices
- `ppn_keluaran` - Output tax invoices
- `bukti_setor` - Tax payment receipts

### Dependencies
- Flask 2.3.3
- SQLAlchemy 2.0.23
- EasyOCR 1.7.0
- Supabase client
- OpenPyXL for Excel generation
- Pillow for image processing
- pdf2image for PDF processing

### Configuration
- Environment-based configuration
- Supabase database connection
- Configurable port settings
- OCR engine configuration
- File upload limits

### Security
- Input validation
- File type restrictions
- SQL injection prevention
- XSS protection

### Performance
- Database connection pooling
- Optimized OCR processing
- Efficient file handling
- Memory management

---

## Release Notes

### Version 1.0.0 - Initial Release

This is the first stable release of Proyek Pajak Backend, a comprehensive solution for processing Indonesian tax documents using OCR technology.

**Key Features:**
- Automated extraction of tax invoice data
- Support for both input and output tax invoices
- Tax payment receipt processing
- Excel export functionality
- RESTful API with comprehensive endpoints
- Database integration with Supabase
- Multi-format file support

**Technical Stack:**
- Backend: Python Flask
- Database: PostgreSQL (Supabase)
- OCR: EasyOCR
- File Processing: Pillow, pdf2image
- Export: OpenPyXL

**Getting Started:**
1. Clone the repository
2. Set up environment variables
3. Install dependencies
4. Configure database connection
5. Run the application

**API Documentation:**
Complete API documentation is available in `API_DOCS.md`

**Deployment:**
Deployment instructions for various platforms are available in `DEPLOYMENT.md`

**Contributing:**
Guidelines for contributing are available in `CONTRIBUTING.md`

---

## Migration Guide

### From Local Database to Supabase

If you're migrating from a local PostgreSQL setup to Supabase:

1. **Export existing data:**
   ```bash
   pg_dump your_local_db > backup.sql
   ```

2. **Update environment variables:**
   ```bash
   DATABASE_URL=postgresql://postgres.username:password@host:5432/postgres
   ```

3. **Run migrations:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Import data (if needed):**
   ```bash
   psql -h your-supabase-host -U your-username -d postgres -f backup.sql
   ```

### Configuration Changes

- **Port Configuration**: Changed from 5000 to 5001 for Windows compatibility
- **SSL Configuration**: Added sslmode=require for Supabase
- **Environment Variables**: Consolidated configuration in .env file

---

## Known Issues

### Fixed in v1.0.0
- ✅ Database connection timeout issues
- ✅ Port 5000 permission denied on Windows
- ✅ OCR accuracy improvements
- ✅ File upload size limitations
- ✅ Excel export formatting issues

### Under Investigation
- OCR performance with low-quality images
- Memory usage optimization for large files
- Error handling for corrupted PDF files

### Future Enhancements
- Batch processing support
- Real-time OCR processing
- Advanced data validation
- Multi-language support
- API rate limiting
- Authentication system

---

## Support

For support and questions:
- 📧 Create an issue on GitHub
- 📖 Check the documentation
- 🔍 Search existing issues
- 💬 Join discussions

## Acknowledgments

Special thanks to:
- EasyOCR team for the OCR engine
- Supabase team for the database platform
- Flask community for the web framework
- All contributors and testers

---

**🚀 Happy processing!**
