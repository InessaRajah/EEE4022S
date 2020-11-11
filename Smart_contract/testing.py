import json
from web3 import Web3
import pytz
from datetime import datetime

#Written by: Inessa Rajah

#Testing advanced contract

#setup 
ganache_url = "http://127.0.0.1:8545"

web3 =Web3(Web3.HTTPProvider(ganache_url))

#Check if node is connected
print(web3.isConnected())


#address = web3.toChecksumAddress('0x90Ef192CEcFb60D0AacFF683f4cFb1Aebf6D31A3')
address = web3.toChecksumAddress('0x316030A4931cBAD4cE139F4Ed0b5FE85Cfc1B5C9')

#how to import abi and bytecode using truffle 
PATH_TRUFFLE_WK = 'C:/Users/Inessa/Desktop/4th_Year/FYP/Methodology_Eth/energy'
truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/Energy.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

#fetch the smart contract
contract = web3.eth.contract(address=address, abi =abi)

#Test 1: Testing addPeer function (writing) and peers[acc] (reading)

#define signing account for transactions- admin for these tests
web3.eth.defaultAccount = web3.eth.accounts[0]

#add peer 1 
# tx_hash = contract.functions.addPeer(str(web3.eth.accounts[1]), True, 1).transact()
# web3.eth.waitForTransactionReceipt(tx_hash)
# print("Successfully added peer 1")
# print("Take a look!")
# print(contract.functions.peers(str(web3.eth.accounts[1])).call())
# #add peer 2
# tx_hash = contract.functions.addPeer(str(web3.eth.accounts[2]), True, 1).transact()
# web3.eth.waitForTransactionReceipt(tx_hash)
# print("Successfully added peer 2")
# print("Take a look!")
# print(contract.functions.peers(str(web3.eth.accounts[2])).call())
# print("Test1 passed")
# # if you try to re-add a peer that already is part of the network- you'll get errors

##Test 2: Testing startTradingPer() - done by admin
cat = pytz.timezone('Africa/Johannesburg')
today = datetime.time(datetime.now(tz = cat))
time = today.hour
today = datetime.date(datetime.now(tz = cat))
date = str(today)

tx_hash = contract.functions.startTradingPer(date, time).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
if ((contract.functions.init().call()) and (contract.functions.iteration_complete().call()==contract.functions.is_optimal().call()==0) and (contract.functions.iteration().call()==contract.functions.localresCounter().call()==0) and (contract.functions.tradeCountIter().call() == contract.functions.trade_penCount().call()== contract.functions.numApprovedTrades().call()==0)):
    print("Trading period started")
    print("Test2 passed")
else:
    ("Test2 failed")


web3.eth.defaultAccount = web3.eth.accounts[1]
one = str(web3.eth.accounts[1])
tx_hash = contract.functions.deregisterPeer().transact()
web3.eth.waitForTransactionReceipt(tx_hash)
print("Peer 1 deregistered")
peer1 = contract.functions.peers(one).call()
print(peer1) 

web3.eth.defaultAccount = web3.eth.accounts[2]
two = str(web3.eth.accounts[2])
tx_hash = contract.functions.deregisterPeer().transact()
web3.eth.waitForTransactionReceipt(tx_hash)
peer2 = contract.functions.peers(two).call()
print(peer2)


##Test 3: peers that want to be involved in this time period register (writing)
#set signing peer to be peer 1 who has been added to network by admin
# if you try to register peer twice - will get an error
#testing registerPeer()
web3.eth.defaultAccount = web3.eth.accounts[1]
print(web3.eth.defaultAccount)
tx_hash = contract.functions.registerPeer().transact()
print("Registering peer 1 to trade in time period")
web3.eth.waitForTransactionReceipt(tx_hash)
print("Peer 1 successfully registered.  Take a look!")
peer1 = contract.functions.peers(str(web3.eth.accounts[1])).call()
print(peer1)
web3.eth.defaultAccount = web3.eth.accounts[2]
tx_hash = contract.functions.registerPeer().transact()
print("Registering peer 2 to trade in time period")
web3.eth.waitForTransactionReceipt(tx_hash)
print("Peer 2 successfully registered.  Take a look!")
peer2 = contract.functions.peers(str(web3.eth.accounts[2])).call()
print(peer2)

if ((contract.functions.peersTrading().call()==2) and (peer1[4]==1) and (peer2[4] ==1)):
    print("Test3 passed")
else:
    print("Test3 failed")


#Test 4: Testing addTradeBid()
#peer 1 will submit trade to peer 2
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
buyer = str(web3.eth.accounts[2])
#tx_hash = contract.functions.addTradeBid(date, time, sender, buyer, 50, 87).transact()
tx_hash = contract.functions.addTradeBid(sender, buyer, 50, 87).transact()
web3.eth.waitForTransactionReceipt(tx_hash)

