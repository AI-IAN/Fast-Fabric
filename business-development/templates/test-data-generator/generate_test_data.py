import argparse
import os
import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

SIZE_MAP = {
    'small': 1000,
    'medium': 100000,
    'large': 1000000
}

def _write_parquet(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)

def generate_ecommerce(base, out_dir):
    num_customers = base
    num_orders = base * 10
    customers = pd.DataFrame({
        'customer_id': np.arange(1, num_customers + 1),
        'name': [fake.name() for _ in range(num_customers)],
        'email': [fake.email() for _ in range(num_customers)],
        'loyalty_status': np.random.choice(['bronze', 'silver', 'gold'], num_customers)
    })

    products = pd.DataFrame({
        'product_id': np.arange(1, 501),
        'name': [fake.word() for _ in range(500)],
        'category': np.random.choice(['electronics', 'apparel', 'home', 'sports'], 500),
        'price': np.random.uniform(5, 500, 500).round(2)
    })

    orders = pd.DataFrame({
        'order_id': np.arange(1, num_orders + 1),
        'customer_id': np.random.choice(customers['customer_id'], num_orders),
        'order_date': [fake.date_time_this_year() for _ in range(num_orders)],
        'total_amount': np.random.uniform(20, 300, num_orders).round(2)
    })

    order_items = pd.DataFrame({
        'order_id': orders['order_id'],
        'product_id': np.random.choice(products['product_id'], num_orders),
        'quantity': np.random.randint(1, 5, num_orders),
        'unit_price': np.random.uniform(5, 500, num_orders).round(2)
    })

    clickstream = pd.DataFrame({
        'event_id': np.arange(1, num_orders * 3 + 1),
        'customer_id': np.random.choice(customers['customer_id'], num_orders * 3),
        'event_type': np.random.choice(['view', 'add_to_cart', 'purchase'], num_orders * 3),
        'product_id': np.random.choice(products['product_id'], num_orders * 3),
        'timestamp': [fake.date_time_this_year() for _ in range(num_orders * 3)]
    })

    base_path = os.path.join(out_dir, 'ecommerce')
    _write_parquet(customers, os.path.join(base_path, 'customers.parquet'))
    _write_parquet(products, os.path.join(base_path, 'products.parquet'))
    _write_parquet(orders, os.path.join(base_path, 'orders.parquet'))
    _write_parquet(order_items, os.path.join(base_path, 'order_items.parquet'))
    _write_parquet(clickstream, os.path.join(base_path, 'clickstream.parquet'))


def generate_financial(base, out_dir):
    num_customers = base
    num_accounts = base * 2
    num_transactions = base * 10
    customers = pd.DataFrame({
        'customer_id': np.arange(1, num_customers + 1),
        'name': [fake.name() for _ in range(num_customers)],
        'address': [fake.address() for _ in range(num_customers)],
        'kyc_status': np.random.choice(['verified', 'pending', 'blocked'], num_customers)
    })

    accounts = pd.DataFrame({
        'account_id': np.arange(1, num_accounts + 1),
        'customer_id': np.random.choice(customers['customer_id'], num_accounts),
        'account_type': np.random.choice(['checking', 'savings', 'credit'], num_accounts),
        'open_date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(num_accounts)],
        'balance': np.random.uniform(100, 100000, num_accounts).round(2)
    })

    transactions = pd.DataFrame({
        'txn_id': np.arange(1, num_transactions + 1),
        'account_id': np.random.choice(accounts['account_id'], num_transactions),
        'amount': np.random.uniform(-5000, 5000, num_transactions).round(2),
        'txn_type': np.random.choice(['debit', 'credit'], num_transactions),
        'txn_time': [fake.date_time_this_year() for _ in range(num_transactions)]
    })

    risk_scores = pd.DataFrame({
        'customer_id': customers['customer_id'],
        'score_date': pd.Timestamp('today'),
        'risk_score': np.random.uniform(0, 1, num_customers).round(3)
    })

    base_path = os.path.join(out_dir, 'financial_services')
    _write_parquet(customers, os.path.join(base_path, 'customers.parquet'))
    _write_parquet(accounts, os.path.join(base_path, 'accounts.parquet'))
    _write_parquet(transactions, os.path.join(base_path, 'transactions.parquet'))
    _write_parquet(risk_scores, os.path.join(base_path, 'risk_scores.parquet'))


