# Telecommunications Call Analytics & Visualization Platform

An object-oriented telecommunications analytics platform that processes customer call records, models billing contracts, and visualizes call activity through an interactive geographic interface.

---

## Features

- Customer and phone line management using modular object-oriented design
- Support for multiple contract models, including monthly, term, and prepaid plans
- Automated billing calculations based on contract-specific pricing rules
- JSON data ingestion and object construction pipeline
- Interactive filtering by customer, call duration, and geographic region
- Geographic visualization of call activity across Toronto using Pygame
- Unit testing for core business logic and filtering functionality

---

## Technologies

- Python
- Object-Oriented Programming (OOP)
- Pygame
- JSON
- Pytest

---

## Project Structure

```
.
├── application.py      # Application entry point
├── customer.py         # Customer management
├── phoneline.py        # Phone line abstraction
├── contract.py         # Billing contract implementations
├── bill.py             # Billing calculations
├── call.py             # Call event model
├── callhistory.py      # Customer call history
├── filter.py           # Interactive filtering algorithms
├── visualizer.py       # Geographic visualization engine
├── dataset.json        # Demonstration dataset
└── data/               # Map and visualization assets
```

---

## System Overview

The application models a simplified telecommunications network where customers own one or more phone lines associated with different billing contracts. Call records are parsed from structured datasets and converted into object representations for processing.

Users can explore call activity through an interactive visualization, apply dynamic filters, and inspect customer communication patterns and billing information.
