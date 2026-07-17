"""Tests for PQC operations."""

import pytest

from app.pqc.operations import demo_ml_kem_768, demo_ml_dsa_65


def test_demo_ml_kem_768():
    """Test ML-KEM-768 demo returns expected structure."""
    result = demo_ml_kem_768()

    assert result["algorithm"] == "ML-KEM-768"
    assert result["fips_standard"] == "FIPS 203"
    assert result["nist_security_level"] == 3
    assert result["public_key_bytes"] == 1184
    assert result["ciphertext_bytes"] == 1088
    assert result["shared_secret_bytes"] == 32
    assert isinstance(result["encapsulation_ok"], bool)
    assert isinstance(result["decapsulation_ok"], bool)


def test_demo_ml_dsa_65():
    """Test ML-DSA-65 demo returns expected structure."""
    result = demo_ml_dsa_65()

    assert result["algorithm"] == "ML-DSA-65"
    assert result["fips_standard"] == "FIPS 204"
    assert result["nist_security_level"] == 3
    assert result["public_key_bytes"] == 1952
    assert result["signature_bytes"] == 3293
    assert isinstance(result["verification_passed"], bool)
