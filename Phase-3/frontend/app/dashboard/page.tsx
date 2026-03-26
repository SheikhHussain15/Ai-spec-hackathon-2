'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import apiClient from '@/utils/api'
import {
  PlusCircle,
  Trash2,
  Edit3,
  CheckCircle,
  Circle,
  MessageSquare,
  X,
  LogOut,
  Check,
} from 'lucide-react'
import { Container, Header, Button, Card, Badge, Skeleton, Input, IconButton, DashboardSkeleton } from '@components/ui'
import { motion, AnimatePresence } from 'framer-motion'

interface Task {
  id: string
  title: string
  description: string
  completed: boolean
  createdAt: string
  updatedAt: string
}

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  // Form state
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')
  const [showForm, setShowForm] = useState(false)

  // AI Chat state
  const [showChat, setShowChat] = useState(false)
  const [chatMessages, setChatMessages] = useState<
    Array<{ role: string; content: string; toolCalls?: any[] }>
  >([])
  const [chatInput, setChatInput] = useState('')
  const [chatLoading, setChatLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Memoized fetchTasks to avoid stale closures
  const fetchTasks = useCallback(async () => {
    try {
      const response = await apiClient.get('/tasks')
      setTasks(response.data)
      setLoading(false)
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch tasks')
      setLoading(false)
    }
  }, [])

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    fetchTasks()
  }, [router, fetchTasks])

  const handleLogout = () => {
    localStorage.removeItem('token')
    router.push('/login')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      if (editingId) {
        // Update existing task
        await apiClient.put(`/tasks/${editingId}`, {
          title: editTitle,
          description: editDescription,
        })

        setEditingId(null)
        setEditTitle('')
        setEditDescription('')
      } else {
        // Create new task
        const response = await apiClient.post('/tasks', {
          title,
          description,
        })
        console.log('Task created successfully:', response.data)

        setTitle('')
        setDescription('')
      }

      fetchTasks() // Refresh tasks
      setShowForm(false)
    } catch (err: any) {
      console.error('Task operation error:', err)

      let errorMessage = 'Operation failed'

      if (err.response) {
        // Server responded with error
        const errorData = err.response.data
        if (errorData?.detail) {
          errorMessage =
            typeof errorData.detail === 'string'
              ? errorData.detail
              : JSON.stringify(errorData.detail)
        } else if (errorData?.message) {
          errorMessage = errorData.message
        }
      } else if (err.request) {
        // Request was made but no response
        errorMessage =
          'No response from server. Please check if the backend is running.'
      } else if (err.message) {
        errorMessage = err.message
      }

      setError(errorMessage)
    }
  }

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await apiClient.delete(`/tasks/${id}`)

        fetchTasks() // Refresh tasks
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to delete task')
      }
    }
  }

  // AI Chat Functions
  const sendChatMessage = async (message: string) => {
    if (!message.trim()) return

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    // Get user ID from token
    let userId = ''
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      userId = payload.user_id || payload.sub
    } catch (e) {
      setError('Invalid authentication token')
      return
    }

    // Add user message to chat
    const userMessage = { role: 'user', content: message }
    setChatMessages((prev) => [...prev, userMessage])
    setChatInput('')
    setChatLoading(true)

    try {
      const response = await apiClient.post(`/api/${userId}/chat`, {
        message: message,
        conversation_id: conversationId || undefined,
      })

      const { response: aiResponse, conversation_id, tool_calls } = response.data

      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: aiResponse,
        toolCalls: tool_calls,
      }
      setChatMessages((prev) => [...prev, aiMessage])

      // Save conversation ID
      if (conversation_id) {
        setConversationId(conversation_id)
        localStorage.setItem('chat_conversation_id', conversation_id)
      }

      // Refresh tasks if AI created/modified tasks
      if (tool_calls && tool_calls.length > 0) {
        console.log('[Dashboard] AI modified tasks, refreshing...')
        // Small delay to ensure database transaction is complete
        setTimeout(() => {
          fetchTasks()
        }, 500)
      }
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.message || 'Failed to get AI response'
      setChatMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `Error: ${errorMessage}` },
      ])
    } finally {
      setChatLoading(false)
    }
  }

  const toggleChat = () => {
    setShowChat(!showChat)
    // Load saved conversation when opening chat
    if (!showChat) {
      const savedConvId = localStorage.getItem('chat_conversation_id')
      if (savedConvId) {
        setConversationId(savedConvId)
      }
    }
  }

  const startEditing = (task: Task) => {
    setEditingId(task.id)
    setEditTitle(task.title)
    setEditDescription(task.description)
    setShowForm(true)
  }

  const toggleComplete = async (id: string, currentStatus: boolean) => {
    try {
      await apiClient.patch(`/tasks/${id}/toggle`)

      fetchTasks() // Refresh tasks
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to update task')
    }
  }

  if (loading) {
    return <DashboardSkeleton numberOfTasks={3} />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <Container size="xl">
          <div className="py-5">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Your Tasks</h1>
                <p className="text-sm text-gray-500 mt-1">
                  Manage and track your tasks efficiently
                </p>
              </div>
              <Button
                variant="ghost"
                size="md"
                onClick={handleLogout}
                className="text-gray-700 hover:text-error-600 hover:bg-error-50"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </Container>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-6 rounded-lg bg-error-50 border border-error-200 p-4"
              role="alert"
            >
              <p className="text-sm text-error-700">{error}</p>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">
              Task Dashboard
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'} total
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <Button
              variant="secondary"
              size="md"
              onClick={toggleChat}
              icon={<MessageSquare className="w-4 h-4" />}
              className="shadow-sm hover:shadow-md transition-shadow"
            >
              {showChat ? 'Hide Chat' : 'AI Assistant'}
            </Button>
            <Button
              variant="primary"
              size="md"
              onClick={() => {
                setShowForm(!showForm)
                setEditingId(null)
                setEditTitle('')
                setEditDescription('')
              }}
              icon={<PlusCircle className="w-4 h-4" />}
              className="shadow-sm hover:shadow-md transition-shadow"
            >
              {showForm ? 'Cancel' : 'Add Task'}
            </Button>
          </div>
        </div>

        {/* Task Form */}
        <AnimatePresence>
          {showForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-8"
            >
              <Card padding="lg" shadow="md" className="border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-5">
                  {editingId ? 'Edit Task' : 'Create New Task'}
                </h3>
                <form onSubmit={handleSubmit} className="space-y-5">
                  {/* Title Field */}
                  <Input
                    id="title"
                    label="Title"
                    type="text"
                    placeholder="Enter task title"
                    value={editingId ? editTitle : title}
                    onChange={(e) =>
                      editingId
                        ? setEditTitle(e.target.value)
                        : setTitle(e.target.value)
                    }
                    required
                  />

                  {/* Description Field */}
                  <div>
                    <label
                      htmlFor="description"
                      className="block text-sm font-medium text-gray-700 mb-2"
                    >
                      Description
                    </label>
                    <textarea
                      id="description"
                      name="description"
                      rows={3}
                      value={editingId ? editDescription : description}
                      onChange={(e) =>
                        editingId
                          ? setEditDescription(e.target.value)
                          : setDescription(e.target.value)
                      }
                      className="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm transition-all duration-200 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 focus:ring-offset-1 disabled:bg-gray-100 disabled:cursor-not-allowed"
                      placeholder="Enter task description (optional)"
                    />
                  </div>

                  <div className="flex gap-3 pt-2">
                    <Button type="submit" variant="primary" size="md">
                      {editingId ? 'Update Task' : 'Create Task'}
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="md"
                      onClick={() => {
                        setShowForm(false)
                        setEditingId(null)
                        setEditTitle('')
                        setEditDescription('')
                      }}
                    >
                      Cancel
                    </Button>
                  </div>
                </form>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Tasks List */}
        <Card padding="none" shadow="md" className="border border-gray-200">
          {tasks.length === 0 ? (
            <div className="text-center py-16 px-4">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No tasks yet
              </h3>
              <p className="text-gray-500 mb-6">
                Create your first task to get started
              </p>
              <Button
                variant="primary"
                size="md"
                onClick={() => {
                  setShowForm(true)
                  setEditingId(null)
                  setEditTitle('')
                  setEditDescription('')
                }}
                icon={<PlusCircle className="w-4 h-4" />}
              >
                Create Task
              </Button>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {tasks.map((task) => (
                <motion.li
                  key={task.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.2 }}
                  className="group hover:bg-gray-50 transition-colors duration-200"
                >
                  <div className="px-5 py-4">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3 flex-1">
                        <button
                          onClick={() => toggleComplete(task.id, task.completed)}
                          className="flex-shrink-0 mt-0.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded-full p-0.5 hover:bg-gray-200 transition-colors"
                          aria-label={
                            task.completed
                              ? 'Mark as incomplete'
                              : 'Mark as complete'
                          }
                        >
                          {task.completed ? (
                            <CheckCircle className="h-6 w-6 text-success-600 hover:text-success-700 transition-colors" />
                          ) : (
                            <Circle className="h-6 w-6 text-gray-400 hover:text-primary-600 transition-colors" />
                          )}
                        </button>
                        <div className="flex-1 min-w-0">
                          <p
                            className={`text-base font-medium truncate transition-all duration-200 ${
                              task.completed
                                ? 'line-through text-gray-500'
                                : 'text-gray-900'
                            }`}
                          >
                            {task.title}
                          </p>
                          {task.description && (
                            <p
                              className={`mt-1 text-sm line-clamp-2 ${
                                task.completed
                                  ? 'text-gray-400 line-through'
                                  : 'text-gray-600'
                              }`}
                            >
                              {task.description}
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center gap-3 flex-shrink-0">
                        <Badge
                          variant={task.completed ? 'completed' : 'pending'}
                        >
                          {task.completed ? 'Completed' : 'Pending'}
                        </Badge>
                        <time className="text-sm text-gray-500 hidden sm:block">
                          {new Date(task.updatedAt).toLocaleDateString()}
                        </time>
                        {/* Desktop: Show on hover, Mobile: Always visible */}
                        <div className="hidden sm:flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <IconButton
                            variant="ghost"
                            size="sm"
                            onClick={() => startEditing(task)}
                            icon={Edit3}
                            tooltip="Edit task"
                            aria-label="Edit task"
                            className="text-gray-500 hover:text-primary-600 hover:bg-primary-50"
                          />
                          <IconButton
                            variant="ghost"
                            size="sm"
                            onClick={() => handleDelete(task.id)}
                            icon={Trash2}
                            tooltip="Delete task"
                            aria-label="Delete task"
                            className="text-gray-500 hover:text-error-600 hover:bg-error-50"
                          />
                        </div>
                      </div>
                    </div>
                    {/* Mobile actions - always visible */}
                    <div className="mt-3 flex items-center gap-2 sm:hidden">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => startEditing(task)}
                        icon={<Edit3 className="w-3 h-3" />}
                      >
                        Edit
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(task.id)}
                        icon={<Trash2 className="w-3 h-3" />}
                      >
                        Delete
                      </Button>
                    </div>
                    {/* Desktop actions - visible on hover */}
                    <div className="hidden sm:flex mt-3 items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => startEditing(task)}
                        icon={<Edit3 className="w-3 h-3" />}
                        className="text-gray-600 hover:text-primary-600"
                      >
                        Edit
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(task.id)}
                        icon={<Trash2 className="w-3 h-3" />}
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                </motion.li>
              ))}
            </ul>
          )}
        </Card>
      </main>

      {/* AI Chat Panel */}
      <AnimatePresence>
        {showChat && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ duration: 0.2 }}
            className="fixed bottom-0 right-0 w-full sm:w-96 h-[600px] max-h-[80vh] bg-white shadow-2xl rounded-tl-xl border border-gray-200 flex flex-col z-50"
          >
            {/* Chat Header */}
            <div className="flex justify-between items-center p-4 border-b border-gray-200 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-tl-xl">
              <div className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                <h3 className="font-semibold">AI Assistant</h3>
              </div>
              <button
                onClick={toggleChat}
                className="text-white/80 hover:text-white transition-colors p-1 hover:bg-white/10 rounded-lg"
                aria-label="Close chat"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50">
              {chatMessages.length === 0 ? (
                <div className="text-center text-gray-500 py-12">
                  <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <MessageSquare className="h-8 h-8 text-primary-600" />
                  </div>
                  <p className="text-sm font-medium">Ask me to help with your tasks!</p>
                  <p className="text-xs mt-2 text-gray-400">
                    Try: &quot;Add a task to review docs&quot;
                  </p>
                </div>
              ) : (
                <>
                  {chatMessages.map((msg, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.2 }}
                      className={`flex ${
                        msg.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm shadow-sm ${
                          msg.role === 'user'
                            ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white'
                            : 'bg-white border border-gray-200 text-gray-900'
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                        {msg.toolCalls && msg.toolCalls.length > 0 && (
                          <div className="mt-2 space-y-1.5">
                            {msg.toolCalls.map((tool: any, tIdx: number) => (
                              <div
                                key={tIdx}
                                className={`text-xs p-2.5 rounded-lg ${
                                  tool.success
                                    ? 'bg-success-50 text-success-800 border border-success-200'
                                    : 'bg-error-50 text-error-800 border border-error-200'
                                }`}
                              >
                                <div className="font-medium flex items-center gap-1.5">
                                  {tool.success ? (
                                    <Check className="w-3 h-3" />
                                  ) : (
                                    <X className="w-3 h-3" />
                                  )}
                                  {tool.tool_name}
                                </div>
                                {tool.result && (
                                  <div className="mt-1 text-gray-600 overflow-hidden text-ellipsis">
                                    {JSON.stringify(tool.result, null, 2).slice(
                                      0,
                                      100
                                    )}
                                    ...
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                  {chatLoading && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex justify-start"
                    >
                      <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
                        <div className="flex gap-1.5">
                          <div
                            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                            style={{ animationDelay: '0ms' }}
                          />
                          <div
                            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                            style={{ animationDelay: '150ms' }}
                          />
                          <div
                            className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                            style={{ animationDelay: '300ms' }}
                          />
                        </div>
                      </div>
                    </motion.div>
                  )}
                  <div ref={chatEndRef} />
                </>
              )}
            </div>

            {/* Chat Input */}
            <div className="p-4 border-t border-gray-200 bg-white">
              <form
                onSubmit={(e) => {
                  e.preventDefault()
                  sendChatMessage(chatInput)
                }}
                className="flex gap-2"
              >
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder="Ask AI to manage tasks..."
                  className="flex-1 px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm transition-all duration-200 placeholder:text-gray-400"
                  disabled={chatLoading}
                />
                <button
                  type="submit"
                  disabled={chatLoading || !chatInput.trim()}
                  className="px-4 py-2.5 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl hover:from-primary-700 hover:to-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow-md flex items-center justify-center"
                  aria-label="Send message"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                    />
                  </svg>
                </button>
              </form>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
