# Data Model

This document defines the data entities for the In-memory Todo Console Application.

## Task Entity

Represents a single to-do item.

### Fields

| Field         | Type    | Description                              | Validation Rules      |
|---------------|---------|------------------------------------------|-----------------------|
| `id`          | Integer | A unique identifier for the task.        | Auto-incrementing, unique. |
| `description` | String  | The text content of the task.            | Required, non-empty.   |
| `completed`   | Boolean | The completion status of the task.       | Defaults to `False`.   |

### State Transitions

- A `Task` is created with `completed` as `False`.
- The `completed` status can be toggled between `False` and `True`.
