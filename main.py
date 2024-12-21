from fastapi import FastAPI
from datetime import datetime
from zoneinfo import ZoneInfo
from Models import Customers
from db import SessionDep,create_all_tables

app = FastAPI()

create_all_tables(app)

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/getTime/{country_code}")
def read_root(countrycode:str):
    countrycode = countrycode.upper()   
    czs=country_timezones.get(countrycode)
    tz = ZoneInfo(czs)
    return {"time": datetime.now(tz).isoformat(), "country": countrycode}

db_customers: list[Customers.Customer] = []

@app.get("/customers",response_model=list[Customers.Customer])
async def get_customers():
    return db_customers

@app.get("/customer/{customer_id}",response_model=Customers.Customer)
async def get_customer(customer_id: int):
    for customer in db_customers:
        if customer.id == customer_id:
            return customer
    return {"error": "Customer not found"}

@app.post("/customer",response_model=Customers.Customer)
async def create_customer(customer: Customers.CustomerCreate, session: SessionDep):
    customer = Customers.Customer.model_validate(customer.model_dump())
    customer.id = len(db_customers) + 1
    db_customers.append(customer)
    return customer

@app.post("/transactions")
async def create_transaction(transaction: Customers.Transaction):
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Customers.Invoice):
    return invoice
