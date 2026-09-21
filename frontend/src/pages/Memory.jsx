import { useState } from "react";

import TextInput from "../components/TextInput";
import AnalysisPipeline from "../components/AnalysisPipeline";
import ResultCard from "../components/ResultCard";
import StatusMessage from "../components/StatusMessage";

import analysisService from "../services/analysisService";
import { validateText } from "../utils/validators";
import {
    formatConfidence,
    formatLanguage,
    formatStatus,
} from "../utils/formatters";

function Analyze() {
    const [text, setText] = useState("");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async () => {
        const validation = validateText(text);

        if (!validation.valid) {
            setError({
                type: "error",
                message: validation.message,
            });

            setResult(null);
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const analysisResult =
                await analysisService.analyzeText(text);

            setResult(analysisResult);
        } catch (err) {
            setError({
                type: "error",
                message:
                    err.userMessage ||
                    "Unable to process the text. Please try again.",
            });
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setText("");
        setResult(null);
        setError(null);
    };

    const hasPredictions =
        result &&
        Array.isArray(result.predictions) &&
        result.predictions.length > 0;

    return (
        <div className="page-container">
            {/* Page Header */}
            <section className="page-header">
                <div>
                    <span className="section-label">
                        Analysis Workspace
                    </span>

                    <h2>Analyze Multilingual Text</h2>

                    <p>
                        Enter text to identify language, aspects, sentiment,
                        stance, and adaptation status.
                    </p>
                </div>
            </section>

            {/* Input Section */}
            <section className="analysis-workspace">
                <div className="analysis-input-panel">
                    <div className="panel-header">
                        <div>
                            <span className="panel-label">
                                Input
                            </span>

                            <h3>Text to Analyze</h3>
                        </div>

                        <span className="input-counter">
                            {text.length} characters
                        </span>
                    </div>

                    <TextInput
                        value={text}
                        onChange={setText}
                        onSubmit={handleAnalyze}
                        loading={loading}
                    />

                    <div className="input-actions">
                        <button
                            type="button"
                            className="button button-secondary"
                            onClick={handleClear}
                            disabled={loading || !text}
                        >
                            Clear Text
                        </button>

                        <button
                            type="button"
                            className="button button-primary"
                            onClick={handleAnalyze}
                            disabled={loading}
                        >
                            {loading ? "Analyzing..." : "Analyze Text"}
                        </button>
                    </div>
                </div>
            </section>

            {/* Error */}
            {error && (
                <section className="status-section">
                    <StatusMessage
                        type={error.type}
                        message={error.message}
                    />
                </section>
            )}

            {/* Processing Pipeline */}
            {(loading || result) && (
                <section className="section">
                    <div className="section-header">
                        <div>
                            <span className="section-label">
                                Processing
                            </span>

                            <h3>Analysis Pipeline</h3>
                        </div>
                    </div>

                    <AnalysisPipeline
                        loading={loading}
                        result={result}
                    />
                </section>
            )}

            {/* Result */}
            {result && (
                <>
                    {/* Summary */}
                    <section className="section">
                        <div className="section-header">
                            <div>
                                <span className="section-label">
                                    Analysis Result
                                </span>

                                <h3>Language &amp; Processing</h3>
                            </div>
                        </div>

                        <div className="summary-grid">
                            <div className="summary-card">
                                <span className="summary-label">
                                    Detected Language
                                </span>

                                <strong className="summary-value">
                                    {formatLanguage(result.language)}
                                </strong>

                                {result.language?.confidence !==
                                    undefined && (
                                    <span className="summary-confidence">
                                        Confidence:{" "}
                                        {formatConfidence(
                                            result.language.confidence
                                        )}
                                    </span>
                                )}
                            </div>

                            <div className="summary-card">
                                <span className="summary-label">
                                    Adaptation Status
                                </span>

                                <strong className="summary-value">
                                    {formatStatus(
                                        result.adaptationStatus
                                    )}
                                </strong>
                            </div>

                            <div className="summary-card">
                                <span className="summary-label">
                                    Predictions
                                </span>

                                <strong className="summary-value">
                                    {result.predictions?.length || 0}
                                </strong>

                                <span className="summary-confidence">
                                    Aspect-level predictions
                                </span>
                            </div>
                        </div>
                    </section>

                    {/* Predictions */}
                    <section className="section">
                        <div className="section-header">
                            <div>
                                <span className="section-label">
                                    ABSA + Stance
                                </span>

                                <h3>Prediction Results</h3>
                            </div>

                            {hasPredictions && (
                                <span className="result-count">
                                    {result.predictions.length}{" "}
                                    {result.predictions.length === 1
                                        ? "prediction"
                                        : "predictions"}
                                </span>
                            )}
                        </div>

                        {hasPredictions ? (
                            <div className="results-grid">
                                {result.predictions.map(
                                    (prediction, index) => (
                                        <ResultCard
                                            key={
                                                prediction.id ||
                                                `${prediction.aspect}-${index}`
                                            }
                                            prediction={prediction}
                                        />
                                    )
                                )}
                            </div>
                        ) : (
                            <StatusMessage
                                type="empty"
                                message="No aspect-level predictions were returned for this text."
                            />
                        )}
                    </section>

                    {/* Processing Details */}
                    <section className="section">
                        <div className="section-header">
                            <div>
                                <span className="section-label">
                                    Traceability
                                </span>

                                <h3>Processing Details</h3>
                            </div>
                        </div>

                        <div className="processing-details">
                            <div className="detail-item">
                                <span>Request ID</span>

                                <strong>
                                    {result.requestId || "Not provided"}
                                </strong>
                            </div>

                            <div className="detail-item">
                                <span>Response Status</span>

                                <strong>
                                    {result.status || "Unknown"}
                                </strong>
                            </div>

                            <div className="detail-item">
                                <span>Adaptation</span>

                                <strong>
                                    {formatStatus(
                                        result.adaptationStatus
                                    )}
                                </strong>
                            </div>
                        </div>
                    </section>
                </>
            )}

            {/* Initial State */}
            {!loading && !result && !error && (
                <section className="empty-analysis">
                    <div className="empty-analysis-icon">AI</div>

                    <h3>Ready for analysis</h3>

                    <p>
                        Enter multilingual text above and select{" "}
                        <strong>Analyze Text</strong> to begin.
                    </p>
                </section>
            )}
        </div>
    );
}

export default Analyze;