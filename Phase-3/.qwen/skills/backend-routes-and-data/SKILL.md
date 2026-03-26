---
name: backend-routes-and-data
description: Design and implement backend routes, handle requests/responses, and connect to databases. Use for API and server-side development.
---

# Backend Skill – Routes, Requests, and Database Integration

## Instructions

1. **Routing**
   - Define RESTful routes (GET, POST, PUT/PATCH, DELETE)
   - Organize routes by resource or feature
   - Use clear and consistent URL naming

2. **Request & Response Handling**
   - Validate incoming request data
   - Handle headers, params, query strings, and body
   - Return proper HTTP status codes
   - Send structured JSON responses
   - Implement error handling and middleware

3. **Database Connection**
   - Configure database connection (SQL or NoSQL)
   - Use environment variables for credentials
   - Implement models/schemas
   - Perform CRUD operations
   - Handle connection errors and retries

4. **Business Logic**
   - Separate controllers from routes
   - Keep logic reusable and testable
   - Avoid heavy logic inside route definitions

## Best Practices
- Follow REST or API design standards
- Use async/await for non-blocking operations
- Centralize error handling
- Never expose sensitive data
- Add basic logging for requests and errors
- Write code that is framework-agnostic when possible

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { getUsers, createUser } from "../controllers/user.controller.js";

const router = express.Router();

router.get("/", getUsers);
router.post("/", createUser);

export default router;
