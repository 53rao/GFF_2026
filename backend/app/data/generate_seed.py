import json
import os
from datetime import datetime, timedelta
import random

# Ensure output directory exists
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

now = datetime.utcnow()

def iso_days_ago(days: int) -> str:
    return (now - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")

def generate():
    customers = []
    transactions = []
    behavior_events = []

    # ----------------------------------------------------
    # SCRIPTED CUSTOMER 1: Rajesh Kumar (LARGE_INFLOW)
    # ----------------------------------------------------
    c1 = {
        "id": "CUST-1001",
        "cif_number": "CIF89230011",
        "full_name": "Rajesh Kumar",
        "email": "rajesh.kumar@example.in",
        "mobile": "+919820101001",
        "segment": "WEALTH",
        "kyc_verified": True,
        "relationship_type": "Priority Account",
        "member_since": "2019-04-12",
        "account_balance": 1450000.0,
        "holdings": [
            {"product_code": "SB_PREM", "product_name": "SBI Savings Plus", "balance": 1450000.0}
        ]
    }
    customers.append(c1)
    # Months 1 & 2 routine salary and spending
    for d in [75, 45, 15]:
        transactions.append({
            "id": f"TX-1001-{d}-SAL",
            "customer_id": "CUST-1001",
            "amount": 150000.0,
            "type": "CREDIT",
            "category": "Salary",
            "description": "MONTHLY SALARY CREDIT - TCS LTD",
            "timestamp": iso_days_ago(d)
        })
    for d in [70, 60, 50, 40, 30, 20, 10]:
        transactions.append({
            "id": f"TX-1001-{d}-DEB",
            "customer_id": "CUST-1001",
            "amount": 18000.0,
            "type": "DEBIT",
            "category": "Bills & Utilities",
            "description": "CREDIT CARD BILL PAYMENT",
            "timestamp": iso_days_ago(d)
        })
    # Recent massive bonus credit 2 days ago
    transactions.append({
        "id": "TX-1001-BONUS",
        "customer_id": "CUST-1001",
        "amount": 850000.0,
        "type": "CREDIT",
        "category": "Bonus / Incentive",
        "description": "ANNUAL PERFORMANCE BONUS FY25",
        "timestamp": iso_days_ago(2)
    })
    for d in [14, 7, 2]:
        behavior_events.append({
            "id": f"BEV-1001-{d}",
            "customer_id": "CUST-1001",
            "event_type": "APP_LOGIN",
            "channel": "YONO_MOBILE",
            "timestamp": iso_days_ago(d)
        })

    # ----------------------------------------------------
    # SCRIPTED CUSTOMER 2: Priya Sharma (SPENDING_SPIKE)
    # ----------------------------------------------------
    c2 = {
        "id": "CUST-1002",
        "cif_number": "CIF89230012",
        "full_name": "Priya Sharma",
        "email": "priya.sharma@example.in",
        "mobile": "+919820101002",
        "segment": "RETAIL",
        "kyc_verified": True,
        "relationship_type": "Standard Savings",
        "member_since": "2021-08-19",
        "account_balance": 320000.0,
        "holdings": [
            {"product_code": "SB_REG", "product_name": "SBI Regular Savings", "balance": 320000.0}
        ]
    }
    customers.append(c2)
    # Normal spending over past 60 days (~20k/month)
    for d in range(60, 10, -8):
        transactions.append({
            "id": f"TX-1002-{d}",
            "customer_id": "CUST-1002",
            "amount": 3500.0,
            "type": "DEBIT",
            "category": "Groceries & Shopping",
            "description": "POS PURCHASE - RELIANCE FRESH",
            "timestamp": iso_days_ago(d)
        })
    # Sudden spending burst in the last 4 days (totaling 2,40,000)
    transactions.append({
        "id": "TX-1002-SPIKE1",
        "customer_id": "CUST-1002",
        "amount": 125000.0,
        "type": "DEBIT",
        "category": "Electronics",
        "description": "POS PURCHASE - APPLE PREMIUM RESELLER",
        "timestamp": iso_days_ago(3)
    })
    transactions.append({
        "id": "TX-1002-SPIKE2",
        "customer_id": "CUST-1002",
        "amount": 85000.0,
        "type": "DEBIT",
        "category": "Travel",
        "description": "ONLINE PURCHASE - MAKEMYTRIP FLIGHTS",
        "timestamp": iso_days_ago(2)
    })
    transactions.append({
        "id": "TX-1002-SPIKE3",
        "customer_id": "CUST-1002",
        "amount": 30000.0,
        "type": "DEBIT",
        "category": "Apparel",
        "description": "POS PURCHASE - ZARA MUMBAI",
        "timestamp": iso_days_ago(1)
    })
    for d in [10, 5, 2]:
        behavior_events.append({
            "id": f"BEV-1002-{d}",
            "customer_id": "CUST-1002",
            "event_type": "APP_LOGIN",
            "channel": "YONO_MOBILE",
            "timestamp": iso_days_ago(d)
        })

    # ----------------------------------------------------
    # SCRIPTED CUSTOMER 3: Amit Patel (DORMANCY_WARNING)
    # ----------------------------------------------------
    c3 = {
        "id": "CUST-1003",
        "cif_number": "CIF89230013",
        "full_name": "Amit Patel",
        "email": "amit.patel@example.in",
        "mobile": "+919820101003",
        "segment": "RETAIL",
        "kyc_verified": True,
        "relationship_type": "Standard Savings",
        "member_since": "2020-01-15",
        "account_balance": 180000.0,
        "holdings": [
            {"product_code": "SB_REG", "product_name": "SBI Regular Savings", "balance": 180000.0}
        ]
    }
    customers.append(c3)
    # Transactions ended 38 days ago
    for d in [80, 65, 50, 38]:
        transactions.append({
            "id": f"TX-1003-{d}",
            "customer_id": "CUST-1003",
            "amount": 5000.0,
            "type": "DEBIT",
            "category": "ATM Withdrawal",
            "description": "ATM CASH WITHDRAWAL",
            "timestamp": iso_days_ago(d)
        })
    # App logins active until 38 days ago, then nothing!
    for d in [75, 60, 48, 38]:
        behavior_events.append({
            "id": f"BEV-1003-{d}",
            "customer_id": "CUST-1003",
            "event_type": "APP_LOGIN",
            "channel": "YONO_MOBILE",
            "timestamp": iso_days_ago(d)
        })

    # ----------------------------------------------------
    # SCRIPTED CUSTOMER 4: Sunita Verma (INVESTMENT_MATURITY)
    # ----------------------------------------------------
    c4 = {
        "id": "CUST-1004",
        "cif_number": "CIF89230014",
        "full_name": "Sunita Verma",
        "email": "sunita.verma@example.in",
        "mobile": "+919820101004",
        "segment": "HNI",
        "kyc_verified": True,
        "relationship_type": "Wealth Management",
        "member_since": "2017-11-20",
        "account_balance": 2800000.0,
        "holdings": [
            {"product_code": "SB_PREM", "product_name": "SBI Savings Plus", "balance": 1300000.0},
            {
                "product_code": "FD_SPECIAL",
                "product_name": "SBI Tax Savings Fixed Deposit",
                "balance": 1500000.0,
                "maturity_date": (now + timedelta(days=8)).strftime("%Y-%m-%d"),
                "interest_rate": 7.1
            }
        ]
    }
    customers.append(c4)
    for d in [30, 15, 3]:
        transactions.append({
            "id": f"TX-1004-{d}",
            "customer_id": "CUST-1004",
            "amount": 25000.0,
            "type": "DEBIT",
            "category": "Investments",
            "description": "SIP DEBIT - SBI MUTUAL FUND",
            "timestamp": iso_days_ago(d)
        })
    for d in [12, 6, 1]:
        behavior_events.append({
            "id": f"BEV-1004-{d}",
            "customer_id": "CUST-1004",
            "event_type": "APP_LOGIN",
            "channel": "YONO_MOBILE",
            "timestamp": iso_days_ago(d)
        })

    # ----------------------------------------------------
    # REMAINING 26 BORING / UNREMARKABLE CUSTOMERS
    # ----------------------------------------------------
    indian_firsts = ["Aarav", "Vikram", "Rohan", "Deepak", "Sanjay", "Manoj", "Karan", "Suresh", "Ramesh", "Anand",
                     "Neha", "Anjali", "Pooja", "Kavita", "Swati", "Divya", "Meena", "Shalini", "Sneha", "Radhika",
                     "Nitin", "Tarun", "Gaurav", "Varun", "Mohit", "Ashish"]
    indian_lasts = ["Gupta", "Singh", "Reddy", "Nair", "Iyer", "Joshi", "Deshmukh", "Chauhan", "Bhatia", "Mehta",
                    "Malhotra", "Kapoor", "Chatterjee", "Roy", "Banerjee", "Sengupta", "Das", "Yadav", "Tiwari", "Mishra",
                    "Saxena", "Chopra", "Thakur", "Pandey", "Shukla", "Agrawal"]

    for idx in range(5, 31):
        cid = f"CUST-{1000 + idx}"
        fname = f"{indian_firsts[idx-5]} {indian_lasts[idx-5]}"
        c = {
            "id": cid,
            "cif_number": f"CIF892300{idx:02d}",
            "full_name": fname,
            "email": f"{fname.lower().replace(' ', '.')}@example.in",
            "mobile": f"+919820101{idx:03d}",
            "segment": "RETAIL" if idx % 3 != 0 else "WEALTH",
            "kyc_verified": True,
            "relationship_type": "Standard Savings",
            "member_since": f"20{18 + (idx % 5)}-05-14",
            "account_balance": float(50000 + (idx * 15000)),
            "holdings": [
                {"product_code": "SB_REG", "product_name": "SBI Regular Savings", "balance": float(50000 + (idx * 15000))}
            ]
        }
        customers.append(c)

        # Normal steady salary and spending
        for m in [60, 30]:
            transactions.append({
                "id": f"TX-{cid}-{m}-SAL",
                "customer_id": cid,
                "amount": float(60000 + (idx * 2000)),
                "type": "CREDIT",
                "category": "Salary",
                "description": "MONTHLY SALARY CREDIT",
                "timestamp": iso_days_ago(m)
            })
        for d in [45, 35, 25, 15, 5]:
            transactions.append({
                "id": f"TX-{cid}-{d}-DEB",
                "customer_id": cid,
                "amount": float(4000 + (idx * 300)),
                "type": "DEBIT",
                "category": "Groceries & Shopping",
                "description": "POS PURCHASE - SUPERMARKET",
                "timestamp": iso_days_ago(d)
            })
        for d in [14, 7, 2]:
            behavior_events.append({
                "id": f"BEV-{cid}-{d}",
                "customer_id": cid,
                "event_type": "APP_LOGIN",
                "channel": "YONO_MOBILE",
                "timestamp": iso_days_ago(d)
            })

    policy_rules = [
        {
            "rule_id": "TRAI_01",
            "name": "TRAI Outbound Calling Window",
            "condition": "channel == 'voice' and (hour < 9 or hour >= 21)",
            "action": "BLOCK_OUTREACH",
            "description": "Calls are strictly prohibited before 9:00 AM or after 9:00 PM IST."
        },
        {
            "rule_id": "RBI_01",
            "name": "Monthly Promotional Frequency Cap",
            "condition": "monthly_contact_count >= 4",
            "action": "BLOCK_OUTREACH",
            "description": "Maximum 4 proactive contacts permitted per calendar month."
        },
        {
            "rule_id": "RBI_02",
            "name": "Post-Decline Cooling Off",
            "condition": "hours_since_last_decline < 48",
            "action": "BLOCK_OUTREACH",
            "description": "Mandatory 48-hour cooling off period after customer declines an offer."
        },
        {
            "rule_id": "DPDP_01",
            "name": "Explicit Consent Verification",
            "condition": "purpose_code not in customer_consents",
            "action": "BLOCK_OUTREACH",
            "description": "Proactive outreach requires active customer consent for the specific product purpose."
        }
    ]

    with open(os.path.join(DATA_DIR, "customers.json"), "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2)
    with open(os.path.join(DATA_DIR, "transactions.json"), "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2)
    with open(os.path.join(DATA_DIR, "behavior_events.json"), "w", encoding="utf-8") as f:
        json.dump(behavior_events, f, indent=2)
    with open(os.path.join(DATA_DIR, "policy_rules.json"), "w", encoding="utf-8") as f:
        json.dump(policy_rules, f, indent=2)
    with open(os.path.join(DATA_DIR, "signals.json"), "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)
    with open(os.path.join(DATA_DIR, "hypotheses.json"), "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)
    with open(os.path.join(DATA_DIR, "cases.json"), "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)
    with open(os.path.join(DATA_DIR, "customer_memory.json"), "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)

    print(f"Seed data successfully generated: {len(customers)} customers, {len(transactions)} transactions.")

if __name__ == "__main__":
    generate()
