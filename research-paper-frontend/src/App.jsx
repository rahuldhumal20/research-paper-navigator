import { useState, useEffect } from "react";
import "./App.css";

function App() {
  // ---------------- STATE ----------------
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("semantic");

  const [uploadProgress, setUploadProgress] = useState(0);
  const [pdfs, setPdfs] = useState([]);

  // ---------------- PDF UPLOAD ----------------
  const uploadPdf = (file) => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/upload");

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        setUploadProgress(Math.round((e.loaded / e.total) * 100));
      }
    };

    xhr.onload = () => {
      setUploadProgress(0);
      fetchPdfs();
    };

    xhr.onerror = () => {
      alert("Upload failed");
      setUploadProgress(0);
    };

    xhr.send(formData);
  };

  // ---------------- SEARCH ----------------
  const search = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResponse(null);
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/ask?query=${encodeURIComponent(query)}`
      );

      if (!res.ok) throw new Error("Backend error");

      const data = await res.json();
      setResponse(data);
    } catch {
      setError("Backend not reachable or internal error");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") search();
  };

  // ---------------- HIGHLIGHT ----------------
  const highlightText = (text, query) => {
    if (!query) return text;

    let highlighted = text;
    query.split(" ").forEach((word) => {
      if (word.length > 2) {
        const regex = new RegExp(`(${word})`, "gi");
        highlighted = highlighted.replace(regex, "<mark>$1</mark>");
      }
    });

    return highlighted;
  };

  // ---------------- GRAPH ----------------
  const buildGraph = () => {
    if (!response || response.type !== "graph") return [];
    return response.papers.map((paper) => ({
      author: response.author,
      paper,
    }));
  };

  // ---------------- PDF LIST ----------------
  const fetchPdfs = async () => {
    const res = await fetch("http://127.0.0.1:8000/pdfs");
    setPdfs(await res.json());
  };

  useEffect(() => {
    fetchPdfs();
  }, []);

  const deletePdf = async (filename) => {
    await fetch(`http://127.0.0.1:8000/delete/${filename}`, {
      method: "DELETE",
    });
    fetchPdfs();
  };

  // ---------------- UI ----------------
  return (
    <div className="container">
      <h2 className="title">🔍 Research Paper Navigator</h2>

      {/* PDF Upload */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="file"
          accept="application/pdf"
          disabled={uploadProgress > 0}
          onChange={(e) => {
            if (e.target.files.length > 0) {
              uploadPdf(e.target.files[0]);
            }
          }}
        />

        {uploadProgress > 0 && (
          <div style={{ marginTop: "10px" }}>
            <progress value={uploadProgress} max="100" />
            <span> {uploadProgress}%</span>
          </div>
        )}
      </div>

      {/* Uploaded PDFs */}
      <h3>📄 Uploaded Papers</h3>
      {pdfs.map((p, i) => (
        <div className="card" key={i}>
          {p.filename} ({p.chunks} chunks)
          <button
              style={{
                float: "right",
                background: "red",
                color: "white",
                border: "none",
                padding: "4px 8px",
                borderRadius: "4px",
              }}
              onClick={() => deletePdf(p.filename)}
            >
              Delete
            </button>

        </div>
      ))}

      {/* Search */}
      <div className="search-box">
        <input
          type="text"
          placeholder="Ask a research question..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button onClick={search}>Search</button>
      </div>

      {loading && <div className="loader">Searching...</div>}
      {error && <div className="error">{error}</div>}

      {/* Results */}
      {response && (
        <>
          {/* Tabs */}
          <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
            <button onClick={() => setActiveTab("semantic")}>Semantic</button>
            <button onClick={() => setActiveTab("graph")}>Graph</button>
            <button onClick={() => setActiveTab("answer")}>Answer</button>
          </div>

          <div className="result-type">
            Result Type: {response.type.toUpperCase()}
          </div>

          {/* SEMANTIC TAB (VECTOR ONLY) */}
          {activeTab === "semantic" &&
            response.type === "vector" &&
            response.results &&
            response.results.documents &&
            response.results.documents[0] &&
            response.results.documents[0].map((doc, i) => (
              <div
                key={i}
                className="card"
                dangerouslySetInnerHTML={{
                  __html: highlightText(doc, query),
                }}
              />
            ))}

          {/* GRAPH TAB */}
          {activeTab === "graph" && response.type === "graph" && (
            <div>
              <h4>Author</h4>
              <div className="card">👤 {response.author}</div>

              <h4>Papers</h4>
              {buildGraph().map((node, i) => (
                <div className="card" key={i}>
                  {node.author} ➝ 📄 {node.paper}
                </div>
              ))}
            </div>
          )}

          {/* ANSWER TAB */}
          {activeTab === "answer" && response && (
          <div>
            <h3>🧠 Answer</h3>

            <div className="card">
              {response.type === "graph" &&
                `The following papers were found for author ${response.author}.`}

              {response.type === "vector" &&
                "This answer is generated based on the most relevant sections from the uploaded papers."}
            </div>

            {response.type === "vector" &&
              response.results?.documents?.[0]?.slice(0, 3).map((doc, i) => (
                <div className="card" key={i}>
                  {doc.substring(0, 200)}...
                </div>
              ))}
          </div>
        )}

        </>
      )}
    </div>
  );
}

export default App;
