import { VideoInfo } from "../clients/youtube-client.js";
import { ToolResponse } from "../types/tool-response.js";
/**
 * Get information about a YouTube video
 */
export declare function getYouTubeVideoInfo(videoUrl: string, language?: string): Promise<ToolResponse<VideoInfo>>;
