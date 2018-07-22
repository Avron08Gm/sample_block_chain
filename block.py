import time
import hashlib

# class definition for each of the 'Block' object of the chain 
class Block:

    def __init__(self,index,proof_of_work,prev_hash,transactions,timestamp = None):
        
        self.index = index                   # index of the block
        
        self.proof_of_work = proof_of_work   # number generated after mining 
        
        self.transactions = transactions     # transaction list of the block
        
        self.prev_hash = prev_hash           # hexdigest of the previous block
        
        if timestamp :
            self.timestamp = timestamp
        else : 
            self.timestamp = time.time()     # time when the block is being created
   

   # function to get the hashed value of the block
    def get_hash(self):

        # getting all the block information in one string   
        block_id = '{}{}{}{}{}'.format(self.index,self.proof_of_work,self.prev_hash,self.transactions,self.timestamp)

        return hashlib.sha256(block_id.encode()).hexdigest()