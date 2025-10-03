
# Security and Compliance Guide

This guide provides an overview of security best practices for the Dropshipping Scanner application.

## Securing API Keys and Secrets

**NEVER hardcode secrets in your code.** Use environment variables to manage sensitive information like API keys, database credentials, and secret keys.

- **Local Development**: Use a `.env` file (and add it to `.gitignore`!) to store environment variables. The `python-dotenv` package, included in `uvicorn[standard]`, can load these automatically.
- **Production (Backend)**:
    - **Render/Railway**: Set environment variables in the service configuration dashboard.
    - **Kubernetes**: Use Kubernetes Secrets to store and manage sensitive data. The `kubernetes.yaml` file includes an example of how to mount secrets as environment variables.
- **Production (Frontend)**:
    - **Netlify**: Use the "Environment variables" section in your site settings. For API keys that need to be accessible in the browser, prefix them with `REACT_APP_`.

## Input Validation and Sanitization

- **Backend**: FastAPI automatically validates incoming data against your Pydantic models. This prevents many common injection and data format attacks.
- **Frontend**: Always sanitize user input before displaying it to prevent Cross-Site Scripting (XSS) attacks. React automatically escapes content rendered in JSX, but be cautious when using `dangerouslySetInnerHTML`.

## Rate Limiting

To prevent abuse of your API, implement rate limiting.

- **FastAPI**: Use a library like `slowapi` to add rate limiting to your endpoints. You can limit requests based on IP address or API key.

## Data Privacy (GDPR/CCPA)

- **Be Transparent**: If you store user data, have a clear privacy policy that explains what data you collect and how you use it.
- **Minimize Data Collection**: Only collect the data you absolutely need.
- **Secure Data**: Ensure any stored product or user data is encrypted at rest and in transit.
- **User Rights**: Provide a way for users to request, view, or delete their data.
