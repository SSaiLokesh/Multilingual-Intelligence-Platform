import { NavLink, Outlet } from "react-router-dom";

function Layout() {
    return (
        <div className="app-shell">
            <header className="app-header">
                <div className="app-brand">
                    <h1>Continuous Multilingual Intelligence</h1>
                    <p>Aspect Sentiment &amp; Stance Platform</p>
                </div>
            </header>

            <div className="app-body">
                <aside className="sidebar">
                    <nav className="navigation" aria-label="Main navigation">
                        <NavLink
                            to="/"
                            end
                            className={({ isActive }) =>
                                isActive
                                    ? "nav-link active"
                                    : "nav-link"
                            }
                        >
                            Dashboard
                        </NavLink>

                        <NavLink
                            to="/analyze"
                            className={({ isActive }) =>
                                isActive
                                    ? "nav-link active"
                                    : "nav-link"
                            }
                        >
                            Analyze
                        </NavLink>

                        <NavLink
                            to="/memory"
                            className={({ isActive }) =>
                                isActive
                                    ? "nav-link active"
                                    : "nav-link"
                            }
                        >
                            Memory
                        </NavLink>

                        <NavLink
                            to="/versions"
                            className={({ isActive }) =>
                                isActive
                                    ? "nav-link active"
                                    : "nav-link"
                            }
                        >
                            Versions
                        </NavLink>
                    </nav>
                </aside>

                <main className="main-content">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}

export default Layout;