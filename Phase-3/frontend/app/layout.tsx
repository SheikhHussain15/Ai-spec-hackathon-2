import '../src/styles/globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A multi-user todo application with authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}