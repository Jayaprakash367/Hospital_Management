# Hospital Management System - Code Fixes and Improvements

## app.py Refactoring
- [ ] Replace hardcoded database path with config.py's DATABASE_PATH
- [ ] Implement context managers for database connections
- [ ] Replace print-based SMS sending with sms.py's SMSManager
- [ ] Add consistent error handling and input validation
- [ ] Refactor repeated session user role checks into decorators
- [ ] Clean up code formatting and add comments
- [ ] Remove duplicate imports and schema comments

## src/utils/config.py
- [ ] Review and confirm directory creation logic
- [ ] Add any missing configuration constants if needed

## src/utils/sms.py
- [ ] Confirm SMS sending logic is robust
- [ ] Ensure consistent usage in app.py

## Other SQLite Files
- [ ] Review src/database/db_manager.py for context managers and error handling
- [ ] Review migrate_db.py, init_db.py, etc. for consistency
- [ ] Apply similar improvements where applicable

## Testing
- [ ] Run existing tests (test_billing.py) to ensure no regressions
- [ ] Add tests for new helper functions if created
