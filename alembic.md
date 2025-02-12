# Alembic Guide

## What is Alembic?
Alembic is a lightweight database migration tool for SQLAlchemy. It helps manage schema changes in a structured and version-controlled manner.

## Setting Up Alembic

1. Install Alembic:
   ```bash
   pip install alembic
   ```

2. Initialize Alembic in your project:
   ```bash
   alembic init alembic
   ```
   This creates an `alembic` directory and an `alembic.ini` configuration file.

3. Configure Alembic:
   - Edit `alembic.ini` and update the `sqlalchemy.url` to match your database connection.
   - Modify `env.py` to use the correct metadata from your SQLAlchemy models.

## Common Alembic Commands

### 1. Create a New Migration
   ```bash
   alembic revision -m "Description of change"
   ```
   This generates a new migration file inside `alembic/versions/`.

### 2. Auto-generate a Migration (Based on Model Changes)
   ```bash
   alembic revision --autogenerate -m "Auto-generated migration"
   ```
   Ensure that `env.py` is properly set up to detect your models.

### 3. Apply Migrations (Upgrade Database)
   ```bash
   alembic upgrade head
   ```
   This applies all pending migrations to the latest version.

### 4. Downgrade Migrations (Rollback Changes)
   ```bash
   alembic downgrade -1
   ```
   Rolls back the last migration. To downgrade to a specific version, use:
   ```bash
   alembic downgrade <revision_id>
   ```

### 5. Check Current Database Version
   ```bash
   alembic current
   ```

### 6. View Migration History
   ```bash
   alembic history
   ```

### 7. Show SQL Script for a Migration
   ```bash
   alembic upgrade head --sql
   ```
   This outputs the SQL commands instead of executing them.

## Best Practices
- Always review migration scripts before applying them.
- Use `--autogenerate` with caution and manually verify changes.
- Keep migrations in version control to maintain history.
- Test migrations in a staging environment before applying them to production.

---
With Alembic, managing database schema changes becomes much easier, providing a structured and efficient way to handle migrations in your project. 🚀