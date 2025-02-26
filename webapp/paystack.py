import requests 
from django.conf import settings

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment (self, ref, amount):
        url = f"{self.base_url}/transaction/verify/{ref}";
        headers = {
            "Authorization":f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json().get("data", {})
            if result.get("amount") == int(amount*100):
                return True, result
            return False, response.json().get("message", "Verification failed")
