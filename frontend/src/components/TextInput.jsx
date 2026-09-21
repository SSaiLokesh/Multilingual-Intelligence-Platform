function TextInput({
    value,
    onChange,
    onSubmit,
    loading,
}) {
    const handleKeyDown = (event) => {
        if (
            event.key === "Enter" &&
            event.ctrlKey &&
            !loading
        ) {
            event.preventDefault();
            onSubmit();
        }
    };

    return (
        <div className="text-input-wrapper">
            <label
                htmlFor="analysis-text"
                className="input-label"
            >
                Enter text
            </label>

            <textarea
                id="analysis-text"
                name="analysis-text"
                className="text-input"
                value={value}
                onChange={(event) =>
                    onChange(event.target.value)
                }
                onKeyDown={handleKeyDown}
                placeholder={
                    "Example: The camera quality is excellent but battery life is poor."
                }
                disabled={loading}
                rows={8}
                aria-describedby="analysis-input-help"
            />

            <div
                id="analysis-input-help"
                className="input-help"
            >
                <span>
                    Enter English or another supported language.
                </span>

                <span>
                    Ctrl + Enter to analyze
                </span>
            </div>
        </div>
    );
}

export default TextInput;
