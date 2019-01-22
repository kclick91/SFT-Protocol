## SFT Unit Testing

SFT Unit Testing covers most the cases from the yellow paper.
Focused on the identity and permission aspects. 

The following components are covered : 

- KYCRegistrar
- SecurityToken
- IssuingEntity
- Custodian
- Mult-Sig / Multi-Owner
- Modules

### Legal Entity Identifier (LEI) 
This test data uses actual examples of LEI for the investor testing phase.

For natural persons, a string that is a concatenation of the persons full legal name, date of birth as DD/MM/YYYY, and their national identification number.

```
JOHNDOE11051980B5420355
```
For artificial persons, that entities LEI number.
https://www.gleif.org/en/about-lei/introducing-the-legal-entity-identifier-lei
```
GE Financing GmbH (LEI)
54930084UKLVMY22DS16
```
```
Jaguar Land Rover Ltd
213800WSGIIZCXF1P572
```
```
British Broadcasting Corporation
5493000IBP32UQZ0KL24
```

### KYC Registrar
- KYC / AML Registry acts as a whitelist for Investors and/or Custodians.
- Once an investor has passed the KYC/AML checks for a registry, they are now free to trade in any tokens that obtain their identification.
- Applied authorities acts as restrictions on the investor/custodian.

### Security Token
- Total Supply and Balances
- Token Transfers

### Issuing Entity
- Token Restrictions
- Identity
- Custodians
- Investor Limits

### Custodian
- Token Transfers
- Ether Transfers
- Beneficial Owners

### Multi-Signature / Multi-Owner
- Authorities
- Token Transfers
- Ether Transfers
- Beneficial Owners

### Possible Real World Scenario
- Token Issuance
- Digital Legal Contract
- Real Estate Securities
- 