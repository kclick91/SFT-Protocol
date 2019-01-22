#!/usr/bin/python3

import time
from array import array
import itertools

DEPLOYMENT = "issuer"


#
# Issuing Entity Testing
#
# Setup : brownie deploy issuer
# Test  : brownie test issuing_entity
#
# Token Constants
#
def check_constants():
    '''Constants '''
    global issuer, token, registrar, total_supply, cust1, cust2
    # BBC total token supply
    total_supply = 1000000
    # BBC issuing entity
    issuer = IssuingEntity[0]
    # BBC Security token
    token = SecurityToken[0]
    # Registrar
    registrar = KYCRegistrar[0]

    # Custodian deployed to provide the instance to test
    cust1 = accounts[10].deploy(Custodian, [accounts[10]], 1)
    cust2 = accounts[11].deploy(Custodian, [accounts[11]], 1)

    issuer.addCustodian(cust1)
    issuer.addCustodian(cust2)

    check.equal(issuer.getInvestorCounts()[0][0], 0, "Investor count is wrong")

    # token name
    check.equal(token.name(), "BBC Token", "Invalid Token Name")
    # token symbol
    check.equal(token.symbol(), "BBCT", "Invalid Token Symbol")
    # token decimals
    check.equal(token.decimals(), 0, "Invalid Token Decimals")
    # token issuer
    check.equal(token.issuer(), issuer.address, "Invalid Token Issuer Address")


#
# Restrictions
#
def check_restrictions():
    '''Adding & Restricting Tokens'''
    # issuer addToken
    token_added = issuer.addToken(SecurityToken[0])
    check.true(token_added, "Invalid Token Association")
    # issuer setTokenRestriction
    token_restricted = issuer.setTokenRestriction(SecurityToken[0].address, True)
    check.true(token_restricted, "Invalid Token Restriction")
    # issuer setGlobalRestriction
    global_restricted = issuer.setGlobalRestriction(True)
    check.true(global_restricted, "Invalid Global Restriction")


#
# Identifying Investors
#
# setRegistrar(address _registrar, bool _allowed)
# getID(address _addr)
# getInvestorRegistrar(bytes32 _id)
# setInvestorRestriction(bytes32 _id, bool _allowed)
#
def check_investors():
    '''Check Investors'''
    # issuer set kyc / aml registrar
    registry = KYCRegistrar[0]

    registrar_added = issuer.setRegistrar(registry.address, True)
    check.true(registrar_added, "Invalid KYCRegistrar Association")

    # setup for issuer.getID
    new_investor_id = registry.generateID("JOHNDOE11051980B5420355")
    check.true(new_investor_id, "Invalid ID Generation")
    cc = [1, 2, 3]
    for count, country, rating in [(c, i[0], i[1]) for c, i in enumerate(itertools.product(cc, [1, 2]), start=2)]:
        registry.addInvestor("investor"+str(count), country, 'aws', rating, 9999999999, [accounts[count]])

    # issuer getID
    existing_investor_id = issuer.getID(accounts[1])
    check.true(existing_investor_id, "Invalid Investor ID")

    # issuer getInvestorRegistrar
    invalid_investor_registrar = issuer.getInvestorRegistrar(existing_investor_id)
    check.equal(invalid_investor_registrar, "0x0000000000000000000000000000000000000000", "Invalid Investor Registrar")

    # issuer setInvestorRestriction
    check_investor_registrar_restriction = issuer.setInvestorRestriction(existing_investor_id, True)
    check.true(check_investor_registrar_restriction, "Invalid Investor Restriction")


#
# Custodian
#
def check_custodians():
    '''Check Custodians'''
    # issuer setBeneficialOwners
    custodian_updated = issuer.setBeneficialOwners(cust1.ownerID(), [issuer.getID(a[2])], False)
    check.true(custodian_updated, "Invalid Custodian Beneficial Owner")


#
# Investor Limits
#
def check_limits():
    '''Check Investor Limits'''
    # Country Codes
    cc = [1, 2, 3]
    investor_count = issuer.getInvestorCounts()[0][0]
    check.equal(investor_count, 0, "Invalid Investor Count")

    # Set Country Codes
    countries_updated = issuer.setCountries(cc, [1, 1, 1], [0, 0, 0])
    check.true(countries_updated, "Invalid Countries Update")
    # Get Country
    issuer_country = issuer.getCountry(cc[0])
    check.equal(issuer_country[0], 1, "Invalid Country Retrieval")

    limits_updated = issuer.setInvestorLimits([1, 1, 1])
    check.true(limits_updated, "Invalid Investor Limits Update")

    # Investor
    investor_country = 1
    investor_allowed = True
    # Raise Limits
    investor_limits = [1, 1, 1]
    # TODO Fix !! ValueError, code not matching the documentation.
    investor_updated = issuer.setCountry(investor_country, investor_allowed, 0, investor_limits)
    check.true(investor_updated, "Invalid Country Update")


#
# Modules
# isActiveModule(address _module)
def check_modules():
    '''Check Modules'''

    # Modules are attached and detached via IssuingEntity.
    non_module_address = accounts[2]
    module_active = token.isActiveModule(non_module_address)
    check.false(module_active, "Module Inactive")
