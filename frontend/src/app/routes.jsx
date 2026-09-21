import { createBrowserRouter } from "react-router-dom";

import Layout from "../components/Layout";

import Dashboard from "../pages/Dashboard";
import Analyze from "../pages/Analyze";
import Memory from "../pages/Memory";
import Versions from "../pages/Versions";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Layout />,
        children: [
            {
                index: true,
                element: <Dashboard />,
            },
            {
                path: "analyze",
                element: <Analyze />,
            },
            {
                path: "memory",
                element: <Memory />,
            },
            {
                path: "versions",
                element: <Versions />,
            },
        ],
    },
]);

export default router;