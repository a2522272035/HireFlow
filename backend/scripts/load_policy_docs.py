"""Script to load policy documents into vector store."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path


async def load_policy_document(file_path: str) -> None:
    """Load a policy document into the vector store."""
    # TODO: Implement document loading
    # 1. Read file content
    # 2. Generate embeddings
    # 3. Store in pgvector
    print(f"Loading document: {file_path}")


async def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python load_policy_docs.py <file_or_directory>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        await load_policy_document(str(path))
    elif path.is_dir():
        for file_path in path.glob("**/*"):
            if file_path.is_file():
                await load_policy_document(str(file_path))
    else:
        print(f"Path not found: {path}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
