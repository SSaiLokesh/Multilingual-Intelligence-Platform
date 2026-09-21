import api from "./api";

const ENDPOINTS = {
    CURRENT_VERSION: "/version",
    VERSION_HISTORY: "/version/history",
};

const getCurrentVersion = async () => {
    return api.get(
        ENDPOINTS.CURRENT_VERSION
    );
};

const getVersionHistory = async () => {
    const response = await api.get(
        ENDPOINTS.VERSION_HISTORY
    );

    return {
        history:
            Array.isArray(response?.history)
                ? response.history
                : Array.isArray(response?.data)
                ? response.data
                : [],
    };
};

const versionService = {
    getCurrentVersion,
    getVersionHistory,
};

export default versionService;