---
name: database-schema-skill
description: Design relational database schemas, create tables, and manage migrations using best practices.
---

# Database Schema & Migrations Skill

## Instructions

1. **Schema Design**
   - Identify entities and relationships
   - Normalize tables (up to 3NF where appropriate)
   - Define primary and foreign keys
   - Choose correct data types

2. **Table Creation**
   - Use clear, consistent naming conventions
   - Add indexes for frequently queried columns
   - Enforce constraints (NOT NULL, UNIQUE, CHECK)
   - Include audit fields (created_at, updated_at)

3. **Migrations**
   - Create reversible migrations (up/down)
   - Avoid destructive changes without backups
   - Keep migrations small and atomic
   - Version control all migration files

4. **Data Integrity**
   - Use foreign key constraints
   - Apply cascading rules carefully
   - Prevent orphaned records
   - Validate data at the database level

## Best Practices
- Prefer explicit schema over implicit behavior
- Never edit old migrations in shared environments
- Use snake_case for tables and columns
- Keep business logic out of the database when possible
- Document schema decisions clearly

## Example Structure

### SQL Table Definition
```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
