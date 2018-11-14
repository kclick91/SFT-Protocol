pragma solidity >0.4.99 <0.6.0;

import "../../open-zeppelin/SafeMath.sol";
import "../ModuleBase.sol";


contract CheckpointModule is STModuleBase {

	using SafeMath for uint256;

	uint256 private time;
	uint256 private totalSupply;
	mapping (address => uint256) private balance;
	mapping (address => bool) private zeroBalance;

	constructor(
		address _token,
		address _issuer,
		uint256 _time
	)
		STModuleBase(_token, _issuer)
		public
	{
		require(_time >= now);
		totalSupply = token.totalSupply();
		time = _time;
	}

	function _getBalance(address _owner) internal view returns (uint256) {
		if (balance[_owner] > 0) return balance[_owner];
		if (zeroBalance[_owner]) return 0;
		return token.balanceOf(_owner);
	}

	function transferTokens(
		address[2] calldata _addr,
		bytes32[2] calldata,
		uint8[2] calldata,
		uint16[2] calldata,
		uint256 _value
	)
		external
		onlyParent
		returns (bool)
	{
		if (now < time) return true;
		if (balance[_addr[0]] == 0 && !zeroBalance[_addr[0]]) {
			balance[_addr[0]] = token.balanceOf(_addr[0]).add(_value);
		}
		if (balance[_addr[1]] == 0 && !zeroBalance[_addr[1]]) {
			uint256 _bal = token.balanceOf(_addr[1]).sub(_value);
			if (_bal == 0) {
				zeroBalance[_addr[1]] == true;
			} else {
				balance[_addr[1]] = _bal;
			}
		}
		return true;
	}

	function balanceChanged(
		address _addr,
		bytes32,
		uint8,
		uint16,
		uint256 _old,
		uint256 _new
	)
		external
		onlyParent
		returns (bool)
	{
		if (now < time) {
			totalSupply = totalSupply.add(_new).sub(_old);
			return true;
		}
		if (balance[_addr] > 0) return true;
		if (zeroBalance[_addr]) return true;
		if (_old > 0) {
			balance[_addr] = _old;
		} else {
			zeroBalance[_addr] = true;
		}
		return true;
	}

	function getBindings() external pure returns (bool, bool, bool) {
		return (false, true, true);
	}

}
