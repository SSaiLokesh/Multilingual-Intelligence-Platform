const validateText = (value) => {
    if (
        value === null ||
        value === undefined
    ) {
        return {
            valid: false,
            message: "Please enter some text.",
        };
    }

    if (typeof value !== "string") {
        return {
            valid: false,
            message: "Text input must be a valid string.",
        };
    }

    if (!value.trim()) {
        return {
            valid: false,
            message: "Text cannot be empty or contain only spaces.",
        };
    }

    return {
        valid: true,
        message: null,
    };
};

export {
    validateText,
};
