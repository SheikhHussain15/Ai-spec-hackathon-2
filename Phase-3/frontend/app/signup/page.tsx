'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import apiClient from '@/utils/api'
import { Container, Card, Input, Button } from '@components/ui'

export default function Signup() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  // Check if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/dashboard')
    }
  }, [router])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Validate password length
    if (password.length < 8) {
      setError('Password must be at least 8 characters long')
      setLoading(false)
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      await apiClient.post('/auth/register', {
        name,
        email,
        password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      // Automatically log in after successful registration
      const loginResponse = await apiClient.post('/auth/login', {
        email,
        password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const { access_token } = loginResponse.data
      localStorage.setItem('token', access_token)

      // Redirect to dashboard after successful registration and login
      router.push('/dashboard')
    } catch (err: any) {
      const errorData = err.response?.data
      let errorMessage = 'Registration failed'

      if (errorData?.message) {
        errorMessage = errorData.message
      } else if (Array.isArray(errorData?.detail)) {
        // Handle Pydantic validation errors
        errorMessage = errorData.detail.map((e: any) => e.msg || e.message).join(', ')
      } else if (errorData?.detail) {
        errorMessage = typeof errorData.detail === 'string' ? errorData.detail : 'Registration failed'
      }

      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Container size="sm" centered>
        <Card padding="lg" shadow="lg">
          {/* Header */}
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Create a new account
            </h2>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Error Message */}
            {error && (
              <div className="rounded-md bg-error-50 p-4" role="alert">
                <p className="text-sm text-error-700">{error}</p>
              </div>
            )}

            {/* Name Field */}
            <Input
              id="name"
              label="Full Name"
              type="text"
              autoComplete="name"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            {/* Email Field */}
            <Input
              id="email"
              label="Email address"
              type="email"
              autoComplete="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            {/* Password Field */}
            <Input
              id="password"
              label="Password"
              type="password"
              autoComplete="current-password"
              placeholder="Create a password (min 8 characters)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />

            {/* Confirm Password Field */}
            <Input
              id="confirm-password"
              label="Confirm Password"
              type="password"
              autoComplete="current-password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={8}
            />

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={loading}
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </Button>
          </form>

          {/* Sign In Link */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                href="/login"
                className="font-medium text-primary-600 hover:text-primary-500"
              >
                Sign in
              </Link>
            </p>
          </div>
        </Card>
      </Container>
    </div>
  )
}
