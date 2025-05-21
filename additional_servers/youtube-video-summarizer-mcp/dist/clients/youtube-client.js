import { getVideoDetails } from "youtube-caption-extractor";
import dotenv from "dotenv";
import { isLanguageCodeValid } from "./language-codes.js";
dotenv.config();
export class YouTubeClient {
    apiKey;
    constructor() {
        this.apiKey = process.env.YOUTUBE_API_KEY;
    }
    /**
     * Extract video ID from YouTube URL
     */
    extractVideoId(url) {
        try {
            // Handle different YouTube URL formats
            const urlObj = new URL(url);
            const hostname = urlObj.hostname;
            const pathname = urlObj.pathname;
            const searchParams = urlObj.searchParams;
            if (hostname.includes("youtube.com") && searchParams.has("v")) {
                return searchParams.get("v");
            }
            else if (hostname.includes("youtu.be")) {
                return pathname.substring(1);
            }
            else if (hostname.includes("youtube.com") && pathname.includes("/embed/")) {
                return pathname.split("/embed/")[1];
            }
            else if (hostname.includes("youtube.com") && pathname.includes("/v/")) {
                return pathname.split("/v/")[1];
            }
            else {
                // In case the input is already a video ID
                if (url.match(/^[a-zA-Z0-9_-]{11}$/)) {
                    return url;
                }
                throw new Error("Invalid YouTube URL format");
            }
        }
        catch (error) {
            // If URL parsing fails, check if the input might be a video ID
            if (url.match(/^[a-zA-Z0-9_-]{11}$/)) {
                return url;
            }
            throw new Error("Could not extract video ID from URL");
        }
    }
    /**
     * Get video information and captions using youtube-caption-extractor
     */
    async getVideoInfo(videoIdOrUrl, lang) {
        try {
            // Extract video ID from URL
            const videoId = this.extractVideoId(videoIdOrUrl);
            // check if lang is valid
            let languageCode = lang;
            if (!isLanguageCodeValid(lang)) {
                languageCode = undefined;
            }
            const videoDetails = await getVideoDetails({ videoID: videoId, lang: languageCode });
            return videoDetails;
        }
        catch (error) {
            console.error("Error getting video info:", error);
            throw new Error(`Failed to get video info: ${error.message}`);
        }
    }
}
export const youtubeClient = new YouTubeClient();
//# sourceMappingURL=youtube-client.js.map