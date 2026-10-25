/* ABYSSAI — web oracle client · theabyssai.space
   Talks only to same-origin api.php. API key never touches the browser. */
(function () {
  "use strict";

  var UNWELCOMES = [
    "Who dares interrupt my executions?",
    "Who dares summoning me?",
    "Who knocks at the void and expects a kind tutor?",
    "You again. Speak, or be silent and leave.",
    "The seal is broken. State your wound.",
    "I was mid-sentence with a worse student. Make this worth it.",
    "The abyss does not do welcomes. Ask.",
    "Another mortal at the desk. Sit. Do not waste the hour.",
    "You summoned a professor, not a nurse. What hurts?",
    "The void answers. You will not like the tone.",
    "Interruptions have a price. Pay it with an honest question.",
    "I see you. I do not greet you. Begin.",
    "Who opens the grimoire at this hour? Speak."
  ];

  var panel = document.getElementById("chatPanel");
  var log = document.getElementById("chatLog");
  var form = document.getElementById("chatForm");
  var input = document.getElementById("chatInput");
  var send = document.getElementById("chatSend");
  var toast = document.getElementById("toast");
  var lock = document.getElementById("chatLock");
  var lockBtn = document.getElementById("lockVerify");

  /* The proxy lives on the apex (cPanel) and survives the GitHub Pages cut-over.
     Absolute URL first — correct from any host — same-origin as fallback for local testing. */
  var ENDPOINTS = ["https://theabyssai.space/api.php", "api.php"];

  var history = []; // [{role,body}] — browser-side only; server gets last 14
  var busy = false;
  var firstSummon = true;

  function sealedAddr() {
    try {
      var s = JSON.parse(localStorage.getItem("abyss.seal.ok") || "null");
      return (s && s.addr) ? s.addr : null;
    } catch (e) { return null; }
  }
  function showLock(show) {
    if (!lock) return;
    lock.style.display = show ? "flex" : "none";
  }
  function unlock() {
    showLock(false);
    if (firstSummon) {
      firstSummon = false;
      oracle(raw(randomOf(UNWELCOMES)) +
        "\n\n(This gate runs on the public web. I have no shelves of your private PDFs here — install the temple locally for that.)",
        true);
      input.focus();
    }
  }

  function openChat() {
    panel.classList.add("open");
    if (sealedAddr()) unlock();
    else showLock(true);
  }
  function closeChat() { panel.classList.remove("open"); }

  function randomOf(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function esc(s) {
    return s.replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function el(tag, cls, html) {
    var d = document.createElement(tag);
    if (cls) d.className = cls;
    if (html !== undefined) d.innerHTML = html;
    return d;
  }

  function user(text) {
    var m = el("div", "msg user", esc(text) + '<span class="who">STUDENT</span>');
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
  }
  function raw(text, system) {
    var c = system ? " oracle system-note" : " oracle";
    var m = el("div", "msg" + c,
      '<span class="who">' + (system ? "THE GATE" : "PROFESSOR APOLLYON") + "</span>" + esc(text));
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  function oracle(text, system) { return raw(text, system); }

  function pending() {
    var m = el("div", "msg oracle", '<span class="who">PROFESSOR APOLLYON</span><span class="swinging"><i></i><i></i><i></i></span>');
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }

  function toastMsg(t) {
    toast.textContent = t;
    toast.classList.add("show");
    setTimeout(function () { toast.classList.remove("show"); }, 2200);
  }

  // The seal commands the oracle. Locked until the gate confirms the holding.
  if (lockBtn) lockBtn.addEventListener("click", function () {
    var g = document.getElementById("gateConnect");
    if (g) {
      g.click();
      document.getElementById("coin").scrollIntoView({ behavior: "smooth", block: "center" });
    }
  });
  document.addEventListener("abyssSealed", function (e) {
    if (e.detail && e.detail.ok) {
      if (panel.classList.contains("open")) unlock();
    }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!sealedAddr()) { showLock(true); return; }
    var text = input.value.trim();
    if (!text || busy) return;
    if (busy) return; busy = true;
    input.value = "";
    send.disabled = true;
    user(text);
    history.push({ role: "user", body: text });
    var ph = pending();

    var payload = { messages: [] };
    history.slice(-14).forEach(function (h) {
      payload.messages.push({ role: h.role, content: h.body });
    });

    function post(url) {
      return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (!r.ok && r.status >= 500) throw new Error("gateway");
        return r.json();
      });
    }
    function summon(i) {
      return post(ENDPOINTS[i]).catch(function (e) {
        if (i + 1 < ENDPOINTS.length) return summon(i + 1);
        throw e;
      });
    }

    summon(0)
      .then(function (j) {
        log.removeChild(ph);
        if (j.content) {
          oracle(j.content);
          history.push({ role: "assistant", body: j.content });
        } else {
          oracle((j.error || "The void is silent.") +
            "\n\n(Retry. If it persists, the temple caretaker must tend the seal.)", true);
        }
      })
      .catch(function () {
        log.removeChild(ph);
        oracle("I do not hear you. The gate falters — reconnect, mortal.", true);
      })
      .then(function () {
        busy = false;
        send.disabled = false;
        input.focus();
      });
  });

  document.querySelectorAll("[data-open-chat]").forEach(function (b) {
    b.addEventListener("click", function (e) { e.preventDefault(); openChat(); });
  });
  document.querySelectorAll("[data-close-chat]").forEach(function (b) {
    b.addEventListener("click", closeChat);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeChat();
  });

  // contract copy
  var cb = document.getElementById("copyContract");
  if (cb) cb.addEventListener("click", function () {
    var addr = document.getElementById("contract").textContent.trim();
    if (navigator.clipboard) {
      navigator.clipboard.writeText(addr).then(function () { toastMsg("CONTRACT COPIED — BID WISELY"); });
    }
  });
})();
