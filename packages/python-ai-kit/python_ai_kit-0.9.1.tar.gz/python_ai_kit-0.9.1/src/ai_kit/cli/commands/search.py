from ai_kit.core.index import Index

async def search_command(query: str, max_results: int = 5):
    """Search the index for information."""
    index = Index()
    return await index.search(query, max_results=max_results)
    