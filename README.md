# 🔍 GoogleSearchMcp

A lightweight, local **MCP (Model Context Protocol) server** that gives any LLM the ability to perform Google searches via [SerpAPI](https://serpapi.com/) and read web page contents via [Jina Reader](https://jina.ai/reader/).

Built with [FastMCP](https://github.com/jlowin/fastmcp) for seamless integration with AI agents, coding assistants, and any MCP-compatible client.

---

## ✨ Features

| Tool | Description |
|---|---|
| `search_web` | Performs Google searches and returns structured results (title, link, snippet). Supports up to 20 results with automatic pagination. |
| `fetch_web_content` | Extracts clean Markdown text from any URL using Jina Reader. Gracefully rejects YouTube links with a helpful error message. |

---

## 🏗️ Architecture

```
┌─────────────────┐      MCP (stdio)      ┌──────────────────┐
│   MCP Client    │◄─────────────────────►│  GoogleSearchMcp │
│ (Claude, Cursor, │                       │   FastMCP Server │
│  or any agent)  │                       └────────┬─────────┘
└─────────────────┘                                │
                                          ┌────────┴─────────┐
                                          │                  │
                                    ┌─────▼──────┐   ┌──────▼───────┐
                                    │  SerpAPI    │   │ Jina Reader  │
                                    │  (Google    │   │ (Web Content │
                                    │   Search)   │   │  Extraction) │
                                    └────────────┘   └──────────────┘
```

---

## 📋 Prerequisites

- **Python** ≥ 3.12
- **uv** (recommended) or **pip** for package management
- API keys for:
  - [SerpAPI](https://serpapi.com/) — for Google search
  - [Jina AI](https://jina.ai/) — for web content reading

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sauravroy34/GoogleSearchMcp.git
cd GoogleSearchMcp
```

### 2. Set up the environment

**Using `uv` (recommended):**

```bash
uv venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
uv sync
```

**Using `pip`:**

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Configure API keys

Create a `.env` file in the project root:

```env
SERP_API_KEY=your_serpapi_key_here
JINA_API_KEY=your_jina_api_key_here
```

> **🔒 Note:** The `.env` file is included in `.gitignore` and will not be committed to version control.

### 4. Run the server

```bash
python main.py
```

The server starts using **stdio** transport, ready to accept MCP connections.

---

## 🔌 Integration with MCP Clients

### Claude Desktop / Cursor / Windsurf

Add the following to your MCP client configuration (e.g., `claude_desktop_config.json` or equivalent):

```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "python",
      "args": ["/absolute/path/to/GoogleSearchMcp/main.py"]
    }
  }
}
```

> Replace `/absolute/path/to/` with the actual path to your cloned repo.

---

## 🛠️ Tools Reference

### `search_web`

Perform a Google search and retrieve organic results.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | *required* | The search query string |
| `required_links` | `int` | `10` | Number of results to return (max: 20) |

**Returns:** A list of result objects, each containing:
- `title` — Page title
- `link` — URL
- `snippet` — Short description from search results

**Example query from an LLM:**
> *"YouTube explanation of Attention is All You Need"*

---

### `fetch_web_content`

Extract clean Markdown content from a web page.

| Parameter | Type | Description |
|---|---|---|
| `url` | `str` | The URL to extract content from |

**Returns:** Markdown-formatted text of the page content.

**Limitations:**
- ❌ Does **not** work with YouTube links (`youtube.com`, `youtu.be`)
- Returns an error message suggesting alternative approaches for video content

---

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| [`fastmcp`](https://github.com/jlowin/fastmcp) | MCP server framework |
| [`requests`](https://docs.python-requests.org/) | HTTP client for API calls |
| [`python-dotenv`](https://github.com/theskumar/python-dotenv) | Load environment variables from `.env` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source. Feel free to use and modify it for your own purposes.

---

## 🔗 Links

- **Repository:** [github.com/Sauravroy34/GoogleSearchMcp](https://github.com/Sauravroy34/GoogleSearchMcp)
- **SerpAPI Docs:** [serpapi.com/search-api](https://serpapi.com/search-api)
- **Jina Reader Docs:** [jina.ai/reader](https://jina.ai/reader/)
- **FastMCP Docs:** [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **MCP Specification:** [modelcontextprotocol.io](https://modelcontextprotocol.io/)
