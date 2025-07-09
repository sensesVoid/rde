# Tool Usage Guidelines

This document outlines how to define and use tools within the AI system.

## Defining a New Tool

1.  **Function Signature:** Define a clear Python function signature with type hints for all arguments.
2.  **Docstring:** Write a comprehensive docstring explaining:
    -   What the tool does.
    -   What each parameter is for.
    -   What the tool returns.
3.  **Atomicity:** A tool should perform one specific, well-defined action.

## Using Tools

- **Selection:** The AI will select the most appropriate tool based on the user's request and the current context.
- **Parameters:** The AI is responsible for providing the correct parameters to the tool.
- **Execution:** The AI will call the tool and handle its output.
- **Error Handling:** If a tool fails, the AI should analyze the error and attempt to recover or report the failure to the user.
