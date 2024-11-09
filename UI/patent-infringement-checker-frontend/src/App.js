import React, { useState } from "react";
import axios from "axios";

function App() {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/analyze", {
        patent_id: patentId,
        company_name: companyName,
      });
      setResults(response.data);
    } catch (error) {
      if (error.response) {
        setError(`Error: ${error.response.data.error || error.message}`);
      } else if (error.request) {
        setError("Error: No response received from the server.");
      } else {
        setError(`Error: ${error.message}`);
      }
      console.error("Detailed error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="App"
      style={{
        padding: "40px",
        maxWidth: "800px",
        margin: "auto",
        fontFamily: "Arial, sans-serif",
        color: "#333",
      }}
    >
      <h1 style={{ textAlign: "center", color: "#4A90E2" }}>Patent Infringement Checker</h1>
      <p style={{ textAlign: "center", color: "#666" }}>
        Enter patent information below to check for potential infringements.
      </p>
      <form
        onSubmit={handleSubmit}
        style={{
          backgroundColor: "#f9f9f9",
          padding: "30px",
          borderRadius: "8px",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
          marginTop: "20px",
        }}
      >
        <div style={{ marginBottom: "20px" }}>
          <label style={{ display: "block", fontWeight: "bold" }}>Patent ID:</label>
          <input
            type="text"
            value={patentId}
            onChange={(e) => setPatentId(e.target.value)}
            required
            style={{
              padding: "10px",
              width: "100%",
              borderRadius: "4px",
              border: "1px solid #ddd",
              marginTop: "5px",
            }}
          />
        </div>
        <div style={{ marginBottom: "20px" }}>
          <label style={{ display: "block", fontWeight: "bold" }}>Company Name:</label>
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            required
            style={{
              padding: "10px",
              width: "100%",
              borderRadius: "4px",
              border: "1px solid #ddd",
              marginTop: "5px",
            }}
          />
        </div>
        <button
          type="submit"
          style={{
            width: "100%",
            padding: "12px",
            backgroundColor: "#4A90E2",
            color: "white",
            fontWeight: "bold",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
          disabled={loading}
        >
          {loading ? "Checking..." : "Analyze Infringement"}
        </button>
      </form>

      {error && (
        <p style={{ color: "red", marginTop: "20px", textAlign: "center" }}>{error}</p>
      )}

      {results && (
        <div
          style={{
            marginTop: "30px",
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
          }}
        >
          <h2 style={{ color: "#4A90E2" }}>Results</h2>
          <p><strong>Patent ID:</strong> {results.patent_id}</p>
          <p><strong>Company Name:</strong> {results.company_name}</p>
          <p><strong>Overall Risk Assessment:</strong> {results.overall_risk_assessment}</p>
          <h3>Top Infringing Products</h3>
          {results.top_infringing_products.length > 0 ? (
            <ul style={{ paddingLeft: "20px" }}>
              {results.top_infringing_products.map((product, index) => (
                <li key={index} style={{ marginBottom: "15px" }}>
                  <p><strong>Product Name:</strong> {product.product_name}</p>
                  <p><strong>Infringement Likelihood:</strong> {product.infringement_likelihood}</p>
                  <p><strong>Relevant Claims:</strong> {product.relevant_claims.join(", ")}</p>
                  <p><strong>Explanation:</strong> {product.explanation}</p>
                  <p><strong>Specific Features:</strong> {product.specific_features.join(", ")}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ color: "#666" }}>No infringing products found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
