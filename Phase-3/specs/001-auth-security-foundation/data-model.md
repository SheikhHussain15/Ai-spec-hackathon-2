# Data Model: Authentication & Security Foundation

## User Entity
- **Fields**:
  - id (UUID/string): Unique identifier for the user
  - email (string): User's email address (unique)
  - createdAt (timestamp): Account creation timestamp
  - updatedAt (timestamp): Last update timestamp
- **Relationships**: 
  - Owns: multiple Task entities (one-to-many)
- **Validation rules**:
  - Email must be valid format
  - Email must be unique
  - ID must be unique and immutable

## JWT Token Structure
- **Claims**:
  - user_id (string): Unique identifier of the authenticated user
  - email (string): Email address of the authenticated user
  - exp (integer): Expiration timestamp (Unix epoch)
  - iat (integer): Issued-at timestamp (Unix epoch)
  - sub (string): Subject identifier (same as user_id)
- **Validation rules**:
  - Token must be signed with shared secret
  - Token must not be expired (exp > current time)
  - Signature must be valid
  - user_id must match the expected format

## API Request Structure
- **Headers**:
  - Authorization (string): Format "Bearer <JWT_TOKEN>"
- **Validation rules**:
  - Authorization header must be present for protected endpoints
  - Token must be properly formatted (Bearer prefix)
  - Token must pass all JWT validation checks