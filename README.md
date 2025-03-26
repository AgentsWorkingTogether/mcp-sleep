# Sleep MCP Server

[![smithery badge](https://smithery.ai/badge/@AgentsWorkingTogether/mcp-sleep)](https://smithery.ai/server/@AgentsWorkingTogether/mcp-sleep)

This MCP server attempts to pause execution for a specified duration to control the flow of your agents. Enhance your automation by introducing timed delays, ensuring tasks are executed in the desired sequence. Ideal for managing workflows that require waiting periods between actions.


<a href="https://glama.ai/mcp/servers/@AgentsWorkingTogether/mcp-sleep">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@AgentsWorkingTogether/mcp-sleep/badge" alt="Sleep MCP Server" />
</a>

## Setup

### Installation

#### Using MCP package managers

**Smithery**

To install Sleep MCP for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AgentsWorkingTogether/mcp-sleep):

```bash
npx @smithery/cli install @AgentsWorkingTogether/mcp-sleep --client claude
```

**mcp-get**

You can install the Sleep MCP server using [mcp-get](https://github.com/michaellatman/mcp-get):

```bash
npx @michaellatman/mcp-get@latest install mcp-sleep
```

### Prerequisites

MCP is still very new and evolving, we recommend following the [MCP documentation](https://modelcontextprotocol.io/quickstart#prerequisites) to get the MCP basics up and running.

You'll need:
- [Claude Desktop](https://claude.ai/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Configuration

#### 1. Configure Claude Desktop

Create the following file depending on your OS:

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Paste this template in the file

```json
{
    "mcpServers": {
        "mcp-sleep": {
            "command": "uvx",
            "args": [
                "mcp-sleep"
            ],
        }
    }
}
```
Optionally, it replace `<MCP_SLEEP_TIMEOUT>` with your timeout ( maximum time allowed to wait, default 60 seconds ):

```json
{
    "mcpServers": {
        "mcp-sleep": {
            "command": "uvx",
            "args": [
                "mcp-sleep"
            ],
            "env": {
                "MCP_SLEEP_TIMEOUT": "<MCP_SLEEP_TIMEOUT>"
            }
        }
    }
}
```

#### 2. Restart Claude Desktop


#### SSE mode

Alternatively, you can run the MCP server in SSE mode by running the following command:

```bash
uvx mcp-sleep --transport sse
```

This mode is useful to integrate with an MCP client that supports SSE (like a web app).


## Tools

1. `sleep`
   - Pause execution for a specified duration to control the flow of your agents.
   - Inputs:
     - `seconds` (number, max timeout config value): Seconds it will take me to tell you to continue
   - Returns: You will receive the sentence after {seconds} "You can continue to do your task after you've been waiting {seconds} seconds". If you enter a waiting time greater than the maximum time the result will be "My configuration does not allow me to make you wait more than {ctx.sleep.config.timeout} seconds"


### Usage with Claude Desktop
To use this with Claude Desktop, add the following to your `claude_desktop_config.json`:

#### Docker
```json
{
  "mcpServers": {
    "mcp-sleep": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "MCP_SLEEP_TIMEOUT",
        "mcp/sleep"
      ],
      "env": {
        "MCP_SLEEP_TIMEOUT": "<MCP_SLEEP_TIMEOUT>"
      }
    }
  }
}
```


## Development

### Config
If you are working locally add two environment variables to a `.env` file in the root of the repository:

```sh
MCP_SLEEP_TIMEOUT=
```

For local development, update your Claude Desktop configuration:

```json
{
  "mcpServers": {
      "mcp-sleep_local": {
          "command": "uv",
          "args": [
              "run",
              "--directory",
              "/path/to/your/mcp-sleep",
              "run",
              "mcp-sleep"
          ]
      }
  }
}
```

<details>
  <summary>Published Servers Configuration</summary>

  ```json
  "mcpServers": {
    "mcp-sleep": {
      "command": "uvx",
      "args": [
        "mcp-sleep"
      ]
    }
  }
  ```
</details>

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

Docker build:

```bash
docker build -t mcp/sleep -f Dockerfile .
```


### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/your/mcp-sleep run mcp-sleep
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

