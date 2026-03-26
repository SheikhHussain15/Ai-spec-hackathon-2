/**
 * TaskList Component
 *
 * Displays a list of tasks with staggered entrance animations using Framer Motion.
 * Uses AnimatePresence for smooth exit animations when tasks are removed.
 * Shows EmptyState component when no tasks exist.
 *
 * @feature 007-advanced-ux
 * @user-story US2: Smooth Animations & Micro-Interactions
 * @user-story US4: Enhanced Task Visualization & Interaction
 */

'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Task, TaskCard } from './TaskCard';
import { EmptyState } from './EmptyState';
import { listItemVariants } from '@/lib/animations';

export interface TaskListProps {
  tasks: Task[];
  onToggle: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
  emptyMessage?: string;
  onCreateTask?: () => void;
}

/**
 * TaskList Component with staggered animations
 *
 * Features:
 * - AnimatePresence for exit animations
 * - listItemVariants with stagger delays (50ms per item)
 * - Smooth entrance and exit transitions
 * - EmptyState component for empty state
 */
export function TaskList({
  tasks,
  onToggle,
  onEdit,
  onDelete,
  emptyMessage,
  onCreateTask,
}: TaskListProps) {
  if (tasks.length === 0) {
    // Use EmptyState component if onCreateTask is provided, otherwise show simple message
    if (onCreateTask) {
      return (
        <EmptyState
          onCreateTask={onCreateTask}
          title={emptyMessage}
        />
      );
    }
    
    // Fallback simple empty state
    return (
      <div className="text-center py-16 px-4">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
          >
            <svg
              className="w-8 h-8 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </motion.div>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {emptyMessage}
        </h3>
        <p className="text-gray-500 text-sm">
          Create your first task to get started
        </p>
      </div>
    );
  }

  return (
    <ul className="space-y-3">
      <AnimatePresence mode="popLayout">
        {tasks.map((task, index) => (
          <motion.div
            key={task.id}
            variants={listItemVariants}
            custom={index}
          >
            <TaskCard
              task={task}
              onToggle={onToggle}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </ul>
  );
}

export default TaskList;
