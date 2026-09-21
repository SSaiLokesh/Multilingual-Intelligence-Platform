import api from "./api";

const ENDPOINTS = {
    ANALYZE_TEXT: "/process/text",
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

const normalizePrediction = (
    prediction,
    index
) => {
    if (!prediction) {
        return null;
    }

    return {
        id:
            prediction.id ||
            `prediction-${index}`,

        aspect:
            prediction.aspect ||
            "Unknown aspect",

        category:
            prediction.category ||
            null,

        sentiment: {
            label:
                prediction.sentiment?.label ||
                "neutral",

            confidence:
                typeof prediction.sentiment?.confidence ===
                "number"
                    ? prediction.sentiment.confidence
                    : 0,
        },

        stance: {
            target:
                prediction.stance?.target ||
                prediction.target ||
                prediction.aspect ||
                "Unknown target",

            label:
                prediction.stance?.label ||
                "neutral",

            confidence:
                typeof prediction.stance?.confidence ===
                "number"
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
              .map(normalizePrediction)
              .filter(Boolean)
        : [];

    return {
        requestId:
            response?.request_id || null,

        status:
            response?.status || "unknown",

        text:
            response?.data?.text || "",

        language: normalizeLanguage(
            response?.data?.language
        ),

        predictions,

        adaptationStatus:
            response?.processing
                ?.adaptation_status ||
            "unknown",

        processing:
            response?.processing || {},
    };
};

const analyzeText = async (text) => {
    const response = await api.post(
        ENDPOINTS.ANALYZE_TEXT,
        {
            text,
        }
    );

    return normalizeResponse(response);
};

const analysisService = {
    analyzeText,
};

export default analysisService;