def generate_healthcare(base, out_dir):
    num_patients = base
    num_encounters = base * 5
    patients = pd.DataFrame({
        'patient_id': np.arange(1, num_patients + 1),
        'name': [fake.name() for _ in range(num_patients)],
        'birth_date': [fake.date_of_birth(minimum_age=0, maximum_age=90) for _ in range(num_patients)],
        'gender': np.random.choice(['M', 'F'], num_patients)
    })

    providers = pd.DataFrame({
        'provider_id': np.arange(1, base + 1),
        'name': [fake.name() for _ in range(base)],
        'specialty': np.random.choice(['cardiology', 'general', 'oncology', 'pediatrics'], base)
    })

    encounters = pd.DataFrame({
        'encounter_id': np.arange(1, num_encounters + 1),
        'patient_id': np.random.choice(patients['patient_id'], num_encounters),
        'provider_id': np.random.choice(providers['provider_id'], num_encounters),
        'encounter_date': [fake.date_time_this_year() for _ in range(num_encounters)],
        'diagnosis_code': np.random.randint(1000, 9999, num_encounters)
    })

    procedures = pd.DataFrame({
        'procedure_id': np.arange(1, num_encounters + 1),
        'encounter_id': encounters['encounter_id'],
        'procedure_code': np.random.randint(10000, 99999, num_encounters),
        'cost': np.random.uniform(100, 10000, num_encounters).round(2)
    })

    medications = pd.DataFrame({
        'patient_id': np.random.choice(patients['patient_id'], num_encounters),
        'medication_name': [fake.word() for _ in range(num_encounters)],
        'start_date': [fake.date_this_year() for _ in range(num_encounters)],
        'end_date': [fake.date_this_year() for _ in range(num_encounters)]
    })

    base_path = os.path.join(out_dir, 'healthcare')
    _write_parquet(patients, os.path.join(base_path, 'patients.parquet'))
    _write_parquet(providers, os.path.join(base_path, 'providers.parquet'))
    _write_parquet(encounters, os.path.join(base_path, 'encounters.parquet'))
    _write_parquet(procedures, os.path.join(base_path, 'procedures.parquet'))
    _write_parquet(medications, os.path.join(base_path, 'medications.parquet'))


def generate_manufacturing(base, out_dir):
    num_factories = max(1, base // 10)
    num_machines = base
    num_runs = base * 5
    factories = pd.DataFrame({
        'factory_id': np.arange(1, num_factories + 1),
        'name': [f'Factory {i}' for i in range(1, num_factories + 1)],
        'location': [fake.city() for _ in range(num_factories)]
    })

    machines = pd.DataFrame({
        'machine_id': np.arange(1, num_machines + 1),
        'factory_id': np.random.choice(factories['factory_id'], num_machines),
        'install_date': [fake.date_between(start_date='-10y', end_date='today') for _ in range(num_machines)],
        'status': np.random.choice(['active', 'maintenance', 'retired'], num_machines)
    })

    production_runs = pd.DataFrame({
        'run_id': np.arange(1, num_runs + 1),
        'factory_id': np.random.choice(factories['factory_id'], num_runs),
        'start_time': [fake.date_time_this_year() for _ in range(num_runs)],
        'end_time': [fake.date_time_this_year() for _ in range(num_runs)],
        'output_units': np.random.randint(100, 10000, num_runs)
    })

    maintenance_logs = pd.DataFrame({
        'log_id': np.arange(1, num_runs + 1),
        'machine_id': np.random.choice(machines['machine_id'], num_runs),
        'service_date': [fake.date_time_this_year() for _ in range(num_runs)],
        'issue_found': np.random.choice(['none', 'minor', 'major'], num_runs),
        'resolution': [fake.sentence(nb_words=6) for _ in range(num_runs)]
    })

    supplier_shipments = pd.DataFrame({
        'shipment_id': np.arange(1, num_runs + 1),
        'supplier_id': np.random.randint(1, 1000, num_runs),
        'part_number': [fake.bothify(text='??#####') for _ in range(num_runs)],
        'quantity': np.random.randint(1, 1000, num_runs),
        'arrival_date': [fake.date_time_this_year() for _ in range(num_runs)]
    })

    base_path = os.path.join(out_dir, 'manufacturing')
    _write_parquet(factories, os.path.join(base_path, 'factories.parquet'))
    _write_parquet(machines, os.path.join(base_path, 'machines.parquet'))
    _write_parquet(production_runs, os.path.join(base_path, 'production_runs.parquet'))
    _write_parquet(maintenance_logs, os.path.join(base_path, 'maintenance_logs.parquet'))
    _write_parquet(supplier_shipments, os.path.join(base_path, 'supplier_shipments.parquet'))


def main():
    parser = argparse.ArgumentParser(description='Generate industry sample data for Fast-Fabric demos.')
    parser.add_argument('--output-dir', required=True, help='Directory to write parquet files')
    parser.add_argument('--size', choices=SIZE_MAP.keys(), default='small', help='Volume of data to generate')
    args = parser.parse_args()

    base = SIZE_MAP[args.size]
    out = args.output_dir

    generate_ecommerce(base, out)
    generate_financial(base, out)
    generate_healthcare(base, out)
    generate_manufacturing(base, out)

if __name__ == '__main__':
    main()
