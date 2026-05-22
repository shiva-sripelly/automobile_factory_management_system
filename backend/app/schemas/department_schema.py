from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    department_name: str
    factory_id: int


class DepartmentUpdate(BaseModel):
    department_name: str | None = None
    factory_id: int | None = None


class DepartmentResponse(BaseModel):
    id: int
    department_name: str
    factory_id: int

    class Config:
        from_attributes = True
