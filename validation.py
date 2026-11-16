
import re
from datetime import datetime, date


def validate_name(name):
    """Check that the patient name is not empty."""
    if not name or not name.strip():
        return False, "Patient name cannot be empty."

    return True, ""


def validate_email(email):
    """Check whether the email address has a valid format."""
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not email or not re.match(email_pattern, email.strip()):
        return False, "Please enter a valid email address."

    return True, ""


def validate_dob(dob):
    """Check date format, actual date and future dates."""

    try:
        birth_date = datetime.strptime(
            dob.strip(), "%d/%m/%Y"
        ).date()

    except ValueError:
        return False, (
            "Invalid date. Use DD/MM/YYYY "
            "and enter a real calendar date."
        )

    if birth_date > date.today():
        return False, "Date of birth cannot be in the future."

    return True, ""


def validate_blood_values(glucose, haemoglobin, cholesterol):
    """Check that all blood test values are numeric."""

    values = {
        "Glucose": glucose,
        "Haemoglobin": haemoglobin,
        "Cholesterol": cholesterol
    }

    for field, value in values.items():
        try:
            number = float(value)

            if not float("-inf") < number < float("inf"):
                return False, f"{field} must be a finite number."

        except (ValueError, TypeError):
            return False, f"{field} must be numeric."

        if number < 0:
            return False, f"{field} cannot be negative."

    return True, ""