trade_bids = contract.functions.trade_bids_mapping(12).call()
if ((contract.functions.iteration().call()==1) and (contract.functions.tradeCountIter().call()==1)):
    print("Trade bid 12 submitted.  Take a look!")
    print(trade_bids)
    print("Total number of trade bids:")
    print(contract.functions.tradeCountIter().call())
    print("Test 4 passed")
else:
    print("Test 4 failed")


#Test 5: Testing addTradeBid() again
# peer 2 submits trade to peer 1
web3.eth.defaultAccount = web3.eth.accounts[2]
sender = str(web3.eth.accounts[2])
buyer = str(web3.eth.accounts[1])
#tx_hash = contract.functions.addTradeBid(date, time, sender, buyer, 50, 87).transact()
tx_hash = contract.functions.addTradeBid(sender, buyer, 50, 87).transact()

web3.eth.waitForTransactionReceipt(tx_hash)
trade_bids = contract.functions.trade_bids_mapping(21).call()
if ((contract.functions.iteration().call()==1) and (contract.functions.tradeCountIter().call()==2)):
    print("Trade bid 21 submitted. Take a look!")
    print(trade_bids)
    print("Total number of trade bids:")
    print(contract.functions.tradeCountIter().call())
    print("Test 5 passed")
else:
    print("Test 5 failed")
    print("Iteration: {}". format(
        contract.functions.iteration().call()
    ))
    print("tradeCountIter: {}". format(
        contract.functions.tradCountIter().call()
    ))


#Test 6: Testing addLocalRes() (writing)
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
tx_hash = contract.functions.addLocalRes(5, 5).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
if ((contract.functions.localresCounter().call()==1) and (contract.functions.global_pres().call() == 5) and (contract.functions.global_dres().call()==5)): 
    print("Added a local residual.  Take a look!")
    print(contract.functions.localres(sender).call())
    print("Test 6 passed")
else:
    print("Test 6 failed")

#Test 7: Testing addLocalRes() again (writing)
#test if checkOptimal is called (iteration_complete = true) and is_optimal is set to false
## change values of global_pres, global_dres, pri_tol and dual_tol appropriately for this test
web3.eth.defaultAccount = web3.eth.accounts[2]
sender = str(web3.eth.accounts[2])
tx_hash = contract.functions.addLocalRes(3, 3).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
if ((contract.functions.localresCounter().call()==2) and (contract.functions.global_pres().call() == 8) and (contract.functions.global_dres().call()==8) and (contract.functions.iteration_complete().call()) and (contract.functions.is_optimal().call()==0)): 
    print("Added a local residual.  Take a look!")
    print(contract.functions.localres(sender).call())
    print("Trade bids submitted are NOT optimal.  New iteration will start.")
    print("Test 7 passed")
else:
    print("Test 7 failed")

# in the following tests will start a new trading iteration where trade bids and local residuals are re-submitted

#Test 8.1: Testing if calling addTradeBid() now executes newIteration()
#peer 1 will submit trade to peer 2
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
buyer = str(web3.eth.accounts[2])
tx_hash = contract.functions.addTradeBid(sender, buyer, 40, 77).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
trade_bids = contract.functions.trade_bids_mapping(12).call()
if ((contract.functions.iteration().call()==2) and (contract.functions.tradeCountIter().call()==1) and (contract.functions.localresCounter().call()==0) and (contract.functions.global_pres().call() == contract.functions.global_dres().call() == 0)):
    print("New trade bid 12 submitted.  Take a look!")
    print(trade_bids)
    print("Total number of trade bids is now back to 1:")
    print(contract.functions.tradeCountIter().call())
    print("Test 8.1 passed")
else:
    print("Test 8.1 failed")


#Test 8.2: Testing if calling addTradeBid() now behaves as expected i.e. normally and does not execute newIteration()
web3.eth.defaultAccount = web3.eth.accounts[2]
sender = str(web3.eth.accounts[2])
buyer = str(web3.eth.accounts[1])
cat = pytz.timezone('Africa/Johannesburg')
today = datetime.time(datetime.now(tz = cat))
time = today.hour
today = datetime.date(datetime.now(tz = cat))
date = str(today)
tx_hash = contract.functions.addTradeBid(sender, buyer, 50, 87).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
trade_bids = contract.functions.trade_bids_mapping(21).call()
if ((contract.functions.iteration().call()==2) and (contract.functions.tradeCountIter().call()==2)):
    print("New trade bid 21 submitted. Take a look!")
    print(trade_bids)
    print("Total number of trade bids is back to 2:")
    print(contract.functions.tradeCountIter().call())
    print("Test 8.2 passed")
else:
    print("Test 8.2 failed")
    print("Iteration: {}". format(
        contract.functions.iteration().call()
    ))
    print("tradeCountIter: {}". format(
        contract.functions.tradCountIter().call()
    ))

#Test 8.3: Add one new local residual
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
tx_hash = contract.functions.addLocalRes(1, 1).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
if ((contract.functions.localresCounter().call()==1) and (contract.functions.global_pres().call() == 1) and (contract.functions.global_dres().call()==1)): 
    print("Added a local residual.  Take a look!")
    print(contract.functions.localres(sender).call())
    print("Test 8.3 passed")
