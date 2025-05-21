import { VideoDetails } from "youtube-caption-extractor";
export type VideoInfo = VideoDetails;
export declare class YouTubeClient {
    private apiKey;
    constructor();
    /**
     * Extract video ID from YouTube URL
     */
    extractVideoId(url: string): string;
    /**
     * Get video information and captions using youtube-caption-extractor
     */
    getVideoInfo(videoIdOrUrl: string, lang?: string): Promise<VideoDetails>;
}
export declare const youtubeClient: YouTubeClient;
