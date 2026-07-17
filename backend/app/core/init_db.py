"""Database initialization and seeding for SQLite."""

import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from app.models.base import Base
from app.models.user import User
from app.models.endpoint import Endpoint
from app.models.model_evaluation import ModelEvaluation
from app.core.security import get_password_hash


def compute_risk_tier(ep_data: dict) -> tuple[str, float]:
    alg_risk = {"RSA-2048": 0.60, "RSA-4096": 0.30, "ECC-256": 0.50, "ECC-384": 0.20}
    exp_risk = {"internet-facing": 1.0, "internal": 0.4, "air-gapped": 0.1}
    traf_risk = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.1}

    cert_urgency = max(0.0, (90.0 - ep_data["cert_expiry_days"]) / 120.0)
    cert_urgency = min(1.0, cert_urgency)

    score = (
        alg_risk[ep_data["algorithm"]] * 0.30
        + (ep_data["data_sensitivity"] / 5.0) * 0.25
        + exp_risk[ep_data["exposure_surface"]] * 0.20
        + traf_risk[ep_data["traffic_volume"]] * 0.15
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


def initialize_sqlite_db(sync_engine):
    """Initialize SQLite database with default tables and seed data if empty."""
    import sys
    is_sqlite = sync_engine.url.drivername.startswith("sqlite")
    if not is_sqlite:
        return

    # Check if the database tables need to be created
    inspector = inspect(sync_engine)
    if not inspector.has_table("users"):
        print("Initializing database tables...")
        Base.metadata.create_all(sync_engine)

    # Do not seed default data if we are running unit tests
    if "pytest" in sys.modules:
        return

    session = Session(sync_engine)

    try:
        # Check if database is already seeded
        admin_exists = session.query(User).filter(User.username == "admin").first()
        if admin_exists:
            return

        print("Seeding database...")

        # 1. Admin user
        hashed_password = get_password_hash("fortiq-demo-2024")
        admin = User(username="admin", hashed_password=hashed_password)
        session.add(admin)

        # 2. Model evaluations
        session.add(ModelEvaluation(
            model_type="vqc", binary_class="all",
            accuracy=0.8542, precision_score=0.8610,
            recall=0.8542, f1_score=0.8521,
            training_samples=80, test_samples=20,
        ))
        session.add(ModelEvaluation(
            model_type="svm", binary_class="all",
            accuracy=0.8000, precision_score=0.8125,
            recall=0.8000, f1_score=0.7981,
            training_samples=80, test_samples=20,
        ))

        # 3. Endpoints
        random.seed(42)
        endpoint_types = ["api", "database", "iot", "firmware", "web"]
        algorithms = ["RSA-2048", "RSA-4096", "ECC-256", "ECC-384"]
        algo_weights = [0.55, 0.20, 0.15, 0.10]
        key_lengths = {"RSA-2048": 2048, "RSA-4096": 4096, "ECC-256": 256, "ECC-384": 384}
        exposures = ["internet-facing", "internal", "air-gapped"]
        exposure_weights = [0.40, 0.45, 0.15]
        traffics = ["low", "medium", "high", "critical"]
        traffic_weights = [0.25, 0.40, 0.25, 0.10]

        prefixes = {
            "api": ["api-gateway", "auth-service", "payment-api", "user-service", "order-api"],
            "database": ["postgres-primary", "redis-cluster", "mongo-replica", "mysql-slave", "cache-db"],
            "iot": ["sensor-hub", "device-controller", "iot-gateway", "smart-meter", "edge-node"],
            "firmware": ["firmware-updater", "boot-loader", "hw-manager", "chip-controller", "device-mgr"],
            "web": ["web-frontend", "admin-portal", "dashboard-ui", "customer-app", "internal-tool"],
        }

        def weighted_choice(items, weights):
            return random.choices(items, weights=weights)[0]

        endpoints = []
        for i in range(100):
            ep_type = random.choice(endpoint_types)
            algo = weighted_choice(algorithms, algo_weights)
            exp = weighted_choice(exposures, exposure_weights)
            traf = weighted_choice(traffics, traffic_weights)

            ports = {
                "api": [8080, 8000, 3000, 443],
                "database": [5432, 3306, 6379, 27017],
                "iot": [1883, 8883, 5683],
                "firmware": [22, 8443, 9000],
                "web": [80, 443, 8080],
            }
            port = random.choice(ports[ep_type])

            data_sens = max(1, min(5, int(random.normalvariate(3, 1.2))))
            cert_expiry = random.randint(-30, 730)

            subnet = random.choice([10, 20, 30, 40, 50])
            host = f"10.{subnet}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            name = f"{random.choice(prefixes[ep_type])}-{random.choice(['prod', 'staging', 'dev'])}-{i:03d}"

            ep_data = {
                "name": name,
                "host": host,
                "port": port,
                "endpoint_type": ep_type,
                "algorithm": algo,
                "key_length": key_lengths[algo],
                "data_sensitivity": data_sens,
                "exposure_surface": exp,
                "traffic_volume": traf,
                "cert_expiry_days": cert_expiry,
            }

            tier, score = compute_risk_tier(ep_data)
            ep_data["risk_tier"] = tier
            ep_data["risk_score"] = score
            ep_data["migration_status"] = "pending"

            endpoints.append(ep_data)

        # Balance distribution
        current = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for ep in endpoints:
            current[ep["risk_tier"]] += 1

        target = {"critical": 15, "high": 30, "medium": 35, "low": 20}
        for ep in endpoints:
            tier = ep["risk_tier"]
            if tier == "critical" and current["critical"] > target["critical"] + 5:
                ep["cert_expiry_days"] = random.randint(200, 730)
                ep["data_sensitivity"] = max(1, ep["data_sensitivity"] - 1)
                new_tier, new_score = compute_risk_tier(ep)
                if new_tier != "critical":
                    current["critical"] -= 1
                    current[new_tier] += 1
                    ep["risk_tier"] = new_tier
                    ep["risk_score"] = new_score
            elif tier == "low" and current["low"] > target["low"] + 5:
                ep["cert_expiry_days"] = random.randint(-30, 60)
                ep["data_sensitivity"] = min(5, ep["data_sensitivity"] + 1)
                new_tier, new_score = compute_risk_tier(ep)
                if new_tier != "low":
                    current["low"] -= 1
                    current[new_tier] += 1
                    ep["risk_tier"] = new_tier
                    ep["risk_score"] = new_score

        for ep_data in endpoints:
            session.add(Endpoint(**ep_data))

        session.commit()
        print("Database successfully seeded.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()
