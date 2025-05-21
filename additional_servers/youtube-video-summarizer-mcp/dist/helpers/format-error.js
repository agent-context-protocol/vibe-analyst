export function formatError(error) {
    if (error instanceof Error) {
        return error.message;
    }
    else if (typeof error === "string") {
        return error;
    }
    else {
        return "An unknown error occurred";
    }
}
//# sourceMappingURL=format-error.js.map