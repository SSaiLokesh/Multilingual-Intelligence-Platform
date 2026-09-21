import { Link } from "react-router-dom";

function Dashboard() {
    return (
        <div className="page-container">
            {/* Page Header */}
            <section className="dashboard-hero">
                <div className="hero-content">
                    <span className="eyebrow">
                        Multilingual NLP Intelligence
                    </span>

                    <h2>
                        Continuous Multilingual
                        <span className="text-accent">
                            {" "}Aspect Sentiment
                        </span>
                        {" "}and Stance Intelligence
                    </h2>

                    <p className="hero-description">
                        Analyze multilingual text using Aspect-Based
                        Sentiment Analysis and Stance Detection through a
                        unified intelligence platform.
                    </p>

                    <div className="hero-actions">
                        <Link to="/analyze" className="button button-primary">
                            Start Analysis
                        </Link>

                        <Link to="/memory" className="button button-secondary">
                            View Memory
                        </Link>
                    </div>
                </div>
            </section>

            {/* Platform Overview */}
            <section className="section">
                <div className="section-header">
                    <div>
                        <span className="section-label">
                            Platform Overview
                        </span>

                        <h3>What the platform analyzes</h3>
                    </div>

                    <p>
                        The MVP provides a unified interface for multilingual
                        opinion analysis.
                    </p>
                </div>

                <div className="overview-grid">
                    <article className="overview-card">
                        <div className="overview-icon">01</div>

                        <h4>Language Detection</h4>

                        <p>
                            Identifies the language of the submitted text and
                            provides a language confidence score.
                        </p>
                    </article>

                    <article className="overview-card">
                        <div className="overview-icon">02</div>

                        <h4>Aspect Analysis</h4>

                        <p>
                            Identifies aspects and their corresponding
                            categories from the submitted text.
                        </p>
                    </article>

                    <article className="overview-card">
                        <div className="overview-icon">03</div>

                        <h4>Sentiment Analysis</h4>

                        <p>
                            Determines whether sentiment toward an aspect is
                            positive, negative, or neutral.
                        </p>
                    </article>

                    <article className="overview-card">
                        <div className="overview-icon">04</div>

                        <h4>Stance Detection</h4>

                        <p>
                            Determines whether the text supports, opposes, or
                            remains neutral toward a target.
                        </p>
                    </article>
                </div>
            </section>

            {/* Research Tasks */}
            <section className="section">
                <div className="section-header">
                    <div>
                        <span className="section-label">
                            Unified Analysis
                        </span>

                        <h3>Two complementary perspectives</h3>
                    </div>
                </div>

                <div className="research-grid">
                    <article className="research-card">
                        <div className="research-card-header">
                            <span className="research-number">ABSA</span>

                            <span className="status-badge status-success">
                                Sentiment
                            </span>
                        </div>

                        <h4>Aspect-Based Sentiment Analysis</h4>

                        <p>
                            Measures sentiment toward a specific aspect of
                            the text.
                        </p>

                        <div className="research-example">
                            <span>Aspect</span>
                            <strong>Camera Quality</strong>

                            <span>Sentiment</span>
                            <strong className="positive-text">
                                Positive
                            </strong>
                        </div>
                    </article>

                    <article className="research-card">
                        <div className="research-card-header">
                            <span className="research-number">STANCE</span>

                            <span className="status-badge status-info">
                                Position
                            </span>
                        </div>

                        <h4>Stance Detection</h4>

                        <p>
                            Determines the position expressed toward a
                            particular target.
                        </p>

                        <div className="research-example">
                            <span>Target</span>
                            <strong>Camera Quality</strong>

                            <span>Stance</span>
                            <strong className="positive-text">
                                Support
                            </strong>
                        </div>
                    </article>
                </div>
            </section>

            {/* System Architecture */}
            <section className="section">
                <div className="section-header">
                    <div>
                        <span className="section-label">
                            Architecture
                        </span>

                        <h3>Frontend to BFF communication</h3>
                    </div>
                </div>

                <div className="architecture-flow">
                    <div className="architecture-node">
                        <span>01</span>
                        <strong>React Frontend</strong>
                        <small>User Interface</small>
                    </div>

                    <div className="architecture-arrow">→</div>

                    <div className="architecture-node architecture-node-active">
                        <span>02</span>
                        <strong>Flask BFF</strong>
                        <small>/api/v1</small>
                    </div>

                    <div className="architecture-arrow">→</div>

                    <div className="architecture-node">
                        <span>03</span>
                        <strong>Backend Services</strong>
                        <small>ML Processing</small>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Dashboard;