else:
    print("Test 8.3 failed")

#Test 9: Add another local residual
# Testing if checkOptimal is called and is_optimal is set to true
## change values of global_pres, global_dres, pri_tol and dual_tol for this test
# for this test pri_tol = dual_tol = 7
web3.eth.defaultAccount = web3.eth.accounts[2]
sender = str(web3.eth.accounts[2])
tx_hash = contract.functions.addLocalRes(1, 1).transact()
web3.eth.waitForTransactionReceipt(tx_hash)
if ((contract.functions.localresCounter().call()==2) and (contract.functions.global_pres().call() == 2) and (contract.functions.global_dres().call()==2) and (contract.functions.iteration_complete().call()) and (contract.functions.is_optimal().call()) and (contract.functions.init().call()==0)): 
    print("Added a local residual.  Take a look!")
    print(contract.functions.localres(sender).call())
    print("Trade bids submitted are optimal")
    print("Test 9 passed")
else:
    print("Test 9 failed")

#Test 10: testing createTrade() function
#create optimal trade from peer 1 to peer 2
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
to = str(web3.eth.accounts[2])
cat = pytz.timezone('Africa/Johannesburg')
today = datetime.time(datetime.now(tz = cat))
time = today.hour
today = datetime.date(datetime.now(tz = cat))
date = str(today)

sender = str(web3.eth.accounts[1])
to = str(web3.eth.accounts[2])

s = contract.functions.peers(sender).call()
b = contract.functions.peers(to).call()
id_set = (s[0] * 10)+ (b[0])

bid = contract.functions.trade_bids_mapping(id_set).call()

#tx_hash = contract.functions.createTrade(date, time, sender, to, bid[4], bid[5]).transact()
tx_hash = contract.functions.createTrade(sender, to, -bid[4], bid[5]).transact()

print("Creating optimal trade from peer 1 to peer 2")
web3.eth.waitForTransactionReceipt(tx_hash)

trade = contract.functions.trades_pending(0).call()
if ((trade[9]) and (contract.functions.trade_penCount().call()==1)):
    print("Optimal trade created and pending approval.")
    print('This was the optimal trade bid: {}'.format(
        bid
    ))

    print("This was the created trade: {}".format(
        trade
    ))

    print("Test 10 passed")


#Test 11: testing createTrade()
#make a non-optimal trade from peer 1 to peer 2
web3.eth.defaultAccount = web3.eth.accounts[1]
sender = str(web3.eth.accounts[1])
to = str(web3.eth.accounts[2])
cat = pytz.timezone('Africa/Johannesburg')
today = datetime.time(datetime.now(tz = cat))
time = today.hour
today = datetime.date(datetime.now(tz = cat))
date = str(today)

sender = str(web3.eth.accounts[1])
to = str(web3.eth.accounts[2])

s = contract.functions.peers(sender).call()
b = contract.functions.peers(to).call()
id_set = (s[0] * 10)+ (b[0])


#tx_hash = contract.functions.createTrade(date, time, sender, to, 4, 55).transact()
tx_hash = contract.functions.createTrade(sender, to, -4, 55).transact()

print("Creating non-optimal trade from peer 1 to peer 2")
web3.eth.waitForTransactionReceipt(tx_hash)

trade = contract.functions.trades_pending(1).call()
if ((trade[9]==0) and (contract.functions.trade_penCount().call()==2)):
    print("Non-optimal trade created and pending approval.")
    print('This was the optimal trade bid for this trade_id: {}'.format(
            bid
    ))

    print("This was the created trade: {}".format(
        trade
    ))

    print("Test 11 passed")


#Test 12: testing approveTrade() function
#have peer 2 approve optimal trade created by peer 1
web3.eth.defaultAccount = web3.eth.accounts[2]
msg_sender = str(web3.eth.accounts[2])
cat = pytz.timezone('Africa/Johannesburg')
today = datetime.time(datetime.now(tz = cat))
time = today.hour
today = datetime.date(datetime.now(tz = cat))
date = str(today)
trades_pen = contract.functions.trade_penCount().call()
for i in range (0, trades_pen):
    trade = contract.functions.trades_pending(i).call()
    if (trade[3] == msg_sender):
        if (trade[9]):
            tx_hash1 = contract.functions.approveTrade(trade[0], trade[1], trade[2], trade[3], trade[4], trade[5], trade[6], trade[7], trade[8], trade[9], date, time, i).transact()
            web3.eth.waitForTransactionReceipt(tx_hash1)
            print("Peer 2 approved optimal trade")
            print("Here is the stored approved, optimal trade:")
            approved = contract.functions.approved(0).call()
            print(approved)
            if (contract.functions.numApprovedTrades().call() == 1):
                print("Test 12 passed")
        else:
            print("Checked trade that was created was not optimal")
            print("Here is the unapproved, non-optimal trade:")
            print(trade)
    else:
        print("Not our trade")



