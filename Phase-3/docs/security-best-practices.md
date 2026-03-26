# Security Best Practices

## JWT Handling
- Store JWTs securely in httpOnly cookies or secure local storage
- Implement proper token expiry checks
- Refresh tokens before they expire
- Never expose JWT secrets in client-side code

## Password Security
- Use bcrypt for password hashing
- Enforce strong password requirements
- Implement rate limiting for login attempts
- Use HTTPS for all authentication endpoints

## User Data Isolation
- Always validate user ID in URL matches JWT claims
- Implement row-level security in database queries
- Use parameterized queries to prevent injection attacks
- Sanitize all user inputs

## API Security
- Implement proper CORS policies
- Use rate limiting to prevent abuse
- Validate all inputs on the server side
- Log security-relevant events

## Environment Configuration
- Store secrets in environment variables
- Use different secrets for different environments
- Never commit secrets to version control
- Rotate secrets regularly