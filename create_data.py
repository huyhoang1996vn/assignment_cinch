
from sqlmodel import Session, select
from models import Products, Attributes, Regions, RentalPeriods, ProductPricings
from datetime import datetime

def create_test_data(session: Session):
    # Check if data exists
    region_exists = session.exec(select(Regions).limit(1)).first()
    if region_exists:
        print("Test data already exists.")
        return

    # Create Regions
    regions = [
        Regions(name="Singapore", code="SG"),
        Regions(name="Malaysia", code="MY")
    ]
    session.add_all(regions)
    session.commit()
    for region in regions:
        session.refresh(region)

    # Create Rental Periods
    rental_periods = [
        RentalPeriods(month=3),
        RentalPeriods(month=6),
        RentalPeriods(month=12)
    ]
    session.add_all(rental_periods)
    session.commit()
    for period in rental_periods:
        session.refresh(period)

    # Product definitions with their attributes
    products_data = [
        # Laptops
        {
            "product": Products(
                name="MacBook Pro 14",
                description="Latest MacBook Pro with M2 chip",
                sku="MB-PRO-14",
                detail="Perfect for developers and creative professionals"
            ),
            "attributes": [
                {"name": "Processor", "value": "M2 Pro"},
                {"name": "RAM", "value": "16GB"},
                {"name": "Storage", "value": "512GB SSD"},
                {"name": "Display", "value": "14-inch Liquid Retina XDR"}
            ],
            "base_price": 1200  # Base price for calculations
        },
        {
            "product": Products(
                name="Dell XPS 13",
                description="Premium Windows Ultrabook",
                sku="DELL-XPS-13",
                detail="Compact and powerful laptop for professionals"
            ),
            "attributes": [
                {"name": "Processor", "value": "Intel i7-1260P"},
                {"name": "RAM", "value": "16GB"},
                {"name": "Storage", "value": "512GB SSD"},
                {"name": "Display", "value": "13.4-inch 4K Touch"}
            ],
            "base_price": 1000
        },
        {
            "product": Products(
                name="ThinkPad X1 Carbon",
                description="Business-class laptop",
                sku="TP-X1-CARBON",
                detail="Durable and reliable business laptop"
            ),
            "attributes": [
                {"name": "Processor", "value": "Intel i7-1270P"},
                {"name": "RAM", "value": "32GB"},
                {"name": "Storage", "value": "1TB SSD"},
                {"name": "Display", "value": "14-inch WQHD"}
            ],
            "base_price": 1100
        },

        # Monitors
        {
            "product": Products(
                name="LG UltraFine 27",
                description="4K Professional Monitor",
                sku="LG-UF-27",
                detail="Perfect for content creation"
            ),
            "attributes": [
                {"name": "Resolution", "value": "3840x2160"},
                {"name": "Panel", "value": "IPS"},
                {"name": "Response Time", "value": "5ms"},
                {"name": "Refresh Rate", "value": "60Hz"}
            ],
            "base_price": 400
        },
        {
            "product": Products(
                name="Dell Ultrasharp 32",
                description="Professional 4K Monitor",
                sku="DELL-US-32",
                detail="Ideal for professional work"
            ),
            "attributes": [
                {"name": "Resolution", "value": "3840x2160"},
                {"name": "Panel", "value": "IPS"},
                {"name": "Response Time", "value": "5ms"},
                {"name": "Color Gamut", "value": "99% sRGB"}
            ],
            "base_price": 500
        },
        {
            "product": Products(
                name="Samsung Odyssey G7",
                description="Gaming Monitor",
                sku="SAM-OD-G7",
                detail="Curved gaming monitor with high refresh rate"
            ),
            "attributes": [
                {"name": "Resolution", "value": "2560x1440"},
                {"name": "Panel", "value": "VA"},
                {"name": "Refresh Rate", "value": "240Hz"},
                {"name": "Curve", "value": "1000R"}
            ],
            "base_price": 600
        },

        # Keyboards
        {
            "product": Products(
                name="Keychron K2",
                description="Wireless Mechanical Keyboard",
                sku="KEY-K2",
                detail="Compact wireless mechanical keyboard"
            ),
            "attributes": [
                {"name": "Switch Type", "value": "Gateron Brown"},
                {"name": "Layout", "value": "75%"},
                {"name": "Connectivity", "value": "Bluetooth/USB-C"},
                {"name": "Backlight", "value": "RGB"}
            ],
            "base_price": 80
        },
        {
            "product": Products(
                name="Logitech MX Keys",
                description="Premium Wireless Keyboard",
                sku="LOG-MX-KEYS",
                detail="Premium typing experience"
            ),
            "attributes": [
                {"name": "Type", "value": "Scissor Switch"},
                {"name": "Layout", "value": "Full-size"},
                {"name": "Connectivity", "value": "Bluetooth/USB"},
                {"name": "Battery Life", "value": "10 days with backlight"}
            ],
            "base_price": 100
        },
        {
            "product": Products(
                name="Ducky One 2",
                description="RGB Mechanical Keyboard",
                sku="DUCKY-ONE2",
                detail="High-quality mechanical keyboard"
            ),
            "attributes": [
                {"name": "Switch Type", "value": "Cherry MX Blue"},
                {"name": "Layout", "value": "TKL"},
                {"name": "Keycaps", "value": "PBT Double-shot"},
                {"name": "Backlight", "value": "RGB"}
            ],
            "base_price": 110
        },

        # Mice
        {
            "product": Products(
                name="Logitech MX Master 3",
                description="Premium Wireless Mouse",
                sku="LOG-MX3",
                detail="Advanced wireless mouse for productivity"
            ),
            "attributes": [
                {"name": "Sensor", "value": "Darkfield"},
                {"name": "DPI", "value": "4000"},
                {"name": "Buttons", "value": "7"},
                {"name": "Battery Life", "value": "70 days"}
            ],
            "base_price": 90
        },
        {
            "product": Products(
                name="Razer DeathAdder V2",
                description="Gaming Mouse",
                sku="RAZ-DA-V2",
                detail="Popular gaming mouse"
            ),
            "attributes": [
                {"name": "Sensor", "value": "Focus+ Optical"},
                {"name": "DPI", "value": "20000"},
                {"name": "Buttons", "value": "8"},
                {"name": "Weight", "value": "82g"}
            ],
            "base_price": 70
        },
        {
            "product": Products(
                name="Glorious Model O",
                description="Lightweight Gaming Mouse",
                sku="GLO-MO",
                detail="Ultra-lightweight gaming mouse"
            ),
            "attributes": [
                {"name": "Sensor", "value": "PixArt PMW-3360"},
                {"name": "Weight", "value": "67g"},
                {"name": "Cable", "value": "Ascended Cord"},
                {"name": "RGB", "value": "Yes"}
            ],
            "base_price": 60
        },

        # Accessories
        {
            "product": Products(
                name="CalDigit TS4",
                description="Thunderbolt 4 Dock",
                sku="CAL-TS4",
                detail="Premium Thunderbolt 4 docking station"
            ),
            "attributes": [
                {"name": "Ports", "value": "18"},
                {"name": "Power Delivery", "value": "98W"},
                {"name": "Display Support", "value": "Up to 8K"},
                {"name": "Ethernet", "value": "2.5Gbps"}
            ],
            "base_price": 300
        },
        {
            "product": Products(
                name="Sony WH-1000XM4",
                description="Wireless Noise-Cancelling Headphones",
                sku="SONY-WH4",
                detail="Premium wireless headphones"
            ),
            "attributes": [
                {"name": "Battery Life", "value": "30 hours"},
                {"name": "Noise Cancelling", "value": "Active"},
                {"name": "Bluetooth", "value": "5.0"},
                {"name": "Codecs", "value": "LDAC, AAC"}
            ],
            "base_price": 350
        },
        {
            "product": Products(
                name="Logitech Brio",
                description="4K Webcam",
                sku="LOG-BRIO",
                detail="Professional 4K webcam"
            ),
            "attributes": [
                {"name": "Resolution", "value": "4K"},
                {"name": "FPS", "value": "60"},
                {"name": "HDR", "value": "Yes"},
                {"name": "FOV", "value": "90°"}
            ],
            "base_price": 200
        },
        {
            "product": Products(
                name="Samsung T7",
                description="Portable SSD",
                sku="SAM-T7",
                detail="Fast portable storage"
            ),
            "attributes": [
                {"name": "Capacity", "value": "1TB"},
                {"name": "Interface", "value": "USB 3.2"},
                {"name": "Speed", "value": "1050MB/s"},
                {"name": "Encryption", "value": "256-bit AES"}
            ],
            "base_price": 150
        },
        {
            "product": Products(
                name="Anker PowerCore",
                description="Power Bank",
                sku="ANK-PC",
                detail="High-capacity power bank"
            ),
            "attributes": [
                {"name": "Capacity", "value": "26800mAh"},
                {"name": "Ports", "value": "3 USB-A"},
                {"name": "Input", "value": "USB-C PD"},
                {"name": "Output", "value": "60W Max"}
            ],
            "base_price": 130
        },
        {
            "product": Products(
                name="Elgato Stream Deck",
                description="Stream Controller",
                sku="ELG-SD",
                detail="Customizable LCD key controller"
            ),
            "attributes": [
                {"name": "Keys", "value": "15"},
                {"name": "Display", "value": "LCD"},
                {"name": "Interface", "value": "USB 2.0"},
                {"name": "Software", "value": "Stream Deck App"}
            ],
            "base_price": 150
        }
    ]

    # Add products and their attributes
    for product_data in products_data:
        product = product_data["product"]
        session.add(product)
        session.commit()
        session.refresh(product)

        # Add attributes
        for attr in product_data["attributes"]:
            attribute = Attributes(
                name=attr["name"],
                value=attr["value"],
                product_id=product.id
            )
            session.add(attribute)
        session.commit()

        base_price = product_data["base_price"]
        
        # Define simple pricing structure
        pricing_data = {
            # Singapore prices (in SGD)
            "SG": {
                3: base_price,              # 3 months - base price
                6: base_price * 1.8,        # 6 months - 1.8x base price
                12: base_price * 3          # 12 months - 3x base price
            },
            # Malaysia prices (in MYR)
            "MY": {
                3: base_price * 3,          # 3 months - 3x base price
                6: base_price * 5,          # 6 months - 5x base price
                12: base_price * 9          # 12 months - 9x base price
            }
        }

        # Add prices for all combinations
        for region in regions:
            for period in rental_periods:
                price = ProductPricings(
                    region_id=region.id,
                    rental_period_id=period.id,
                    product_id=product.id,
                    price=int(pricing_data[region.code][period.month])
                )
                session.add(price)
        session.commit()

    print("Created 18 products with attributes and pricing")
    return True