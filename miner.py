class Miner:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.target = "0" * difficulty
    
    def mine_block(self, block):
        """Mine a block using proof of work"""
        print(f"Mining block {block.index}...")
        while True:
            computed_hash = block.calculate_hash()
            if computed_hash.startswith(self.target):
                block.hash = computed_hash
                print(f"Block mined! Hash: {computed_hash[:20]}... Nonce: {block.nonce}")
                return True
            block.nonce += 1
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.target = "0" * difficulty