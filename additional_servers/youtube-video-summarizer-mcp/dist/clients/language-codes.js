export const languageCodes = [
    "en", "es", "fr", "de", "zh", "zh-TW", "ja", "ko", "ru", "ar",
    "pt", "it", "nl", "hi", "bn", "tr", "vi", "he", "th", "el",
    "pl", "sv", "cs", "hu", "fi"
];
export const isLanguageCodeValid = (code) => {
    if (!code) {
        return false;
    }
    return languageCodes.includes(code);
};
//# sourceMappingURL=language-codes.js.map