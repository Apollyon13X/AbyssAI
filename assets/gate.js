/* ABYSSAI — Holders' Gate (index.html) · theabyssai.space
   Verify 17,000,000 $ABYSS AND 3,333 $QOMX on BSC.
   On pass: the button ignites into ENTER THE ABYSS and leads to
   /the_professor_advisory. Reads go to a public BSC RPC (AB module). */
(function () {
  "use strict";

  var conn = document.getElementById("gateConnect");
  var body = document.getElementById("gateBody");
  if (!conn || !body) return;

  var provider = null;
  var account = null;

  function short(a) { return a.slice(0, 6) + "…" + a.slice(-4); }
  function fail(t) {
    conn.textContent = t;
    setTimeout(function () { resetLabel(); }, 3200);
  }
  function resetLabel() {
    if (window.AB && AB.addr()) { conn.textContent = "⟁ ENTER THE ABYSS"; conn.classList.add("flame-blood"); return; }
    conn.textContent = "Connect Wallet · Verify Holding";
  }
  setLabel();

  function setLabel() {
    if (AB.addr()) {
      conn.textContent = "⟁ ENTER THE ABYSS";
      conn.classList.add("flame-blood");
    }
  }

  function render(res) {
    body.hidden = false; // reveal rows + verdict in all outcomes
    document.getElementById("gateAddr").textContent = "◈ " + short(res.address);
    var all = true;
    res.results.forEach(function (r) {
      var pass = r.wei >= BigInt(r.token.need);
      all = all && pass;
      id(r.token.slot, "val").textContent = AB.human(r.wei);
      var mark = id(r.token.slot, "mark");
      mark.textContent = pass ? "✓" : "✗";
      mark.className = "mark " + (pass ? "ok" : "bad");
      id(r.token.slot, "row").className = "gate-row " + (pass ? "ok" : "bad");
    });
    var v = document.getElementById("gateVerdict");
    if (all) {
      v.textContent = "⟁ SEAL CONFIRMED — ENTER THE ABYSS";
      v.className = "gate-verdict ok";
      AB.set(res.address);
      conn.textContent = "⟁ ENTER THE ABYSS";
      conn.classList.add("flame-blood");
    } else {
      v.textContent = "SEAL WITHHELD — both holdings are required, not or.";
      v.className = "gate-verdict bad";
      AB.clear();
      conn.classList.remove("flame-blood");
      conn.textContent = "Connect Wallet · Verify Holding";
    }
  }
  function id(slot, kind) {
    var map = { Abyss: "Abyss", Qomx: "Qomx" };
    return document.getElementById(kind + map[slot] || kind);
  }

  function verify(cand) {
    var addr = cand || account || (AB.addr && AB.addr());
    if (!addr) return fail("No wallet account — reconnect");
    conn.textContent = "Counting the endless eyes…";
    return AB.verify(addr)
      .then(render)
      .catch(function () { fail("RPC failed — try again"); });
  }

  // Returning holder: re-verify silently on load so the page reflects the seal
  if (window.AB && AB.addr()) {
    verify(AB.addr()).catch(function () {});
  }

  conn.addEventListener("click", function () {
    if (AB.addr()) { location.href = "the_professor_advisory.html"; return; }
    provider = window.ethereum;
    if (!provider) { fail("No Web3 wallet found — install MetaMask"); return; }
    conn.textContent = "Opening the seal…";
    provider.request({ method: "eth_requestAccounts" })
      .then(function (accs) {
        account = accs && accs[0];
        if (!account) throw new Error("no account");
        return AB.ensureBSC(provider).then(verify);
      })
      .catch(function (e) {
        if (e && (e.code === 4001 || /rejected|denied/i.test(String(e.message || "")))) fail("Summon refused — wallet rejected the rite");
        else fail("The gate jammed — try again");
      });
  });

  if (window.ethereum) {
    window.ethereum.on("accountsChanged", function (accs) {
      account = accs && accs[0];
      if (account) verify();
      else {
        body.hidden = true;
        AB.clear();
        resetLabel();
      }
    });
    window.ethereum.on("chainChanged", function () {
      if (account) AB.ensureBSC(window.ethereum).then(verify).catch(function () {});
    });
  }

  // Contract copy (moved from the old chat widget)
  var cb = document.getElementById("copyContract");
  if (cb && !cb.dataset.wired) {
    cb.dataset.wired = "1";
    cb.addEventListener("click", function () {
      var addr = (document.getElementById("contract").textContent || "").trim();
      if (navigator.clipboard && addr) {
        navigator.clipboard.writeText(addr).then(function () { toastMsg("CONTRACT COPIED — BID WISELY"); });
      }
    });
  }
  function toastMsg(t) {
    var toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = t;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2200);
  }

  // ---------- caretaker ledger: struck ONCE against the INITIAL pool ----------
  // Change these three lines only if a new agreement is signed; never per-login.
  var LEDGER = {
    poolAbyss: "17000000",       // initial $ABYSS pool
    poolQomx:  "3333",           // initial $QOMX pool
    abyssCuts: [ ["operations", 7], ["CEO of team split", 3] ],  // % points of pool
    qomxCut: 3,                  // % point of pool
    caretaker: "0x1b84ff8487A5b773a50a311015f86849da720EBC"
  };
  function num(str) { return parseFloat(str); }
  function fmt(n) {
    return n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 });
  }
  function strikeLedger() {
    var a = num(LEDGER.poolAbyss), q = num(LEDGER.poolQomx);
    var abyssTotal = a * (LEDGER.abyssCuts.reduce(function (s, c) { return s + c[1]; }, 0) / 100);
    var qomxTotal  = q * (LEDGER.qomxCut / 100);
    var elA = document.getElementById("ledAbyss");
    var elQ = document.getElementById("ledQomx");
    if (elA) elA.textContent = "→ caretaker " + fmt(abyssTotal) + " (" +
      LEDGER.abyssCuts.map(function (c) { return c[0] + " " + fmt(a * c[1] / 100); }).join(" + ") + ")";
    if (elQ) elQ.textContent = "→ caretaker " + fmt(Math.round(qomxTotal * 100) / 100) + " (custodial fee " + LEDGER.qomxCut + "%)";
  }
  if (document.getElementById("ledAbyss")) strikeLedger();
  window.AB.StrikeLedger = strikeLedger; // portal lock reuses the same strike
})();
