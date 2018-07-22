# !!!!!!!
"""
   BEFORE RUNNING THIS SCRIPT, ENSURE THAT TWO SERVERS ARE ALREADY RUNNING AT : 'http://127.0.0.1:5000' AND 'http://127.0.0.1:5001' . (localhost)

"""
# !!!!!!!

# this entire code is there for testing the working of blockchain in localhost. It's not yet intended for computers running remotely.


import requests
from block_chain import BlockChain

blockchain = BlockChain()
blockchain.create_genesis_block()

def register_node(node_addr , serv_addr):
    requests.post(serv_addr + '/register_node' , json = {
        'node-address' : node_addr
    })

    print(' Node : {} has registered in the server : {}'.format(node_addr,serv_addr))

def create_transaction(serv_addr , data) :
    requests.post( serv_addr + '/create_transaction', json = {
        data # 'data' is a dictionary object
    } )
    
    print('Transaction has successfully completed for server : {}.'.format(serv_addr))

def mine_block(serv_addr):
    requests.get(serv_addr + '/mine_block').json()

    print('New block has been successfully mined for server: {}'.format(serv_addr))

def print_server_chain (serv_addr):
    response = requests.get(serv_addr + '/get_full_chain').json()

    print('Chain (in JSON format) for the server : {} is {}.'.format(serv_addr,response))

def sync_chain(serv_addr):
    response = requests.get(serv_addr + '/sync_chain').json()

    print('Chain in server : {} successfully synced.'.format(serv_addr))
    print('Result (in JSON) : {}'.format(response))

# now let's assume that the port : '5000' is our server (presonal computer) and the port : '5001' is some node (reomte computer)

server = 'http://127.0.0.1:5000'
node = 'http://127.0.0.1:5001'

register_node(server,node)

# real life transaction is not yet implemented
create_transaction(server , {
    'sender' : 'Us',
    'reciever' : 'Someone',
    'total_amount' : 99
    } )

# by mining a new block for the node, its chain's length would increase by 1. 
mine_block(node)

print_server_chain(server) # server's chain
print_server_chain(node) # node's chain
# if you notice the output, you would find that node's chain is having one more block. Its the block which was mined during the transaction

# so inoreder to have consensus, all the chains involved in P2P nerwork must be synced. But, here, there is only need for syncing chain between 'node' and 'server' which are running locally.
sync_chain(server)

# now on printing the server's chain after syncing, we can see that it's same as that of node's.
print_server_chain(server)