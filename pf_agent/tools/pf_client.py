"""PingFederate REST client"""

import requests
from typing import Dict, Any
from ..config import InstanceConfig
from ..domain.models import LicenseView, ApplyLicenseRequest, LicenseAgreement


class PFClient:
    """REST client for PingFederate APIs"""
    
    def __init__(self, timeout: int = 30) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        # In real implementation, add auth headers here
        # self.session.headers.update({"Authorization": "Bearer <token>"})
    
    def get_license(self, instance: InstanceConfig) -> LicenseView:
        """Get license information from PingFederate instance"""
        url = f"{instance.base_url}/license"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return LicenseView(**data)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to get license from {instance.id}: {e}")
    
    def put_license(self, instance: InstanceConfig, encoded_license: str) -> LicenseView:
        """Apply a new license to PingFederate instance"""
        url = f"{instance.base_url}/license"
        
        request_data = ApplyLicenseRequest(value=encoded_license)
        
        try:
            response = self.session.put(
                url, 
                json=request_data.model_dump(),
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return LicenseView(**data)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to apply license to {instance.id}: {e}")
    
    def get_license_agreement(self, instance: InstanceConfig) -> LicenseAgreement:
        """Get license agreement status"""
        url = f"{instance.base_url}/license/agreement"
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return LicenseAgreement(**data)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to get license agreement from {instance.id}: {e}")
    
    def put_license_agreement(self, instance: InstanceConfig, agreement: LicenseAgreement) -> LicenseAgreement:
        """Update license agreement status"""
        url = f"{instance.base_url}/license/agreement"
        
        try:
            response = self.session.put(
                url,
                json=agreement.model_dump(),
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return LicenseAgreement(**data)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to update license agreement for {instance.id}: {e}")
