from sqlalchemy import Column, Date, Integer, Numeric, String

from app.database import Base


class FactoryExpense(Base):
    __tablename__ = "factory_expenses"

    id = Column(Integer, primary_key=True, index=True)
    expense_type = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(Date, nullable=False)
    remarks = Column(String, nullable=True)
