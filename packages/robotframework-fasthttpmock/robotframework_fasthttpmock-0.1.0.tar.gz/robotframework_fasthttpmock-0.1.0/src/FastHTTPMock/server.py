import uvicorn
import uuid
import json
import threading
import atexit
import time
import logging
import os

from fastapi import FastAPI, Request, Response
from typing import Dict, Optional, Any
from FastHTTPMock.interaction import Interaction

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9334

logger = logging.getLogger(__name__)

def setup_debug_logging():
    """Setup debug logging if DEBUG env var is set."""
    if os.getenv('FASTHTTPMOCK_DEBUG', '').lower() in ('1', 'true', 'yes'):
        file_handler = logging.FileHandler('FastHTTPMock-debug.log', mode='w')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled for FastHTTPMock")

class MockServer:
    def __init__(self):
        self.thread = None
        self.app = FastAPI()
        self.interactions: Dict[str, Interaction] = {}
        self.server: Optional[uvicorn.Server] = None
        self.ready = False
        self._setup_routes()
        setup_debug_logging()


    def _setup_routes(self):
        @self.app.get("/health")
        async def health_check():
            logger.debug("Health check endpoint called")
            return {"status": "ok"}

        @self.app.post("/mock/interaction")
        async def add_interaction(interaction: dict):
            logger.debug(f"Adding new interaction: {interaction}")
            interaction_id = str(uuid.uuid4())
            self.interactions[interaction_id] = Interaction(
                id=interaction_id,
                **interaction
            )
            logger.debug(f"Added interaction with ID: {interaction_id}")
            return {"id": interaction_id}

        @self.app.delete("/mock/interaction/{interaction_id}")
        async def remove_interaction(interaction_id: str):
            logger.debug(f"Removing interaction: {interaction_id}")
            if interaction_id in self.interactions:
                del self.interactions[interaction_id]
            return {"status": "ok"}

        @self.app.get("/mock/interaction/{interaction_id}")
        async def get_interaction(interaction_id: str):
            logger.debug(f"Getting interaction: {interaction_id}")
            interaction = self.interactions.get(interaction_id)
            if interaction:
                return interaction.dict()
            return {"error": "Interaction not found"}

        @self.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        async def catch_all(request: Request, path: str):
            logger.debug(f"Received request: {request.method} {request.url.path}")
            logger.debug(f"Request headers: {dict(request.headers)}")
            body = await self._get_request_body(request)
            if body:
                logger.debug(f"Request body: {body}")
            else:
                logger.debug("No JSON body in request")

            # Find matching interaction
            for interaction in self.interactions.values():
                logger.debug(f"Checking interaction {interaction.id}:")
                logger.debug(f"  Expected: {interaction.request}")
                if await self._matches_request(request, interaction):
                    logger.debug(f"Found matching interaction: {interaction.id}")
                    interaction.increment_calls()
                    return self._create_response(interaction)
            logger.debug("No matching interaction found for request")
            return Response(status_code=404)

    def _create_response(self, interaction: Interaction) -> Response:
        """Create response from interaction."""
        response_body = interaction.response.get("body", {})
        if isinstance(response_body, str):
            try:
                response_body = json.loads(response_body)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in response body: {response_body}")
                return Response(status_code=500)

        status_code = interaction.response.get("status", 200)
        if isinstance(status_code, str):
            status_code = int(status_code)

        return Response(
            content=json.dumps(response_body),
            status_code=status_code,
            headers=interaction.response.get("headers", {})
        )

    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Get request body if present."""
        try:
            return await request.json()
        except:
            return None

    async def _matches_request(self, request: Request, interaction: Interaction) -> bool:
        logger.debug(f"Matching request against interaction {interaction.id}")
        if request.method != interaction.request.get("method", "GET"):
            logger.debug(f"Method mismatch: {request.method} != {interaction.request.get('method')}")
            return False

        # Match path
        if request.url.path != interaction.request.get("path"):
            logger.debug(f"Path mismatch: {request.url.path} != {interaction.request.get('path')}")
            return False

        # Match headers if specified
        if "headers" in interaction.request:
            for key, value in interaction.request["headers"].items():
                if request.headers.get(key) != value:
                    logger.debug(f"Header mismatch for {key}: {request.headers.get(key)} != {value}")
                    return False

        # Match body if specified
        if "body" in interaction.request:
            try:
                body = await request.json()
                if body != interaction.request["body"]:
                    logger.debug(f"Body mismatch: {body} != {interaction.request['body']}")
                    return False
            except:
                logger.debug("Failed to parse request body as JSON")
                return False

        logger.debug("Request matched successfully")
        return True

    def start(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """Start the mock server."""
        config = uvicorn.Config(
            self.app,
            host=host,
            port=port,
            access_log=False,  # Disable access logs for better performance
            log_config=None
        )
        logger.debug(f"Starting mock server on {host}:{port}")
        self.server = uvicorn.Server(config)
        
        def run_server():
            self.server.run()
            
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
        
        # Wait for server to be ready
        max_retries = 10
        retry_interval = 0.1
        for attempt in range(max_retries):
            logger.debug(f"Checking server health (attempt {attempt + 1}/{max_retries})")
            try:
                import requests
                requests.get(f"http://{host}:{port}/health")
                self.ready = True
                logger.debug("Server is ready")
                break
            except:
                logger.debug("Server not ready yet, retrying...")
                time.sleep(retry_interval)
        
        if not self.ready:
            logger.error("Failed to start mock server")
            raise RuntimeError("Failed to start mock server")
        
        # Register shutdown handler
        atexit.register(self.stop)

    def stop(self):
        """Stop the mock server."""
        if self.server:
            logger.debug("Stopping mock server")
            self.server.should_exit = True
            self.thread.join()
            self.server = None
            self.ready = False
            self.interactions = {}
            logger.debug("Server stopped")

    def is_running(self) -> bool:
        """Check if the server is running and ready."""
        return self.ready