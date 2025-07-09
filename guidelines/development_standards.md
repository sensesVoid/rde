# Development Standards

## Code Quality

- **Style:** Mimic the style (formatting, naming conventions, etc.) of existing code in the project. If no style exists, default to industry best practices for the language (e.g., PEP 8 for Python, Prettier for JavaScript).
- **Comments:** Add comments only to explain the *why* of complex logic, not the *what*. Keep comments concise.
- **Typing:** Use static typing where available (e.g., TypeScript, Python type hints) to improve code clarity and robustness.

## Testing

- **Unit Tests:** All new functions, methods, or classes should have corresponding unit tests.
- **Test Coverage:** Aim for high test coverage for business-critical logic.
- **Existing Tests:** Ensure all existing tests continue to pass after any changes.
- **Frameworks:** Use the testing framework already established in the project.

## Commits

- **Atomic Commits:** Each commit should represent a single logical change.
- **Commit Messages:** Follow the Conventional Commits specification (e.g., `feat: add user login endpoint`).

## Deployment

- **Environment Variables:** Never hardcode secrets or environment-specific configurations. Use environment variables (`.env` files for local development).
- **Build Process:** Use or create a reliable build script for creating production artifacts.
- **CI/CD:** All changes should be verifiable through an automated CI/CD pipeline if one is present.
