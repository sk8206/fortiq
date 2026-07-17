"""Migration configuration generator."""

from app.models.endpoint import Endpoint


def generate_migration_configs(endpoint: Endpoint) -> list[str]:
    """Generate PQC migration configs for endpoint.

    Args:
        endpoint: Endpoint model instance

    Returns:
        List of configuration text strings
    """
    configs = []

    if endpoint.endpoint_type == "api":
        configs.append(_generate_api_config(endpoint))
    elif endpoint.endpoint_type == "database":
        configs.append(_generate_database_config(endpoint))
    elif endpoint.endpoint_type == "iot":
        configs.append(_generate_iot_config(endpoint))
    elif endpoint.endpoint_type == "firmware":
        configs.append(_generate_firmware_config(endpoint))
    elif endpoint.endpoint_type == "web":
        configs.append(_generate_web_config(endpoint))

    return configs


def _generate_api_config(endpoint: Endpoint) -> str:
    """Generate Nginx TLS config for API endpoint."""
    return f"""# Nginx TLS Configuration for {endpoint.name}
# Post-Quantum Cryptography Migration

server {{
    listen {endpoint.port} ssl http2;
    server_name {endpoint.host};

    # PQC Certificate Chain
    ssl_certificate /etc/nginx/certs/{endpoint.name}-mlkem768.crt;
    ssl_certificate_key /etc/nginx/certs/{endpoint.name}-mlkem768.key;

    # PQC Cipher Suites (ML-KEM-768 + ML-DSA-65)
    ssl_protocols TLSv1.3;
    ssl_ciphers 'TLS_MLKEM768X25519_ECDSA_WITH_AES_256_GCM_SHA384';
    ssl_prefer_server_ciphers on;

    # Hybrid Mode (Classical + PQC)
    ssl_ecdh_curve mlkem768:x25519:secp384r1;

    # HSTS with PQC
    add_header Strict-Transport-Security "max-age=31536000" always;
}}
"""


def _generate_database_config(endpoint: Endpoint) -> str:
    """Generate PostgreSQL SSL config for database endpoint."""
    return f"""# PostgreSQL SSL Configuration for {endpoint.name}
# Post-Quantum Cryptography Migration
# Signature Algorithm: ML-DSA-65 (FIPS 204)

# postgresql.conf
ssl = on
ssl_cert_file = '/var/lib/postgresql/certs/{endpoint.name}-mldsa65.crt'
ssl_key_file = '/var/lib/postgresql/certs/{endpoint.name}-mldsa65.key'
ssl_ca_file = '/var/lib/postgresql/certs/pqc-ca.crt'

# PQC Cipher Suites
ssl_ciphers = 'TLS_MLKEM768X25519_RSA_WITH_AES_256_GCM_SHA384'
ssl_prefer_server_ciphers = on
ssl_min_protocol_version = 'TLSv1.3'

# Client Certificate Verification
ssl_ca_file = '/var/lib/postgresql/certs/pqc-client-ca.crt'
"""


def _generate_iot_config(endpoint: Endpoint) -> str:
    """Generate MQTT TLS config for IoT endpoint."""
    return f"""# MQTT TLS Configuration for {endpoint.name}
# Post-Quantum Cryptography Migration

# mosquitto.conf
listener {endpoint.port}
protocol mqtt

# PQC Certificates
certfile /etc/mosquitto/certs/{endpoint.name}-mlkem768.crt
keyfile /etc/mosquitto/certs/{endpoint.name}-mlkem768.key
cafile /etc/mosquitto/certs/pqc-ca.crt

# TLS Configuration
tls_version tlsv1.3
ciphers TLS_MLKEM768X25519_ECDSA_WITH_CHACHA20_POLY1305_SHA256

# Client Authentication
require_certificate true
use_identity_as_username true
"""


def _generate_firmware_config(endpoint: Endpoint) -> str:
    """Generate firmware certificate config."""
    return f"""# Firmware Certificate Chain for {endpoint.name}
# Post-Quantum Cryptography Migration

# Certificate Chain
Certificate: {endpoint.name}-mldsa65.crt
  Subject: CN={endpoint.name}
  Issuer: CN=Fortiq PQC CA
  Signature Algorithm: ML-DSA-65
  Public Key: ML-KEM-768 (1184 bytes)
  Valid From: 2026-01-01
  Valid To: 2027-01-01

# Verification Command
$ fortiq-verify --cert {endpoint.name}-mldsa65.crt --ca pqc-ca.crt --algorithm ML-DSA-65

# Firmware Update Command
$ fortiq-flash --firmware {endpoint.name}.bin --cert {endpoint.name}-mldsa65.crt --verify
"""


def _generate_web_config(endpoint: Endpoint) -> str:
    """Generate Apache/Node.js TLS config for web endpoint."""
    return f"""# Apache TLS Configuration for {endpoint.name}
# Post-Quantum Cryptography Migration

<VirtualHost *:{endpoint.port}>
    ServerName {endpoint.host}

    # PQC SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/apache2/certs/{endpoint.name}-mlkem768.crt
    SSLCertificateKeyFile /etc/apache2/certs/{endpoint.name}-mlkem768.key
    SSLCertificateChainFile /etc/apache2/certs/pqc-chain.crt

    # PQC Cipher Suite
    SSLProtocol TLSv1.3
    SSLCipherSuite TLS_MLKEM768X25519_RSA_WITH_AES_256_GCM_SHA384
    SSLHonorCipherOrder on

    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000"
</VirtualHost>
"""
