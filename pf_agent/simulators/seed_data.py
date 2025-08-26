"""Deterministic seed data for simulator"""

import random
from datetime import datetime, timedelta
from typing import Dict, List


# Seed for deterministic data generation
RANDOM_SEED = 42


def generate_instance_data() -> Dict[str, Dict]:
    """Generate deterministic mock data for PF instances"""
    random.seed(RANDOM_SEED)
    
    # Base date for license expiry calculations
    base_date = datetime.now()
    
    instances = {
        "pf1": {
            "issuedTo": "Acme Corporation",
            "product": "PingFederate",
            "expiryDate": (base_date + timedelta(days=45)).strftime("%Y-%m-%d"),
            "licenseKeyId": "LIC-PROD-ABC123"
        },
        "pf2": {
            "issuedTo": "Acme Corporation", 
            "product": "PingFederate",
            "expiryDate": (base_date + timedelta(days=120)).strftime("%Y-%m-%d"),
            "licenseKeyId": "LIC-PROD-DEF456"
        },
        "pf3": {
            "issuedTo": "Acme Corporation",
            "product": "PingFederate",
            "expiryDate": (base_date + timedelta(days=15)).strftime("%Y-%m-%d"),  # WARNING
            "licenseKeyId": "LIC-STAGE-GHI789"
        },
        "pf4": {
            "issuedTo": "Acme Corporation",
            "product": "PingFederate", 
            "expiryDate": (base_date + timedelta(days=90)).strftime("%Y-%m-%d"),
            "licenseKeyId": "LIC-DEV-JKL012"
        },
        "pf5": {
            "issuedTo": "Acme Corporation",
            "product": "PingFederate",
            "expiryDate": (base_date - timedelta(days=5)).strftime("%Y-%m-%d"),  # EXPIRED
            "licenseKeyId": "LIC-DEV-MNO345"
        }
    }
    
    return instances


def generate_cluster_status() -> Dict:
    """Generate mock cluster status data"""
    return {
        "nodes": [
            {"id": "pf1", "status": "ACTIVE", "role": "ADMIN"},
            {"id": "pf2", "status": "ACTIVE", "role": "ENGINE"},
            {"id": "pf3", "status": "ACTIVE", "role": "ENGINE"},
            {"id": "pf4", "status": "ACTIVE", "role": "ENGINE"}, 
            {"id": "pf5", "status": "ACTIVE", "role": "ENGINE"}
        ],
        "cluster_state": "ACTIVE",
        "last_config_update": datetime.now().isoformat()
    }
