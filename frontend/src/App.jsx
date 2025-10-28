import React, { useEffect, useMemo, useRef, useState } from "react";
import io from "socket.io-client";
import './App.css';

// ---------- styles (minimal & clean) ----------
const styles = {
  page: { fontFamily: "Sarabun, system-ui, sans-serif", padding: 16, color: "#0f172a" },
  header: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 },
  pill: { padding: "4px 10px", borderRadius: 999, background: "#eef2ff", fontSize: 12 },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 16, marginBottom: 24 },
  card: { display: "flex", flexDirection: "column", alignItems: "center", gap: 8, borderRadius: 16, border: "1px solid #e5e7eb", padding: 12, cursor: "pointer", background: "#fff", boxShadow: "0 1px 3px rgba(0,0,0,0.06)", transition: "transform .06s ease" },
  cardImg: { width: 120, height: 120, objectFit: "contain" },
  hline: { height: 1, background: "#e5e7eb", margin: "16px 0" },
  summaryWrap: { display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 12 },
  summaryItem: { background: "#f8fafc", border: "1px solid #e5e7eb", borderRadius: 12, padding: "8px 12px" },
  table: { borderCollapse: "collapse", width: "100%", maxWidth: 960 },
  th: { textAlign: "left", borderBottom: "1px solid #e5e7eb", padding: 8, background: "#f8fafc" },
  td: { padding: 8, borderBottom: "1px solid #f1f5f9" },
  statusPass: { color: "#16a34a", fontWeight: 700 },
  statusFail: { color: "#dc2626", fontWeight: 700 },
  toolbar: { display: "flex", gap: 8, alignItems: "center", marginBottom: 12, flexWrap: "wrap" },
  input: { border: "1px solid #e5e7eb", borderRadius: 10, padding: "8px 10px", minWidth: 220 },
  btn: { padding: "10px 14px", borderRadius: 12, border: "1px solid #e5e7eb", background: "#111827", color: "#fff", cursor: "pointer" },
  btnGhost: { padding: "10px 14px", borderRadius: 12, border: "1px solid #e5e7eb", background: "#fff", color: "#111827", cursor: "pointer" },
  btnDisabled: { opacity: .6, cursor: "not-allowed" },
  logsWrap: { display: "grid", gridTemplateColumns: "1fr", gap: 12 },
  logBox: { background: "#0b1020", color: "#e5e7eb", padding: 12, borderRadius: 12, minHeight: 160, whiteSpace: "pre-wrap", overflow: "auto", maxHeight: 280 },
  shotsWrap: { display: "flex", gap: 20, alignItems: "flex-start", flexWrap: "wrap" },
  col: { flex: 1, minWidth: 320 },
  img: { maxWidth: 400, width: "100%", margin: 10, borderRadius: 12, border: "1px solid #eee" },
  badge: { fontSize: 12, background: "#f1f5f9", border: "1px solid #e2e8f0", borderRadius: 999, padding: "2px 8px" },
};

// ---------- small widgets ----------
const StatusDot = ({ online }) => (
  <span style={{ ...styles.pill, background: online ? "#dcfce7" : "#fee2e2", color: online ? "#166534" : "#7f1d1d" }}>
    {online ? "Socket: connected" : "Socket: disconnected"}
  </span>
);

function SummaryBar({ summary }) {
  return (
    <div>
      <h3>📊 Summary</h3>
      <div style={styles.summaryWrap}>
        <div style={styles.summaryItem}>Total Test: <b>{summary.total}</b></div>
        <div style={styles.summaryItem}>✅ Passed: <b style={styles.statusPass}>{summary.passed}</b></div>
        <div style={styles.summaryItem}>❌ Failed: <b style={styles.statusFail}>{summary.failed}</b></div>
        <div style={styles.summaryItem}>⏱️ Duration: <b>{summary.duration_sec}</b>s</div>
      </div>
    </div>
  );
}

