# EEE4022S

The following repository contains code that simulates a P2P energy trading market facilitated via an Ethereum smart contract.

The P2P_energy_trading folder contains the necessary code to run the P2P energy trading simulation in isolation.

The contents of the Smart_contract folder is all the code required to set-up the smart contract for deployment on an Ethereum test network.  
The smart contract code written in Solidity can be found under Smart_contract\contracts\Energy.sol.
The Smart_Contact\testing.py script contains the unit tests used to validate the smart contract's operation.

The contents of the Integrated_System folder is the code required to simulate the integrated P2P energy trading and smart contract system.
The files contained in the Integrated_System\Testing folder are the unit tests written to validate the operation of the integrated system.
The code in Integrated_System\receipt.js is the code used to decode the blockchain transaction input.
