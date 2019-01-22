#!/usr/bin/python3

import itertools


# Generate and Initialize the core Actors for the Security Token
def deploy():
    global accountA, accountB, token_name, token_symbol, token_supply, cc
    accountA = accounts[0]
    accountB = accounts[1]

    # Country Codes
    cc = [1, 2, 3]

    # Initialize Issuer
    issuer_owners = [accounts[1]]
    issuer_threshold = 1
    issuer = accounts[1].deploy(IssuingEntity, issuer_owners, issuer_threshold)

    # Initialize Test Security Token
    token_name = "ABC Token"
    token_symbol = "ABCT"
    token_supply = 1000000
    token = accounts[1].deploy(SecurityToken, issuer, token_name, token_symbol, token_supply)

    # Initialize KYCRegistrar Actors
    kyc_owners = [accountA]
    kyc_threshold = 0
    kyc_registrar = accounts[0].deploy(KYCRegistrar, kyc_owners, kyc_threshold)

    # Issuer Initialization
    issuer.addToken(token)
    issuer.setRegistrar(kyc_registrar, True)

    # Add Investors to KYC
    for count, country, rating in [(c, i[0], i[1]) for c, i in enumerate(itertools.product(cc, [1, 2]), start=2)]:
        kyc_registrar.addInvestor("investor"+str(count), country, 'aws', rating, 9999999999, [accounts[count]])

    # Set Country Codes
    issuer.setCountries(cc, [1, 1, 1], [0, 0, 0])
