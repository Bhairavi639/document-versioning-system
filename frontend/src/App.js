import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);

  const handleCompare = async () => {
    if (!file1 || !file2) {
      alert("Please upload both files");
      return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    try {
      const res = await axios.post("http://127.0.0.1:8000/compare", formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error comparing documents");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📄 Document Comparison Tool</h1>

      <div style={styles.card}>
        <input type="file" onChange={(e) => setFile1(e.target.files[0])} />
        <br /><br />
        <input type="file" onChange={(e) => setFile2(e.target.files[0])} />

        <br /><br />

        <button style={styles.button} onClick={handleCompare}>
          Compare Documents
        </button>
      </div>

      {result && (
        <div style={styles.resultCard}>
          <h2>Comparison Result</h2>
          

          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Type</th>
                <th style={styles.th}>Old</th>
                <th style={styles.th}>New</th>
              </tr>
            </thead>
            <tbody>
              {result.diff.map((item, index) => (
                <tr key={index}>
                  <td style={styles.td}>{item.type}</td>
                  <td style={styles.td}>{item.old}</td>
                  <td style={styles.td}>{item.new}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <br />

          <a
            href={`http://127.0.0.1:8000/download-report?path=${result.report_path}`}
            target="_blank"
            rel="noreferrer"
            style={styles.download}
          >
            ⬇ Download Report
          </a>
        </div>
      )}
    </div>
  );
}

/* ✅ STYLES (THIS FIXES YOUR ERROR) */
const styles = {
  container: {
    textAlign: "center",
    padding: "40px",
    backgroundColor: "#f5f7fa",
    minHeight: "100vh",
  },

  title: {
    marginBottom: "30px",
  },

  card: {
    background: "#fff",
    padding: "20px",
    borderRadius: "10px",
    display: "inline-block",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
  },

  button: {
    backgroundColor: "#007bff",
    color: "white",
    padding: "10px 20px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },

  resultCard: {
    marginTop: "30px",
    background: "#fff",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
  },

  summaryBox: {
  backgroundColor: "#eef6ff",
  padding: "20px",
  marginBottom: "20px",
  borderRadius: "8px",
  border: "1px solid #bcdcff",
  textAlign: "left",
},

  table: {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: "10px",
  },

  th: {
    border: "1px solid #ddd",
    padding: "10px",
    backgroundColor: "#007bff",
    color: "white",
  },

  td: {
    border: "1px solid #ddd",
    padding: "10px",
  },

  download: {
    display: "inline-block",
    marginTop: "15px",
    color: "#28a745",
    fontWeight: "bold",
    textDecoration: "none",
  },
};

export default App;