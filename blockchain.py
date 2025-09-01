from datetime import datetime
import json
from miner import Miner
from block import Block
from transaction import Transaction
class ZakatBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.participants = {}
        self.zakat_collector = "Zakat_Fund"
        self.miner = Miner()
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], '0')
        self.miner.mine_block(genesis_block)
        self.chain.append(genesis_block)
        self.participants[self.zakat_collector] = 0
    
    def register_participant(self, roll_number, initial_balance=200):
        """Register a new participant with initial balance"""
        if roll_number in self.participants:
            return False, f"Participant {roll_number} already exists"
        
        self.participants[roll_number] = initial_balance
        
        # Create initialization transaction
        transaction = Transaction('System', roll_number, initial_balance, 'Initialization')
        transaction.set_remaining_balance(initial_balance)
        
        self.pending_transactions.append(transaction)
        
        # Auto-mine block
        self.mine_pending_transactions()
        
        return True, f"Participant {roll_number} registered with {initial_balance} coins"
    
    def add_transaction(self, sender, receiver, amount, transaction_type='Transfer'):
        """Add a transaction between participants"""
        if sender not in self.participants:
            return False, f"Sender {sender} is not registered"
        if receiver not in self.participants:
            return False, f"Receiver {receiver} is not registered"
        if self.participants[sender] < amount:
            return False, f"Insufficient balance. {sender} has {self.participants[sender]} coins"
        
        # Update balances
        self.participants[sender] -= amount
        self.participants[receiver] += amount
        # Create transaction
        transaction = Transaction(sender, receiver, amount, transaction_type)
        transaction.set_remaining_balance(self.participants[sender])
        self.pending_transactions.append(transaction)
        # Auto-mine block
        self.mine_pending_transactions()
        return True, transaction
    
    def calculate_zakat(self, participant):
        """Calculate 2.5% zakat for a participant"""
        if participant not in self.participants:
            return 0
        return round(self.participants[participant] * 0.025, 2)
    
    def pay_zakat(self, participant):
        """Pay zakat from participant to zakat fund"""
        if participant not in self.participants:
            return False, f"Participant {participant} not found"
        zakat_amount = self.calculate_zakat(participant)
        if zakat_amount == 0:
            return False, f"No zakat due for {participant}"
        if self.participants[participant] < zakat_amount:
            return False, f"Insufficient balance to pay zakat"
        # Update balances
        self.participants[participant] -= zakat_amount
        self.participants[self.zakat_collector] += zakat_amount
        # Create zakat transaction
        transaction = Transaction(participant, self.zakat_collector, zakat_amount, 'Zakat', True)
        transaction.set_remaining_balance(self.participants[participant])
        self.pending_transactions.append(transaction)
        # Auto-mine block
        self.mine_pending_transactions()
        
        return True, transaction
    
    def collect_zakat_from_all(self):
        """Collect zakat from all participants except zakat fund"""
        results = []
        participants_to_collect = [p for p in self.participants.keys() if p != self.zakat_collector]
        for participant in participants_to_collect:
            success, result = self.pay_zakat(participant)
            results.append((participant, success, result))
        return results
    
    def mine_pending_transactions(self):
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            return False, "No transactions to mine"
        
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), self.pending_transactions.copy(), last_block.hash)
        
        # Mine the block
        self.miner.mine_block(new_block)
        self.chain.append(new_block)
        # Clear pending transactions
        self.pending_transactions = []
        
        return True, new_block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash integrity
            if current_block.hash != current_block.calculate_hash():
                return False
            # Check previous hash link
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_participant_balance(self, participant):
        return self.participants.get(participant, 0)
    
    def display_participants(self):
        print("\n" + "="*50)
        print("PARTICIPANTS AND BALANCES")
        print("="*50)
        for participant, balance in self.participants.items():
            if participant == self.zakat_collector:
                print(f"   {participant}: {balance} coins (Zakat Fund)")
            else:
                print(f"   {participant}: {balance} coins")
        print("="*50)
    
    def display_chain_summary(self):
        print(f"\n BLOCKCHAIN SUMMARY")
        print(f"   Total Blocks: {len(self.chain)}")
        print(f"   Chain Valid: {' Yes' if self.is_chain_valid() else ' No'}")
        print(f"   Total Participants: {len(self.participants)}")
        print(f"   Zakat Fund Balance: {self.participants[self.zakat_collector]} coins")
