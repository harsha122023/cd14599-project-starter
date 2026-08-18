# Udatracker Completed Project

This directory contains the completed code for the Udatracker project. The application consists of a backend API (Flask) managing an in-memory `OrderTracker` built using Test-Driven Development (TDD), and a static frontend.

## Getting Started

Follow these instructions to set up your environment and run the application.

### Prerequisites
- Python 3.x
- `pip`

### Setup and Installation

1. Navigate to the `backend` directory:
   ```bash
   cd starter/backend
   ```
2. Activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Tests
To verify the implementation with the test suite, run from the `starter` directory:
```bash
python -m pytest backend/tests
```

### Running the Application
To start the Flask server, run the following from the `starter` directory:
```bash
python -m backend.app
```
Once the server is running, navigate to `http://127.0.0.1:5000/` in your web browser to view the frontend interface.

## API Endpoints
- **`POST /api/orders`**: Create a new order
- **`GET /api/orders/<order_id>`**: Retrieve a specific order
- **`PUT /api/orders/<order_id>/status`**: Update the status of an existing order
- **`GET /api/orders`**: List all orders (supports `?status=` query parameter)
