from pydantic import BaseModel
from typing import Optional


class RoboticsBase(BaseModel):
    robot_code: str
    robot_name: str
    automation_type: str
    department_id: int
    maintenance_cycle_days: int
    current_status: str = "active"


class RoboticsCreate(RoboticsBase):
    pass


class RoboticsUpdate(BaseModel):
    robot_name: Optional[str] = None
    automation_type: Optional[str] = None
    department_id: Optional[int] = None
    maintenance_cycle_days: Optional[int] = None
    current_status: Optional[str] = None


class RoboticsResponse(RoboticsBase):
    id: int

    class Config:
        from_attributes = True