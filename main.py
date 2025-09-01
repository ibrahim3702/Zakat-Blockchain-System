import os
from blockchain import ZakatBlockchain 
from miner import Miner
from transaction import Transaction
from block import Block

class ZakatBlockchainMenu:
    def __init__(self):
        self.blockchain = ZakatBlockchain()
        self.running = True
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        print("\n" + "="*60)
        print("ZAKAT BLOCKCHAIN MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Register New Participant")
        print("2. Make Transaction")
        print("3. Pay Individual Zakat")
        print("4. Collect Zakat from All Participants")
        print("5. View Participants & Balances")
        print("6. View Blockchain Summary")
        print("7. View Detailed Transaction History")
        print("8. View Mining Details")
        print("9. Validate Blockchain")
        print("0. Exit")
        print("="*60)
    
    def register_participant(self):
        """Function to register participant"""
        print("\nREGISTER NEW PARTICIPANT")
        print("-" * 30)
        roll_number = input("Enter participant roll number: ").strip()
        if not roll_number:
            print("Invalid roll number!")
            return
        
        try:
            balance = input("Enter initial balance (default 200): ").strip()
            balance = int(balance) if balance else 200
        except ValueError:
            balance = 200
        
        success, message = self.blockchain.register_participant(roll_number, balance)
        print(message)
    
    def make_transaction(self):
        """Function to perform transaction between two members of the blockchain"""
        print("\nMAKE TRANSACTION")
        print("-" * 20)
        
        participants = [p for p in self.blockchain.participants.keys() if p != self.blockchain.zakat_collector]
        if len(participants) < 2:
            print("At least 2 participants are required to make transactions.")
            return
        
        print("Available participants:")
        for i, p in enumerate(participants, 1):
            balance = self.blockchain.participants[p]
            print(f"  {i}. {p} (Balance: {balance} coins)")
        
        try:
            sender = input("\nEnter sender roll number: ").strip()
            receiver = input("Enter receiver roll number: ").strip()
            amount = float(input("Enter amount: "))
            
            success, result = self.blockchain.add_transaction(sender, receiver, amount)
            if success:
                print("Transaction successful.")
                print(result)
            else:
                print(f"Transaction failed: {result}")
        
        except ValueError:
            print("Invalid amount entered.")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def pay_individual_zakat(self):
        """Function to collect zakat from the individual member of the blockchain"""
        print("\nPAY INDIVIDUAL ZAKAT")
        print("-" * 25)
        
        participants = [p for p in self.blockchain.participants.keys() if p != self.blockchain.zakat_collector]
        if not participants:
            print("No participants found.")
            return
        
        print("Participants:")
        for i, p in enumerate(participants, 1):
            balance = self.blockchain.participants[p]
            zakat_due = self.blockchain.calculate_zakat(p)
            print(f"  {i}. {p} (Balance: {balance}, Zakat Due: {zakat_due})")
        
        participant = input("\nEnter participant roll number: ").strip()
        
        success, result = self.blockchain.pay_zakat(participant)
        if success:
            print("Zakat payment successful.")
            print(result)
        else:
            print(f"Zakat payment failed: {result}")
    
    def collect_zakat_from_all(self):
        """Function to collect zakat from all the members of the blockchain"""
        print("\nCOLLECTING ZAKAT FROM ALL PARTICIPANTS")
        print("-" * 45)
        
        results = self.blockchain.collect_zakat_from_all()
        
        if not results:
            print("No participants to collect zakat from.")
            return
        
        total_collected = 0
        successful_payments = 0
        
        for participant, success, result in results:
            if success:
                print(f"{participant}: Zakat paid successfully")
                total_collected += result.amount
                successful_payments += 1
            else:
                print(f"{participant}: {result}")
        
        print("\nZAKAT COLLECTION SUMMARY")
        print(f"  Successful Payments: {successful_payments}/{len(results)}")
        print(f"  Total Zakat Collected: {total_collected} coins")
        print(f"  Zakat Fund Balance: {self.blockchain.participants[self.blockchain.zakat_collector]} coins")
    
    def view_participants(self):
        self.blockchain.display_participants()
    
    def view_blockchain_summary(self):
        self.blockchain.display_chain_summary()
    
    def view_transaction_history(self):
        print("\nDETAILED TRANSACTION HISTORY")
        print("="*70)
        
        all_transactions = []
        for block in self.blockchain.chain:
            for transaction in block.transactions:
                transaction_copy = transaction.copy()
                transaction_copy['block_index'] = block.index
                transaction_copy['block_hash'] = block.hash[:10] + "..." if block.hash else "N/A"
                all_transactions.append(transaction_copy)
        
        if not all_transactions:
            print("No transactions found.")
            return
        
        initializations = [tx for tx in all_transactions if tx['transaction_type'] == 'Initialization']
        transfers = [tx for tx in all_transactions if tx['transaction_type'] == 'Transfer']
        zakat_payments = [tx for tx in all_transactions if tx['transaction_type'] == 'Zakat']
        
        print(f"Total Transactions: {len(all_transactions)}")
        print(f"  Initializations: {len(initializations)}")
        print(f"  Transfers: {len(transfers)}")
        print(f"  Zakat Payments: {len(zakat_payments)}")
        
        total_zakat = sum(tx['amount'] for tx in zakat_payments)
        print(f"\nTotal Zakat Collected: {total_zakat} coins")
        
        print(f"\nTransaction Details:")
        for i, tx in enumerate(all_transactions, 1):
            marker = ""
            if tx['zakat_payment']:
                marker = " [ZAKAT]"
            elif tx['transaction_type'] == 'Initialization':
                marker = " [INIT]"
            
            print(f"{i:2d}. {tx['sender']} => {tx['receiver']}: {tx['amount']} coins{marker}")
            print(f"    Block: {tx['block_index']} | Balance After: {tx['remaining_balance']} | {tx['timestamp'][:19]}")
    
    def view_mining_details(self):
        print("\nMINING DETAILS")
        print("="*40)
        print(f"Mining Difficulty: {self.blockchain.miner.difficulty}")
        print(f"Target Pattern: {self.blockchain.miner.target}")
        print(f"Total Blocks Mined: {len(self.blockchain.chain)}")
        
        print(f"\nBlock Details:")
        for block in self.blockchain.chain:
            print(f"  Block {block.index}:")
            print(f"    Hash: {block.hash[:30] if block.hash else 'N/A'}...")
            print(f"    Nonce: {block.nonce}")
            print(f"    Transactions: {len(block.transactions)}")
    
    def validate_blockchain(self):
        print("\nBLOCKCHAIN VALIDATION")
        print("-" * 25)
        
        is_valid = self.blockchain.is_chain_valid()
        if is_valid:
            print("Blockchain is valid.")
            print("All blocks are properly linked and hashes are correct.")
        else:
            print("Blockchain is invalid.")
            print("Some blocks may have been tampered with or corrupted.")
        
        print(f"\nIntegrity Report:")
        print(f"  Total Blocks: {len(self.blockchain.chain)}")
        print(f"  Genesis Block Valid: {'Yes' if self.blockchain.chain[0].previous_hash == '0' else 'No'}")
        print(f"  Chain Continuity: {'Yes' if is_valid else 'No'}")
    
    def run(self):
        while self.running:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (0-9): ").strip()
                if choice == '1':
                    self.register_participant()
                elif choice == '2':
                    self.make_transaction()
                elif choice == '3':
                    self.pay_individual_zakat()
                elif choice == '4':
                    self.collect_zakat_from_all()
                elif choice == '5':
                    self.view_participants()
                elif choice == '6':
                    self.view_blockchain_summary()
                elif choice == '7':
                    self.view_transaction_history()
                elif choice == '8':
                    self.view_mining_details()
                elif choice == '9':
                    self.validate_blockchain()
                elif choice == '0':
                    print("\nThank you for using Zakat Blockchain System.")
                    self.running = False
                else:
                    print("Invalid choice. Please enter a number between 0 and 9.")
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")

def initialize_demo_data(menu_system):
    print("\nInitializing demo data...")
    
    demo_participants = ["22F-3702", "22F-3693", "22F-3628", "22F-3701"]
    for participant in demo_participants:
        menu_system.blockchain.register_participant(participant)
    
    demo_transactions = [
        ("22F-3702", "22F-3701", 30),
        ("22F-3701", "22F-3693", 25),
        ("22F-3693", "22F-3628", 20)
    ]
    
    for sender, receiver, amount in demo_transactions:
        menu_system.blockchain.add_transaction(sender, receiver, amount)
    
    print("Demo data initialized.")


print("Welcome to Zakat Blockchain System.")

choice = input("\nWould you like to initialize with demo data? (y/n): ").strip().lower()

menu_system = ZakatBlockchainMenu()

if choice in ['y', 'yes']:
    initialize_demo_data(menu_system)
    input("Press Enter to continue to main menu...")

menu_system.run()
