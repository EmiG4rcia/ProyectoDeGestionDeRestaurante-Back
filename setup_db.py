import pymysql
from sqlalchemy import text
from core.database import engine, Base
from core.config import settings

# ─── Step 1: Create database if it doesn't exist ───────────
def create_database():
    # Parse connection without DB name
    url = settings.DATABASE_URL
    base_url = url.rsplit('/', 1)[0]
    db_name = url.rsplit('/', 1)[1]

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Database '{db_name}' ready.")

# ─── Step 2: Create all tables ─────────────────────────────
def create_tables():
    # Import all models so SQLAlchemy registers them
    from features.auth.models import AdminUser
    from features.customers.models import Customer
    from features.orders.models import Order, OrderItem
    from features.menu.models import MenuItem
    from features.tables.models import Table
    from features.sales.models import Payment
    import features.sessions.models  # if exists

    Base.metadata.create_all(bind=engine)
    print("All tables created.")

# ─── Step 3: Seed menu items ───────────────────────────────
def seed_menu(db):
    from features.menu.models import MenuItem

    existing = db.query(MenuItem).count()
    if existing > 0:
        print("Menu items already seeded — skipping.")
        return

    items = [
        MenuItem(category="Hamburguesas", name="Smash Clásica", description="Medallón de carne aplastado, queso cheddar, pepinillos y salsa especial", price=1200.00, is_available=True),
        MenuItem(category="Hamburguesas", name="Smash Doble", description="Doble medallón de carne, doble cheddar, cebolla caramelizada y lechuga", price=1600.00, is_available=True),
        MenuItem(category="Hamburguesas", name="Smash Crispy", description="Medallón de pollo crocante, mayonesa de ajo y repollo morado", price=1400.00, is_available=True),
        MenuItem(category="Sandwiches", name="Club Sandwich", description="Pollo a la plancha, panceta, tomate, lechuga y mayonesa en pan de molde", price=1100.00, is_available=True),
        MenuItem(category="Sandwiches", name="Veggie Sandwich", description="Vegetales grillados, hummus, rúcula y queso brie", price=1000.00, is_available=True),
        MenuItem(category="Pizzas", name="Pizza Margherita", description="Salsa de tomate, mozzarella fresca y albahaca", price=1500.00, is_available=True),
        MenuItem(category="Pizzas", name="Pizza Pepperoni", description="Salsa de tomate, mozzarella y pepperoni importado", price=1700.00, is_available=True),
        MenuItem(category="Papas Fritas", name="Papas Simples", description="Papas fritas crocantes con sal y especias", price=500.00, is_available=True),
        MenuItem(category="Papas Fritas", name="Papas con Cheddar", description="Papas fritas bañadas en salsa cheddar casera", price=700.00, is_available=True),
        MenuItem(category="Bebidas", name="Coca Cola", description="Lata 354ml", price=400.00, is_available=True),
        MenuItem(category="Bebidas", name="Agua Mineral", description="Botella 500ml con o sin gas", price=300.00, is_available=True),
        MenuItem(category="Bebidas", name="Limonada Casera", description="Limonada fresca con menta y jengibre", price=600.00, is_available=True),
    ]
    db.add_all(items)
    db.commit()
    print(f"{len(items)} menu items seeded.")

# ─── Step 4: Seed tables (mesas) ───────────────────────────
def seed_tables(db):
    from features.tables.models import Table

    existing = db.query(Table).count()
    if existing > 0:
        print("Tables already seeded — skipping.")
        return

    tables = [
        Table(table_number="1", qr_token="table_1_a1b2c3d4", status="available"),
        Table(table_number="2", qr_token="table_2_e5f6g7h8", status="available"),
        Table(table_number="3", qr_token="table_3_i9j0k1l2", status="available"),
    ]
    db.add_all(tables)
    db.commit()
    print(f"{len(tables)} tables seeded.")

# ─── Step 5: Create admin user ─────────────────────────────
def create_admin(db):
    from features.auth.models import AdminUser

    existing = db.query(AdminUser).first()
    if existing:
        print("Admin user already exists — skipping.")
        return

    from features.auth.service import create_first_admin
    import getpass

    print("\n=== ADMIN USER SETUP ===")
    username = input("Username (default: admin): ").strip() or "admin"
    password = getpass.getpass("Main password: ")
    sales_password = getpass.getpass("Sales password: ")

    admin, recovery_code = create_first_admin(
        db=db,
        username=username,
        password=password,
        sales_password=sales_password,
    )

    print(f"\nAdmin '{admin.username}' created successfully.")
    print("\n" + "=" * 40)
    print("RECOVERY CODE — SAVE THIS SOMEWHERE SAFE:")
    print(f">>> {recovery_code} <<<")
    print("This code will NOT be shown again.")
    print("=" * 40 + "\n")

# ─── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== ENCOM — Database Setup ===\n")

    # 1. Create DB
    create_database()

    # 2. Create tables
    create_tables()

    # 3. Seed data
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        seed_menu(db)
        seed_tables(db)
        create_admin(db)
    finally:
        db.close()

    print("\n=== Setup complete. Run 'fastapi dev main.py' to start the server. ===\n")