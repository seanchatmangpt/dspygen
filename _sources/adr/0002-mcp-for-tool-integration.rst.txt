ADR-0002: Use MCP for Claude Desktop Integration
================================================

:Status: Accepted
:Date: 2024-09-14
:Deciders: Sean Chatman

Context
-------

dspygen modules and tools need to be accessible from AI assistants (Claude, etc.) without custom plugins per host application.

Decision
--------

Implement the **Model Context Protocol (MCP)** server as the primary integration surface for AI assistants.

Rationale
---------

- MCP is Anthropic's open protocol — supported by Claude Desktop natively
- Single server exposes all dspygen capabilities as tools, resources, and prompts
- stdio transport works without network configuration
- Growing ecosystem of MCP clients beyond Claude

Consequences
------------

- ``dspygen-mcp`` script entry point runs the stdio server
- All new dspygen capabilities should be exposed as MCP tools
- SSE transport available for web-based integrations
- Breaking MCP protocol changes require versioning the server
