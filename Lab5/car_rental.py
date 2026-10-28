"""Car rental demo with safer validation and file handling."""

import hashlib
import os
import re
import secrets
import sqlite3
import tempfile
from datetime import datetime

fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car after validating its plate and daily rate."""
    if not is_valid_plate(plate):
        raise ValueError("Invalid number plate")
    if daily_rate < 0:
        raise ValueError("Daily rate cannot be negative")
    if features is None:
        features = []
    fleet[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": list(features),
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Register a customer using a parameterized SQL query."""
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )


def find_customer(name):
    """Find customers by exact name safely."""
    return conn.execute("SELECT * FROM customers WHERE name = ?", (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Rent an available car for a registered customer."""
    if not find_customer(customer):
        raise ValueError("Customer not registered")
    if plate not in fleet:
        raise ValueError("Car not found")
    if not fleet[plate]["available"]:
        raise ValueError("Car is not available")

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days
    if days <= 0:
        raise ValueError("End date must be after start date")

    cost = days * fleet[plate]["rate"]
    booking = {
        "code": booking_code(),
        "plate": plate,
        "customer": customer,
        "days": days,
        "cost": cost,
    }
    bookings.append(booking)
    fleet[plate]["available"] = False
    return cost


def return_car(plate, km_driven):
    """Return a known car and calculate any extra-distance charge."""
    if plate not in fleet:
        raise ValueError("Car not found")
    if km_driven < 0:
        raise ValueError("Distance cannot be negative")
    fleet[plate]["available"] = True
    return max(0, km_driven - 300) * 5


def booking_code():
    """Generate a hard-to-guess booking identifier."""
    return f"BK-{secrets.token_hex(4).upper()}"


def licence_hash(licence):
    """Return a SHA-256 digest of a licence string."""
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(rule, amount):
    """Apply only the supported 10 percent promotion."""
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if rule == "10%":
        return amount * 0.9
    raise ValueError("Unsupported promotion rule")


def is_valid_plate(plate):
    """Check the expected Indian vehicle plate format."""
    return bool(re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", plate))


def write_receipt(booking):
    """Write a receipt to a securely created temporary file."""
    fd, path = tempfile.mkstemp(suffix=".txt", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as receipt:
            receipt.write(
                f"Booking {booking['code']}: {booking['plate']} "
                f"for {booking['days']} days = Rs.{booking['cost']}\n"
            )
    except Exception:
        try:
            os.unlink(path)
        except OSError:
            pass
        raise
    return path


def admin_login(user, password):
    """Check credentials against a configured environment password."""
    expected_password = os.environ.get("CAR_RENTAL_ADMIN_PASSWORD")
    return bool(
        expected_password
        and user == "admin"
        and secrets.compare_digest(password, expected_password)
    )


def available_cars():
    """Return the number plates of all available cars."""
    return [plate for plate, car in fleet.items() if car["available"]]


def main():
    """Run a small demonstration of the car-rental functions."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)

    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")

    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Promo price:", apply_promo("10%", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print("Admin:", admin_login("admin", ""))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
