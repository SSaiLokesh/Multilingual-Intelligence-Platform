function StatusMessage({ type = "info", message }) {
    const icons = {
        loading: "…",
        success: "✓",
        error: "!",
        warning: "!",
        empty: "○",
        info: "i",
    };

    return (
        <div
            className={`status-message status-${type}`}
            role={
                type === "error"
                    ? "alert"
                    : "status"
            }
        >
            <div className="status-icon">
                {icons[type] || icons.info}
            </div>

            <div className="status-content">
                <strong>
                    {type === "loading"
                        ? "Processing"
                        : type === "error"
                        ? "Error"
                        : type === "warning"
                        ? "Notice"
                        : type === "success"
                        ? "Success"
                        : type === "empty"
                        ? "No Data"
                        : "Information"}
                </strong>

                <p>{message}</p>
            </div>
        </div>
    );
}

export default StatusMessage;
