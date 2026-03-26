import Link from 'next/link'
import { Container, Button } from '@components/ui'

/**
 * Home Page - Landing Page
 * 
 * Mobile-first responsive design:
 * - Base styles: Mobile (320-639px)
 * - md: breakpoint: Tablet (768px+)
 * - lg: breakpoint: Desktop (1024px+)
 */
export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white flex flex-col justify-center py-8 px-4 sm:px-6 lg:px-8 lg:py-12">
      <Container size="md" centered>
        <div className="bg-white py-8 px-6 shadow-xl sm:rounded-xl sm:px-10 lg:px-12 border border-gray-100 w-full max-w-sm sm:max-w-md lg:max-w-lg">
          <div className="text-center space-y-4 sm:space-y-6">
            {/* Title */}
            <div className="space-y-2 sm:space-y-3">
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 tracking-tight">
                Welcome to Todo App
              </h1>
              <p className="text-base sm:text-lg text-gray-600 max-w-sm mx-auto leading-relaxed">
                Manage your tasks efficiently with our secure, AI-powered platform
              </p>
            </div>

            {/* Divider */}
            <div className="w-12 h-1 bg-primary-500 rounded-full mx-auto sm:w-16" />

            {/* Action Buttons */}
            <div className="space-y-3 pt-4">
              <Link href="/login" className="block">
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  className="shadow-md hover:shadow-lg transition-shadow min-h-[48px] sm:min-h-[52px]"
                >
                  Sign In
                </Button>
              </Link>

              <Link href="/register" className="block">
                <Button
                  variant="secondary"
                  size="lg"
                  fullWidth
                  className="shadow-sm hover:shadow-md transition-shadow min-h-[48px] sm:min-h-[52px]"
                >
                  Create Account
                </Button>
              </Link>
            </div>

            {/* Features */}
            <div className="pt-6 border-t border-gray-100">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4 text-xs sm:text-sm text-gray-500">
                <div className="flex flex-col items-center space-y-1">
                  <span className="font-semibold text-gray-700 text-base sm:text-lg">🚀 Fast</span>
                  <span>Instant task management</span>
                </div>
                <div className="flex flex-col items-center space-y-1">
                  <span className="font-semibold text-gray-700 text-base sm:text-lg">🔒 Secure</span>
                  <span>JWT authentication</span>
                </div>
                <div className="flex flex-col items-center space-y-1">
                  <span className="font-semibold text-gray-700 text-base sm:text-lg">🤖 AI-Powered</span>
                  <span>Smart assistance</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Container>
    </div>
  )
}
