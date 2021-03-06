pragma solidity >=0.4.24 <0.5.0;

/** @title Minimal Custodian Interface */
interface MiniCustodian {

	function ownerID() external view returns (bytes32);
	
	function receiveTransfer(
		address _token,
		bytes32 _id,
		uint256 _value
	)
		external
		returns (bool);
	
	function balanceOf(
		address _token,
		bytes32 _id
	)
		external
		view
		returns (uint256);

	function isBeneficialOwner(
		address _issuer,
		bytes32 _id
	)
		external
		view
		returns (bool);
}
