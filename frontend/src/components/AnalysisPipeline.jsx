function AnalysisPipeline({ loading, result }) {
    const stages = [
        {
            id: "input",
            label: "Input received",
            description: "Text accepted for processing",
            completed: Boolean(loading || result),
        },
        {
            id: "language",
            label: "Language & aspects processed",
            description: "Language and aspect information generated",
            completed: Boolean(result),
        },
        {
            id: "sentiment",
            label: "Sentiment & stance processed",
            description: "ABSA and stance predictions generated",
            completed: Boolean(result),
        },
        {
            id: "adaptation",
            label: "Adaptation record stored",
            description: "Adaptation status received from BFF",
            completed: Boolean(result),
        },
        {
            id: "complete",
            label: "Analysis complete",
            description: "Results are ready",
            completed: Boolean(result) && !loading,
        },
    ];

    return (
        <div className="pipeline">
            {stages.map((stage, index) => {
                const isCurrent =
                    loading &&
                    !stage.completed &&
                    (index === 1 || index === 2);

                return (
                    <div
                        className={`pipeline-stage ${
                            stage.completed
                                ? "pipeline-completed"
                                : ""
                        } ${
                            isCurrent
                                ? "pipeline-current"
                                : ""
                        }`}
                        key={stage.id}
                    >
                        <div className="pipeline-indicator">
                            {stage.completed ? "✓" : index + 1}
                        </div>

                        <div className="pipeline-content">
                            <strong>{stage.label}</strong>

                            <span>{stage.description}</span>
                        </div>

                        {index < stages.length - 1 && (
                            <div
                                className={`pipeline-line ${
                                    stage.completed
                                        ? "pipeline-line-completed"
                                        : ""
                                }`}
                            />
                        )}
                    </div>
                );
            })}
        </div>
    );
}

export default AnalysisPipeline;
