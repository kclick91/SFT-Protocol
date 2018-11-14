pragma solidity >0.4.99 <0.6.0;

import "../ModuleBase.sol";


contract CountryLockModule is STModuleBase {

	string public name = "CountryTimeLock";
	mapping (uint16 => uint256) public countryLock;

	function modifyCountryLock(uint16 _country, uint256 _epochTime) public onlyIssuer {
		countryLock[_country] = _epochTime;
	}

	function checkTransfer(
		address[2] calldata,
		bytes32,
		bytes32[2] calldata,
		uint8[2] calldata,
		uint16[2] calldata _country,
		uint256
	)
		external
		view
		returns (bool)
	{
		require(countryLock[_country[0]] < now);
		require(countryLock[_country[1]] < now);
	}

	function getBindings() external pure returns (bool, bool, bool) {
		return (true, false, false);
	}

}
