import requests
from typing import Dict, List, Optional, Union
import json

class Intram:
    """
    Python implementation of Intram payment integration
    """
    
    BASE_URL = "https://webservices.intram.org:4002/api/v1/"
    BASE_URL_SANDBOX = "https://webservices.intram.org:4002/api/v1/"
    VERIFY_URL = "/transactions/confirm/"
    PAYOUT_URL = "payments/request"

    def __init__(
        self,
        public_key: str,
        private_key: str,
        secret: str,
        marchand_id: str,
        sandbox: bool = False
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.secret = secret
        self.marchand_id = marchand_id
        self.sandbox = "sandbox" if sandbox else "live"
        self.const = self.BASE_URL_SANDBOX if sandbox else self.BASE_URL
        
        self.redirection_url = None
        self.items = []
        self.amount = 0
        self.devise = None
        self.cancel_url = None 
        self.return_url = None
        self.generate_url = None
        self.tva = []
        self.description = None
        self.name_store = None
        self.postal_address_store = None
        self.phone_store = None
        self.logo_url_store = None
        self.website_url_store = None
        self.template = "default"
        self.custom_data = None
        self.currency = None
        
        self.headers = {
            "X-API-KEY": self.public_key,
            "X-PRIVATE-KEY": self.private_key,
            "X-SECRET-KEY": self.secret,
            "X-MARCHAND-KEY": self.marchand_id,
            "Content-Type": "application/json"
        }
        
        self.keys = {
            "public": self.public_key,
            "private": self.private_key,
            "secret": self.secret
        }

    
    def get_transaction_status(self, transaction_id: str) -> Dict:
        """
        Get status of a transaction
        
        Args:
            transaction_id: ID of transaction to check
            
        Returns:
            dict: Transaction status response
        """
        if not all([transaction_id, self.private_key, self.public_key, self.secret]):
            return {"status": "ERROR: KEY MISSING"}
            
        try:
            response = requests.get(
                f"{self.const}{self.VERIFY_URL}{transaction_id}",
                headers=self.headers,
                verify=False
            )
            return response.json()
            
        except Exception as e:
            return {"status": "ERROR INITIALIZE TRANSACTION CONFIRMATION"}

    def set_request_payment(self) -> Dict:
        """
        Initialize a payment request
        
        Returns:
            dict: Payment request response
        """
        required_fields = [
            self.currency,
            #self.items,
            self.amount,
            self.name_store,
            self.template,
            self.private_key,
            self.public_key,
            self.secret
        ]
        
        if not all(required_fields):
            return {"status": "ERROR: KEY MISSING"}
            
        try:
            # Prepare request data
            invoice = {
                "keys": self.keys,
                "currency": self.currency,
                "items": self.items,
                "taxes": self.tva,
                "amount": self.amount,
                "description": self.description,
                "custom_datas": self.custom_data
            }
            
            actions = {
                "cancel_url": self.cancel_url,
                "return_url": self.return_url,
                "callback_url": self.redirection_url
            }
            
            store = {
                "name": self.name_store,
                "postal_adress": self.postal_address_store,
                "logo_url": self.logo_url_store,
                "web_site_url": self.website_url_store,
                "phone": self.phone_store,
                "template": self.template
            }
            
            payload = {
                "invoice": invoice,
                "store": store,
                "actions": actions
            }
            
            response = requests.post(
                f"{self.const}{self.PAYOUT_URL}",
                headers=self.headers,
                json=payload,
                verify=False
            )
            
            return response.json()
            
        except Exception as e:
            return {"status": "ERROR INITIALIZE TRANSACTION CONFIRMATION"}

    # Getters and setters
    def get_currency(self) -> Optional[str]:
        return self.currency
        
    def set_currency(self, currency: str) -> None:
        self.currency = currency
        
    def get_description(self) -> Optional[str]:
        return self.description
        
    def set_description(self, description: str) -> None:
        self.description = description
        
    def get_items(self) -> List:
        return self.items
        
    def set_items(self, items: List) -> None:
        self.items = items
        
    def get_amount(self) -> Union[int, float]:
        return self.amount
        
    def set_amount(self, amount: Union[int, float]) -> None:
        self.amount = amount
        
    def get_tva(self) -> List:
        return self.tva
        
    def set_tva(self, tva: List) -> None:
        self.tva = tva
        
    def get_name_store(self) -> Optional[str]:
        return self.name_store
        
    def set_name_store(self, name_store: str) -> None:
        self.name_store = name_store
        
    def get_postal_address_store(self) -> Optional[str]:
        return self.postal_address_store
        
    def set_postal_address_store(self, address: str) -> None:
        self.postal_address_store = address
        
    def get_phone_store(self) -> Optional[str]:
        return self.phone_store
        
    def set_phone_store(self, phone: str) -> None:
        self.phone_store = phone
        
    def get_logo_url_store(self) -> Optional[str]:
        return self.logo_url_store
        
    def set_logo_url_store(self, url: str) -> None:
        self.logo_url_store = url
        
    def get_website_url_store(self) -> Optional[str]:
        return self.website_url_store
        
    def set_website_url_store(self, url: str) -> None:
        self.website_url_store = url
        
    def get_template(self) -> Optional[str]:
        return self.template
        
    def set_template(self, template: str) -> None:
        self.template = template
        
    def get_custom_data(self) -> Optional[Dict]:
        return self.custom_data
        
    def set_custom_data(self, data: Dict) -> None:
        self.custom_data = data
        
    def get_redirection_url(self) -> Optional[str]:
        return self.redirection_url
        
    def set_redirection_url(self, url: str) -> None:
        self.redirection_url = url
        
    def get_cancel_url(self) -> Optional[str]:
        return self.cancel_url
        
    def set_cancel_url(self, url: str) -> None:
        self.cancel_url = url
        
    def get_return_url(self) -> Optional[str]:
        return self.return_url
        
    def set_return_url(self, url: str) -> None:
        self.return_url = url
