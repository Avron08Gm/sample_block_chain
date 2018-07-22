from block import Block

# class definition for the blockchain
class BlockChain:

    def __init__(self):
        
        self.chain = []                    # list of the Block objects in the chain
        
        self.current_node_transactions = []  # transaction info going to be added to ledger

        self.nodes = set()                   # set of all the unique nodes

    # function to create the genesis block
    def create_genesis_block(self):
        
        self.create_new_block(proof_of_work=0,prev_hash=0)

    # function to create a new block and add it to the blockchain 
    def create_new_block(self,proof_of_work,prev_hash):
        
        block=Block(
            index=len(self.chain),
            proof_of_work=proof_of_work,
            prev_hash=prev_hash,
            transactions=self.current_node_transactions)

        self.current_node_transactions = [] # transaction list is reset

        self.chain.append(block)            # append new block to the blockchain

        return block

    # function to make new transaction
    def create_new_transaction(self,sender,reciever,total_amount):

        self.current_node_transactions.append({
            'sender' : sender,
            'reciever' : reciever,
            'total_amount' : total_amount
        })
    
        # return the index of new block 

        return self.get_last_block().index + 1
    
    # function to generate the proof of work for a new block
    @staticmethod
    def create_proof_of_work(prev_proof):

        # this is a very easy algorithm for finding proof of work : Find the sum of the number and previous proof of work number which is divisible by 13
        #--------------------------begin-----------------------------

        proof=prev_proof + 1
        
        while ( proof + prev_proof ) % 13 != 0 :
            proof += 1

        #---------------------------end-----------------------------
        # an easily computable algorithm is intentionally applied here, so that mining when testing dosen't waste too much time. However, a properly working cryptographic algorithm can be used here instead too :) 

        return proof
    
    # function to get the last Block object of the chain
    def get_last_block(self):
        
        return self.chain[-1]
    
    # function to mine a new block
    def mine_block(self,miner_addr):

        self.create_new_transaction(
            sender = '0-0-0',
            reciever = miner_addr,
            total_amount = 1
        )

        last_block = self.get_last_block()
        last_proof = last_block.proof_of_work
        last_hash = last_block.get_hash()

        new_proof = self.create_proof_of_work(last_proof)

        new_block = self.create_new_block( new_proof , last_hash )

        return vars(new_block) # return a dictionary object consisting all attributes as key , value pair 

    # function to get the list of blocks in the form of dict
    def get_serialized_chain(self):

        return [vars(block) for block in self.chain]
    
    # function to create a new node
    def create_new_node(self,address):
        
        self.nodes.add(address)
         
        return True

    # function to return a copy of a Block object
    @staticmethod
    def get_block_copy(block_data):
        return Block (
            block_data['index'],
            block_data['proof_of_work'],
            block_data['prev_hash'],
            block_data['transactions'],
            timestamp = block_data['timestamp']
        )