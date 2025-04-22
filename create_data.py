from models import *
from sqlmodel import Session, select
from models import (
    Products,
    Attributes,
    Regions,
    RentalPeriods,
    ProductPricings,
)


def create_test_data(session: Session):  # Added session parameter
    # Check if data exists to avoid duplicates
    region_exists = session.exec(select(Regions).limit(1)).first()
    if region_exists:
        print("Test data already exists.")
        return

    # Create Regions
    region_sg = Regions(name="Singapore", code="SG")
    region_my = Regions(name="Malaysia", code="MY")
    session.add(region_sg)
    session.add(region_my)
    session.commit()  # Commit here to get IDs for foreign keys
    session.refresh(region_sg)
    session.refresh(region_my)
    print("Created Regions")

    # Create Rental Periods
    period_3m = RentalPeriods(month=3)
    period_6m = RentalPeriods(month=6)
    period_12m = RentalPeriods(month=12)
    session.add(period_3m)
    session.add(period_6m)
    session.add(period_12m)
    session.commit()
    session.refresh(period_3m)
    session.refresh(period_6m)
    session.refresh(period_12m)
    print("Created Rental Periods")

    # Create Products
    product_laptop = Products(
        name="Laptop X1", description="High-performance laptop", sku="LPX1-001"
    )
    product_monitor = Products(
        name="Monitor Pro", description="4K UHD Monitor", sku="MNP-001"
    )
    product_keyboard = Products(
        name="Keyboard Pro", description="Mechanical Keyboard", sku="KBP-001"
    )  # Added Keyboard
    product_mouse = Products(
        name="Mouse Master", description="Wireless Ergonomic Mouse", sku="MSM-001"
    )  # Added Mouse
    session.add(product_laptop)
    session.add(product_monitor)
    session.add(product_keyboard)  # Add keyboard to session
    session.add(product_mouse)  # Add mouse to session
    session.commit()
    session.refresh(product_laptop)
    session.refresh(product_monitor)
    session.refresh(product_keyboard)  # Refresh keyboard
    session.refresh(product_mouse)  # Refresh mouse
    print("Created Products")

    # Create Attributes
    # Laptop Attributes
    attr_laptop_ram = Attributes(name="RAM", value="16GB", product_id=product_laptop.id)
    attr_laptop_cpu = Attributes(
        name="CPU", value="Intel i7", product_id=product_laptop.id
    )
    attr_laptop_storage = Attributes(
        name="Storage", value="512GB SSD", product_id=product_laptop.id
    )

    # Monitor Attributes
    attr_monitor_size = Attributes(
        name="Size", value="27 inch", product_id=product_monitor.id
    )
    attr_monitor_res = Attributes(
        name="Resolution", value="3840x2160", product_id=product_monitor.id
    )
    attr_monitor_panel = Attributes(
        name="Panel Type", value="IPS", product_id=product_monitor.id
    )

    # Keyboard Attributes
    attr_keyboard_type = Attributes(
        name="Type", value="Mechanical", product_id=product_keyboard.id
    )
    attr_keyboard_switch = Attributes(
        name="Switch", value="Blue", product_id=product_keyboard.id
    )
    attr_keyboard_layout = Attributes(
        name="Layout", value="US QWERTY", product_id=product_keyboard.id
    )

    # Mouse Attributes
    attr_mouse_type = Attributes(
        name="Type", value="Wireless", product_id=product_mouse.id
    )
    attr_mouse_dpi = Attributes(name="DPI", value="1600", product_id=product_mouse.id)
    attr_mouse_buttons = Attributes(
        name="Buttons", value="5", product_id=product_mouse.id
    )

    session.add_all(
        [
            attr_laptop_ram,
            attr_laptop_cpu,
            attr_laptop_storage,
            attr_monitor_size,
            attr_monitor_res,
            attr_monitor_panel,
            attr_keyboard_type,
            attr_keyboard_switch,
            attr_keyboard_layout,
            attr_mouse_type,
            attr_mouse_dpi,
            attr_mouse_buttons,
        ]
    )
    # No need to commit here if pricings are added next, commit at the end is fine
    print("Created Attributes")

    # Create Product Pricings
    # Laptop Prices
    pricing_laptop_sg_3m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_3m.id,
        product_id=product_laptop.id,
        price=300,
    )
    pricing_laptop_sg_6m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_6m.id,
        product_id=product_laptop.id,
        price=550,
    )
    pricing_laptop_sg_12m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_12m.id,
        product_id=product_laptop.id,
        price=1000,
    )
    pricing_laptop_my_3m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_3m.id,
        product_id=product_laptop.id,
        price=900,
    )  # Assuming MYR
    pricing_laptop_my_6m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_6m.id,
        product_id=product_laptop.id,
        price=1650,
    )
    pricing_laptop_my_12m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_12m.id,
        product_id=product_laptop.id,
        price=3000,
    )

    # Monitor Prices
    pricing_monitor_sg_3m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_3m.id,
        product_id=product_monitor.id,
        price=100,
    )
    pricing_monitor_sg_6m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_6m.id,
        product_id=product_monitor.id,
        price=180,
    )
    pricing_monitor_sg_12m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_12m.id,
        product_id=product_monitor.id,
        price=320,
    )
    pricing_monitor_my_3m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_3m.id,
        product_id=product_monitor.id,
        price=300,
    )  # Assuming MYR
    pricing_monitor_my_6m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_6m.id,
        product_id=product_monitor.id,
        price=540,
    )
    pricing_monitor_my_12m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_12m.id,
        product_id=product_monitor.id,
        price=960,
    )

    # Keyboard Prices
    pricing_keyboard_sg_3m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_3m.id,
        product_id=product_keyboard.id,
        price=50,
    )
    pricing_keyboard_sg_6m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_6m.id,
        product_id=product_keyboard.id,
        price=90,
    )
    pricing_keyboard_sg_12m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_12m.id,
        product_id=product_keyboard.id,
        price=160,
    )
    pricing_keyboard_my_3m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_3m.id,
        product_id=product_keyboard.id,
        price=150,
    )  # Assuming MYR
    pricing_keyboard_my_6m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_6m.id,
        product_id=product_keyboard.id,
        price=270,
    )
    pricing_keyboard_my_12m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_12m.id,
        product_id=product_keyboard.id,
        price=480,
    )

    # Mouse Prices
    pricing_mouse_sg_3m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_3m.id,
        product_id=product_mouse.id,
        price=40,
    )
    pricing_mouse_sg_6m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_6m.id,
        product_id=product_mouse.id,
        price=70,
    )
    pricing_mouse_sg_12m = ProductPricings(
        region_id=region_sg.id,
        rental_period_id=period_12m.id,
        product_id=product_mouse.id,
        price=120,
    )
    pricing_mouse_my_3m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_3m.id,
        product_id=product_mouse.id,
        price=120,
    )  # Assuming MYR
    pricing_mouse_my_6m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_6m.id,
        product_id=product_mouse.id,
        price=210,
    )
    pricing_mouse_my_12m = ProductPricings(
        region_id=region_my.id,
        rental_period_id=period_12m.id,
        product_id=product_mouse.id,
        price=360,
    )

    session.add_all(
        [
            pricing_laptop_sg_3m,
            pricing_laptop_sg_6m,
            pricing_laptop_sg_12m,
            pricing_laptop_my_3m,
            pricing_laptop_my_6m,
            pricing_laptop_my_12m,
            pricing_monitor_sg_3m,
            pricing_monitor_sg_6m,
            pricing_monitor_sg_12m,
            pricing_monitor_my_3m,
            pricing_monitor_my_6m,
            pricing_monitor_my_12m,
            pricing_keyboard_sg_3m,
            pricing_keyboard_sg_6m,
            pricing_keyboard_sg_12m,  # Add keyboard prices
            pricing_keyboard_my_3m,
            pricing_keyboard_my_6m,
            pricing_keyboard_my_12m,
            pricing_mouse_sg_3m,
            pricing_mouse_sg_6m,
            pricing_mouse_sg_12m,  # Add mouse prices
            pricing_mouse_my_3m,
            pricing_mouse_my_6m,
            pricing_mouse_my_12m,
        ]
    )
    session.commit()  # Commit attributes and pricings together
    print("Created Product Pricings")
    print("Test data creation complete.")
