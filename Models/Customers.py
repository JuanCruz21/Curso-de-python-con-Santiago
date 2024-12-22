from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel,Field

class CustomerBase(SQLModel):
    name: str = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None,max_length=100)
    phone: str | None = Field(default=None,max_length=20)
    address: str | None = Field(default=None,max_length=100)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
        
class Transaction(BaseModel):
    id: int
    amount: float
    date: str
    description: str | None
    
class Invoice(BaseModel):
    id: int
    total: float
    customer: Customer
    transactions: list[Transaction]
    
    @property
    def total(self):
        return sum([Transaction.amount for Transaction in self.transactions])