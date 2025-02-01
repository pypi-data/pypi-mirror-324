# PyZDC

[![CI](https://img.shields.io/github/actions/workflow/status/GuttoF/dq-sus/ci.yaml?branch=main&logo=github&label=CI)](https://github.com/GuttoF/pyzdc/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![License](https://img.shields.io/github/license/GuttoF/dq-sus.svg)](https://github.com/GuttoF/pyzdc/blob/main/LICENSE)
[![CI](https://github.com/GuttoF/pyzdc/actions/workflows/ci.yaml/badge.svg)](https://github.com/Guttof/pyzdc/actions/workflows/ci.yaml)

**PyZDC** is a Python tool designed to simplify the analysis of epidemiological data related to the **Aedes aegypti**, focusing on diseases such as **Dengue**, **Zika**, and **Chikungunya**. It is fast, extensible, and easy to use.

---

## **Features**
- Automated extraction of epidemiological data.
- Data transformation and validation using **DuckDB** and **Pandera**.
- Specific functions to access processed tables, including notifications, personal data, clinical signs, and more.
- Fully compatible with **Python 3.12+**.

---

## **Installation**

Install the package via `pip`:

```bash
pip install pyzdc
```

Install the package using `uv` or `poetry`:

```bash
# uv
uv add pyzdc

# poetry
poetry add pyzdc
```

---

## **Quick Example**

Here’s a quick example to get you started:

```python
import pandas as pd
import pyzdc as zdc

# Fetch notification data for Chikungunya cases in 2022 and 2023
df = zdc.get_notifications(years=[2022, 2023], disease="CHIK")

# Display the first few rows
print(df.head())

# Save the DataFrame to a CSV file
df.to_csv("notifications.csv", index=False)
```

This will output something like:

```
       notification_id    notification_type  disease_condition_id      notification_date    notification_week    notification_year    notification_state_id    notification_city_id    notification_region_id    notification_health_unit_id 
  0                  1                    2  A92.0                              20220108               202201                 2022                       12                  120033                  1941                            9542566 
  1                  2                    2  A92.0                              20220216               202207                 2022                       12                  120033                  1941                            9542566 
  2                  3                    2  A92.0                              20220126               202204                 2022                       12                  120033                  1941                            9542566 
  3                  4                    2  A92.0                              20220108               202201                 2022                       12                  120033                  1941                            9542566 
  4                  5                    2  A92.0                              20220126               202204                 2022                       12                  120033                  1941                            2000083 
```
---

## **Help**

For more information, see the [documentation](https://pyzdc.readthedocs.io/en/latest/).

---

## **Contributing**

Contributions are welcome! Follow these steps to contribute:

### **1. Fork the Repository**
Create a fork of the repository in your GitHub account.

### **2. Clone the Repository**
Clone your fork locally:
```bash
git clone https://github.com/your-username/dq-sus.git
cd dq-sus
```

### **3. Create a Branch**
Create a branch for your changes:
```bash
git checkout -b feature-name
```

### **4. Install Dependencies**
Install the required dependencies using `pip` or `uv`:
```bash
pip install -r requirements.txt
```

### **5. Make Changes and Test**
Implement your changes and ensure all tests pass:
```bash
pytest
```

### **6. Commit and Push**
Commit your changes and push to your fork:
```bash
git add .
git commit -m "Add feature description"
git push origin feature-name
```

### **7. Open a Pull Request**
Submit a pull request to the `dev` branch of the original repository.

---

## **Security**

To report security vulnerabilities, please review our [security policy](https://github.com/GuttoF/dq-sus/security/policy).

---

## **License**

This project is licensed under the [MIT License](https://github.com/GuttoF/dq-sus/blob/main/LICENSE).


