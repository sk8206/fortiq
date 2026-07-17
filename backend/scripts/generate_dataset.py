#!/usr/bin/env python3
"""Generate 100 synthetic endpoints with realistic risk distribution.

Usage: python scripts/generate_dataset.py
"""

import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import SyncSessionLocal
from app.models.endpoint import Endpoint


# Constants from PRD
ENDPOINT_TYPES = ["api", "database", "iot", "firmware", "web"]
ALGORITHMS = ["RSA-2048", "RSA-4096", "ECC-256", "ECC-384"]
ALGORITHM_KEY_LENGTHS = {
    "RSA-2048": 2048,
    "RSA-4096": 4096,
    "ECC-256": 256,
    "ECC-384": 384,
}
EXPOSURE_SURFACES = ["internet-facing", "internal", "air-gapped"]
TRAFFIC_VOLUMES = ["low", "medium", "high", "critical"]

# Distribution targets from PLAN.md
ALGORITHM_WEIGHTS = [0.55, 0.20, 0.15, 0.10]  # RSA-2048, RSA-4096, ECC-256, ECC-384
EXPOSURE_WEIGHTS = [0.40, 0.45, 0.15]  # internet-facing, internal, air-gapped
TRAFFIC_WEIGHTS = [0.25, 0.40, 0.25, 0.10]  # low, medium, high, critical

# Risk scoring weights from PLAN.md
ALG_RISK = {"RSA-2048": 0.60, "RSA-4096": 0.30, "ECC-256": 0.50, "ECC-384": 0.20}
EXP_RISK = {"internet-facing": 1.0, "internal": 0.4, "air-gapped": 0.1}
TRAF_RISK = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.1}


def compute_risk_tier(row: dict) -> tuple[str, float]:
    """Compute risk tier and score from endpoint attributes."""
    cert_urgency = max(0, (90 - row["cert_expiry_days"]) / 120)
    cert_urgency = min(1.0, cert_urgency)

    score = (
        ALG_RISK[row["algorithm"]] * 0.30
        + (row["data_sensitivity"] / 5.0) * 0.25
        + EXP_RISK[row["exposure_surface"]] * 0.20
        + TRAF_RISK[row["traffic_volume"]] * 0.15
        + cert_urgency * 0.10
    )
    score = min(max(score, 0.0), 1.0)

    if score > 0.75:
        tier = "critical"
    elif score > 0.50:
        tier = "high"
    elif score > 0.25:
        tier = "medium"
    else:
        tier = "low"

    return tier, round(score, 4)


def generate_ip_address(subnet_base: int) -> str:
    """Generate IP address in 10.x.x.x range."""
    return f"10.{subnet_base}.{random.randint(1, 254)}.{random.randint(1, 254)}"


def generate_endpoint_name(idx: int, endpoint_type: str) -> str:
    """Generate a realistic endpoint name."""
    prefixes = {
        "api": ["api-gateway", "auth-service", "payment-api", "user-service", "order-api"],
        "database": ["postgres-primary", "redis-cluster", "mongo-replica", "mysql-slave", "cache-db"],
        "iot": ["sensor-hub", "device-controller", "iot-gateway", "smart-meter", "edge-node"],
        "firmware": ["firmware-updater", "boot-loader", "hw-manager", "chip-controller", "device-mgr"],
        "web": ["web-frontend", "admin-portal", "dashboard-ui", "customer-app", "internal-tool"],
    }
    prefix = random.choice(prefixes[endpoint_type])
    env = random.choice(["prod", "staging", "dev"])
    return f"{prefix}-{env}-{idx:03d}"


