[
    {
        "inputs": [
            {
                "internalType": "contract IPokPokProtocol",
                "name": "_protocolAddress",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "CallerNotAdmin",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "CallerNotOwner",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "InsufficientValueForFeeding",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "InvalidFeedAmount",
        "type": "error"
    },
    {
        "inputs": [],
        "name": "ReentrancyGuardReentrantCall",
        "type": "error"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "address",
                "name": "newAdmin",
                "type": "address"
            }
        ],
        "name": "AdminUpdated",
        "type": "event"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "contract IPokPokProtocol",
                "name": "newProtocol",
                "type": "address"
            }
        ],
        "name": "ProtocolUpdated",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "admin",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "feedChicken",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "harvestChicken",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "creator",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IChickenData.Asset",
                        "name": "asset",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "spotPrice",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "strikePrice",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "size",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "upfrontPayment",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "commissionSchedule",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "enum IChickenData.OptionSide",
                        "name": "side",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "maturityTimestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "enum IChickenData.FeedCurrency",
                        "name": "feedCurrency",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes",
                        "name": "signature",
                        "type": "bytes"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "amount",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "dueOn",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bool",
                                "name": "fed",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IChickenData.FeedingSchedule[]",
                        "name": "feedingSchedule",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "address",
                        "name": "issuer",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "settled",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "quoteTime",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IPokPokProtocol.Hatchery",
                "name": "_hatchery",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "hatchChicken",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "creator",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IChickenData.Asset",
                        "name": "asset",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "spotPrice",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "strikePrice",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "size",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "upfrontPayment",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "commissionSchedule",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "enum IChickenData.OptionSide",
                        "name": "side",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "maturityTimestamp",
                        "type": "uint256"
                    },
                    {
                        "internalType": "enum IChickenData.FeedCurrency",
                        "name": "feedCurrency",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes",
                        "name": "signature",
                        "type": "bytes"
                    },
                    {
                        "components": [
                            {
                                "internalType": "uint256",
                                "name": "amount",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "dueOn",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bool",
                                "name": "fed",
                                "type": "bool"
                            }
                        ],
                        "internalType": "struct IChickenData.FeedingSchedule[]",
                        "name": "feedingSchedule",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "address",
                        "name": "issuer",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "settled",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "quoteTime",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IPokPokProtocol.Hatchery",
                "name": "_hatchery",
                "type": "tuple"
            },
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "strike",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "size",
                        "type": "uint256"
                    },
                    {
                        "internalType": "enum ISpreadData.OptionSide",
                        "name": "side",
                        "type": "uint8"
                    },
                    {
                        "internalType": "enum ISpreadData.OptionPosition",
                        "name": "position",
                        "type": "uint8"
                    }
                ],
                "internalType": "struct ISpreadData.Leg[]",
                "name": "_spread",
                "type": "tuple[]"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "hatchChickenWithSpread",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            },
            {
                "internalType": "uint256[]",
                "name": "_feeds",
                "type": "uint256[]"
            }
        ],
        "name": "multiFeed",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "protocol",
        "outputs": [
            {
                "internalType": "contract IPokPokProtocol",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_tokenAddr",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "rescueAnyERC20Tokens",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_newAdmin",
                "type": "address"
            }
        ],
        "name": "updateAdmin",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract IPokPokProtocol",
                "name": "_newProtocol",
                "type": "address"
            }
        ],
        "name": "updateProtocol",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]