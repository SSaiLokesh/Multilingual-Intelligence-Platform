import {
    formatCategory,
    formatConfidence,
    formatLabel,
} from "../utils/formatters";

function ResultCard({ prediction }) {
    if (!prediction) {
        return null;
    }

    const sentiment = prediction.sentiment || {};
    const stance = prediction.stance || {};

    return (
        <article className="result-card">
            {/* Aspect Header */}
            <div className="result-card-header">
                <div>
                    <span className="result-label">
                        Aspect
                    </span>

                    <h4>
                        {prediction.aspect || "Unknown aspect"}
                    </h4>
                </div>

                {prediction.category && (
                    <span className="category-badge">
                        {formatCategory(
                            prediction.category
                        )}
                    </span>
                )}
            </div>

            {/* Sentiment */}
            <div className="prediction-section">
                <div className="prediction-section-header">
                    <span className="prediction-title">
                        SENTIMENT
                    </span>

                    <span className="prediction-context">
                        Aspect
                    </span>
                </div>

                <div className="prediction-value-row">
                    <strong
                        className={`prediction-value sentiment-${String(
                            sentiment.label || ""
                        ).toLowerCase()}`}
                    >
                        {formatLabel(sentiment.label)}
                    </strong>

                    <span className="confidence-badge">
                        {formatConfidence(
                            sentiment.confidence
                        )}
                    </span>
                </div>

                <div className="confidence-bar">
                    <div
                        className="confidence-fill sentiment-fill"
                        style={{
                            width: `${Math.max(
                                0,
                                Math.min(
                                    100,
                                    Number(
                                        sentiment.confidence ||
                                            0
                                    ) * 100
                                )
                            )}%`,
                        }}
                    />
                </div>
            </div>

            {/* Stance */}
            <div className="prediction-section">
                <div className="prediction-section-header">
                    <span className="prediction-title">
                        STANCE
                    </span>

                    <span className="prediction-context">
                        Target
                    </span>
                </div>

                <div className="stance-target">
                    {stance.target ||
                        prediction.target ||
                        prediction.aspect ||
                        "Unknown target"}
                </div>

                <div className="prediction-value-row">
                    <strong
                        className={`prediction-value stance-${String(
                            stance.label || ""
                        ).toLowerCase()}`}
                    >
                        {formatLabel(stance.label)}
                    </strong>

                    <span className="confidence-badge">
                        {formatConfidence(
                            stance.confidence
                        )}
                    </span>
                </div>

                <div className="confidence-bar">
                    <div
                        className="confidence-fill stance-fill"
                        style={{
                            width: `${Math.max(
                                0,
                                Math.min(
                                    100,
                                    Number(
                                        stance.confidence ||
                                            0
                                    ) * 100
                                )
                            )}%`,
                        }}
                    />
                </div>
            </div>
        </article>
    );
}

export default ResultCard;
