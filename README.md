# 💰 Advanced Salary & Loan Calculator

This project is a multi-container FinTech application designed to provide comprehensive salary advance eligibility checks and detailed loan repayment calculations, including amortization schedules. It's built with a modern microservice architecture, leveraging popular Python frameworks and containerization technologies for scalability, maintainability, and ease of deployment.

## ✨ Features

- **Salary Advance Calculation:**
  - Determines eligibility based on gross monthly salary and a defined policy (e.g., percentage of salary).
  - Calculates approved advance amount and associated fees (flat and percentage-based).
- **Loan Repayment Calculation:**
  - Computes total repayable amount, total interest accrued, and estimated monthly payments.
  - Generates a detailed, month-by-month amortization schedule using Pandas for accurate financial tracking.
- **User-Friendly Interface:** Intuitive web UI built with Streamlit for easy input and result display.
- **Robust Backend API:** High-performance API built with FastAPI, handling all complex business logic and data processing.
- **Containerized Environment:** Both frontend and backend are Dockerized for consistent development and deployment across different environments.
- **Orchestration with Docker Compose:** Seamless multi-container setup, allowing services to communicate reliably.

## 🚀 Technologies Used

- **Frontend:**
  - [Streamlit](https://streamlit.io/) - For rapid UI development.
  - [Requests](https://requests.readthedocs.io/) - For making HTTP requests to the backend API.
- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for building APIs.
  - [Pydantic](https://pydantic.dev/) - For data validation and settings management.
  - [Pandas](https://pandas.pydata.org/) - For powerful data manipulation, especially for financial calculations and amortization.
- **Containerization:**
  - [Docker](https://www.docker.com/) - For packaging applications into isolated containers.
  - [Docker Compose](https://docs.docker.com/compose/) - For defining and running multi-container Docker applications.

## 📦 Project Structure

.

```
├── docker-compose.yml           # Defines the multi-service application
├── frontend/                    # Streamlit app (frontend)
│   ├── app.py                   # Streamlit UI and API integration
│   ├── Dockerfile               # Dockerfile for Streamlit service
│   └── requirements.txt         # Python dependencies for frontend
├── backend/                     # FastAPI app (backend)
│   ├── app/
│   │   ├── main.py              # FastAPI main application and endpoints
│   │   └── models.py            # Pydantic models for request/response validation
│   ├── Dockerfile               # Dockerfile for FastAPI service
│   └── requirements.txt         # Python dependencies for backend
└── README.md                    # Project documentation
```

## ⚙️ How to Run Locally

To run this application on your local machine, ensure you have Docker and Docker Compose installed.

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/your-username/fintech-calculator.git](https://github.com/your-username/fintech-calculator.git)
    cd fintech-calculator
    ```

2.  **Build and Run with Docker Compose:**
    This command will build the Docker images for both the frontend and backend services, set up internal networking, and start the containers. The `--build` flag ensures that the images are rebuilt if there are any changes to your code or `Dockerfile`s. The `-d` flag runs the containers in detached mode (in the background).

    ```bash
    docker compose up --build -d
    ```

3.  **Access the Application:**
    Once the containers are up and running (this might take a minute or two as Docker downloads base images and installs dependencies), open your web browser and navigate to:

    ```
    http://localhost:8501
    ```

4.  **Stop the Application:**
    To stop and remove the running containers, navigate to the project's root directory in your terminal and run:
    ```bash
    docker compose down
    ```

## 🌐 API Documentation (Backend)

The FastAPI backend automatically generates interactive API documentation. Once the application is running locally (or deployed), you can access it at:

http://localhost:8000/docs # Swagger UI
http://localhost:8000/redoc # ReDoc

You can use these interfaces to test the `/calculate_advance` and `/calculate_loan` endpoints directly.

## 🚀 Deployment

This multi-container applicatio deployed to a VPS(Digital Ocean).

**Deployment URL:**
`http://138.68.180.236:8501`

**Basic VPS Deployment Steps:**

1.  **Provisioned a Linux VPS:** (Ubuntu 22.04 LTS).
2.  **SSH into Server:**
3.  **Installed Docker & Docker Compose:**
4.  **Transferred Project Files:**
5.  **Navigated to the working directory & Run:**
6.  **Configured Firewall:**

## ⚠️ Assumptions and Limitations

- **Single-User / No Authentication:** This application is designed for single-user calculations and does not include user authentication or data persistence (e.g., saving past calculations to a database).
- **Simplified Financial Policies:** The salary advance eligibility and loan interest calculations are based on simplified, configurable policies within the backend logic. Real-world financial applications would involve more complex algorithms, credit checks, and regulatory compliance.
- **No HTTPS in Basic Deployment:** The provided local and basic VPS deployment runs over HTTP. For production environments, HTTPS should be implemented using a reverse proxy (e.g., Nginx, Caddy) with SSL certificates (e.g., Let's Encrypt).
- **No Advanced Error Handling:** While basic error handling is present, production-grade applications would include more robust logging, monitoring, and specific error responses.
- **No Asynchronous Database Operations:** Currently, no database is integrated. Future enhancements could include Firestore, PostgreSQL, etc., for user data or calculation history.

## 💡 Future Enhancements

- **Database Integration:** Implement a database (e.g., PostgreSQL, MongoDB, Firestore) to store user profiles, calculation history, or custom financial policies.
- **User Authentication & Authorization:** Add a login system (e.g., OAuth, JWT) to personalize the experience and secure endpoints.
- **Advanced Financial Models:** Incorporate more sophisticated loan types, credit scoring, or risk assessment.
- **Analytics & Reporting:** Integrate tools for visualizing financial trends or user behavior.
- **CI/CD Pipeline:** Automate testing, building, and deployment processes.
- **HTTPS & Custom Domain:** Secure the application with SSL and link it to a custom domain.
- **More Responsive UI:** Further enhance the Streamlit UI for better responsiveness on various devices.

## 🤝 Contribution

Feel free to fork this repository, submit pull requests, or open issues if you have suggestions or find bugs.
