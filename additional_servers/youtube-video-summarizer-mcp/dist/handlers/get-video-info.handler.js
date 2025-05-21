import { youtubeClient } from "../clients/youtube-client.js";
import { formatError } from "../helpers/format-error.js";
/**
 * Get information about a YouTube video
 */
export async function getYouTubeVideoInfo(videoUrl, language) {
    try {
        const videoInfo = await youtubeClient.getVideoInfo(videoUrl, language);
        return {
            result: videoInfo,
            isError: false,
            error: null,
        };
    }
    catch (error) {
        return {
            result: null,
            isError: true,
            error: formatError(error),
        };
    }
}
//# sourceMappingURL=get-video-info.handler.js.map