
# Full-Stack Dropshipping Scanner Application

This project is a comprehensive, full-stack dropshipping analysis tool designed for cloud deployment. It uses a Python FastAPI backend, a React/Tailwind CSS frontend, and AI-powered analysis to identify high-margin dropshipping opportunities.

## Project Scope and Features

- **Scrape Product Listings**: Fetches product data from eBay, Amazon, and Facebook Marketplace.
- **AI-Powered Analysis**: Uses AI to analyze products for potential margin, market demand, and seller reliability.
- **Data Visualization**: A modern, responsive UI to visualize product data and AI metrics with charts and tables.
- **DevOps Ready**: Includes Docker containerization, Kubernetes configuration, and CI/CD setup instructions.

## Project Structure

```
/
├── backend/            # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py       # Main API logic
│   │   └── test_main.py  # Backend unit tests
│   ├── mcp_worker/       # AI analysis worker
│   │   └── worker.py
│   └── requirements.txt
├── frontend/           # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   └── ProductSearch.js # Main React component
│   │   ├── App.js
│   │   ├── index.css     # Tailwind CSS directives
│   │   └── index.js
│   ├── netlify.toml      # Netlify deployment config
│   ├── package.json
│   └── tailwind.config.js
├── docs/               # Documentation
│   ├── collaboration.md
│   ├── monitoring.md
│   ├── scalability.md
│   └── security.md
├── Dockerfile          # Docker configuration for the backend
├── kubernetes.yaml     # Kubernetes example configuration
└── README.md           # This file
```

## Setup and Running the Project

### Backend

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the development server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be available at `http://localhost:8000`.

### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm start
    ```
    The frontend will be available at `http://localhost:3000`.

## Deployment

### Backend (Render/Railway/Cloud Run)

1.  **Containerize your application:**
    Build the Docker image:
    ```bash
    docker build -t dropshipping-backend .
    ```
2.  **Push to a registry:**
    Push the image to Docker Hub, Google Container Registry (GCR), or another registry.
    ```bash
    docker push your-registry/dropshipping-backend:latest
    ```
3.  **Deploy on your chosen platform:**
    - **Render/Railway**: Connect your Git repository and point it to your `Dockerfile`.
    - **Cloud Run**: Deploy the container image from GCR.

### Frontend (Netlify)

1.  **Push your code to a GitHub repository.**
2.  **Create a new site on Netlify and connect it to your repository.**
3.  **Configure build settings:**
    - **Build command**: `npm run build`
    - **Publish directory**: `build`
4.  **API Redirects**: The `netlify.toml` file is already configured to proxy requests from `/api/*` to your backend. **Remember to update the `to` field in `netlify.toml` to your live backend URL.**

## Project Transfer Instructions

To transfer this project, you can use the following method to encode and decode the project files.

### Encoding

1.  **Create a zip archive of the project:**
    ```bash
    zip -r dropshipping_app.zip backend frontend docs Dockerfile kubernetes.yaml README.md
    ```
2.  **Encode the zip file in Base64:**
    ```bash
    import base64

    with open('dropshipping_app.zip', 'rb') as f:
        encoded_zip = base64.b64encode(f.read()).decode('utf-8')

    with open('dropshipping_base64.txt', 'w') as f:
        f.write(encoded_zip)
    ```

### Decoding

1.  **Save the Base64 content into a file named `dropshipping_base64.txt`.**
2.  **Run the following Python script to decode it:**
    ```python
    import base64

    with open('dropshipping_base64.txt', 'r') as f:
        encoded_zip = f.read()

    decoded_zip = base64.b64decode(encoded_zip)

    with open('decoded_app.zip', 'wb') as f:
        f.write(decoded_zip)

    print("Successfully decoded to decoded_app.zip")
    ```
3.  **Unzip the file:**
    ```bash
    unzip decoded_app.zip
    ```
