

var Web3 = require('web3')
const abiDecoder = require('abi-decoder'); 

const ABI = [
    {
      "inputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "admin",
      "outputs": [
        {
          "internalType": "address",
          "name": "admin_account",
          "type": "address"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "approved",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price_c",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "bool",
          "name": "approve_from",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "approve_to",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "optimal",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "name": "approved_trades",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price_c",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "bool",
          "name": "approve_from",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "approve_to",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "optimal",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "dual_tol",
      "outputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "global_dres",
      "outputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "global_pres",
      "outputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "init",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "is_optimal",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "iteration",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "iteration_complete",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "localres",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "primal_res",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "dual_res",
          "type": "int256"
        },
        {
          "internalType": "uint256",
          "name": "iteration",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "localresCounter",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "localres_list",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "primal_res",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "dual_res",
          "type": "int256"
        },
        {
          "internalType": "uint256",
          "name": "iteration",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "numApprovedTrades",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "peers",
      "outputs": [
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "prosumer",
          "type": "bool"
        },
        {
          "internalType": "uint8",
          "name": "building",
          "type": "uint8"
        },
        {
          "internalType": "bool",
          "name": "isPeerActive",
          "type": "bool"
        },
        {
          "internalType": "uint256",
          "name": "num_trades_pending",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "peersCount",
      "outputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "peersTrading",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "pri_tol",
      "outputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "tradeCountIter",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "name": "trade_bids_mapping",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price",
          "type": "int256"
        },
        {
          "internalType": "uint256",
          "name": "iteration",
          "type": "uint256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [],
      "name": "trade_penCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "trades_pending",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price_c",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "bool",
          "name": "approve_from",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "approve_to",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "optimal",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": true,
      "inputs": [
        {
          "internalType": "int256",
          "name": "",
          "type": "int256"
        }
      ],
      "name": "trades_pending_mapping",
      "outputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price_c",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "bool",
          "name": "approve_from",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "approve_to",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "optimal",
          "type": "bool"
        }
      ],
      "payable": false,
      "stateMutability": "view",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "new_admin",
          "type": "address"
        }
      ],
      "name": "setAdmin",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "acc",
          "type": "address"
        },
        {
          "internalType": "bool",
          "name": "role",
          "type": "bool"
        },
        {
          "internalType": "uint8",
          "name": "build",
          "type": "uint8"
        }
      ],
      "name": "addPeer",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "string",
          "name": "date_set",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "time_period",
          "type": "uint256"
        }
      ],
      "name": "startTradingPer",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "registerPeer",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "s",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "buy",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "amount",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price_c",
          "type": "int256"
        }
      ],
      "name": "addTradeBid",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "int256",
          "name": "p_res",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "d_res",
          "type": "int256"
        }
      ],
      "name": "addLocalRes",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "amount",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "price",
          "type": "int256"
        }
      ],
      "name": "createTrade",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [
        {
          "internalType": "address",
          "name": "trade_from",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "trade_to",
          "type": "address"
        },
        {
          "internalType": "int256",
          "name": "trade_kwh",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "trade_price_c",
          "type": "int256"
        },
        {
          "internalType": "int256",
          "name": "id",
          "type": "int256"
        },
        {
          "internalType": "bool",
          "name": "trade_approve_from",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "trade_approve_to",
          "type": "bool"
        },
        {
          "internalType": "bool",
          "name": "trade_optimal",
          "type": "bool"
        },
        {
          "internalType": "string",
          "name": "date_approved",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "time_approved",
          "type": "uint256"
        },
        {
          "internalType": "int256",
          "name": "trades_pending_ind",
          "type": "int256"
        }
      ],
      "name": "approveTrade",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "constant": false,
      "inputs": [],
      "name": "deregisterPeer",
      "outputs": [],
      "payable": false,
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]
//const testABI = [{"inputs": [{"type": "address", "name": ""}], "constant": true, "name": "isInstantiation", "payable": false, "outputs": [{"type": "bool", "name": ""}], "type": "function"}, {"inputs": [{"type": "address[]", "name": "_owners"}, {"type": "uint256", "name": "_required"}, {"type": "uint256", "name": "_dailyLimit"}], "constant": false, "name": "create", "payable": false, "outputs": [{"type": "address", "name": "wallet"}], "type": "function"}, {"inputs": [{"type": "address", "name": ""}, {"type": "uint256", "name": ""}], "constant": true, "name": "instantiations", "payable": false, "outputs": [{"type": "address", "name": ""}], "type": "function"}, {"inputs": [{"type": "address", "name": "creator"}], "constant": true, "name": "getInstantiationCount", "payable": false, "outputs": [{"type": "uint256", "name": ""}], "type": "function"}, {"inputs": [{"indexed": false, "type": "address", "name": "sender"}, {"indexed": false, "type": "address", "name": "instantiation"}], "type": "event", "name": "ContractInstantiation", "anonymous": false}];
abiDecoder.addABI(ABI);

const testData = '0x8c18ba290000000000000000000000009e1d8f6a261e178cc9ad00ab9928c1cb3bafcedb000000000000000000000000cd88dfd9528a1d14fc5abd02badeb685751402f5fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff5250000000000000000000000000000000000000000000000000000000000008baa';
const decodedData = abiDecoder.decodeMethod(testData);
// Web3.eth.getTransactionReceipt("0x5df9500f41300b996642b16edcb5f967ed5ce37e467f1578c5ca9e2cda6c0b1e", function(e, receipt) {
//     const decodedLogs = abiDecoder.decodeLogs(receipt.logs);
//   });
console.log(decodedData)