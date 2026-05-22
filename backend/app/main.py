from fastapi import FastAPI
from app.database import Base, engine

from app.routes import auth_routes
from app.routes import factory_routes
from app.routes import department_routes
from app.routes import workers
from app.routes import production_line_routes
from app.routes import robotics_routes
from app.routes import maintenance_routes
from app.routes import raw_material_routes
from app.routes import inventory_transaction_routes
from app.routes import vehicle_production_routes
from app.routes import attendance_routes
from app.routes import payroll_routes
from app.routes import factory_expense_routes
from app.routes import quality_check_routes
from app.routes import warehouse_routes
from app.routes import supplier_routes
from app.routes import reports_routes
from app.routes import safety_incident_routes
from app.routes import machinery_routes
from app.routes import iot_monitoring_routes
from app.routes import ai_prediction_routes
from app.models.user import User
from app.models.factory import Factory
from app.models.factory_expense import FactoryExpense
from app.models.department import Department
from app.models.worker import Worker
from app.models.production_line import ProductionLine
from app.models.robotics import Robotics
from app.models.machinery import Machinery
from app.models.maintenance_log import MaintenanceLog
from app.models.raw_material import RawMaterial
from app.models.inventory_transaction import InventoryTransaction
from app.models.vehicle_production import VehicleProduction
from app.models.attendance import Attendance
from app.models.payroll import Payroll
from app.models.quality_check import QualityCheck
from app.models.warehouse import Warehouse
from app.models.safety_incident import SafetyIncident
from app.models.supplier import Supplier


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automobile Factory ERP Backend"
)


app.include_router(auth_routes.router)
app.include_router(factory_routes.router)
app.include_router(department_routes.router)
app.include_router(workers.router)
app.include_router(production_line_routes.router)
app.include_router(robotics_routes.router)
app.include_router(maintenance_routes.router)
app.include_router(raw_material_routes.router)
app.include_router(inventory_transaction_routes.router)
app.include_router(vehicle_production_routes.router)
app.include_router(vehicle_production_routes.production_router)
app.include_router(attendance_routes.router)
app.include_router(payroll_routes.router)
app.include_router(factory_expense_routes.router)
app.include_router(factory_expense_routes.expenses_router)
app.include_router(quality_check_routes.router)
app.include_router(quality_check_routes.quality_alias_router)
app.include_router(warehouse_routes.router)
app.include_router(supplier_routes.router)
app.include_router(reports_routes.router)
app.include_router(reports_routes.analytics_router)
app.include_router(safety_incident_routes.router)
app.include_router(machinery_routes.router)
app.include_router(iot_monitoring_routes.router)
app.include_router(ai_prediction_routes.router)


@app.get("/")
def home():
    return {
        "message": "Backend Running Successfully"
    }
