# blockchain.py

import config
from block import Block, InvalidBlock
from transaction import Transaction

class Blockchain(object):
    def __init__(self):
        self.chain = [Block()]
        self.mempool = []

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if transaction.verify() and transaction not in self.mempool:
            self.mempool.append(transaction)
            return True
        else:
            return False

    def new_block(self, block=None):
        if block is None:
            block = self.last_block
        transactions = self.mempool[:config.blocksize]
        self.mempool = self.mempool[config.blocksize:]
        new_block = block.next(transactions)
        return new_block

    def extend_chain(self, block):
        if block.previous_hash != self.last_block.hash():
            raise InvalidBlock("Invalid previous hash")
        if block.index != self.last_block.index + 1:
            raise InvalidBlock("Invalid index")
        if not block.validity():
            raise InvalidBlock("Invalid block")
        self.chain.append(block)

    def __str__(self):
        return f"Blockchain: {len(self.chain)} blocks"

    def validity(self):
        if self.chain[0].index != 0:
            return False
        used_transactions = set()
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            prev_block = self.chain[i - 1]
            if block.previous_hash != prev_block.hash():
                return False
            if not block.validity():
                return False
            for t in block.transactions:
                tx_hash = t.hash()
                if tx_hash in used_transactions:
                    return False
                used_transactions.add(tx_hash)
        return True

    def __len__(self):
        return len(self.chain)

    def merge(self, other):
        if len(other.chain) > len(self.chain) and other.validity():
            self.chain = other.chain.copy()
            self.mempool = other.mempool.copy()

    def log(self):
        print(self)
        for b in self.chain:
            b.log()