import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount, Route

from mcp_server_jupyter.notebook_manager import NotebookManager

# Initialize server instance for Jupyter notebook management
server = Server("mcp-server-jupyter")
sse = SseServerTransport("/messages/")


# Set up Starlette routes for SSE transport
async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:  # noqa: SLF001
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name="Jupyter notebook manager",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


# Configure CORS middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST"],
        allow_headers=["Accept", "Content-Type", "Origin"],
        expose_headers=["Content-Type", "Content-Length"],
        allow_credentials=False,
    )
]

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
    middleware=middleware,
)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="read_notebook_with_outputs",
            description=(
                "Read the current version of the notebook at notebook_path, "
                "including cell outputs. "
                "Use this before modifying a notebook to understand "
                "its existing content and determine "
                "if changes are needed."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                },
                "required": ["notebook_path"],
            },
        ),
        types.Tool(
            name="read_notebook_source_only",
            description=(
                "Read the current version of the notebook "
                "at notebook_path without outputs. "
                "Use this when size limitations prevent "
                "reading the full notebook with outputs. "
                "Individual cell outputs can be retrieved "
                "using the read_output_of_cell tool."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                },
                "required": ["notebook_path"],
            },
        ),
        types.Tool(
            name="read_output_of_cell",
            description="Read the output of a specific cell in a notebook, by cell_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                    "cell_id": {"type": "string"},
                },
                "required": ["notebook_path", "cell_id"],
            },
        ),
        types.Tool(
            name="execute_cell",
            description=(
                "Executes a specific cell in a notebook and returns its output. "
                "Useful to check that the cell runs without errors "
                "as well as produces the desired output."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                    "cell_id": {"type": "string"},
                },
                "required": ["notebook_path", "cell_id"],
            },
        ),
        types.Tool(
            name="add_cell",
            description="Add a new cell to the notebook at the specified position.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                    "cell_type": {"type": "string"},
                    "source": {"type": "string"},
                    "position": {"type": "integer"},
                },
                "required": ["notebook_path", "source"],
            },
        ),
        types.Tool(
            name="edit_cell",
            description="Edit the source code of an existing cell in the notebook.",
            inputSchema={
                "type": "object",
                "properties": {
                    "notebook_path": {"type": "string"},
                    "cell_id": {
                        "type": "string",
                        "description": (
                            "Unique ID of the cell to edit. This can be obtained using "
                            "read_notebook_source_only or read_notebook_with_outputs."
                        ),
                    },
                    "source": {"type": "string"},
                },
                "required": ["notebook_path", "cell_id", "source"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Route tool calls to their respective handlers"""
    if name == "read_notebook_with_outputs":
        return _read_notebook(arguments["notebook_path"])
    elif name == "read_notebook_source_only":
        return _read_notebook(arguments["notebook_path"], with_outputs=False)
    elif name == "read_output_of_cell":
        return _read_cell_output(arguments["notebook_path"], arguments["cell_id"])
    elif name == "execute_cell":
        return _execute_cell(arguments["notebook_path"], arguments["cell_id"])
    elif name == "add_cell":
        return _add_cell(
            arguments["notebook_path"],
            arguments.get("cell_type", "code"),
            arguments["source"],
            arguments.get("position", -1),
        )
    elif name == "edit_cell":
        return _edit_cell(
            arguments["notebook_path"], arguments["cell_id"], arguments["source"]
        )

    raise ValueError(f"Unknown tool: {name}")


def _add_cell(
    notebook_path: str, cell_type: str, source: str, position: int
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Add a new cell to the notebook with the souce specified.

    Args:
        notebook_path: Path to the target notebook
        cell_type: Type of cell to add ('code' or 'markdown')
        source: Cell content
        position: Index where to insert the cell (-1 for append)

    Returns:
        A new cell id if successful, or an error message if not
    """
    try:
        nb_manager = NotebookManager(notebook_path)
        new_cell_index = nb_manager.add_cell(
            cell_type=cell_type,
            source=source,
            position=position,
        )
        nb_manager.save_notebook()
        id = nb_manager.get_cell_by_index(new_cell_index).get("id")
        return [
            types.TextContent(
                type="text", text=f"Cell with id {id} added successfully."
            ),
        ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"An error happened while trying to add a new cell: {str(e)}",
            )
        ]


def _edit_cell(
    notebook_path: str,
    id: str,
    source: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Edit an existing cell.

    Args:
        notebook_path: Path to the target notebook
        id: Unique identifier of the cell to edit
        source: New cell content

    Returns:
        Cell id if successful, or an error message if not
    """
    nb_manager = NotebookManager(notebook_path)
    if not nb_manager.update_cell_source(id=id, new_source=source):
        return [
            types.TextContent(
                type="text",
                text="No cell with the specified ID exists in the notebook.",
            )
        ]

    nb_manager.save_notebook()

    return [
        types.TextContent(type="text", text=f"Cell with id {id} updated successfully."),
    ]


def _read_notebook(
    notebook_path: str,
    with_outputs: bool = True,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Read contents of a notebook with optional outputs.

    Args:
        notebook_path: Path to the notebook
        with_outputs: Include execution outputs if True

    Returns:
        List of cell contents and outputs
    """
    nb_manager = NotebookManager(notebook_path)
    results = []

    for nb in nb_manager.get_notebook_details():
        results.extend(
            [
                types.TextContent(type="text", text=f"Cell with ID: {nb.cell_id}"),
                types.TextContent(type="text", text=nb.content),
            ]
        )

        if with_outputs and nb.cell_type == "code":
            results.extend(
                [
                    types.TextContent(
                        type="text", text=f"Output of cell {nb.cell_id}:"
                    ),
                    *(output.output for output in nb.outputs),
                ]
            )

    return results


def _read_cell_output(
    notebook_path: str,
    cell_id: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Read execution outputs of a specific cell.

    Args:
        notebook_path: Path to the notebook
        cell_id: ID of the target cell

    Returns:
        List of cell outputs
    """
    nb_manager = NotebookManager(notebook_path)
    cell = nb_manager.get_cell_by_id(cell_id)
    results = []

    for nb in nb_manager.parse_notebook_nodes(cell):
        if nb.cell_type == "code":
            results.extend(
                [
                    types.TextContent(
                        type="text", text=f"Output of cell {nb.cell_id}:"
                    ),
                    *(output.output for output in nb.outputs),
                ]
            )

    return results


def _execute_cell(
    notebook_path: str,
    cell_id: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Executes a specific cell in a notebook and returns its output.

    Args:
        notebook_path: Path to the notebook
        cell_id: ID of the target cell

    Returns:
        Cell outputs
    """
    nb_manager = NotebookManager(notebook_path)
    executed_nb_json = nb_manager.execute_cell_by_id(cell_id, {})
    nb_manager.save_notebook()

    return [output.output for nb in executed_nb_json for output in nb.outputs]


async def run(transport_type="stdio", port=8000):
    if transport_type == "stdio":
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="Jupyter notebook manager",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    elif transport_type == "sse":
        import uvicorn

        config = uvicorn.Config(starlette_app, host="127.0.0.1", port=port)
        uvicorn_server = uvicorn.Server(config)
        await uvicorn_server.serve()


def main():
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(description="MCP Jupyter Server")
    parser.add_argument(
        "transport",
        nargs="?",
        default="stdio",
        choices=["stdio", "sse"],
        help="Transport type (stdio or sse)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)",
    )

    args = parser.parse_args()
    asyncio.run(run(args.transport, args.port))
