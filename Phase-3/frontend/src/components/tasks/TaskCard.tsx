/**
 * TaskCard Component
 *
 * Displays an individual task with enhanced visual hierarchy, status indicators,
 * and intuitive action buttons. Uses Framer Motion for smooth animations.
 *
 * Visual Hierarchy:
 * - Title: Prominent (font-semibold, larger size, high contrast)
 * - Description: Secondary (smaller, muted color)
 * - Metadata: Subtle (smallest, gray color)
 *
 * Status Indicators:
 * - Color-coded badges for pending, in-progress, completed
 * - Immediately visible at top of card
 *
 * Action Buttons:
 * - Edit and Delete with clear iconography
 * - Visible on hover/focus with smooth transition
 * - Touch-friendly 44x44px minimum
 *
 * Responsive Design:
 * - Mobile (320-639px): Single column layout, full-width touch-friendly actions
 * - Tablet (768px+): Optimized spacing, multi-column metadata
 * - Desktop (1024px+): Enhanced hover states, larger touch targets
 *
 * Touch Targets: All interactive elements minimum 44x44px
 *
 * @feature 007-advanced-ux
 * @user-story US2: Smooth Animations & Micro-Interactions
 * @user-story US3: Responsive Design
 * @user-story US4: Enhanced Task Visualization & Interaction
 */

'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Edit2, Trash2, Check, Circle } from 'lucide-react';
import { Badge } from '@/components/ui';
import { Checkbox } from '@/components/ui';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

/**
 * TaskCard Component with enhanced visual hierarchy and status indicators
 *
 * Features:
 * - Clear visual hierarchy: Title > Description > Metadata
 * - Color-coded status badges (pending, in-progress, completed)
 * - Action buttons visible on hover/focus
 * - Smooth animations for all interactions
 * - Mobile-first responsive layout
 * - Touch-friendly 44x44px minimum interactive areas
 */
export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  // Determine status badge variant based on completion state
  const statusVariant = task.completed ? 'completed' : 'pending';
  const statusLabel = task.completed ? 'Completed' : 'Pending';

  return (
    <motion.li
      layout
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20, transition: { duration: 0.2 } }}
      whileHover={{ scale: 1.01 }}
      transition={{ duration: 0.2, ease: 'easeOut' }}
      className="group relative rounded-xl border bg-white p-4 sm:p-5 shadow-sm transition-shadow duration-200 hover:shadow-md"
    >
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Checkbox with animation - Touch target min 44x44px */}
        <div className="mt-0.5 flex-shrink-0">
          <div className="min-w-[44px] min-h-[44px] flex items-center justify-center -ml-2">
            <Checkbox
              checked={task.completed}
              onCheckedChange={() => onToggle(task.id)}
            />
          </div>
        </div>

        {/* Content - Enhanced Visual Hierarchy */}
        <div className="flex-1 min-w-0 space-y-2">
          {/* Status Badge - Immediately visible at top */}
          <div className="flex items-center justify-between gap-2 flex-wrap">
            <Badge variant={statusVariant}>
              {task.completed && <Check className="w-3 h-3" />}
              {statusLabel}
            </Badge>

            {/* Action Buttons (visible on hover/focus) - Touch targets min 44x44px */}
            <div className="flex items-center gap-1 opacity-0 transition-opacity duration-200 group-hover:opacity-100 group-focus-within:opacity-100">
              <button
                onClick={() => onEdit(task)}
                className="min-w-[44px] min-h-[44px] flex items-center justify-center p-2 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors duration-150"
                aria-label="Edit task"
                type="button"
              >
                <Edit2 className="w-4 h-4" />
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="min-w-[44px] min-h-[44px] flex items-center justify-center p-2 text-gray-500 hover:text-error-600 hover:bg-error-50 rounded-lg transition-colors duration-150"
                aria-label="Delete task"
                type="button"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Title - PROMINENT (font-semibold, larger size, high contrast) */}
          <h3
            className={`font-semibold text-gray-900 truncate transition-all duration-200 text-base sm:text-lg ${
              task.completed ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>

          {/* Description - SECONDARY (smaller, muted color) */}
          {task.description && (
            <p
              className={`text-sm line-clamp-2 transition-all duration-200 ${
                task.completed ? 'line-through text-gray-400' : 'text-gray-600'
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Metadata - SUBTLE (smallest, gray color) */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="text-xs text-gray-500">
              Updated: {new Date(task.updatedAt).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
    </motion.li>
  );
}

export default TaskCard;
