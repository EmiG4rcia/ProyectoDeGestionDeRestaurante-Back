from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

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
from core.database import Base, engine
from core.database import SessionLocal


def initialize_database():
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed menu items if empty
        if db.query(MenuItem).count() == 0:
            items = [
                MenuItem(
                    category="Hamburguesas",
                    name="Smash Clásica",
                    description="Medallón de carne aplastado, queso cheddar, pepinillos y salsa especial",
                    price=1200.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Hamburguesas",
                    name="Smash Doble",
                    description="Doble medallón de carne, doble cheddar, cebolla caramelizada y lechuga",
                    price=1600.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Hamburguesas",
                    name="Smash Crispy",
                    description="Medallón de pollo crocante, mayonesa de ajo y repollo morado",
                    price=1400.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Sandwiches",
                    name="Club Sandwich",
                    description="Pollo a la plancha, panceta, tomate, lechuga y mayonesa en pan de molde",
                    price=1100.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Sandwiches",
                    name="Veggie Sandwich",
                    description="Vegetales grillados, hummus, rúcula y queso brie",
                    price=1000.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Pizzas",
                    name="Pizza Margherita",
                    description="Salsa de tomate, mozzarella fresca y albahaca",
                    price=1500.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Pizzas",
                    name="Pizza Pepperoni",
                    description="Salsa de tomate, mozzarella y pepperoni importado",
                    price=1700.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Papas Fritas",
                    name="Papas Simples",
                    description="Papas fritas crocantes con sal y especias",
                    price=500.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Papas Fritas",
                    name="Papas con Cheddar",
                    description="Papas fritas bañadas en salsa cheddar casera",
                    price=700.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Bebidas",
                    name="Coca Cola",
                    description="Lata 354ml",
                    price=400.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Bebidas",
                    name="Agua Mineral",
                    description="Botella 500ml con o sin gas",
                    price=300.00,
                    is_available=True,
                ),
                MenuItem(
                    category="Bebidas",
                    name="Limonada Casera",
                    description="Limonada fresca con menta y jengibre",
                    price=600.00,
                    is_available=True,
                ),
            ]
            db.add_all(items)
            db.commit()
            print("Menu items seeded.")

        # Seed tables (mesas) if empty
        if db.query(Table).count() == 0:
            tables = [
                Table(
                    table_number="1", qr_token="table_1_a1b2c3d4", status="available"
                ),
                Table(
                    table_number="2", qr_token="table_2_e5f6g7h8", status="available"
                ),
                Table(
                    table_number="3", qr_token="table_3_i9j0k1l2", status="available"
                ),
            ]
            db.add_all(tables)
            db.commit()
            print("Tables seeded.")

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Jills Sandwich Admin API",
    description="API para el panel de administracion",
    version="1.0.0",
    lifespan=lifespan,
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
