"""
TruthLens AI — Custom Exception Handlers
Maps backend errors to safe, user-friendly HTTP responses.
"""

from fastapi import Request
from fastapi.responses import JSONResponse


class GroqAPIError(Exception):
    """Raised when the Groq API returns an error."""
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GroqRateLimitError(GroqAPIError):
    """Raised when the Groq API rate limit is exceeded."""
    def __init__(self):
        super().__init__(
            message="The AI service is currently rate-limited. Please wait a moment and try again.",
            status_code=429,
        )


class GroqTimeoutError(GroqAPIError):
    """Raised when the Groq API request times out."""
    def __init__(self):
        super().__init__(
            message="The AI service took too long to respond. Please try again.",
            status_code=504,
        )


class GroqModelUnavailableError(GroqAPIError):
    """Raised when the configured model is not available."""
    def __init__(self, model_name: str):
        super().__init__(
            message=f"The configured AI model '{model_name}' is currently unavailable. Please check the model name in your environment configuration.",
            status_code=503,
        )


class AnalysisParsingError(Exception):
    """Raised when the AI response cannot be parsed into the expected format."""
    def __init__(self, message: str = "The AI returned an unexpected response format. Please try again."):
        self.message = message
        super().__init__(self.message)


# --- FastAPI Exception Handlers ---

async def groq_api_error_handler(request: Request, exc: GroqAPIError) -> JSONResponse:
    """Handle Groq API errors with safe messages."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "detail": None},
    )


async def analysis_parsing_error_handler(request: Request, exc: AnalysisParsingError) -> JSONResponse:
    """Handle AI response parsing errors."""
    return JSONResponse(
        status_code=500,
        content={"error": exc.message, "detail": None},
    )


async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler — never exposes stack traces or secrets."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred. Please try again later.",
            "detail": None,
        },
    )
