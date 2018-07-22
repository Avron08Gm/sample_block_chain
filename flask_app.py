from flask import Flask , jsonify , request , url_for
from block_chain import BlockChain
from uuid import uuid4

app = Flask(__name__)    

blockchain = BlockChain()

blockchain.create_genesis_block()

# make a unique adddress for the current node
node_address = uuid4().hex

# app to carry out the transaction process
@app.route( '/make_transaction' , methods = ['POST'] )
def make_transaction():
    transaction_data = request.get_json()
    index = blockchain.create_new_transaction(**transaction_data)

    response = {
        'message' : 'Transaction has been successfully done.',
        'block_index' : index
    }

    return jsonify(response) , 201

# app for mining 
@app.route( '/mine' , methods = ['GET'] )
def mine():
    block = blockchain.mine_block(node_address)

    response = {
        'message' : 'New block successfully mined.',
        'block_data' : block
    }

    return jsonify(response)

# returning complete chain
@app.route( '/full_chain' , methods = ['GET'] )
def get_full_chain():
    response = {
        'chain' : blockchain.get_serialized_chain() 
    }

    return jsonify(response)

# registering a node
@app.route( '/register_node' , methods = ['POST'] )
def register_node():
    node_data=request.get_json()

    blockchain.create_new_node(node_data.get('address'))
    
    response = {
        'message' : 'Successfully created new node.',
        'node_count' : len(blockchain.nodes),
        'nodes' : list(blockchain.nodes)
    }

    return jsonify(response) , 201

def get_neighbour_chains():
    neighbour_chains = []

    for node_address in blockchain.nodes:
        response = request.get(node_address + url_for('get_full_chain')).json()
        chain = response['chain']
        neighbour_chains.append(chain)
    
    return neighbour_chains 

# Syncing the chain
@app.route('/sync_chain' , methods = ['GET'])
def consensus():
    neighbour_chains=get_neighbour_chains()

    if not neighbour_chains : 
        return jsonify({
            'message' : 'No neighbouring chains are currently available.'
        })

    longest_chain = max(neighbour_chains , key = len)

    if len(blockchain.chain) >= longest_chain:
        response = {
            'message' : 'No new blocks are there.',
            'chain' : blockchain.get_serialized_chain()
        }
    else: # if our blockchain is not the longest, then it means new block(s) is/are there in some other chain
        blockchain.chain = [blockchain.get_block_copy( block_data ) for block_data in longest_chain]
        response = {
            'message' : 'New block(s) is/are added.',
            'chain' : blockchain.get_serialized_chain()
        }

    return jsonify(response)


# for testing the working of 'flask_app.py' in case of any edits
#-------------------------
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument( '-H', '--host' ,default='127.0.0.1')
parser.add_argument( '-p', '--port' ,default=5000, type=int)
args = parser.parse_args()

app.run( host = args.host , debug = True , port = args.port )
#--------------------------