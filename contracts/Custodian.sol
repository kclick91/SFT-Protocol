pragma solidity >0.4.99 <0.6.0;

import "./SecurityToken.sol";
import "./MultiSig.sol";

/// @title Custodian Contract
contract Custodian is MultiSigMultiOwner {

	string public name;
	bytes32 public id;
	mapping (address => bool) public addresses;

	constructor(
		string memory _name,
		address[] memory _owners,
		uint64 _threshold
	)
		MultiSigMultiOwner(_owners, _threshold)
		public
	{
		name = _name;
		id = keccak256(abi.encodePacked(address(this)));
	}

	function transfer(
		address _token,
		address _to,
		uint256 _value
	)
		external
		returns (bool)
	{
		if (!_checkMultiSig()) return false;
		require(SecurityToken(_token).transfer(_to, _value));
		return true;
	}

}
