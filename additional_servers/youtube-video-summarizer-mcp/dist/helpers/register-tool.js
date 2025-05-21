export const RegisterTool = (server, toolDefinition) => {
    server.tool(toolDefinition.name, toolDefinition.description, toolDefinition.schema, toolDefinition.handler);
};
//# sourceMappingURL=register-tool.js.map