def generate_endpoints(n: int = 100) -> list[dict]:
    """Generate n synthetic endpoints."""
    endpoints = []

    for i in range(n):
        endpoint_type = random.choice(ENDPOINT_TYPES)
        algorithm = random.choices(ALGORITHMS, weights=ALGORITHM_WEIGHTS)[0]
        exposure = random.choices(EXPOSURE_SURFACES, weights=EXPOSURE_WEIGHTS)[0]
        traffic = random.choices(TRAFFIC_VOLUMES, weights=TRAFFIC_WEIGHTS)[0]

        # Data sensitivity: normal distribution centered at 3
        data_sensitivity = int(np.clip(np.random.normal(3, 1.2), 1, 5))

        # Cert expiry: uniform -30 to 730 (negative = expired)
        cert_expiry_days = random.randint(-30, 730)

        # Port based on type
        port_ranges = {
            "api": [8080, 8000, 3000, 443],
            "database": [5432, 3306, 6379, 27017],
            "iot": [1883, 8883, 5683],
            "firmware": [22, 8443, 9000],
            "web": [80, 443, 8080],
        }
        port = random.choice(port_ranges[endpoint_type])

        # Generate subnet groups (for network graph edges)
        subnet_base = random.choice([10, 20, 30, 40, 50])

        endpoint = {
            "name": generate_endpoint_name(i, endpoint_type),
            "host": generate_ip_address(subnet_base),
            "port": port,
            "endpoint_type": endpoint_type,
            "algorithm": algorithm,
            "key_length": ALGORITHM_KEY_LENGTHS[algorithm],
            "data_sensitivity": data_sensitivity,
            "exposure_surface": exposure,
            "traffic_volume": traffic,
            "cert_expiry_days": cert_expiry_days,
        }

        # Compute risk
        tier, score = compute_risk_tier(endpoint)
        endpoint["risk_tier"] = tier
        endpoint["risk_score"] = score
        endpoint["migration_status"] = "pending"

        endpoints.append(endpoint)

    return endpoints


def balance_distribution(endpoints: list[dict], target: dict) -> list[dict]:
    """Balance the tier distribution to match targets."""
    # Target: ~15 Critical, ~30 High, ~35 Medium, ~20 Low
    current = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for ep in endpoints:
        current[ep["risk_tier"]] += 1

    print(f"Initial distribution: {current}")

    # Adjust by modifying attributes to shift risk scores
    for ep in endpoints:
        tier = ep["risk_tier"]

        # If we have too many of a tier, try to shift some
        if tier == "critical" and current["critical"] > target["critical"] + 5:
            # Lower risk by improving cert expiry
            ep["cert_expiry_days"] = random.randint(200, 730)
            ep["data_sensitivity"] = max(1, ep["data_sensitivity"] - 1)
            new_tier, new_score = compute_risk_tier(ep)
            if new_tier != "critical":
                current["critical"] -= 1
                current[new_tier] += 1
                ep["risk_tier"] = new_tier
                ep["risk_score"] = new_score

        elif tier == "low" and current["low"] > target["low"] + 5:
            # Increase risk by degrading cert expiry
            ep["cert_expiry_days"] = random.randint(-30, 60)
            ep["data_sensitivity"] = min(5, ep["data_sensitivity"] + 1)
            new_tier, new_score = compute_risk_tier(ep)
            if new_tier != "low":
                current["low"] -= 1
                current[new_tier] += 1
                ep["risk_tier"] = new_tier
                ep["risk_score"] = new_score

    print(f"Adjusted distribution: {current}")
    return endpoints


def main():
    """Generate and insert synthetic endpoints."""
    print("Generating 100 synthetic endpoints...")

    # Set seed for reproducibility
    random.seed(42)
    np.random.seed(42)

    endpoints = generate_endpoints(100)

    # Balance distribution
    target = {"critical": 15, "high": 30, "medium": 35, "low": 20}
    endpoints = balance_distribution(endpoints, target)

    # Save to CSV
    df = pd.DataFrame(endpoints)
    csv_path = Path(__file__).parent.parent / "data" / "endpoints_synthetic.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved to {csv_path}")

    # Insert to database
    print("Inserting into database...")
    session = SyncSessionLocal()
    try:
        # Clear existing endpoints
        session.query(Endpoint).delete()
        session.commit()

        for ep_data in endpoints:
            endpoint = Endpoint(**ep_data)
            session.add(endpoint)

        session.commit()
        print(f"Inserted {len(endpoints)} endpoints into database.")

        # Verify distribution
        from sqlalchemy import func

        dist = (
            session.query(Endpoint.risk_tier, func.count(Endpoint.id))
            .group_by(Endpoint.risk_tier)
            .all()
        )
        print("Final distribution in DB:")
        for tier, count in dist:
            print(f"  {tier}: {count}")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
