#!/usr/bin/python3

import itertools


# Generate and Initialize the core Actors for the Issuing Entity
def deploy():
    global issuer, token_name, token_symbol, token_supply

    # Initialize Issuer
    issuer_owners = [accounts[1]]
    issuer_threshold = 0
    issuer = accounts[1].deploy(IssuingEntity, issuer_owners, issuer_threshold)

    # Initialize Test BBCT Security Token
    token_name = "BBC Token"
    token_symbol = "BBCT"
    token_supply = 1000000
    token = accounts[1].deploy(SecurityToken, issuer, token_name, token_symbol, token_supply)

    # Initialize KYCRegistrar Actors
    kyc_owners = [accounts[0], accounts[1]]
    kyc_threshold = 0
    kyc_registrar = accounts[0].deploy(KYCRegistrar, kyc_owners, kyc_threshold)

    issuer.setRegistrar(kyc_registrar, True)
