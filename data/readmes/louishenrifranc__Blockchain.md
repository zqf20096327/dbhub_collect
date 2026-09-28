# Blockchain
* Implement a blockchain for a school project. 
* Simpler version of the blockchain: register domain name in the blockchain  
* Only CPP code

# Requirements
* ![cryptocpp](https://www.cryptopp.com/)
* ![boost](http://www.boost.org/)

# Implementation
The project was to build a functionnal blockchain. I wasn't able to code the network part in the short period of time, so only the cores function of the blockchain works (some network class have been start, but nothing finished).  
In this blockchain implementation, you can: 
* Identify as a new user, and create a transaction
```{cpp}
Identite id("Franc Louis Henri", "Jerome");
cout << id.getNom() << " " << id.getPrenom() << endl;
KeyPair p = id.getKeyPair(); // Get key

string nomDeDomaine = "facebook.com";
string information = "69.63.176.13";
Transaction t(id, nomDeDomaine, information);
```
* Add this transaction to the blockchain
```{cpp}

BlockChain blockchain; // Create a blockchain
Block genesis(0); // Create first block
std::shared_ptr<Block> ptr0 = std::make_shared<Block>(genesis);
blockchain.push_back(genesis)

// create some transactions
vector<Transaction> transactions_block1{ t1,t,t2,t22,t3,t4 };

// create a new block referencing the previous one
Block block1(ptr0, transactions_block1);

// Compute the proof of work
block1.solveProofofWork();

// add it to the blockhain
blockchain.push_back(block1)
```
* I also implemented a database from scratch, and not used any other implementation (because the goal was to understand and practise by coding). Probably not optimal, still cool to code. The database is used to save all traduction _domaine name -> IP + informations_.  
```{cpp}
DataBase database;

// Get all transaction of a block
vector all_transaction = std::get<2>(block1).get_Transactions_List()

// Get the entry of the last transaction in the database
database.get(all_transaction.back())

// push a transaction database.push_back(transaction)
// push a all block database.update(block)
```


