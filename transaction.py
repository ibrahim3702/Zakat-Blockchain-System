
# transaction.py
import json
from datetime import datetime

class Transaction:
    def __init__(self, sender, receiver, amount, transaction_type='Transfer', zakat_payment=False):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.transaction_type = transaction_type
        self.zakat_payment = zakat_payment
        self.timestamp = datetime.now().isoformat()
        self.remaining_balance = None
    
    def set_remaining_balance(self, balance):
        self.remaining_balance = balance
    
    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'zakat_payment': self.zakat_payment,
            'remaining_balance': self.remaining_balance,
            'transaction_type': self.transaction_type,
            'timestamp': self.timestamp
        }
    
    def __str__(self):
        zakat_marker = " [ZAKAT]" if self.zakat_payment else ""
        return f"{self.sender} => {self.receiver}: {self.amount} coins{zakat_marker}"
