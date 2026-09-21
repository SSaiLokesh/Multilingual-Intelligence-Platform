const formatConfidence = (value) => {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "—";
    }

    const numericValue = Number(value);

    if (Number.isNaN(numericValue)) {
        return "—";
    }

    const normalized =
        numericValue > 1
            ? numericValue
            : numericValue * 100;

    const rounded =
        Math.round(normalized * 10) / 10;

    return `${rounded}%`;
};

const formatLabel = (value) => {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "Unknown";
    }

    const normalized = String(value)
        .trim()
        .toLowerCase();

    if (!normalized) {
        return "Unknown";
    }

    return normalized
        .split(/[\s_-]+/)
        .map(
            (word) =>
                word.charAt(0).toUpperCase() +
                word.slice(1)
        )
        .join(" ");
};

const formatLanguage = (language) => {
    if (!language) {
        return "Unknown";
    }

    if (typeof language === "string") {
        return formatLabel(language);
    }

    if (language.name) {
        return language.name;
    }

    if (language.code) {
        return language.code.toUpperCase();
    }

    return "Unknown";
};

const formatCategory = (category) => {
    return formatLabel(category);
};

const formatStatus = (status) => {
    if (
        status === null ||
        status === undefined ||
        status === ""
    ) {
        return "Unknown";
    }

    return formatLabel(status);
};

export {
    formatConfidence,
    formatLabel,
    formatLanguage,
    formatCategory,
    formatStatus,
};