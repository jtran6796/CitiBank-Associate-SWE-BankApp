from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Literal
from routers import customers, accounts

app = FastAPI(root_path="/api")

customers = []

class Account(BaseModel):
  Id: int
  account_number: int
  account_type: Literal["checking", "savings"]
  balance: float = None
  
class AccountCreate(BaseModel):
  account_type: Literal["checking", "savings"]
  balance: float = None
  
class AccountResponse(BaseModel):
  pass
  
class Customer(BaseModel):
  Id: int
  name: str
  email: EmailStr
  accounts: list[Account] = []

class CustomerCreate(BaseModel):
  name: str
  email: EmailStr
  accounts: list[Account] = []

class CustomerResponse(BaseModel):
  pass
  
customers.append(Customer(Id = 0, name = "John Doe", email = "john@example.com", accounts = []))

@app.get("/customers", tags=["Customers"], response_model = list[Customer])
def get_all_customers():
  if len(customers) == 0:
    raise HTTPException(status_code=404, detail="There are 0 customers.")
  return customers

@app.get("/customers/premium", tags=["Customers"], response_model = list[Customer])
def get_all_premium_customers():
  premium = []
  total_balance = 0
  for customer in customers:
    for account in customer.accounts:
      total_balance += account.balance
    if total_balance >= 1000:
      premium.append(customer)
    total_balance = 0
  if len(premium) == 0:
    raise HTTPException()
  return premium

@app.get("/customers/{id}", tags=["Customers"], response_model = Customer)
def get_customer_by_id(id: int):
  for customer in customers:
    if customer.Id == id:
      return customer
  raise HTTPException(status_code=404, detail="ID does not exist.")

@app.get("/customers/search", tags=["Customers"], response_model = Customer)
def get_customer_name(name: str):
  for customer in customers:
    if customer.name == name.lower():
      return customer
  raise HTTPException(status_code="404", detail="No customer found with that name.")

@app.post("/customers", tags=["Customers"], response_model = Customer)
def create_customer(new_customer: CustomerCreate):
  new_id = len(customers)
  customer = Customer(Id = new_id, **new_customer.model_dump())
  customers.append(customer)
  return customer

@app.put("/customers/{id}", tags=["Customers"], response_model = Customer)
def update_customer(id: int, customer: Customer):
  for i, c in enumerate(customers):
    if c.Id == id:
      customers[i] = customer
      return customers[i]
  raise HTTPException()

@app.delete("/customers/{id}", tags=["Customers"])
def delete_customer(id: int):
  for i, customer in enumerate(customers):
    if customer.Id == id:
      customers.pop(i)
      return{"detail": "Customer successfully deleted"}
  raise HTTPException()
    

@app.get("/accounts", tags=["Accounts"], response_model=list[Account])
def get_all_accounts():
  list_accounts = []
  for customer in customers:
    for account in customer.accounts:
      list_accounts.append(account)
  if len(list_accounts) == 0:
    raise HTTPException()
  return list_accounts

@app.get("/accounts/{id}", tags=["Accounts"], response_model=Account)
def get_account_by_id(id: int):
  for customer in customers:
    if customer.Id == id:
      return customer.accounts
  raise HTTPException()
  

@app.get("/accounts/search", tags=["Accounts"], response_model=Account)
def get_account_by_name(name: str):
  for customer in customers:
    if customer.name == name:
      return customer.accounts
  raise HTTPException()

@app.post("/accounts", tags=["Accounts"], response_model=list[Account])
def create_account(id: int, new_account: AccountCreate):
  for customer in customers:
    if customer.Id == id:
      new_account_number = len(customer.accounts)
      account = Account(Id = id, account_number = new_account_number, **new_account.model_dump())
      customer.accounts.append(account)
      return customer.accounts

@app.put("/accounts/{id}", tags=["Accounts"])
def update_account(id: int, new_account = Account):
  for customer in customers:
    if customer.Id == id:
      for i, account in enumerate(customer.accounts):
        if account.account_number == new_account.account_number:
          customer.accounts[i] = new_account
          return customer.accounts[i]
      raise HTTPException()
  raise HTTPException()
        
@app.delete("/accounts/{id}", tags=["Accounts"])
def delete_account(id: int, account_number: int):
  for customer in customers:
    if customer.Id == id:
      for i,account in enumerate(customer.accounts):
        if account.account_number == account_number:
          customer.accounts.pop(i)
          return{"detail": "Account successfully deleted"}
      raise HTTPException()
  raise HTTPException()
  