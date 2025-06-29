"""
Mock Data Generator for Fabric Fast-Track Development
Generates realistic sample data for testing data ingestion pipelines
without requiring real data sources
"""

import json
import csv
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker for realistic data generation
fake = Faker()
Faker.seed(42)  # Consistent test data
random.seed(42)

class MockDataGenerator:
    """Generate mock data for various business scenarios"""
    
    def __init__(self, output_path="./mock_data/"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def generate_customers(self, count=1000):
        """Generate customer data mimicking CRM systems"""
        customers = []
        
        for i in range(count):
            customer = {
                "CustomerID": i + 1,
                "CustomerName": fake.company(),
                "ContactName": fake.name(),
                "Email": fake.email(),
                "Phone": fake.phone_number(),
                "Address": fake.street_address(),
                "City": fake.city(),
                "State": fake.state_abbr(),
                "ZipCode": fake.zipcode(),
                "Country": fake.country_code(),
                "Industry": fake.random_element([
                    "Technology", "Healthcare", "Finance", "Retail", 
                    "Manufacturing", "Education", "Government"
                ]),
                "CompanySize": fake.random_element([
                    "Small (1-50)", "Medium (51-200)", "Large (201-1000)", "Enterprise (1000+)"
                ]),
                "AnnualRevenue": random.randint(100000, 50000000),
                "CreatedDate": fake.date_time_between(start_date="-2y", end_date="now"),
                "ModifiedDate": fake.date_time_between(start_date="-30d", end_date="now"),
                "IsActive": random.choice([True, True, True, False]),  # 75% active
                "Source": fake.random_element(["Website", "Referral", "Cold Call", "Trade Show", "Partner"])
            }
            customers.append(customer)
        
        return customers
    
    def generate_sales_data(self, customer_count=1000, sales_count=5000):
        """Generate sales transaction data"""
        sales = []
        
        for i in range(sales_count):
            sale = {
                "SaleID": i + 1,
                "CustomerID": random.randint(1, customer_count),
                "ProductID": random.randint(1, 100),
                "ProductName": fake.random_element([
                    "Professional Services", "Software License", "Hardware", 
                    "Support Contract", "Training", "Consulting"
                ]),
                "Category": fake.random_element([
                    "Software", "Hardware", "Services", "Support"
                ]),
                "Quantity": random.randint(1, 100),
                "UnitPrice": round(random.uniform(10, 10000), 2),
                "TotalAmount": 0,  # Will calculate
                "SaleDate": fake.date_time_between(start_date="-1y", end_date="now"),
                "SalesRep": fake.name(),
                "Region": fake.random_element([
                    "North America", "Europe", "Asia Pacific", "Latin America"
                ]),
                "Channel": fake.random_element([
                    "Direct", "Partner", "Online", "Retail"
                ]),
                "Status": fake.random_element([
                    "Closed Won", "Closed Lost", "In Progress", "Qualified"
                ])
            }
            sale["TotalAmount"] = round(sale["Quantity"] * sale["UnitPrice"], 2)
            sales.append(sale)
        
        return sales
    
    def generate_financial_data(self, months=24):
        """Generate financial/accounting data"""
        financial = []
        start_date = datetime.now() - timedelta(days=months*30)
        
        for month in range(months):
            current_date = start_date + timedelta(days=month*30)
            
            # Generate monthly financial records
            for account in ["Revenue", "Expenses", "Assets", "Liabilities"]:
                record = {
                    "RecordID": len(financial) + 1,
                    "Date": current_date,
                    "Account": account,
                    "AccountCode": fake.random_int(min=1000, max=9999),
                    "Description": f"Monthly {account} - {current_date.strftime('%B %Y')}",
                    "Amount": self._generate_financial_amount(account),
                    "Currency": "USD",
                    "Department": fake.random_element([
                        "Sales", "Marketing", "Engineering", "Operations", "Finance"
                    ]),
                    "CreatedBy": fake.name(),
                    "ModifiedDate": current_date
                }
                financial.append(record)
        
        return financial
    
    def _generate_financial_amount(self, account_type):
        """Generate realistic financial amounts based on account type"""
        if account_type == "Revenue":
            return round(random.uniform(50000, 500000), 2)
        elif account_type == "Expenses":
            return round(random.uniform(10000, 100000), 2)
        elif account_type == "Assets":
            return round(random.uniform(100000, 1000000), 2)
        else:  # Liabilities
            return round(random.uniform(20000, 200000), 2)
    
    def generate_api_response(self, endpoint_type="customers", count=100):
        """Generate mock API responses in JSON format"""
        
        if endpoint_type == "customers":
            data = self.generate_customers(count)
        elif endpoint_type == "sales":
            data = self.generate_sales_data(100, count)
        elif endpoint_type == "financial":
            data = self.generate_financial_data(12)[:count]
        else:
            data = []
        
        # Wrap in typical API response structure
        api_response = {
            "status": "success",
            "data": data,
            "pagination": {
                "page": 1,
                "per_page": count,
                "total": count,
                "total_pages": 1
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "endpoint": endpoint_type,
                "version": "v1"
            }
        }
        
        return api_response
    
    def save_as_csv(self, data, filename):
        """Save data as CSV file"""
        filepath = os.path.join(self.output_path, filename)
        
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
            print(f"Saved {len(data)} records to {filepath}")
        
        return filepath
    
    def save_as_json(self, data, filename):
        """Save data as JSON file"""
        filepath = os.path.join(self.output_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"Saved data to {filepath}")
        return filepath
    
    def save_as_excel(self, data, filename, sheet_name="Sheet1"):
        """Save data as Excel file"""
        filepath = os.path.join(self.output_path, filename)
        
        if data:
            df = pd.DataFrame(data)
            df.to_excel(filepath, sheet_name=sheet_name, index=False)
            print(f"Saved {len(data)} records to {filepath}")
        
        return filepath
    
    def generate_incremental_updates(self, original_data, update_percentage=0.1):
        """Generate incremental updates to simulate delta loading"""
        
        update_count = int(len(original_data) * update_percentage)
        updates = random.sample(original_data, update_count)
        
        for record in updates:
            # Simulate field updates
            if "ModifiedDate" in record:
                record["ModifiedDate"] = datetime.now()
            if "Email" in record:
                record["Email"] = fake.email()
            if "TotalAmount" in record:
                record["TotalAmount"] = round(record["TotalAmount"] * random.uniform(0.8, 1.2), 2)
        
        return updates

def generate_all_sample_data():
    """Generate complete sample dataset for development"""
    
    generator = MockDataGenerator()
    
    print("Generating mock data for Fabric Fast-Track development...")
    
    # Generate customer data
    customers = generator.generate_customers(1000)
    generator.save_as_csv(customers, "customers.csv")
    generator.save_as_json(customers, "customers.json")
    
    # Generate sales data
    sales = generator.generate_sales_data(1000, 5000)
    generator.save_as_csv(sales, "sales.csv")
    generator.save_as_excel(sales, "sales.xlsx")
    
    # Generate financial data
    financial = generator.generate_financial_data(24)
    generator.save_as_csv(financial, "financial.csv")
    
    # Generate API responses
    api_customers = generator.generate_api_response("customers", 100)
    generator.save_as_json(api_customers, "api_customers_response.json")
    
    api_sales = generator.generate_api_response("sales", 200)
    generator.save_as_json(api_sales, "api_sales_response.json")
    
    # Generate incremental updates
    customer_updates = generator.generate_incremental_updates(customers, 0.05)
    generator.save_as_csv(customer_updates, "customers_incremental.csv")
    
    print("Mock data generation completed\!")
    print(f"Files saved to: {generator.output_path}")
    
    return {
        "customers": len(customers),
        "sales": len(sales),
        "financial": len(financial),
        "api_customers": len(api_customers["data"]),
        "api_sales": len(api_sales["data"]),
        "customer_updates": len(customer_updates)
    }

if __name__ == "__main__":
    stats = generate_all_sample_data()
    print(f"Generated data statistics: {stats}")
