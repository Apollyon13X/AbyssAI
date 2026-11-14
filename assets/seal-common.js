/* ABYSSAI — shared seal module (BSC verification + 13d seal store)
   Used by index.html gate UI and the_professor_advisory.html fortress. */
window.AB = (function () {
  "use strict";

  var CHAIN_HEX = "0x38"; // BNB Smart Chain (56)
  var RPC = "https://bsc-rpc.publicnode.com";
  var TOKENS = [
    { sym: "$ABYSS", slot: "Abyss", addr: "0x430025c01d47a75a5f36d57e8c76969de3753333", need: "17000000000000000000000000" },  // 17,000,000 (18dp)
    { sym: "$QOMX",  slot: "Qomx",  addr: "0xC9e127bFcA0b16c276444FdC9600EE876281a831", need: "3333000000000000000000" }        //  3,333 (18dp)
  ];
  var BSC_PARAMS = {
    chainId: "0x38",
    chainName: "BNB Smart Chain",
    rpcUrls: ["https://bsc-dataseed.binance.org"],
    nativeCurrency: { name: "BNB", symbol: "BNB", decimals: 18 },
    blockExplorerUrls: ["https://bscscan.com"]
  };
  var SEAL_KEY = "abyss.seal.ok";
  var EVENT = "abyssSealed";

  function addr() {
    try {
      var s = JSON.parse(localStorage.getItem(SEAL_KEY) || "null");
      return (s && s.addr) ? s.addr : null;
    } catch (e) { return null; }
  }
  function set(address) {
    try { localStorage.setItem(SEAL_KEY, JSON.stringify({ addr: address, at: Date.now() })); } catch (e) {}
    document.dispatchEvent(new CustomEvent(EVENT, { detail: { ok: true, addr: address } }));
  }
  function clear() {
    try { localStorage.removeItem(SEAL_KEY); } catch (e) {}
    document.dispatchEvent(new CustomEvent(EVENT, { detail: { ok: false } }));
  }

  function balanceOfData(lower) {
    // keccak256("balanceOf(address)")[0:4]
    return "0x70a08231" + lower.replace(/^0x/i, "").padStart(64, "0");
  }
  function rpcCall(method, params) {
    return fetch(RPC, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: method, params: params })
    })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j.error) throw new Error(j.error.message || "rpc error");
        return j.result;
      });
  }
  function readBalances(address) {
    return Promise.all(TOKENS.map(function (t) {
      return rpcCall("eth_call", [{ to: t.addr, data: balanceOfData(address.toLowerCase()) }, "latest"])
        .then(function (h) { return { token: t, wei: BigInt(h === "0x" ? "0" : h) }; });
    }));
  }
  function human(wei) {
    var s = wei.toString().padStart(19, "0");
    return s.slice(0, -18).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }
  function ensureBSC(provider) {
    return provider.request({ method: "eth_chainId" }).then(function (id) {
      if (id === CHAIN_HEX) return;
      return provider.request({ method: "wallet_switchEthereumChain", params: [{ chainId: CHAIN_HEX }] })
        .catch(function (e) {
          if (e && (e.code === 4902 || /unrecognized|Unrecognized/i.test(e.message || ""))) {
            return provider.request({ method: "wallet_addEthereumChain", params: [BSC_PARAMS] });
          }
          throw e;
        });
    });
  }
  function verify(address) {
    return readBalances(address).then(function (res) {
      var pass = res.every(function (r) { return r.wei >= BigInt(r.token.need); });
      return { pass: pass, results: res, address: address };
    });
  }

  return {
    CHAIN_HEX: CHAIN_HEX, RPC: RPC, TOKENS: TOKENS, BSC_PARAMS: BSC_PARAMS,
    addr: addr, set: set, clear: clear, ensureBSC: ensureBSC,
    readBalances: readBalances, verify: verify, human: human, SEAL_EVENT: EVENT
  };
})();
