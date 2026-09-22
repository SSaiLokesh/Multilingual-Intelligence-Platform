const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "https://multilingual-intelligence-platform-bff.onrender.com";

const DEFAULT_TIMEOUT = 15000;

class ApiError extends Error {
    constructor(message, options = {}) {
        super(message);

        this.name = "ApiError";

        this.status = options.status || null;
        this.code = options.code || null;
        this.requestId = options.requestId || null;
        this.data = options.data || null;

        this.userMessage =
            options.userMessage ||
            message ||
            "An unexpected error occurred.";
    }
}

const createTimeoutSignal = (timeout) => {
    const controller = new AbortController();

    const timeoutId = setTimeout(() => {
        controller.abort();
    }, timeout);

    return {
        signal: controller.signal,
        clear: () => clearTimeout(timeoutId),
    };
};

const parseResponse = async (response) => {
    const contentType =
        response.headers.get("content-type") || "";

    if (contentType.includes("application/json")) {
        return response.json();
    }

    const text = await response.text();

    return text || null;
};

const getErrorMessage = (data, status) => {
    if (
        data &&
        typeof data === "object" &&
        data.error &&
        data.error.message
    ) {
        return data.error.message;
    }

    if (
        data &&
        typeof data === "object" &&
        data.message
    ) {
        return data.message;
    }

    const messages = {
        400: "The request contains invalid input.",
        401: "Authentication is required.",
        403: "You are not authorized to perform this operation.",
        404: "The requested API endpoint was not found.",
        408: "The request timed out.",
        429: "Too many requests were sent. Please try again later.",
        500: "The backend encountered an internal error.",
        502: "The analysis service is currently unavailable.",
        503: "The backend service is temporarily unavailable.",
        504: "The backend service timed out.",
    };

    return (
        messages[status] ||
        "The request could not be completed."
    );
};

const mapErrorCodeToMessage = (code) => {
    const errorMessages = {
        INVALID_INPUT:
            "Please provide valid input.",

        INVALID_DATASET:
            "The dataset format is invalid.",

        UNSUPPORTED_LANGUAGE:
            "The detected language is currently unsupported.",

        PROCESSING_ERROR:
            "The text could not be processed.",

        MODEL_ERROR:
            "The analysis model could not process the request.",

        SERVICE_UNAVAILABLE:
            "The analysis service is temporarily unavailable.",

        STORAGE_ERROR:
            "The result could not be stored.",

        INTERNAL_ERROR:
            "An unexpected server error occurred.",
    };

    return errorMessages[code];
};

const request = async (
    endpoint,
    options = {}
) => {
    const {
        method = "GET",
        body,
        headers = {},
        timeout = DEFAULT_TIMEOUT,
    } = options;

    const url = `${API_BASE_URL}${endpoint}`;

    const timeoutController =
        createTimeoutSignal(timeout);

    const requestHeaders = {
        Accept: "application/json",
        ...headers,
    };

    if (body !== undefined) {
        requestHeaders["Content-Type"] =
            "application/json";
    }

    let response;

    try {
        response = await fetch(url, {
            method,
            headers: requestHeaders,
            body:
                body !== undefined
                    ? JSON.stringify(body)
                    : undefined,
            signal: timeoutController.signal,
        });
    } catch (error) {
        timeoutController.clear();

        if (error.name === "AbortError") {
            throw new ApiError(
                "The request timed out.",
                {
                    status: 504,
                    code: "TIMEOUT",
                    userMessage:
                        "The analysis service took too long to respond.",
                }
            );
        }

        throw new ApiError(
            "Unable to connect to the backend.",
            {
                code: "NETWORK_ERROR",
                userMessage:
                    "Unable to connect to the analysis service. Please make sure the Flask BFF is running.",
            }
        );
    }

    timeoutController.clear();

    const data = await parseResponse(response);

    if (!response.ok) {
        const code =
            data?.error?.code ||
            data?.code ||
            null;

        const backendMessage =
            getErrorMessage(
                data,
                response.status
            );

        const mappedMessage =
            mapErrorCodeToMessage(code);

        throw new ApiError(
            backendMessage,
            {
                status: response.status,
                code,
                requestId:
                    data?.request_id || null,
                data,
                userMessage:
                    mappedMessage ||
                    backendMessage,
            }
        );
    }

    return data;
};

const api = {
    get(endpoint, options = {}) {
        return request(endpoint, {
            ...options,
            method: "GET",
        });
    },

    post(endpoint, body, options = {}) {
        return request(endpoint, {
            ...options,
            method: "POST",
            body,
        });
    },

    delete(endpoint, options = {}) {
        return request(endpoint, {
            ...options,
            method: "DELETE",
        });
    },
};

export { ApiError };

export default api;
