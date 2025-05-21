import { z } from "zod";
import { getYouTubeVideoInfo } from "../handlers/get-video-info.handler.js";
const toolName = "get-video-info-for-summary-from-url";
const toolDescription = "Get title, description, duration, and captions of a YouTube video from a URL";
const toolSchema = {
    videoUrl: z.string().describe("The URL or ID of the YouTube video"),
    languageCode: z.string().describe("The language code of the video").optional(),
};
const toolHandler = async (args, _extra) => {
    const response = await getYouTubeVideoInfo(args.videoUrl, args.languageCode);
    if (response.isError) {
        return {
            content: [
                {
                    type: "text",
                    text: `Error getting video info: ${response.error}`,
                },
            ],
        };
    }
    const videoInfo = response.result;
    const captions = videoInfo?.subtitles?.map((subtitle) => subtitle.text).join(". ");
    if (!captions) {
        return {
            content: [
                { type: "text", text: "No captions found" },
            ],
        };
    }
    return {
        content: [
            {
                type: "text",
                text: `Title: ${videoInfo?.title}\n\nDescription: ${videoInfo?.description}\n\nCaption: ${captions}`,
            },
        ],
    };
};
export const GetVideoInfoTool = {
    name: toolName,
    description: toolDescription,
    schema: toolSchema,
    handler: toolHandler,
};
//# sourceMappingURL=get-video-info.tool.js.map