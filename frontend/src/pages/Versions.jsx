import { useEffect, useState } from "react";

import StatusMessage from "../components/StatusMessage";
import versionService from "../services/versionService";

function Versions() {
    const [currentVersion, setCurrentVersion] = useState(null);
    const [history, setHistory] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let mounted = true;

        const loadVersions = async () => {
            try {
                setLoading(true);
                setError(null);

                const [current, versionHistory] =
                    await Promise.all([
                        versionService.getCurrentVersion(),
                        versionService.getVersionHistory(),
                    ]);

                if (mounted) {
                    setCurrentVersion(current);
                    setHistory(versionHistory.history || []);
                }
            } catch (err) {
                if (mounted) {
                    setError(
                        err.userMessage ||
                            "Version information is not currently available."
                    );
                }
            } finally {
                if (mounted) {
                    setLoading(false);
                }
            }
        };

        loadVersions();

        return () => {
            mounted = false;
        };
    }, []);

    return (
        <div className="page-container">
            <section className="page-header">
                <div>
                    <span className="section-label">
                        Adaptation State
                    </span>

                    <h2>Versions</h2>

                    <p>
                        View the adaptation-service state and version history
                        exposed by the BFF.
                    </p>
                </div>
            </section>

            {loading && (
                <StatusMessage
                    type="loading"
                    message="Loading version information..."
                />
            )}

            {!loading && error && (
                <StatusMessage
                    type="warning"
                    message={error}
                />
            )}

            {!loading && !error && (
                <>
                    <section className="section">
                        <div className="section-header">
                            <div>
                                <span className="section-label">
                                    Current State
                                </span>

                                <h3>Current Version</h3>
                            </div>
                        </div>

                        <div className="current-version-card">
                            <span className="version-label">
                                Current Adaptation State
                            </span>

                            <strong>
                                {currentVersion?.version ||
                                    currentVersion?.current_version ||
                                    "Unknown"}
                            </strong>

                            <p>
                                This represents the version information
                                provided by the adaptation backend.
                            </p>
                        </div>
                    </section>

                    <section className="section">
                        <div className="section-header">
                            <div>
                                <span className="section-label">
                                    History
                                </span>

                                <h3>Version History</h3>
                            </div>
                        </div>

                        {history.length === 0 ? (
                            <StatusMessage
                                type="empty"
                                message="No version history is currently available."
                            />
                        ) : (
                            <div className="version-list">
                                {history.map((item, index) => (
                                    <article
                                        className="version-card"
                                        key={
                                            item.version ||
                                            item.id ||
                                            index
                                        }
                                    >
                                        <div className="version-card-main">
                                            <span className="version-number">
                                                {item.version ||
                                                    "Unknown"}
                                            </span>

                                            <h4>
                                                {item.description ||
                                                    "Adaptation state update"}
                                            </h4>

                                            {item.timestamp && (
                                                <span className="version-date">
                                                    {item.timestamp}
                                                </span>
                                            )}
                                        </div>

                                        {item.records !==
                                            undefined && (
                                            <div className="version-records">
                                                <span>
                                                    Records
                                                </span>

                                                <strong>
                                                    {item.records}
                                                </strong>
                                            </div>
                                        )}
                                    </article>
                                ))}
                            </div>
                        )}
                    </section>
                </>
            )}
        </div>
    );
}

export default Versions;