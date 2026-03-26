---
name: auth-skill
description: Implement secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Secure Authentication System

## Overview

This skill provides guidance and patterns for implementing modern, secure authentication systems. It covers user registration, login flows, password security, token-based authentication, and integration with Better Auth.

Use this skill when building APIs, web applications, or SaaS platforms that require robust authentication.

---

## Instructions

### 1. Core Authentication Flows
- Implement user signup with input validation
- Implement user signin with credential verification
- Securely hash and store passwords
- Authenticate users using JWT tokens

### 2. Password Security
- Hash passwords using `bcrypt` or `argon2`
- Apply salting automatically via the hashing library
- Never store or log plain-text passwords
- Enforce strong password requirements

### 3. JWT Token Handling
- Generate JWT on successful signin
- Use short-lived access tokens
- Store secrets in environment variables
- Verify JWTs on protected routes
- Invalidate tokens on logout where applicable

### 4. Better Auth Integration
- Configure Better Auth with a database adapter
- Use built-in session and token strategies
- Customize authorization callbacks
- Extend user metadata and roles
- Integrate seamlessly with existing auth flows

---

## Best Practices

- Always validate and sanitize user input
- Use HTTPS in all environments
- Store JWTs in HTTP-only cookies when possible
- Rotate JWT secrets periodically
- Protect sensitive routes with middleware
- Avoid leaking auth errors that reveal system details
- Log authentication events without sensitive data

---

## Example Implementation

### Signup and Signin (Node.js)

```ts
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

export async function signup(req, res) {
  const { email, password } = req.body;

  const hashedPassword = await bcrypt.hash(password, 12);

  await db.user.create({
    data: { email, password: hashedPassword },
  });

  res.status(201).json({ message: "User created" });
}

export async function signin(req, res) {
  const { email, password } = req.body;

  const user = await db.user.findUnique({ where: { email } });
  if (!user) return res.status(401).json({ error: "Invalid credentials" });

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(401).json({ error: "Invalid credentials" });

  const token = jwt.sign(
    { userId: user.id },
    process.env.JWT_SECRET,
    { expiresIn: "15m" }
  );

  res.json({ token });
}
