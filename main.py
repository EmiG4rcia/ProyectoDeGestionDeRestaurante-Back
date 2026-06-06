from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from features.auth.router import router as auth_router
from features.orders.router import router as orders_router
from features.customers.router import router as customers_router
from features.menu.router import router as menu_router
from features.tables.router import router as tables_router
from features.sales.router import router as sales_router

from features.auth.models import AdminUser
from features.customers.models import Customer
from features.orders.models import Order, OrderItem
from features.menu.models import MenuItem
from features.tables.models import Table
from features.sales.models import Payment

app = FastAPI(
    title="Jills Sandwich Admin API",
    description="API para el panel de administracion",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(menu_router, prefix="/menu-items", tags=["Menu"])
app.include_router(tables_router, prefix="/tables", tags=["Tables"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Admin API running"}