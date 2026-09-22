import api from "./api";

const ENDPOINTS = {
    ANALYZE_TEXT: "/process",
};

/**
 * Generate a unique request ID for every analysis request.
 *
 * Uses the browser's built-in crypto.randomUUID().
 * Falls back to a timestamp-based ID if randomUUID
 * is not available.
 */
const generateRequestId = () => {
    if (
        typeof crypto !== "undefined" &&
        typeof crypto.randomUUID === "function"
    ) {
        return crypto.randomUUID();
    }

    return `req_${Date.now()}_${Math.random()
        .toString(36)
        .substring(2, 10)}`;
};

const normalizeLanguage = (language) => {
    if (!language) {
        return null;
    }

    return {
        name: language.name || "Unknown",
        code: language.code || null,
        confidence:
            typeof language.confidence === "number"
                ? language.confidence
                : null,
    };
};

const normalizePrediction = (prediction, index) => {
    if (!prediction) {
        return null;
    }

    return {
        id: prediction.id || `prediction-${index}`,

        aspect: prediction.aspect || "Unknown aspect",

        category: prediction.category || null,

        sentiment: {
            label: prediction.sentiment?.label || "neutral",

            confidence:
                typeof prediction.sentiment?.confidence === "number"
                    ? prediction.sentiment.confidence
                    : 0,
        },

        stance: {
            target:
                prediction.stance?.target ||
                prediction.target ||
                prediction.aspect ||
                "Unknown target",

            label: prediction.stance?.label || "neutral",

            confidence:
                typeof prediction.stance?.confidence === "number"
                    ? prediction.stance.confidence
                    : 0,
        },
    };
};

const normalizeResponse = (response) => {
    const predictions = Array.isArray(
        response?.data?.predictions
    )
        ? response.data.predictions
              .map((prediction, index) =>
                  normalizePrediction(prediction, index)
              )
              .filter(Boolean)
        : [];

    return {
        requestId: response?.request_id || null,

        status: response?.status || "unknown",

        text: response?.data?.text || "",

        language: normalizeLanguage(
            response?.data?.language
        ),

        predictions,

        adaptationStatus:
            response?.adaptation?.action || "unknown",

        adaptation:
            response?.adaptation || {},

        processing:
            response?.processing || {},
    };
};

/**
 * Send text to the BFF for complete analysis.
 *
 * Frontend
 *    ↓
 * BFF /process
 *    ↓
 * Service 1
 *    ↓
 * Service 2
 *    ↓
 * Service 3
 *    ↓
 * BFF response
 */
const analyzeText = async (text) => {
    const requestId = generateRequestId();

    const requestBody = {
        request_id: requestId,
        text: text,
    };

    console.log(
        "[Analysis Service] Sending request to BFF:",
        requestBody
    );

    try {
        const response = await api.post(
            ENDPOINTS.ANALYZE_TEXT,
            requestBody
        );

        console.log(
            "[Analysis Service] BFF response:",
            response
        );

        return normalizeResponse(response);
    } catch (error) {
        console.error(
            "[Analysis Service] BFF request failed:",
            error
        );

        throw error;
    }
};

const analysisService = {
    analyzeText,
};

export default analysisService;