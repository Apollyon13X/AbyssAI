/**
 * @title NDAMutualNFT - Soulbound NDA NFT Contract
 * @author Nebojsa Nesic (Founder & CEO, AbyssAI)
 * @notice A mutual Non-Disclosure Agreement tokenized as a soulbound ERC-721 NFT.
 *         Each minted token represents a signed mutual NDA between two parties.
 *         Deployed on Base (L2). Budget reference: 0.75 ETH for deployment gas.
 * @dev This contract is NOT legally binding by itself. It is a cryptographic
 *      attestation layer that references an off-chain signed NDA document.
 *      Parties must execute the legal NDA document off-chain and store its
 *      content hash (IPFS) on-chain via this contract.
 */

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NDAMutualNFT is ERC721, ERC721Burnable, Ownable, ReentrancyGuard {
    // Soulbound: tokens are non-transferable by default
    bool public immutable soulbound = true;

    // Mapping: tokenId -> structured NDA record
    struct NDARecord {
        address partyA;
        address partyB;
        string ndaHash;        // IPFS hash of signed NDA document
        string ndaTitle;       // e.g., "Mutual NDA - AbyssAI x Counterparty"
        uint256 effectiveDate; // Unix timestamp
        bool partyASigned;     // cryptographic attestation by Party A
        bool partyBSigned;     // cryptographic attestation by Party B
        bool fullyExecuted;    // true when both parties signed
        bool revoked;          // if either party revokes before execution
    }

    mapping(uint256 => NDARecord) public ndaRecords;
    mapping(address => uint256[]) public partyNDAs; // address -> tokenIds they are party to
    mapping(address => mapping(address => bool)) public mutualNDAExists; // prevent duplicate NDAs between same pair

    uint256 public nextTokenId;

    event NDAMinted(
        uint256 indexed tokenId,
        address indexed partyA,
        address indexed partyB,
        string ndaHash,
        uint256 effectiveDate
    );

    event NDASigned(
        uint256 indexed tokenId,
        address indexed signer,
        bool fullyExecuted
    );

    event NDARevoked(uint256 indexed tokenId, address indexed revoker);

    /**
     * @notice Initialize the NDA NFT contract
     */
    constructor() ERC721("AbyssAI Mutual NDA", "NDAABYSS") {
        nextTokenId = 1;
    }

    /**
     * @notice Mint a new mutual NDA NFT (draft, unsigned)
     * @param _partyA First party address
     * @param _partyB Second party address
     * @param _ndaTitle Human-readable title for the NDA
     * @dev Only the owner (admin) can create the initial draft. Either party
     *      can later sign to attest.
     */
    function createNDA(
        address _partyA,
        address _partyB,
        string calldata _ndaTitle
    ) external onlyOwner nonReentrant {
        require(_partyA != address(0), "Invalid party A");
        require(_partyB != address(0), "Invalid party B");
        require(_partyA != _partyB, "Parties must differ");
        require(!mutualNDAExists[_partyA][_partyB], "NDA already exists between parties");
        require(!mutualNDAExists[_partyB][_partyA], "NDA already exists between parties");

        uint256 tokenId = nextTokenId++;
        _safeMint(_partyA, tokenId);

        ndaRecords[tokenId] = NDARecord({
            partyA: _partyA,
            partyB: _partyB,
            ndaHash: "",
            ndaTitle: _ndaTitle,
            effectiveDate: block.timestamp,
            partyASigned: false,
            partyBSigned: false,
            fullyExecuted: false,
            revoked: false
        });

        mutualNDAExists[_partyA][_partyB] = true;
        partyNDAs[_partyA].push(tokenId);
        partyNDAs[_partyB].push(tokenId);

        emit NDAMinted(tokenId, _partyA, _partyB, "", block.timestamp);
    }

    /**
     * @notice Upload IPFS hash of the signed NDA document
     * @param _tokenId The NDA token ID
     * @param _hash    IPFS hash (CID) of the executed NDA document
     * @dev Can be called by either party before full execution.
     */
    function setNDAHash(uint256 _tokenId, string calldata _hash) external nonReentrant {
        NDARecord storage r = ndaRecords[_tokenId];
        require(_hash != "", "Hash cannot be empty");
        require(r.partyA == msg.sender || r.partyB == msg.sender, "Not a party");
        require(!r.revoked, "NDA revoked");
        require(!r.fullyExecuted, "Already executed");
        r.ndaHash = _hash;
    }

    /**
     * @notice Party A signs (attests) the NDA
     * @param _tokenId The NDA token ID
     * @dev Requires msg.sender == partyA. Sets partyASigned = true.
     *      If both parties signed, marks fullyExecuted = true.
     */
    function signPartyA(uint256 _tokenId) external nonReentrant {
        _sign(_tokenId, true);
    }

    /**
     * @notice Party B signs (attests) the NDA
     * @param _tokenId The NDA token ID
     * @dev Requires msg.sender == partyB. Sets partyBSigned = true.
     *      If both parties signed, marks fullyExecuted = true.
     */
    function signPartyB(uint256 _tokenId) external nonReentrant {
        _sign(_tokenId, false);
    }

    function _sign(uint256 _tokenId, bool _isPartyA) internal nonReentrant {
        NDARecord storage r = ndaRecords[_tokenId];
        require(!r.revoked, "NDA revoked");
        require(r.ndaHash != "", "NDA hash not set");
        require(!r.fullyExecuted, "Already fully executed");

        if (_isPartyA) {
            require(msg.sender == r.partyA, "Only Party A can sign as A");
            require(!r.partyASigned, "Party A already signed");
            r.partyASigned = true;
        } else {
            require(msg.sender == r.partyB, "Only Party B can sign as B");
            require(!r.partyBSigned, "Party B already signed");
            r.partyBSigned = true;
        }

        if (r.partyASigned && r.partyBSigned) {
            r.fullyExecuted = true;
            r.effectiveDate = block.timestamp;
        }

        emit NDASigned(_tokenId, msg.sender, r.fullyExecuted);
    }

    /**
     * @notice Revoke an unsigned or partially executed NDA
     * @param _tokenId The NDA token ID
     * @dev Either party may revoke before full execution. Burns the token.
     */
    function revokeNDA(uint256 _tokenId) external nonReentrant {
        NDARecord storage r = ndaRecords[_tokenId];
        require(!r.revoked, "Already revoked");
        require(!r.fullyExecuted, "Cannot revoke executed NDA");
        require(msg.sender == r.partyA || msg.sender == r.partyB, "Not a party");

        r.revoked = true;
        mutualNDAExists[r.partyA][r.partyB] = false;

        _burn(_tokenId);

        emit NDARevoked(_tokenId, msg.sender);
    }

    /**
     * @notice Check if an NDA is fully executed (both parties signed)
     * @param _tokenId The NDA token ID
     * @return True if fully executed
     */
    function isExecuted(uint256 _tokenId) public view returns (bool) {
        return ndaRecords[_tokenId].fullyExecuted;
    }

    /**
     * @notice Get NDA record summary
     * @param _tokenId The NDA token ID
     * @return Structured record data
     */
    function getNDARecord(uint256 _tokenId)
        external
        view
        returns (
            address partyA,
            address partyB,
            string memory ndaHash,
            string memory ndaTitle,
            uint256 effectiveDate,
            bool partyASigned,
            bool partyBSigned,
            bool fullyExecuted,
            bool revoked
        )
    {
        NDARecord storage r = ndaRecords[_tokenId];
        return (
            r.partyA,
            r.partyB,
            r.ndaHash,
            r.ndaTitle,
            r.effectiveDate,
            r.partyASigned,
            r.partyBSigned,
            r.fullyExecuted,
            r.revoked
        );
    }

    /**
     * @notice Soulbound enforcement: disable transfers
     */
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal override {
        require(!soulbound, "NDA NFTs are soulbound and non-transferable");
    }

    /**
     * @notice Owner can pause/unpause soulbound behavior (emergency only)
     * @param _soulbound New soulbound state
     */
    function setSoulbound(bool _soulbound) external onlyOwner {
        soulbound = _soulbound;
    }
}
