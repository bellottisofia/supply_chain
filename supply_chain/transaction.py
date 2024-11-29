# transaction.py

import json
import hashlib
from datetime import datetime
from ecdsa import VerifyingKey, BadSignatureError

class IncompleteTransaction(Exception):
    pass

class Transaction(object):
    def __init__(self, product_id, event, date=None, signature=None, public_key=None, author=None):
        self.product_id = product_id
        self.event = event  # E.g., "ProductCreated", "StatusUpdated to Manufactured"
        self.date = date or datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.signature = signature
        self.public_key = public_key
        self.author = author

    @property
    def data(self):
        return {
            "product_id": self.product_id,
            "event": self.event,
            "date": self.date,
            "signature": self.signature,
            "public_key": self.public_key,
            "author": self.author,
        }

    def json_dumps(self):
        return json.dumps(self.data, sort_keys=True)

    def sign(self, private_key):
        self.public_key = private_key.verifying_key.to_pem().decode()
        self.author = hashlib.sha256(self.public_key.encode()).hexdigest()
        message = f"{self.product_id}{self.event}{self.date}".encode()
        self.signature = private_key.sign(message).hex()

    def verify(self):
        if not self.signature or not self.public_key:
            return False
        try:
            vk = VerifyingKey.from_pem(self.public_key.encode())
            message = f"{self.product_id}{self.event}{self.date}".encode()
            vk.verify(bytes.fromhex(self.signature), message)
            return True
        except BadSignatureError:
            return False

    def __str__(self):
        return f"Transaction for product {self.product_id}: {self.event}"

    def __lt__(self, other):
        return self.date < other.date

    def hash(self):
        transaction_string = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()