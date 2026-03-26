'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import apiClient from '@/utils/api'
import { Container, Card, Input, Button } from '@components/ui'
import { LogIn } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [touchedFields, setTouchedFields] = useState<Record<string, boolean>>({})
  const router = useRouter()

  // Check if user is already logged in
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/dashboard')
    }
  }, [router])

  // Validation functions
  const validateEmail = (value: string): string => {
    if (!value.trim()) {
      return 'Email address is required'
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      return 'Please enter a valid email address'
    }
    return ''
  }

  const validatePassword = (value: string): string => {
    if (!value) {
      return 'Password is required'
    }
    return ''
  }

  // Blur handlers for field-level validation
  const handleEmailBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const value = e.target.value
    setTouchedFields(prev => ({ ...prev, email: true }))
    const error = validateEmail(value)
    setFieldErrors(prev => ({ ...prev, email: error }))
  }

  const handlePasswordBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const value = e.target.value
    setTouchedFields(prev => ({ ...prev, password: true }))
    const error = validatePassword(value)
    setFieldErrors(prev => ({ ...prev, password: error }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Validate all fields
    const emailError = validateEmail(email)
    const passwordError = validatePassword(password)

    setFieldErrors({
      email: emailError,
      password: passwordError
    })

    // Check if any errors
    if (emailError || passwordError) {
      setLoading(false)
      return
    }

    try {
      const response = await apiClient.post('/auth/login', {
        email,
        password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      const { access_token } = response.data
      localStorage.setItem('token', access_token)

      // Show success state before redirect
      setSuccess(true)
      
      // Redirect to dashboard after successful login
      setTimeout(() => {
        router.push('/dashboard')
      }, 1000)
    } catch (err: any) {
      const errorData = err.response?.data
      let errorMessage = 'Login failed'

      if (errorData?.message) {
        errorMessage = errorData.message
      } else if (Array.isArray(errorData?.detail)) {
        // Handle Pydantic validation errors
        errorMessage = errorData.detail.map((e: any) => e.msg || e.message).join(', ')
      } else if (errorData?.detail) {
        errorMessage = typeof errorData.detail === 'string' ? errorData.detail : 'Incorrect email or password'
      }

      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Container size="sm" centered>
        <Card padding="lg" shadow="lg" className="border border-gray-100">
          {/* Header */}
          <div className="text-center mb-8 space-y-2">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-600 rounded-xl mb-4 shadow-md">
              <LogIn className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-3xl font-bold text-gray-900">
              Welcome back
            </h2>
            <p className="text-gray-600">
              Sign in to access your tasks
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Success Message */}
            {success && (
              <div
                className="rounded-lg bg-success-50 border border-success-200 p-4 flex items-start gap-3"
                role="status"
                aria-live="polite"
              >
                <svg
                  className="w-5 h-5 text-success-600 flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <div>
                  <p className="text-sm font-medium text-success-800">Welcome back!</p>
                  <p className="text-sm text-success-700 mt-1">Redirecting to your dashboard...</p>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && !success && (
              <div
                className="rounded-lg bg-error-50 border border-error-200 p-4 flex items-start gap-3"
                role="alert"
              >
                <svg
                  className="w-5 h-5 text-error-600 flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
                <p className="text-sm text-error-700">{error}</p>
              </div>
            )}

            {/* Email Field */}
            <Input
              id="email"
              label="Email address"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onBlur={handleEmailBlur}
              error={touchedFields.email ? fieldErrors.email : undefined}
              success={touchedFields.email && !fieldErrors.email && email.length > 0}
              successMessage={touchedFields.email && !fieldErrors.email && email.length > 0 ? 'Valid email address' : undefined}
              required
              disabled={loading || success}
            />

            {/* Password Field */}
            <Input
              id="password"
              label="Password"
              type="password"
              autoComplete="current-password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onBlur={handlePasswordBlur}
              error={touchedFields.password ? fieldErrors.password : undefined}
              success={touchedFields.password && !fieldErrors.password && password.length > 0}
              successMessage={touchedFields.password && !fieldErrors.password && password.length > 0 ? undefined : undefined}
              required
              disabled={loading || success}
            />

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={loading}
              disabled={success}
              className="mt-2"
            >
              {loading ? 'Signing in...' : success ? 'Success!' : 'Sign in'}
            </Button>
          </form>

          {/* Sign Up Link */}
          <div className="mt-6 pt-6 border-t border-gray-100 text-center">
            <p className="text-sm text-gray-600">
              Don&apos;t have an account?{' '}
              <Link
                href="/register"
                className="font-medium text-primary-600 hover:text-primary-700 transition-colors"
              >
                Sign up for free
              </Link>
            </p>
          </div>
        </Card>
      </Container>
    </div>
  )
}
