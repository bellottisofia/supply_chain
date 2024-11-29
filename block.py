# block.py

import hashlib
import json
from datetime import datetime
from transaction import Transaction
import config

class InvalidBlock(Exception):
    pass

class Block(object):
    def __init__(self, data=None):
        if data is None:
            self.index = 0
            self.timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.transactions = []
            self.previous_hash = '0' * 64
            self.nonce = 0
            self.miner = None
        else:
            try:
                self.index = data['index']
                self.timestamp = data['timestamp']
                self.transactions = [
                    Transaction(**t) if isinstance(t, dict) else t for t in data['transactions']
                ]
                self.previous_hash = data['previous_hash']
                self.nonce = data['nonce']
                self.miner = data.get('miner', None)
            except KeyError as e:
                raise InvalidBlock(f"Missing field {e}")

    def next(self, transactions):
        data = {
            'index': self.index + 1,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': [t.data for t in transactions],
            'previous_hash': self.hash(),
            'nonce': 0
        }
        return Block(data)

    def hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.data for t in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }

    def __str__(self):
        return f"Block #{self.index} [Prev Hash: {self.previous_hash}, Hash: {self.hash()}]"

    def valid_proof(self, difficulty=config.default_difficulty):
        if self.index == 0:
            return True
        return self.hash().startswith('0' * difficulty)

    def mine(self, difficulty=config.default_difficulty):
        while not self.valid_proof(difficulty):
            self.nonce += 1

    def validity(self):
        if self.index == 0:
            return True
        if not self.valid_proof():
            return False
        return True

    def log(self):
        print(f"Block #{self.index} with {len(self.transactions)} transactions")