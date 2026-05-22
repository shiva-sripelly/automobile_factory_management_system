# Automobile Factory Management System

This project is a backend ERP system for managing an automobile factory. It is built with FastAPI, SQLAlchemy, and a relational database. The system covers factory administration, workers, production, machinery, robotics, maintenance, inventory, payroll, quality control, expenses, warehouses, suppliers, safety incidents, reports, and analytics.

## Core Modules

- Authentication and Role Management
- Factory and Department Management
- Employee and Worker Management
- Production Line Management
- Robotics and Machinery Management
- Maintenance Management
- Inventory and Raw Material Management
- Vehicle Production Tracking
- Shift and Attendance Management
- Payroll and Salary Management
- Cost and Expense Tracking
- Quality Control System
- Warehouse Management
- Supplier and Purchase Management
- Reports and Analytics Dashboard
- Safety Incident Management
- IoT/Factory Monitoring Support
- AI Production Prediction

## Main Database Tables

The backend includes models for these main tables:

- 'users'
- 'factories'
- 'departments'
- 'workers'
- 'attendance'
- 'machinery'
- 'robotics'
- 'maintenance_logs'
- 'raw_materials'
- 'suppliers'
- 'production_lines'
- 'vehicle_production'
- 'quality_checks'
- 'warehouse'
- 'inventory_transactions'
- 'payroll'
- 'factory_expenses'
- 'safety_incidents'

## Important API Endpoints

### Authentication

- 'POST /auth/register'
- 'POST /auth/login'
- 'GET /auth/me'

### Workers

- 'POST /workers'
- 'GET /workers'
- 'GET /workers/{worker_id}'
- 'PUT /workers/{worker_id}'
- 'DELETE /workers/{worker_id}'

### Machinery and Robotics

- 'POST /machinery'
- 'GET /machinery'
- 'GET /machinery/{machine_id}'
- 'PUT /machinery/{machine_id}'
- 'DELETE /machinery/{machine_id}'
- 'POST /robotics'
- 'GET /robotics'
- 'GET /robotics/{robot_id}'
- 'PUT /robotics/{robot_id}'
- 'DELETE /robotics/{robot_id}'

### Maintenance

- 'POST /maintenance'
- 'GET /maintenance'
- 'GET /maintenance/cost-report'

### Production and Quality

- 'POST /production'
- 'GET /production'
- 'GET /production/live-status'
- 'POST /quality-check'
- 'GET /quality-report'

### Payroll and Expenses

- 'POST /payroll/generate'
- 'GET /payroll'
- 'POST /expenses'
- 'GET /expenses'

### Analytics and Monitoring

- 'GET /analytics/production'
- 'GET /analytics/cost'
- 'GET /analytics/machine-performance'
- 'GET /reports/dashboard'
- 'GET /iot-monitoring/factory-status'
- 'GET /ai-production-prediction/next-day'

## Backend Setup

1. Go to the backend folder:

   '''powershell
   cd backend
   '''

2. Create and activate a virtual environment:

   '''powershell
   python -m venv venv
   .\venv\Scripts\activate
   '''

3. Install dependencies:

   '''powershell
   pip install -r requirements.txt
   '''

4. Configure environment variables in 'backend/.env'.

5. Run the backend server:

   '''powershell
   uvicorn app.main:app --reload
   '''

6. Open the API documentation:

   '''
   http://127.0.0.1:8000/docs
   '''

## Project Structure

'''
backend/
  app/
    dependencies/   Authentication and role dependencies
    models/         SQLAlchemy database models
    routes/         FastAPI route modules
    schemas/        Pydantic request and response schemas
    services/       Business logic helpers
    utils/          Password hashing and JWT helpers
    main.py         FastAPI application entry point
'''

## Notes

- SQLAlchemy models are registered in 'app/main.py' before 'Base.metadata.create_all(bind=engine)' runs.
- API routes are organized by module, such as workers, machinery, payroll, expenses, production, quality, and reports.
- Some reporting, monitoring, and AI prediction endpoints are analytics endpoints and do not require separate database tables.
