from difflib import diff_bytes
from hashlib import sha256

def updateHash(*args):
    hashing_text = ""
    h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

# print(updateHash("Hello", 1, "yess"))        

class Block:

    def __init__(self, number = 0, previous_hash = "0" * 64, data = None, nonce = 0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        return updateHash(self.previous_hash, self.number, self.data, self.nonce)
    
    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s" %(self.number, self.hash(), self.previous_hash, self.data, self.nonce))




class Blockchain:
    difficulty = 4
    
    def __init__(self):
        self.chain = []
    
    def add(self, block):
        self.chain.append(block)

    def mine(self, block):
        #htis block is passed with data, previoushash as 0, nonce as 0
        #now we have to find the correct nonce
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass
        
        while True: 
            # block.nonce += 1
            hash_of_the_block = block.hash()
            if(hash_of_the_block[:self.difficulty] == "0"*self.difficulty):
                self.add(block)
                break
            else:
                block.nonce +=1

    def isValid(self):
        if self.chain[0].hash()[:self.difficulty] != "0"*self.difficulty:
            return False
        for i in range(1, len(self.chain)):
            if(self.chain[i-1].hash() != self.chain[i].previous_hash or self.chain[i].hash()[:self.difficulty] != "0"*self.difficulty ):
                return False
        return True





def main():
    # block = Block("Hello world", 1)  #calls init from block class -> takes block number and data to be hashed
    # print(block)
    blockchain1 = Blockchain()
    database1 = ["hello world", "hello", "whats up", "bye"]

    num = 0
    for data in database1:
        num += 1
        blockchain1.mine(Block(data, num))

    for i in blockchain1.chain:
        print("block_number: ", i.number)
        print("previous_hash: ", i.previous_hash)
        print("hash: ", i.hash())
        print("data: ",i.data)
        print("nonce: ",i.nonce)

    print("Checking validity")
    print(blockchain1.isValid())


if __name__ == '__main__':
    main()