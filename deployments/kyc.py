#!/usr/bin/python3

import itertools


# Generate and Initialize the core Actors for the KYCRegistrar
#
# Authority
# X addAuthority(address[] _addr, uint16[] _countries, uint32 _threshold)
# setAuthorityCountries(bytes32 _id, uint16[] _countries, bool _auth)
# setAuthorityThreshold(bytes32 _id, uint32 _threshold)
# setAuthorityRestriction(bytes32 _id, bool _permitted)
#
# Investors
# generateID(string _idString)
# addInvestor(bytes32 _id, uint16 _country, bytes3 _region, uint8 _rating, uint40 _expires, address[] _addr)
# updateInvestor(bytes32 _id, bytes3 _region, uint8 _rating, uint40 _expires)
# setInvestorRestriction(bytes32 _id, bool _permitted)
# setInvestorAuthority(bytes32[] _id, bytes32 _authID)
#
# Investor Info
# getID(address _addr)
# getInvestor(address _addr)
# getInvestors(address _from, address _to)
# getRating(bytes32 _id)
# getRegion(bytes32 _id)
# getCountry(bytes32 _id)
# getExpires(bytes32 _id)
# isPermitted(address _addr)
#
# Addresses
# registerAddresses(bytes32 _id, address[] _addr)
# restrictAddresses(bytes32 _id, address[] _addr)
#
def deploy():
    global accountA, accountB, token_name, token_symbol, token_supply, cc
    accountA = accounts[0]
    accountB = accounts[1]

    # Country Codes
    cc = [1, 2, 3]

    # Initialize Issuer
    issuer_owners = [accounts[0]]
    issuer_threshold = 1
    issuer = accounts[0].deploy(IssuingEntity, issuer_owners, issuer_threshold)

    # Initialize Test Security Token
    token_name = "GEF Token"
    token_symbol = "GEFT"
    token_supply = 1000000
    token = accounts[0].deploy(SecurityToken, issuer, token_name, token_symbol, token_supply)

    # Initialize KYCRegistrar Actors
    kyc_owners = [accounts[0]]
    kyc_threshold = 1
    kyc_registrar = accounts[0].deploy(KYCRegistrar, kyc_owners, kyc_threshold)

    # Issuer Initialization
    issuer.addToken(token)
    issuer.setRegistrar(kyc_registrar, True)

    # Add Investors to KYC
    for count, country, rating in [(c, i[0], i[1]) for c, i in enumerate(itertools.product(cc, [1, 2]), start=2)]:
        kyc_registrar.addInvestor("investor"+str(count), country, 'aws', rating, 9999999999, [accounts[count]])

    # Set Country Codes
    issuer.setCountries(cc, [1, 1, 1], [0, 0, 0])
