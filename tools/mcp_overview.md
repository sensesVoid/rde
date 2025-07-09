# Model Control Programs (MCPs)

## Overview

A Model Control Program (MCP) is a higher-level script or process that orchestrates the AI model's behavior to accomplish complex tasks within the Reflexive Development Engine. It acts as a "main loop" or a state machine, guiding the AI through a series of steps.

## Key Responsibilities of an MCP

1.  **State Management:** Keep track of the current state of the task (e.g., `ANALYZING`, `CODING`, `TESTING`).
2.  **Context Priming:** Load the necessary context (from the `persistency` and `guidelines` directories) into the AI's prompt at each step.
3.  **Tool Orchestration:** Call the appropriate tools based on the current state and the AI's output.
4.  **Looping and Chaining:** Chain multiple AI calls together. For example, the output of one AI generation (e.g., a plan) can be used as the input for the next (e.g., executing the plan).
5.  **Verification:** After the AI completes a step, the MCP can run verification checks (e.g., run a linter, execute tests) to ensure the quality of the output.

## Example MCP Flow

**Goal:** Add a new feature based on a PRD.

1.  **State: `PLANNING`**
    -   **MCP Action:** Load `prd.md`, `guidelines/*.md`.
    -   **Prompt:** "Analyze the PRD and create a step-by-step implementation plan."
    -   **AI Output:** A plan.
2.  **State: `CODING`**
    -   **MCP Action:** Load the plan, relevant source code files.
    -   **Prompt:** "Execute step 1 of the plan: [details of step 1]."
    -   **AI Output:** Source code.
3.  **State: `TESTING`**
    -   **MCP Action:** Save the code, run the project's test suite.
    -   **Prompt:** "The tests passed/failed with this output: [test output]. If failed, please fix the code."
    -   **AI Output:** Fixed code or a confirmation that tests passed.
4.  **Loop:** Continue for all steps in the plan.
