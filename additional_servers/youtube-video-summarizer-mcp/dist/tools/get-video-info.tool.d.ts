import { z } from "zod";
import { ToolDefinition } from "../types/tool-definition.js";
declare const toolSchema: {
    videoUrl: z.ZodString;
    languageCode: z.ZodOptional<z.ZodString>;
};
export declare const GetVideoInfoTool: ToolDefinition<typeof toolSchema>;
export {};
