import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
export class YouTubeMcpServer {
    static instance = null;
    constructor() { }
    static GetServer() {
        if (YouTubeMcpServer.instance === null) {
            YouTubeMcpServer.instance = new McpServer({
                name: "YouTube Video Summariser",
                version: "1.0.0",
                capabilities: {
                    tools: {},
                },
            });
        }
        return YouTubeMcpServer.instance;
    }
}
//# sourceMappingURL=youtube-mcp-server.js.map