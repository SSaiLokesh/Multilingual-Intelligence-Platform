import api from "./api";

const ENDPOINTS = {
    MEMORY: "/memory",
};

const getMemory = async () => {
    const response = await api.get(
        ENDPOINTS.MEMORY
    );

    return {
        records:
            Array.isArray(response?.records)
                ? response.records
                : Array.isArray(response?.data)
                ? response.data
                : [],
    };
};

const memoryService = {
    getMemory,
};

export default memoryService;
