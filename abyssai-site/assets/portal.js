/* ABYSSAI — THE PROFESSOR'S ADVISORY · abyssai.space/the_professor_advisory
   Full-page Oracle. Seal-checked entry. 13-day history shelf with PDF/DOCX export,
   .json sync files (import = merge). Optional ARCHIVES mode pulls public-domain
   passages from archive.org (filtered shelves: psychology, propaganda/influence
   read defensively, mysticism/stoicism, occultism/hermetics, manipulation —
   inoculation only, never a playbook). */
(function () {
  "use strict";

  var RETENTION_MS = 13 * 24 * 3600 * 1000;
  var STORE_KEY = "abyss.threads.v2";
  var SEAL_KEY = "abyss.seal.ok";
  var SEAL_TTL_MS = 7 * 3600 * 1000; // 7 hours session
  var ENDPOINTS = ["https://abyssai.space/api.php", "api.php"];
  var UNWELCOMES = [
    "Who dares interrupt my executions?", "Who dares summoning me?",
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
  var ARCHIVE_SHELVES = [
    { key: "psychology", terms: 'subject:(psychology OR psychoanalysis OR "analytical psychology")' },
    { key: "influence",  terms: 'subject:(propaganda OR persuasion OR "public opinion" OR "social influence")' },
    { key: "spiritual",  terms: 'subject:(mysticism OR stoicism OR "spiritual life")' },
    { key: "occult",     terms: 'subject:(occultism OR hermetics OR hermeticism OR alchemy OR theurgy)' },
    { key: "dark-psych (defensive)", terms: 'subject:(narcissism OR "psychological manipulation" OR machiavellianism)' }
  ];
  var STOPWORDS = "the a an of and or to in is are was were for on with as that this it at be by from i my me you your we our not do did what how why when who".split(" ");

  // ---------- dom ----------
  var log = document.getElementById("chatLog");
  var form = document.getElementById("chatForm");
  var input = document.getElementById("chatInput");
  var send = document.getElementById("chatSend");
  var lock = document.getElementById("portalLock");
  var lockBtn = document.getElementById("lockVerify");
  var lockRows = document.getElementById("lockRows");
  var timerChip = document.getElementById("archiveTimer");
  var arriveLeft = document.getElementById("arriveLeft");
  var threadList = document.getElementById("threadList");
  var toast = document.getElementById("toast");
  var btnArchives = document.getElementById("btnArchives");
  var btnNew = document.getElementById("btnNew");
  var btnExports = document.getElementById("btnExports");
  var exportDrop = document.getElementById("exportDrop");
  var importFile = document.getElementById("importFile");
  var sideToggle = document.getElementById("sideToggle");

  // ---------- state ----------
  var busy = false;
  var archivesOn = false;
  var store = load();
  var activeId = null;
  var firstSummon = true;
  var sessionStart = null; // session start time for 7-hour timeout
  var sessionTimer = null; // interval for session timeout check

  // ---------- seal helpers ----------
  function sealLoad() {
    try {
      var s = JSON.parse(localStorage.getItem(SEAL_KEY) || "null");
      if (s && s.addr && s.ts) {
        var age = Date.now() - s.ts;
        if (age < SEAL_TTL_MS) return { addr: s.addr, ts: s.ts, valid: true };
        // expired — clear
        localStorage.removeItem(SEAL_KEY);
      }
    } catch (e) {}
    return null;
  }
  function sealSave(addr) {
    try { localStorage.setItem(SEAL_KEY, JSON.stringify({ addr: addr, ts: Date.now() })); } catch (e) {}
  }
  function sealClear() {
    try { localStorage.removeItem(SEAL_KEY); } catch (e) {}
  }

  // ---------- session timeout (7 hours) ----------
  function startSessionTimer() {
    if (sessionTimer) clearInterval(sessionTimer);
    sessionStart = Date.now();
    sessionTimer = setInterval(function () {
      var age = Date.now() - sessionStart;
      if (age >= SEAL_TTL_MS) {
        // 7 hours reached — auto logout
        sealClear();
        if (sessionTimer) { clearInterval(sessionTimer); sessionTimer = null; }
        sessionStart = null;
        activeId = null;
        log.innerHTML = "";
        renderThreads();
        renderThread();
        showLock(true);
        toastMsg("Session expired — 7 hours reached. Reconnect to enter again.");
      }
    }, 60000); // check every minute
  }
  function stopSessionTimer() {
    if (sessionTimer) { clearInterval(sessionTimer); sessionTimer = null; }
    sessionStart = null;
  }

  // ---------- load ----------
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(STORE_KEY) || "null");
      if (s && Array.isArray(s.threads)) return s;
    } catch (e) {}
    return { threads: [] };
  }
  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) { toastMsg("Archive full — the disks of yesterday reject new ink"); }
  }
  function purge() {
    var now = Date.now();
    var before = store.threads.length;
    store.threads = store.threads.filter(function (t) { return (t.created + RETENTION_MS) > now; });
    if (store.threads.length !== before) { save(); toastMsg((before - store.threads.length) + " working(s) dissolved by the void"); }
  }
  function soonest() {
    if (!store.threads.length) return null;
    var m = Infinity;
    store.threads.forEach(function (t) { m = Math.min(m, t.created); });
    return m + RETENTION_MS;
  }
  function active() {
    for (var i = 0; i < store.threads.length; i++) if (store.threads[i].id === activeId) return store.threads[i];
    return null;
  }
  function ensureThread() {
    if (!active()) {
      var t = { id: "w" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), title: "Untitled working", created: Date.now(), updated: Date.now(), msgs: [] };
      store.threads.push(t); activeId = t.id; save();
    }
    return active();
  }

  // ---------- dom helpers ----------
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function el(tag, cls, html) { var d = document.createElement(tag); if (cls) d.className = cls; if (html !== undefined) d.innerHTML = html; return d; }
  function toastMsg(t) { toast.textContent = t; toast.classList.add("show"); setTimeout(function () { toast.classList.remove("show"); }, 2600); }
  function user(text) {
    log.appendChild(el("div", "msg user", esc(text) + '<span class="who">STUDENT · ' + fmtT(Date.now()) + "</span>"));
    log.scrollTop = log.scrollHeight;
  }
  function oracle(text, system) {
    var msg = el("div", "msg oracle" + (system ? " system-note" : ""),
      '<span class="who">' + (system ? "THE GATE" : "PROFESSOR APOLLYON · " + fmtT(Date.now())) + "</span>" + esc(text));
    log.appendChild(msg); log.scrollTop = log.scrollHeight;
    return msg;
  }
  function pending() {
    var m = el("div", "msg oracle", '<span class="who">PROFESSOR APOLLYON</span><span class="swinging"><i></i><i></i><i></i><i></i></span>');
    log.appendChild(m); log.scrollTop = log.scrollHeight;
    return m;
  }
  function fmtT(ms) {
    var d = new Date(ms);
    return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);
  }
  function fmtDay(ms) {
    var d = new Date(ms);
    return d.toISOString().slice(0, 10);
  }
  function slug(t) {
    return (t || "advisory").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || "advisory";
  }

  // ---------- timer ----------
  function fmtRemaining(ms) {
    var neg = ms < 0; ms = Math.abs(ms);
    var d = Math.floor(ms / 86400000);
    var h = Math.floor((ms % 86400000) / 3600000);
    var m = Math.floor((ms % 3600000) / 60000);
    return (neg ? "PAST DUE " : "") + d + "d " + ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2);
  }
  function tick() {
    purge();
    var s = soonest();
    if (s === null) {
      timerChip.textContent = "ARCHIVE HOLLOW · 13d SHELF STARTS ON FIRST INK";
      timerChip.classList.remove("severe");
      arriveLeft.textContent = "nothing to dissolve yet";
    } else {
      var r = s - Date.now();
      timerChip.textContent = "DISSOLVES IN " + fmtRemaining(r);
      timerChip.classList.toggle("severe", r < 2 * 86400000);
      arriveLeft.textContent = fmtRemaining(r);
    }
    renderThreads();
  }

  // ---------- threads sidebar ----------
  function threadTitle(t) {
    for (var i = 0; i < t.msgs.length; i++) if (t.msgs[i].r === "user") return t.msgs[i].text.slice(0, 64);
    return t.title || "Untitled working";
  }
  function renderThreads() {
    threadList.innerHTML = "";
    store.threads.slice().sort(function (a, b) { return b.updated - a.updated; }).forEach(function (t) {
      var li = el("li", t.id === activeId ? "active" : "");
      li.appendChild(el("span", "t-title", esc(threadTitle(t)) + '<span class="t-date">' + fmtDay(t.created) + "</span>"));
      var del = el("button", "t-del", "✕");
      del.title = "Burn this working";
      del.addEventListener("click", function (e) {
        e.stopPropagation();
        if (!confirm("Burn this working? The void keeps no ashes.")) return;
        store.threads = store.threads.filter(function (x) { return x.id !== t.id; });
        if (activeId === t.id) activeId = null;
        save(); tick(); ensureThread(); renderThread();
      });
      li.appendChild(del);
      li.addEventListener("click", function () { activeId = t.id; save(); renderThread(); renderThreads(); });
      threadList.appendChild(li);
    });
  }
  function renderThread() {
    log.innerHTML = "";
    var t = active(); if (!t) return;
    t.msgs.forEach(function (m) {
      if (m.r === "user") log.appendChild(el("div", "msg user", esc(m.text) + '<span class="who">STUDENT · ' + fmtT(m.t) + "</span>"));
      else log.appendChild(el("div", "msg oracle" + (m.r === "gate" ? " system-note" : ""), '<span class="who">' + (m.r === "gate" ? "THE GATE" : "PROFESSOR APOLLYON · " + fmtT(m.t)) + "</span>" + esc(m.text)));
    });
    log.scrollTop = log.scrollHeight;
  }

  // ---------- ARCHIVES (archive.org public endpoints; CORS:*) ----------
  function keywords(text) {
    var w = text.toLowerCase().replace(/[^a-z']+/g, " ").split(/\s+/).filter(function (x) {
      return x.length > 3 && STOPWORDS.indexOf(x) === -1;
    });
    return w.slice(0, 6);
  }
  function jget(url, ms) {
    var c = new AbortController();
    var to = setTimeout(function () { c.abort(); }, ms || 12000);
    return fetch(url, { signal: c.signal }).then(function (r) {
      clearTimeout(to);
      if (!r.ok) throw new Error("http " + r.status);
      return r.json();
    });
  }
  function collectPassages(q) {
    var kws = keywords(q);
    var query = kws.length ? kws.join(" ") : "shadow work";
    var passages = [];
    var hunts = ARCHIVE_SHELVES.map(function (shelf) {
      var url = "https://archive.org/advancedsearch.php?q=" + encodeURIComponent("(" + shelf.terms + ") AND mediatype:(texts)") +
        "&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=year&sort%5B%5D=downloads+desc&rows=3&output=json";
      return jget(url).then(function (j) {
        var docs = (j.response && j.response.docs) || [];
        return Promise.allSettled(docs.map(function (d) {
          return jget("https://archive.org/metadata/" + d.identifier, 10000).then(function (m) {
            var u = "https://" + m.server + "/fulltext/inside.php?item_id=" + d.identifier +
              "&doc=" + d.identifier + "&path=" + encodeURIComponent(m.dir) + "&q=" + encodeURIComponent(query);
            return jget(u, 14000).then(function (f) {
              var ms = (f && f.matches) || [];
              for (var i = 0; i < ms.length; i++) {
                var txt = String(ms[i].text || "").replace(/\s+/g, " ").trim();
                if (txt.length >= 60) {
                  passages.push({ title: (d.creator || "") + " “" + d.title + "” [" + d.identifier + "]", text: txt.slice(0, 1500) });
                  return; // one passage per book
                }
              }
            });
          });
        }));
      }).catch(function () { /* shelf quiet */ });
    });
    return Promise.allSettled(hunts).then(function () {
      return passages.slice(0, 6);
    });
  }

  // ---------- send ----------
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!sealLoad()) { showLock(true); return; }
    var text = input.value.trim();
    if (!text || busy) return;
    busy = true; send.disabled = true; input.value = "";
    var t = ensureThread();
    t.msgs.push({ r: "user", text: text, t: Date.now() }); t.updated = Date.now(); save();
    user(text);
    var ph = pending();

    var payload = { messages: [] };
    var hist = t.msgs.slice(-14).filter(function (m) { return m.r === "user" || m.r === "oracle"; });
    while (hist.length && hist[0].r !== "user") hist.shift(); // api.php expects the first voice to be the student's
    hist.forEach(function (m) {
      payload.messages.push({ role: m.r === "user" ? "user" : "assistant", content: m.text });
    });

    var when = Promise.resolve([]);
    if (archivesOn) when = collectPassages(text).then(function (p) {
      if (p.length) payload.context = { passages: p };
      return p;
    });

    when.then(function (passages) {
      function post(url) {
        return fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        }).then(function (r) {
          if (!r.ok && r.status >= 500 && url !== ENDPOINTS[ENDPOINTS.length - 1]) throw new Error("gateway-" + r.status);
          return r.json();
        });
      }
      function summon(i) {
        return post(ENDPOINTS[i]).catch(function (err) {
          if (i + 1 < ENDPOINTS.length) return summon(i + 1);
          throw err;
        });
      }
      return summon(0).then(function (j) {
        log.removeChild(ph);
        var t2 = active(); // use existing active thread, do not auto-create
        if (!t2) t2 = t;
        if (j.content) {
          oracle(j.content);
          t2.msgs.push({ r: "oracle", text: j.content, t: Date.now() }); t2.updated = Date.now(); save();
        } else {
          var errMsg = j.error || "The void is silent.";
          var errCode = j.code ? " (code " + j.code + ")" : "";
          var note = errMsg + errCode +
            "\n\n(Retry. If it persists, the temple caretaker must tend the seal.)";
          oracle(note, true);
          t2.msgs.push({ r: "gate", text: note, t: Date.now() }); save();
        }
        renderThreads();
      });
    }).catch(function (err) {
      try { log.removeChild(ph); } catch (e) {}
      var msg = err.message || "The void is silent.";
      if (msg.indexOf("gateway-") === 0) msg = "Gateway error HTTP " + msg.replace("gateway-", "") + " — try again.";
      else if (msg === "gateway") msg = "Gateway error — try the alternate endpoint.";
      var o = oracle(msg + "\n\n(Retry. If it persists, the temple caretaker must tend the seal.)", true);
      var t2 = active(); if (!t2) t2 = t;
      t2.msgs.push({ r: "gate", text: o.textContent, t: Date.now() }); save();
    }).then(function () {
      busy = false; send.disabled = false; input.focus();
    });
  });

  // ---------- exports ----------
  function threadToText(t) {
    var lines = [
      "PROFESSOR APOLLYON'S ADVISORY — ABYSSAI · abyssai.space",
      "Working: " + threadTitle(t),
      "Opened: " + new Date(t.created).toISOString().slice(0, 16).replace("T", " ") + " UTC",
      "Holder: " + (sealLoad() ? sealLoad().addr : "unjudged"),
      "────────────────────────────────────────",
      ""
    ];
    t.msgs.forEach(function (m) {
      var who = m.r === "user" ? "STUDENT" : (m.r === "gate" ? "THE GATE" : "PROFESSOR APOLLYON");
      lines.push("[" + fmtT(m.t) + "] " + who + ":");
      lines.push(m.text);
      lines.push("");
    });
    lines.push("────────────────────────────────────────", "The abyss network touches nothing local. This file was forged in your browser.");
    return lines.join("\n");
  }
  function dl(blob, name) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 800);
  }
  var EXP_PREFIX;
  function exportPDF(t) {
    if (typeof window.jspdf === "undefined") return toastMsg("PDF forge is cold (CDN offline) — use SYNC FILE");
    var docPDF = new window.jspdf.jsPDF({ unit: "pt", format: "a4" });
    if (typeof EXP_PREFIX === "undefined") EXP_PREFIX = 0;
    var M = 54, W = docPDF.internal.pageSize.getWidth() - 2 * M, Y = 64;
    function pageBreak(need) {
      if (Y + need > docPDF.internal.pageSize.getHeight() - 48) { docPDF.addPage(); Y = 64; }
    }
    docPDF.setFont("times", "normal");
    docPDF.setFontSize(16);
    docPDF.text("PROFESSOR APOLLYON'S ADVISORY", M, Y); Y += 20;
    docPDF.setFontSize(10);
    docPDF.setTextColor(120);
    docPDF.text("AbyssAI · Whispers From The Void · " + new Date().toISOString().slice(0, 10) + " · Holder " + (sealLoad() ? sealLoad().addr : "—"), M, Y); Y += 14;
    docPDF.setTextColor(40);
    docPDF.setFontSize(11);
    var msgs = t.msgs;
    var outer = 0;
    function line(l) {
      docPDF.setFont("times", "normal");
      var wrapped = docPDF.splitTextToSize(l, W);
      wrapped.forEach(function (seg) { pageBreak(16); docPDF.text(seg, M, Y); Y += 15; });
    }
    msgs.forEach(function (m) {
      var who = m.r === "user" ? "STUDENT" : (m.r === "gate" ? "THE GATE" : "PROFESSOR APOLLYON");
      pageBreak(18);
      docPDF.setFont("courier", "bold");
      line("[" + fmtT(m.t) + "] " + who);
      outer++;
      line(m.text || "");
      Y += 8;
    });
    docPDF.save("abyssai-advisory-" + slug(t.title) + ".pdf");
    toastMsg("PDF FORGED — " + msgs.length + " turns");
  }
  function exportDOCX(t) {
    if (typeof window.docx === "undefined") return toastMsg("DOCX forge is cold (CDN offline) — use SYNC FILE");
    var D = window.docx;
    var children = [
      new D.Paragraph({ text: "PROFESSOR APOLLYON'S ADVISORY", heading: D.HeadingLevel.HEADING_1 }),
      new D.Paragraph({ text: "AbyssAI · Whispers From The Void · " + new Date().toISOString().slice(0, 10), size: 18, italics: true })
    ];
    t.msgs.forEach(function (m) {
      var who = m.r === "user" ? "STUDENT" : (m.r === "gate" ? "THE GATE" : "PROFESSOR APOLLYON");
      children.push(new D.Paragraph({ text: who, bold: true, spacing: { before: 240 } }));
      (m.text || "").split("\n").forEach(function (ln) {
        children.push(new D.Paragraph({ text: ln }));
      });
    });
    var docDOCX = new D.Document({ sections: [{ properties: {}, children: children }] });
    D.Packer.toBlob(docDOCX).then(function (b) {
      dl(b, "abyssai-advisory-" + slug(t.title) + ".docx");
      toastMsg("DOCX FORGED — " + t.msgs.length + " turns");
    });
  }
  function exportJSON() {
    if (!store.threads.length) return toastMsg("Nothing to sync — the archive is hollow");
    var payload = { kind: "abyssai-advisory-sync", v: 2, exported: Date.now(), threads: store.threads };
    dl(new Blob([JSON.stringify(payload, null, 1)], { type: "application/json" }),
      "abyssai-advisory-sync-" + new Date().toISOString().slice(0, 10) + ".json");
    toastMsg("SYNC FILE FORGED — " + store.threads.length + " workings");
  }
  exportDrop.addEventListener("click", function (e) {
    var btn = e.target.closest("button");
    if (!btn) return;
    exportDrop.parentNode.classList.remove("open");
    var t = ensureThread();
    if (btn.dataset.export === "pdf") exportPDF(t);
    if (btn.dataset.export === "docx") exportDOCX(t);
    if (btn.dataset.export === "json") exportJSON();
    if (btn.dataset.import) importFile.click();
  });
  btnExports.addEventListener("click", function (e) {
    e.stopPropagation();
    exportDrop.parentNode.classList.toggle("open");
  });
  document.addEventListener("click", function (e) {
    if (!exportDrop.contains(e.target) && e.target !== btnExports) exportDrop.parentNode.classList.remove("open");
  });
  importFile.addEventListener("change", function () {
    var f = importFile.files && importFile.files[0];
    importFile.value = "";
    if (!f) return;
    var fr = new FileReader();
    fr.onload = function () {
      try {
        var j = JSON.parse(String(fr.result));
        if (j.kind !== "abyssai-advisory-sync" || !Array.isArray(j.threads)) throw 0;
        var added = 0;
        j.threads.forEach(function (t) {
          if (!t || !Array.isArray(t.msgs)) return;
          var exists = store.threads.some(function (x) {
            return x.created === t.created &&
              (x.msgs[0] && t.msgs[0] && x.msgs[0].text === t.msgs[0].text);
          });
          if (exists) return;
          store.threads.push({ id: "w" + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), title: t.title || threadTitle(t), created: Number(t.created) || Date.now(), updated: Number(t.updated) || Date.now(), msgs: t.msgs.slice(0, 400) });
          added++;
        });
        save(); purge(); tick(); renderThread();
        toastMsg(added + " workings restored from the vessel");
      } catch (err) {
        toastMsg("That vessel will not open — wrong shape");
      }
    };
    fr.readAsText(f);
  });

  // ---------- archives toggle ----------
  btnArchives.addEventListener("click", function () {
    archivesOn = !archivesOn;
    btnArchives.textContent = archivesOn ? "ARCHIVES·ON" : "ARCHIVES·OFF";
    btnArchives.style.color = archivesOn ? "var(--gold-hi)" : "";
    toastMsg(archivesOn
      ? "ARCHIVES OPEN — archive.org shelves will be consulted (psychology · influence · spiritual · occult · dark-psych, inoculation only)"
      : "ARCHIVES CLOSED");
  });

  // ---------- misc chrome ----------
  btnNew.addEventListener("click", function () {
    activeId = null; ensureThread(); renderThread(); tick(); input.focus();
  });
  if (sideToggle) sideToggle.addEventListener("click", function () {
    document.querySelector(".portal-side").classList.toggle("open");
  });

  // ---------- seal gate ----------
  function showLock(s) {
    lock.style.display = s ? "flex" : "none";
  }
  function short(a) { return a.slice(0, 6) + "…" + a.slice(-4); }
  lockBtn.addEventListener("click", function () {
    var provider = window.ethereum;
    if (!provider) return toastMsg("No Web3 wallet found — install MetaMask");
    lockBtn.textContent = "Reading the endless eyes…";
    provider.request({ method: "eth_requestAccounts" })
      .then(function (accs) {
        var addr = accs && accs[0];
        if (!addr) throw new Error("no account");
        return AB.ensureBSC(provider).then(function () { return AB.verify(addr); });
      })
      .then(function (res) {
        res.results.forEach(function (r) {
          var pass = r.wei >= BigInt(r.token.need);
          var m = document.getElementById("mark" + r.token.slot + "Lock");
          var v = document.getElementById("val" + r.token.slot + "Lock");
          if (v) v.textContent = AB.human(r.wei);
          if (m) { m.textContent = pass ? "✓" : "✗"; m.className = "mark " + (pass ? "ok" : "bad"); }
        });
        if (res.pass) {
          AB.set(res.address);
          sealSave(res.address);
          startSessionTimer();
          showLock(false);
          if (store.threads.length > 0) {
            activeId = store.threads[store.threads.length - 1].id; // reopen most recent working
          } else {
            activeId = null; // no auto thread — user clicks NEW INVOCATION
          }
          renderThread();
          tick();
          toastMsg("SEAL CONFIRMED — welcome to the Advisory, holder " + short(res.address));
        } else {
          AB.clear();
          sealClear();
          toastMsg("SEAL WITHHELD — both holdings are required, not or");
        }
      })
      .catch(function (e) {
        toastMsg((e && e.code === 4001) ? "Summon refused — wallet rejected the rite" : "The gate jammed — try again");
      })
      .then(function () { lockBtn.textContent = "Prove Holding"; });
  });

  // ---------- boot ----------
  // ALWAYS show the lock on entry — no bypass via cached seal
  purge();
  tick();
  setInterval(tick, 30000);

  // Cross-tab wallet disconnect listener
  if (window.ethereum) {
    window.ethereum.on("accountsChanged", function (accs) {
      if (!accs || accs.length === 0) {
        sealClear();
        stopSessionTimer();
        showLock(true);
        activeId = null;
        log.innerHTML = "";
        renderThreads();
        renderThread();
      } else {
        // wallet reconnected — check if we have a valid seal (already paid)
        var saved = sealLoad();
        if (saved) {
          // valid seal exists — return session without re-verification
          AB.set(saved.addr);
          startSessionTimer();
          showLock(false);
          if (store.threads.length > 0) {
            activeId = store.threads[store.threads.length - 1].id;
          } else {
            activeId = null;
          }
          renderThread();
          tick();
          renderThreads();
          toastMsg("SEAL RE-CONFIRMED — welcome back, holder " + short(saved.addr));
        } else {
          // no valid seal — require re-verification
          showLock(true);
          toastMsg("Session expired — reconnect and prove holding again.");
        }
      }
    });
  }

  // Boot: always lock first, then check if we can restore a valid session
  showLock(true);
  activeId = null;
  log.innerHTML = "";
  var saved = sealLoad();
  if (saved) {
    // valid unexpired seal — return session automatically
    AB.set(saved.addr);
    startSessionTimer();
    showLock(false);
    if (store.threads.length > 0) {
      activeId = store.threads[store.threads.length - 1].id;
    }
    firstSummon = false;
    renderThread();
    renderThreads();
    toastMsg("SEAL RESTORED — welcome back, holder " + short(saved.addr));
  } else {
    firstSummon = false;
    renderThread();
    renderThreads();
  }
  function randomOf(a) { return a[Math.floor(Math.random() * a.length)]; }
})();