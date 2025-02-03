import requests
from typing import Optional, List

from .constants import BASE_URL, HEADERS_ACCEPT, DEFAULT_MODEL_NAME
from .exceptions import (
    OylanAPIError,
    OylanAPIAuthError,
    OylanAPIRequestError,
    OylanAPINotFoundError,
    OylanAPIServerError
)

class Client:
    """
    A Python client for the Oylan Assistant API.

    Example:
    from OylanAPI import Client
    client = Client(api_key="YOUR_API_KEY")
    """

    def __init__(self, api_key: str):
        """
        Initialize the Oylan API client with the given API key.
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Api-Key {self.api_key}",
            "Accept": HEADERS_ACCEPT
        })

    def _handle_response(self, response: requests.Response):
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                return None
        elif response.status_code == 400:
            raise OylanAPIRequestError(f"Invalid request parameters: {response.text}")
        elif response.status_code == 401:
            raise OylanAPIAuthError("Authentication credentials were not provided or are invalid.")
        elif response.status_code == 404:
            raise OylanAPINotFoundError("Requested resource not found.")
        elif 500 <= response.status_code < 600:
            raise OylanAPIServerError("An unexpected server error occurred.")
        else:
            raise OylanAPIError(f"Unexpected status code {response.status_code}: {response.text}")

    # --------------------------------------------------
    # 1) GET /assistant/ (List all)
    # --------------------------------------------------
    def list_assistants(self):
        url = f"{BASE_URL}/assistant/"
        response = self.session.get(url)
        return self._handle_response(response)

    # --------------------------------------------------
    # 2) POST /assistant/
    # --------------------------------------------------
    def create_assistant(self,
                         name: str,
                         description: Optional[str] = None,
                         temperature: float = 1.0,
                         max_tokens: int = 200,
                         model: str = DEFAULT_MODEL_NAME,
                         system_instructions: Optional[str] = None,
                         context: Optional[str] = None):
        url = f"{BASE_URL}/assistant/"
        payload = {
            "name": name,
            "description": description,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "model": model,
            "system_instructions": system_instructions,
            "context": context
        }
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    # --------------------------------------------------
    # 3) GET /assistant/models
    # --------------------------------------------------
    def list_models(self):
        url = f"{BASE_URL}/assistant/models/"
        response = self.session.get(url)
        return self._handle_response(response)

    # --------------------------------------------------
    # 4) POST /assistant/{assistant_id}/interactions/
    # --------------------------------------------------
    def create_interaction(self,
                           assistant_id: int,
                           text_prompt: Optional[str] = None,
                           file_prompt: Optional[int] = None,
                           images: Optional[List[str]] = None,
                           stream: bool = False):
        url = f"{BASE_URL}/assistant/{assistant_id}/interactions/"

        data = {
            "assistant": str(assistant_id),
            "stream": "true" if stream else "false"
        }
        if text_prompt:
            data["text_prompt"] = text_prompt
        if file_prompt is not None:
            data["file_prompt"] = str(file_prompt)

        files = []
        if images:
            for img_path in images:
                files.append(("image", open(img_path, "rb")))

        # multipart/form-data (files + form fields)
        with requests.Session() as s:
            s.headers.update(self.session.headers)
            response = s.post(url, data=data, files=files)

        return self._handle_response(response)

    # --------------------------------------------------
    # 5) GET /assistant/{assistant_id}/
    # --------------------------------------------------
    def get_assistant(self, assistant_id: int):
        url = f"{BASE_URL}/assistant/{assistant_id}/"
        response = self.session.get(url)
        return self._handle_response(response)

    # --------------------------------------------------
    # 6) PUT /assistant/{assistant_id}/
    # --------------------------------------------------
    def update_assistant(self,
                         assistant_id: int,
                         name: str,
                         description: Optional[str] = None,
                         temperature: float = 1.0,
                         max_tokens: int = 200,
                         model: str = DEFAULT_MODEL_NAME,
                         system_instructions: Optional[str] = None,
                         context: Optional[str] = None):
        url = f"{BASE_URL}/assistant/{assistant_id}/"
        payload = {
            "name": name,
            "description": description,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "model": model,
            "system_instructions": system_instructions,
            "context": context
        }
        response = self.session.put(url, json=payload)
        return self._handle_response(response)

    # --------------------------------------------------
    # 7) PATCH /assistant/{assistant_id}/
    # --------------------------------------------------
    def patch_assistant(self, assistant_id: int, **kwargs):
        url = f"{BASE_URL}/assistant/{assistant_id}/"
        response = self.session.patch(url, json=kwargs)
        return self._handle_response(response)

    # --------------------------------------------------
    # 8) DELETE /assistant/{assistant_id}/
    # --------------------------------------------------
    def delete_assistant(self,
                         assistant_id: int,
                         delete_contexts: bool = True,
                         clear_base_context: bool = True):
        url = f"{BASE_URL}/assistant/{assistant_id}/"
        params = {
            "delete_contexts": str(delete_contexts).lower(),
            "clear_base_context": str(clear_base_context).lower()
        }
        response = self.session.delete(url, params=params)
        if response.status_code == 204:
            return True
        return self._handle_response(response)

    # --------------------------------------------------
    # 9) POST /assistant/{assistant_id}/upload-docx/
    # --------------------------------------------------
    def upload_docx(self,
                    assistant_id: int,
                    file_paths: List[str],
                    csrf_token: Optional[str] = None):
        url = f"{BASE_URL}/assistant/{assistant_id}/upload-docx/"
        files_data = []
        for path in file_paths:
            files_data.append((
                "files",
                (
                    path,
                    open(path, "rb"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            ))

        headers = self.session.headers.copy()
        if csrf_token:
            headers["X-CSRFToken"] = csrf_token

        with requests.Session() as s:
            s.headers.update(headers)
            response = s.post(url, files=files_data)

        return self._handle_response(response)
