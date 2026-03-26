/**
 * EmptyState Component
 *
 * Displays a friendly empty state when no tasks exist.
 * Includes an illustration icon, clear messaging, and a prominent call-to-action.
 *
 * Features:
 * - Friendly illustration/icon to soften the empty state
 * - Clear, helpful message explaining the empty state
 * - Prominent "Create First Task" call-to-action button
 * - Smooth entrance animation
 * - Responsive design for all screen sizes
 *
 * @feature 007-advanced-ux
 * @user-story US4: Enhanced Task Visualization & Interaction
 *
 * @example
 * ```tsx
 * <EmptyState
 *   onCreateTask={() => setShowTaskForm(true)}
 * />
 * ```
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, Plus } from 'lucide-react';
import { Button } from '@/components/ui';

export interface EmptyStateProps {
  /** Callback when create task button is clicked */
  onCreateTask: () => void;
  /** Custom title (optional) */
  title?: string;
  /** Custom description (optional) */
  description?: string;
}

/**
 * EmptyState Component
 *
 * A friendly, actionable empty state component that encourages users
 * to create their first task. Uses smooth animations and clear visual
 * hierarchy to provide an inviting experience.
 *
 * Design Principles:
 * - Friendly: Uses warm iconography and encouraging language
 * - Clear: Immediately explains what the empty state means
 * - Actionable: Provides a prominent, obvious next step
 * - Accessible: Proper ARIA labels and keyboard navigation
 */
export function EmptyState({
  onCreateTask,
  title = "No tasks yet",
  description = "Get started by creating your first task. Stay organized and boost your productivity!"
}: EmptyStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="flex flex-col items-center justify-center py-12 sm:py-16 px-4 text-center"
      role="status"
      aria-label="No tasks available"
    >
      {/* Friendly Illustration Icon */}
      <div className="mb-6 sm:mb-8">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{
            delay: 0.1,
            duration: 0.4,
            type: 'spring',
            stiffness: 200,
            damping: 15,
          }}
          className="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center mx-auto"
        >
          <ClipboardList className="w-10 h-10 sm:w-12 sm:h-12 text-primary-600" />
        </motion.div>
      </div>

      {/* Title - Clear and Friendly */}
      <h2 className="text-xl sm:text-2xl font-semibold text-gray-900 mb-2 sm:mb-3">
        {title}
      </h2>

      {/* Description - Helpful Context */}
      <p className="text-sm sm:text-base text-gray-600 max-w-md mb-6 sm:mb-8 leading-relaxed">
        {description}
      </p>

      {/* Call-to-Action Button - Prominent and Actionable */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.3 }}
      >
        <Button
          variant="primary"
          size="lg"
          onClick={onCreateTask}
          icon={<Plus className="w-5 h-5" />}
          className="shadow-md hover:shadow-lg transition-shadow duration-200"
        >
          Create Your First Task
        </Button>
      </motion.div>

      {/* Decorative Elements - Subtle visual interest */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="mt-8 flex gap-2"
        aria-hidden="true"
      >
        <div className="w-2 h-2 rounded-full bg-primary-200" />
        <div className="w-2 h-2 rounded-full bg-primary-300" />
        <div className="w-2 h-2 rounded-full bg-primary-400" />
      </motion.div>
    </motion.div>
  );
}

export default EmptyState;
