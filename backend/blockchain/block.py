import time

from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.util.hex_to_binary import hex_to_binary

GENESIS_DATA  = {
    'timestamp': 1,
    'last_hash':'genesis_hash',
    'hash':'genesis_hash',
    'data':[],
    'difficulty':3,
    'nonce': 'genesis_nonce'
}
# Scream Case syntax
class Block:

    """
    Block: storage unit
    """
    def __init__(self,timestamp,last_hash,hash,data,difficulty,nonce):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp:{self.timestamp},\n'
            f'last_hash:{self.last_hash},\n'
            f'hash:{self.hash},\n'
            f'data:{self.data}),\n'
            f'difficulty:{self.difficulty}),\n'
            f'nonce:{self.nonce})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        """
        Serialize the block into a dictionary of its attribtes.

        """
        return self.__dict__
        

    
    # A decorator takes in a function, adds some functionality and returns it 
    
    # Functions are objects; they can be referenced to,
    #  passed to a variable and returned from other functions as well.
    
    # Functions can be defined inside another function and 
    # can also be passed as argument to another function.


    @staticmethod
    def mine_block(last_block,data):
        """
        Mine a BLock based on the given parameters
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block,timestamp)
        nonce = 0
        # hash = f'{timestamp}-{last_hash}'----->temporary hash
        hash = crypto_hash(timestamp,last_hash,data,difficulty,nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block,timestamp)
            hash = crypto_hash(timestamp,last_hash,data,difficulty,nonce)


        return Block(timestamp,last_hash,hash,data,difficulty,nonce)

    @staticmethod
    def genesis():
        """
        First Block
        """
        # return Block(
        #     timestamp = GENESIS_DATA['timestamp'],
        #     last_hash = GENESIS_DATA['last_hash'],
        #     hash = GENESIS_DATA['hash'],
        #     data = GENESIS_DATA['data']
        #     )
        return Block(**GENESIS_DATA)
        # ** --unpacks the entire Genesis data dictionary

    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block;sjson representation back into a block instance.
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the adjusted difficulty according to the MINE_RATE.
        Incease the dfficulty for quickly mined Blocks. And Vice-Versa.

        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        
        if (last_block.difficulty - 1)>0:
            return last_block.difficulty - 1

        return 1


    @staticmethod
    def is_valid_block(last_block,block):
        """
        validating block:
            - block must contain proper last_hash reference
            - block must meet proof o fwork i.e. difficulty number and number of 0's
            - the difficulty must only adjust by 1            
            - block hash must be a valid combination of block field
            - 
        """
        
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The proof of work requirement was not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.nonce,
            block.difficulty
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')




def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block,'foo')
    bad_block.last_hash = 'foo'
    # Block.is_valid_block(genesis_block,bad_block)

    try:
        Block.is_valid_block(genesis_block,bad_block)

    except Exception as e:
        print(f' is_valid_block:{e}')


if __name__=='__main__': 
    main()