function CaseTable({ rows }) {
  return (
    <div>
      <h4>🧪 Test cases</h4>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>#</th>
            <th style={styles.th}>Name</th>
            <th style={styles.th}>Status</th>
            <th style={styles.th}>Category</th>
            <th style={styles.th}>Duration (s)</th>
            <th style={styles.th}>Message</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>
              <td style={styles.td}>{i + 1}</td>
              <td style={styles.td}>{r.name}</td>
              <td style={{ ...styles.td, ...(r.status === "passed" ? styles.statusPass : styles.statusFail) }}>{r.status}</td>
              <td style={styles.td}>{r.category || ""}</td>
              <td style={styles.td}>{r.duration_sec ?? ""}</td>
              <td style={styles.td}>{r.message || ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Screenshots({ title, items }) {
  return (
    <div style={styles.col}>
      <h4>{title} <span style={styles.badge}>{items.length}</span></h4>
      <div style={{ padding: 10 }}>
        {items.map((s, i) => (
          <div key={i}>
            {s.filename && <p style={{ margin: "6px 0" }}>{s.filename}</p>}
            {s.url ? (
              <a href={s.url} target="_blank" rel="noreferrer">
                <img loading="lazy" src={s.src} alt={s.filename || `screenshot-${i}`} style={styles.img} />
              </a>
            ) : (
              <img loading="lazy" src={s.src} alt={s.filename || `screenshot-${i}`} style={styles.img} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function CardsGrid({ cards, onRun, running }) {
  return (
    <div>
      <div style={styles.header}>
        <h2>เลือกผู้ว่าจ้าง / บริการ</h2>
        <span style={styles.pill}>ทั้งหมด {cards.length} รายการ</span>
      </div>
      <div style={styles.grid}>
        {cards.map((c) => (
          <button
            key={c.code}
            onClick={() => onRun(c.code)}
            style={{ ...styles.card, ...(running ? styles.btnDisabled : {}) }}
            disabled={running}
            title={`Run tests for ${c.title}`}
            onMouseDown={(e) => e.currentTarget.style.transform = "scale(0.98)"}
            onMouseUp={(e) => e.currentTarget.style.transform = "scale(1)"}
            onMouseLeave={(e) => e.currentTarget.style.transform = "scale(1)"}
          >
            <img src={c.image} alt={c.alt || c.title} style={styles.cardImg} />
            <p style={{ margin: 0, fontWeight: 600, textAlign: "center" }}>{c.title}</p>
            <small style={{ opacity: 0.7 }}>Code: {c.code}</small>
          </button>
        ))}
      </div>
    </div>
  );
}

// ---------- main app ----------
export default function App() {
  const [cards, setCards] = useState([]);
  const [summary, setSummary] = useState({ total: 0, passed: 0, failed: 0, duration_sec: 0 });
  const [caseRows, setCaseRows] = useState([]);
  const [out, setOut] = useState("⏳ ยังไม่ได้เริ่มรัน Automate Test\n");
  const [syslog, setSyslog] = useState("┌ Automate Test Console\n");
  const [shotsResult, setShotsResult] = useState([]);
  const [shotsNegative, setShotsNegative] = useState([]);
  const [running, setRunning] = useState(false);
  const [showTop, setShowTop] = useState(false);
  const [socketOnline, setSocketOnline] = useState(false);

  // optional: เลือก TC เฉพาะ (คอมมา) ส่งไป backend ร่วมกับ tenant code
  const [tcs, setTcs] = useState(""); // ex: "TC001,TC003"

  const logBoxRef = useRef(null);
  const socketRef = useRef(null);

  // fetch cards
  useEffect(() => {
    fetch("/api/cards")
      .then((r) => r.json())
      .then((data) => setCards(data))
      .catch(() => setCards([]));
  }, []);

  // connect socket (ใช้ proxy ของ Vite, ไม่ต้องใส่ URL)
  useEffect(() => {
    const s = io({
      autoConnect: true,
      reconnection: true,
      reconnectionDelay: 500,
      reconnectionAttempts: Infinity,
      // transports: ["polling"],
      transports: ["websocket", "polling"],
    });
    socketRef.current = s;

    s.on("connect", () => {
      setSocketOnline(true);
      setSyslog((p) => p + `• socket connected: ${s.id}\n`);
    });

    s.on("disconnect", () => {
      setSocketOnline(false);
      setSyslog((p) => p + `• socket disconnected\n`);
    });

    s.on("test_result", (msg) => {
      setOut((p) => p + msg + "\n");
    });

    s.on("test_case_result", (data) => {
      setCaseRows((rows) => [...rows, data]);
    });

    const MAX_SHOTS = 30;
    s.on("screenshot", (data) => {
      const item = { src: data.base64 ? `data:image/png;base64,${data.base64}` : undefined,
                    url: data.url, filename: data.filename };
      if ((data.category || "").toLowerCase() === "nagative") {
        setShotsNegative((prev) => [item, ...prev].slice(0, MAX_SHOTS));
      } else {
        setShotsResult((prev) => [item, ...prev].slice(0, MAX_SHOTS));
      }
    });

    s.on("test_case_summary", (data) => {
      setSummary(data);
      setRunning(false);
    });

    return () => s.disconnect();
  }, []);

  // auto-scroll log
  useEffect(() => {
    const el = logBoxRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [out, syslog]);

  useEffect(() => {
    const handleScroll = () => {
      setShowTop(window.scrollY > 300);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const startTest = (tenantCode) => {
    if (!socketOnline) {
      setSyslog((p) => p + "• socket not connected\n");
      return;
    }
    setRunning(true);
    // reset UI
    setOut("⏳ กำลังรัน Automate Test...\n");
    setCaseRows([]);
    setSummary({ total: 0, passed: 0, failed: 0, duration_sec: 0 });
    setShotsResult([]);
    setShotsNegative([]);

    // payload: { code, tcs: ['TC001','TC006'] }
    const tcsList = tcs
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean);

    socketRef.current?.emit("start_test", { code: tenantCode, tcs: tcsList });
    requestAnimationFrame(() => logBoxRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
  };

  return (
    <div>
    <div style={styles.page}>
      <div style={styles.header}>
        <h1 style={{ margin: 0 }}>Automate Test – POS NSS (React)</h1>
        <StatusDot online={socketOnline} />
      </div>

      {/* Toolbar: optional filter TC */}
      <div style={styles.toolbar}>
        <label style={{ fontSize: 14 }}>เลือก TC (เช่น TC001,TC003):</label>
        <input
          style={styles.input}
          placeholder="ปล่อยว่าง = รันทั้งหมด"
          value={tcs}
          onChange={(e) => setTcs(e.target.value)}
        />
        <span style={{ ...styles.pill, background: running ? "#fee2e2" : "#dcfce7", color: running ? "#7f1d1d" : "#166534" }}>
          {running ? "Running…" : "Idle"}
        </span>
      </div>

      <CardsGrid cards={cards} onRun={startTest} running={running} />

      <div style={styles.hline} />
      <SummaryBar summary={summary} />
      <CaseTable rows={caseRows} />

      <div style={styles.hline} />
      <h3>⚙️ Log Automate Test</h3>
      <div style={styles.logsWrap}>
        <div ref={logBoxRef} style={styles.logBox}>
          {out}
          {"\n"}
          {syslog}
        </div>
      </div>

      <div style={styles.hline} />
      <h3>📸 Screenshots</h3>
      <div style={styles.shotsWrap}>
        <div style={styles.col}>
          <h4>Result <span style={styles.badge}>{shotsResult.length}</span></h4>
          <div style={{ padding: 10 }}>
            {shotsResult.map((s, i) => (
              <div key={`r-${i}`}>
                {s.filename && <p style={{ margin: "6px 0" }}>{s.filename}</p>}
                {s.url ? (
                  <a href={s.url} target="_blank" rel="noreferrer">
                    <img loading="lazy" src={s.src} alt={s.filename || `result-${i}`} style={styles.img} />
                  </a>
                ) : (
                  <img loading="lazy" src={s.src} alt={s.filename || `result-${i}`} style={styles.img} />
                )}
              </div>
            ))}
          </div>
        </div>

        <div style={styles.col}>
          <h4>Negative <span style={styles.badge}>{shotsNegative.length}</span></h4>
          <div style={{ padding: 10 }}>
            {shotsNegative.map((s, i) => (
              <div key={`n-${i}`}>
                {s.filename && <p style={{ margin: "6px 0" }}>{s.filename}</p>}
                {s.url ? (
                  <a href={s.url} target="_blank" rel="noreferrer">
                    <img loading="lazy" src={s.src} alt={s.filename || `negative-${i}`} style={styles.img} />
                  </a>
                ) : (
                  <img loading="lazy" src={s.src} alt={s.filename || `negative-${i}`} style={styles.img} />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{ height: 24 }} />
    </div>
      {showTop && (
        <button className="btn-to-top" onClick={scrollToTop}>
          ⬆
        </button>
      )}
    </div>
  );
}
