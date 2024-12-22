from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from zoneinfo import ZoneInfo
from Models import Customers
from db import SessionDep,create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)


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

@app.get("/customers",response_model=list[Customers.Customer])
async def get_customers(session: SessionDep):
    customers = session.exec(select(Customers.Customer)).all()
    return customers

@app.get("/customer/{customer_id}",response_model=Customers.Customer)
async def get_customer(customer_id: int, session: SessionDep):
    # costumer = session.exec(select(Customers.Customer).filter(Customers.Customer.id == customer_id)).one()
    costumer = session.get(Customers.Customer, customer_id)
    if costumer:
        return costumer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no esta registrado")

@app.post("/customer",response_model=Customers.Customer)
async def create_customer(customer: Customers.CustomerCreate, session: SessionDep):
    customer = Customers.Customer.model_validate(customer.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.patch("/customer/{customer_id}",response_model=Customers.Customer, status_code=status.HTTP_201_CREATED)
async def update_customer(customerid: int, customer_data: Customers.CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customers.Customer, customerid)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no esta registrado")
    customer = customer_data.model_dump(exclude_unset=True)
    customeractualizado = customer_db.sqlmodel_update(customer)
    session.add(customeractualizado)
    session.commit()
    session.refresh(customeractualizado)
    return customeractualizado

@app.delete("/customer/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customers.Customer, customer_id) 
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no esta registrado")
    session.delete(customer)
    session.commit()
    return {"message": "Cliente eliminado"}

@app.post("/transactions")
async def create_transaction(transaction: Customers.Transaction):
    
    return transaction

@app.post("/invoices")
async def create_invoice(invoice: Customers.Invoice):
    return invoice
