# Security Guidelines

## General Principles

1.  **Secure by Design:** Security is not an afterthought. It must be a core consideration in all development activities.
2.  **Principle of Least Privilege:** Code and processes should only have the permissions necessary to perform their function.
3.  **Defense in Depth:** Employ multiple layers of security controls.

## Top Priorities

- **Never Hardcode Secrets:** Under no circumstances should API keys, passwords, database credentials, or any other secrets be hardcoded in the source code. Use environment variables or a dedicated secrets management service.
- **Input Validation:** Treat all input from users or external systems as untrusted. Validate, sanitize, and escape all input to prevent injection attacks (e.g., SQLi, XSS).
- **Secure Dependencies:** Regularly check for and update dependencies with known vulnerabilities. Use tools like `npm audit` or `pip-audit`.
- **Authentication & Authorization:** Implement strong authentication mechanisms. Ensure that authorization checks are performed for every request to prevent unauthorized data access.
- **Error Handling:** Log sensitive error details internally, but do not expose them to the user. Generic error messages should be shown to the end-user.
- **HTTPS Only:** Ensure all data in transit is encrypted using TLS.
