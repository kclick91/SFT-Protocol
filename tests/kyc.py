#!/usr/bin/python3

import time
from array import array

DEPLOYMENT = "kyc"

#
# Issuing Entity Testing
#
# Setup : brownie deploy kyc
# Test  : brownie test kyc
#
# Trusted entities that provide KYC / AML services for network participants
# and behaves as a whitelist allow access to multiple securities with the same profile.
#
# Authority
# addAuthority(address[] _addr, uint16[] _countries, uint32 _threshold)
# setAuthorityCountries(bytes32 _id, uint16[] _countries, bool _auth)
# setAuthorityThreshold(bytes32 _id, uint32 _threshold)
# setAuthorityRestriction(bytes32 _id, bool _permitted)
#
#
# kyc = accounts[0].deploy(KYCRegistrar, [accounts[0]], 0)
# issuer = accounts[1].deploy(IssuingEntity, [accounts[1]], 1)
# token = accounts[1].deploy(SecurityToken, issuer, "Test Token", "TST", 1000000)
# issuer.addToken(token)
# issuer.setRegistrar(kyc, True)
#
# for count,country,rating in [(c,i[0],i[1]) for c,i in enumerate(itertools.product([1,2,3], [1,2]), start=2)]:
#     kyc.addInvestor("investor"+str(count), country, 'aws', rating, 9999999999, [accounts[count]])
#
# issuer.setCountries([1,2,3],[1,1,1],[0,0,0])


def check_authorities():
    '''Create authority'''

    global issuer, token, registrar
    issuer = IssuingEntity[0]
    # GEF Token
    token = SecurityToken[0]
    # Registrar
    registrar = KYCRegistrar[0]

    # Security Token Properties Test
    check.equal(token.name(), "GEF Token", "Token Name Invalid")
    check.equal(token.symbol(), "GEFT", "Token Symbol Invalid")

    new_auth_owners = [accounts[1]]
    auth_countries = [1, 2, 3]
    auth_threshold = 0

    # registrar addAuthority
    registered_auth = registrar.addAuthority(new_auth_owners, auth_countries, auth_threshold)
    check.true(registered_auth, "Invalid Authority Update")

    # Once an authority has been designated they may use KYCRegistrar.registerAddresses or
    # KYCRegistrar.restrictAddresses to modify their associated addresses.

    registrar_id = registrar.getID(accounts[1])
    registrar_investor = registrar.getInvestor(accounts[1])
    check.true(registrar_investor, "Invalid Investor Query")

    updated_countries_auth = registrar.setAuthorityCountries(registrar_id, [5, 6, 7], True)
    check.true(updated_countries_auth, "Invalid Countries Authority Update")

    # TODO - !! Value Error May Be Precedence issue
    # registrar.registerAddresses(bytes32 _id, address[] _addr)
    # registrar.restrictAddresses(bytes32 _id, address[] _addr)
    # check.confirm(registrar.registerAddresses(registrar_id, [accounts[2]]), "Invalid Registration")
    # registrar.setAuthorityThreshold(registrar_id, 0)



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
def check_investors():
    '''Investors'''

