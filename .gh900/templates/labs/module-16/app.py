"""GH-900 Module 16 FastAPI exercise baseline.

The application intentionally starts with one working route. During the exercise,
add the Pydantic request model and POST /analyze-text endpoint described in the
course Issue. Review any Copilot-generated code and verify it with the tests.
"""

from fastapi import FastAPI

app = FastAPI(title="GH-900 Copilot Python Practice")


@app.get("/health")
def health() -> dict[str, str]:
    """Return a deterministic health response for baseline verification."""
    return {"status": "ok"}


# TODO: Add a Pydantic BaseModel containing `text: str`.
# TODO: Add POST /analyze-text.
# TODO: Reject text that is empty after trimming whitespace.
# TODO: Return deterministic input length and a checksum/hash.
