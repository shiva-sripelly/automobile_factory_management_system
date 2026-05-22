from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance
from app.models.factory_expense import FactoryExpense
from app.models.inventory_transaction import InventoryTransaction
from app.models.machinery import Machinery
from app.models.maintenance_log import MaintenanceLog
from app.models.payroll import Payroll
from app.models.quality_check import QualityCheck
from app.models.raw_material import RawMaterial
from app.models.safety_incident import SafetyIncident
from app.models.supplier import Supplier
from app.models.vehicle_production import VehicleProduction
from app.models.warehouse import Warehouse
from app.models.worker import Worker


router = APIRouter(
    prefix="/reports",
    tags=["Reports & Analytics Dashboard"]
)

analytics_router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def _sum_or_zero(db: Session, column):
    return db.query(func.coalesce(func.sum(column), 0)).scalar()


@router.get("/dashboard")
def get_dashboard_report(db: Session = Depends(get_db)):
    total_production_cost = _sum_or_zero(
        db,
        VehicleProduction.production_cost
    )
    total_payroll = _sum_or_zero(db, Payroll.final_salary)
    total_factory_expenses = _sum_or_zero(db, FactoryExpense.amount)
    total_maintenance_cost = _sum_or_zero(
        db,
        MaintenanceLog.maintenance_cost
    )
    total_inventory_value = _sum_or_zero(
        db,
        RawMaterial.stock_quantity * RawMaterial.unit_price
    )

    return {
        "workers": {
            "total": db.query(Worker).count(),
            "active": db.query(Worker).filter(
                Worker.status == "active"
            ).count()
        },
        "production": {
            "total_records": db.query(VehicleProduction).count(),
            "completed": db.query(VehicleProduction).filter(
                VehicleProduction.completion_status == "completed"
            ).count(),
            "pending": db.query(VehicleProduction).filter(
                VehicleProduction.completion_status == "pending"
            ).count(),
            "total_cost": total_production_cost
        },
        "quality": {
            "total_checks": db.query(QualityCheck).count(),
            "passed": db.query(QualityCheck).filter(
                QualityCheck.quality_status == "passed"
            ).count(),
            "failed": db.query(QualityCheck).filter(
                QualityCheck.quality_status == "failed"
            ).count()
        },
        "finance": {
            "total_payroll": total_payroll,
            "total_factory_expenses": total_factory_expenses,
            "total_maintenance_cost": total_maintenance_cost,
            "total_expenses": (
                total_payroll
                + total_factory_expenses
                + total_maintenance_cost
            )
        },
        "inventory": {
            "total_materials": db.query(RawMaterial).count(),
            "total_stock_quantity": _sum_or_zero(
                db,
                RawMaterial.stock_quantity
            ),
            "total_inventory_value": total_inventory_value,
            "total_transactions": db.query(InventoryTransaction).count()
        },
        "warehouse": {
            "total_warehouses": db.query(Warehouse).count(),
            "total_capacity": _sum_or_zero(db, Warehouse.capacity)
        },
        "suppliers": {
            "total_suppliers": db.query(Supplier).count()
        },
        "attendance": {
            "total_records": db.query(Attendance).count(),
            "total_overtime_hours": _sum_or_zero(
                db,
                Attendance.overtime_hours
            )
        },
        "safety": {
            "total_incidents": db.query(SafetyIncident).count()
        }
    }


@router.get("/finance")
def get_finance_report(db: Session = Depends(get_db)):
    payroll_total = _sum_or_zero(db, Payroll.final_salary)
    factory_expense_total = _sum_or_zero(db, FactoryExpense.amount)
    maintenance_total = _sum_or_zero(db, MaintenanceLog.maintenance_cost)

    return {
        "payroll_total": payroll_total,
        "factory_expense_total": factory_expense_total,
        "maintenance_total": maintenance_total,
        "grand_total": payroll_total + factory_expense_total + maintenance_total
    }


@router.get("/production")
def get_production_report(db: Session = Depends(get_db)):
    return {
        "total_records": db.query(VehicleProduction).count(),
        "completed": db.query(VehicleProduction).filter(
            VehicleProduction.completion_status == "completed"
        ).count(),
        "pending": db.query(VehicleProduction).filter(
            VehicleProduction.completion_status == "pending"
        ).count(),
        "total_cost": _sum_or_zero(db, VehicleProduction.production_cost)
    }


@router.get("/quality")
def get_quality_report(db: Session = Depends(get_db)):
    return {
        "total_checks": db.query(QualityCheck).count(),
        "passed": db.query(QualityCheck).filter(
            QualityCheck.quality_status == "passed"
        ).count(),
        "failed": db.query(QualityCheck).filter(
            QualityCheck.quality_status == "failed"
        ).count()
    }


@router.get("/inventory")
def get_inventory_report(db: Session = Depends(get_db)):
    return {
        "total_materials": db.query(RawMaterial).count(),
        "total_stock_quantity": _sum_or_zero(db, RawMaterial.stock_quantity),
        "total_inventory_value": _sum_or_zero(
            db,
            RawMaterial.stock_quantity * RawMaterial.unit_price
        ),
        "total_transactions": db.query(InventoryTransaction).count()
    }


@analytics_router.get("/production")
def get_production_analytics(db: Session = Depends(get_db)):
    return get_production_report(db)


@analytics_router.get("/cost")
def get_cost_analytics(db: Session = Depends(get_db)):
    return get_finance_report(db)


@analytics_router.get("/machine-performance")
def get_machine_performance_analytics(db: Session = Depends(get_db)):
    return {
        "total_machines": db.query(Machinery).count(),
        "active_machines": db.query(Machinery).filter(
            Machinery.machine_status == "active"
        ).count(),
        "inactive_machines": db.query(Machinery).filter(
            Machinery.machine_status != "active"
        ).count(),
        "total_running_hours": _sum_or_zero(db, Machinery.running_hours),
        "maintenance_logs": db.query(MaintenanceLog).filter(
            MaintenanceLog.machine_id.isnot(None)
        ).count()
    }
