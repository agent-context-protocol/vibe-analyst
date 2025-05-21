import { ZodRawShape } from "zod";
import { ToolDefinition } from "../types/tool-definition.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
export declare const RegisterTool: <Args extends ZodRawShape>(server: McpServer, toolDefinition: ToolDefinition<Args>) => void;
