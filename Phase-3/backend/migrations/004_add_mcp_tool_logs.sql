-- Migration 004: Add MCP Tool Execution Logs (Optional Audit Table)
-- Purpose: Track all MCP tool invocations for audit and debugging
-- Created: 2026-02-18
-- Feature: 004-mcp-server

-- Create tool_execution_logs table
CREATE TABLE IF NOT EXISTS tool_execution_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    invocation_inputs JSONB NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    error_code TEXT,
    execution_time_ms INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for user-scoped queries (fast lookups by user_id)
CREATE INDEX IF NOT EXISTS idx_tool_logs_user_id ON tool_execution_logs(user_id);

-- Create index for tool name filtering (analytics by tool type)
CREATE INDEX IF NOT EXISTS idx_tool_logs_tool_name ON tool_execution_logs(tool_name);

-- Create index for created_at (time-based queries)
CREATE INDEX IF NOT EXISTS idx_tool_logs_created_at ON tool_execution_logs(created_at);

-- Create composite index for user + tool queries
CREATE INDEX IF NOT EXISTS idx_tool_logs_user_tool ON tool_execution_logs(user_id, tool_name);

-- Comment on table
COMMENT ON TABLE tool_execution_logs IS 'Audit log for MCP tool invocations (development/debugging only)';

-- Comment on columns
COMMENT ON COLUMN tool_execution_logs.user_id IS 'Authenticated user ID who invoked the tool';
COMMENT ON COLUMN tool_execution_logs.tool_name IS 'Name of the MCP tool invoked';
COMMENT ON COLUMN tool_execution_logs.invocation_inputs IS 'Input parameters (sanitized, no sensitive data)';
COMMENT ON COLUMN tool_execution_logs.success IS 'Whether the tool execution succeeded';
COMMENT ON COLUMN tool_execution_logs.error_message IS 'Error message if execution failed';
COMMENT ON COLUMN tool_execution_logs.error_code IS 'Error code (VALIDATION_ERROR, OWNERSHIP_VIOLATION, etc.)';
COMMENT ON COLUMN tool_execution_logs.execution_time_ms IS 'Tool execution time in milliseconds';

-- Rollback script (for development only)
-- DROP TABLE IF EXISTS tool_execution_logs CASCADE;
