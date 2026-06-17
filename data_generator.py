import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_data(file_name="mock_budget.xlsx"):
    expense_categories = ["Groceries", "Rent", "Bills", "Transport", "Entertainment"]
    income_categories = ["Salary", "Used Sales", "Refunds"]

    data = []
    start_date = datetime(2025, 1, 1)

    # Generates 100 random transactions
    for i in range(100):
        random_days = random.randint(0, 365)
        transaction_date = start_date + timedelta(days=random_days)

        transaction_type = random.choices(["Income", "Expense"], weights=[0.2, 0.8])[0]

        if transaction_type == "Expense":
            category = random.choice(expense_categories)
            amount = round(random.uniform(10.0, 500.0), 2)
            if category == "Rent":
                amount = round(random.uniform(600.0, 1000.0), 2)
        else:
            category = random.choice(income_categories)
            amount = round(random.uniform(1500.0, 3000.0), 2) if category == "Salary" else round(random.uniform(50.0, 200.0), 2)

        data.append({
            "Date": transaction_date.strftime("%Y-%m-%d"),
            "Type": transaction_type,
            "Category": category,
            "Amount_EUR": amount
        })

    df = pd.DataFrame(data)
    df = df.sort_values(by="Date").reset_index(drop=True)
    df.to_excel(file_name, index=False)
    print(f" File '{file_name}' generated successfully!")

if __name__ == "__main__":
    generate_mock_data()
