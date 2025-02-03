import logging
import requests
import os
import json
from typing import Optional
import time

class BskySession:
    """
    Represents a session with the BlueSky social network.
    The session handles authentication, token refreshing, and provides methods for making authenticated requests.
    
    Attributes:
        handle (str): The user handle (e.g., username) used for authentication.
        app_password (str): The application-specific password for authentication.
        access_token (str): Token provided by BlueSky after successful authentication.
        refresh_token (str): Token used to refresh the access token when it expires.
        did (str): A unique identifier for the session.
        session_file (str): Path to the file where session tokens are stored.
    """
    
    BASE_URL = "https://bsky.social/xrpc"

    def __init__(self, handle: str, app_password: str, session_dir: Optional[str] = None):
        """
        Initializes a BlueSky session.

        Args:
            handle (str): User handle for authentication.
            app_password (str): Application-specific password for authentication.
            session_file (str, optional): Custom path for session storage.
        """
        self.handle = handle
        self.app_password = app_password
        
        # Create sessions directory in current working directory
        sessions_dir = session_dir or os.path.join(os.getcwd(), '.bsky_sessions')
        os.makedirs(sessions_dir, exist_ok=True)
        
        self.session_file = os.path.join(sessions_dir, f'{handle}_session.json')
        
        self.access_token = None
        self.refresh_token = None
        self.did = None
        self._load_session()

    def _create_session(self):
        """
        Creates a new session with BlueSky.

        Returns:
            None
        """
        url = f"{self.BASE_URL}/com.atproto.server.createSession"
        payload = {"identifier": self.handle, "password": self.app_password}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            session = resp.json()
            self.access_token = session["accessJwt"]
            self.refresh_token = session.get("refreshJwt")
            self.did = session["did"]
            
            self._save_session()
            logging.info(f"New session created for {self.handle}")
        
        except requests.RequestException as e:
            logging.error(f"Session creation failed: {e}")
            raise ConnectionError(f"Error creating session: {e}")

    def _refresh_access_token(self):
        """
        Refreshes the access token using the refresh token.
        If refresh fails, initiates a new authentication session.

        Returns:
            None
        """
        url = f"{self.BASE_URL}/com.atproto.server.refreshSession"
        headers = {"Authorization": f"Bearer {self.refresh_token}"}
        try:
            resp = requests.post(url, headers=headers, timeout=10)
            
            if resp.status_code == 401:
                logging.warning("Refresh token is no longer valid. Creating new session.")
                self._create_session()
                return
            
            resp.raise_for_status()
        except requests.RequestException as e:
            logging.error("Error %s: %s", getattr(resp, 'status_code', 'No Response'), getattr(resp, 'text', str(e)))
            logging.warning("Failed to refresh token. Creating new session.")
            self._create_session()
            return

        session = resp.json()
        self.access_token = session["accessJwt"]
        self.refresh_token = session.get("refreshJwt")
        self.did = session["did"]
        self._save_session()
        logging.info("Access token refreshed successfully.")

    def _load_session(self):
        """
        Loads the session tokens from persistent storage.

        Returns:
            None
        """
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r') as f:
                    session = json.load(f)
                
                # Validate session data
                if not all(session.get(key) for key in ["accessJwt", "refreshJwt", "did"]):
                    logging.warning("Incomplete session data. Creating new session.")
                    self._create_session()
                    return
                
                self.access_token = session["accessJwt"]
                self.refresh_token = session["refreshJwt"]
                self.did = session["did"]
                
                logging.info(f"Session loaded for {self.handle}")
            
            except (IOError, json.JSONDecodeError) as e:
                logging.warning(f"Session load failed: {e}")
                self._create_session()
        else:
            logging.info(f"No session found for {self.handle}. Creating new session.")
            self._create_session()

    def _save_session(self):
        """
        Saves the current session tokens to persistent storage.

        Returns:
            None
        """
        session_data = {
            "accessJwt": self.access_token,
            "refreshJwt": self.refresh_token,
            "did": self.did,
            "created_at": time.time()
        }
        
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
            logging.info(f"Session saved for {self.handle}")
        
        except IOError as e:
            logging.error(f"Session save failed: {e}")
            raise

    def get_auth_header(self) -> dict:
        """
        Generates the authentication header using the session's access token.

        Returns:
            dict: Authorization header for authenticated API requests.
        """
        return {"Authorization": f"Bearer {self.access_token}"}

    def api_call(self, endpoint: str, method: str = 'GET', json: Optional[dict] = None, data: Optional[bytes] = None, headers: Optional[dict] = None, params: Optional[dict] = None, retry: int = 1) -> dict:
        """
        Makes an authenticated API call to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to call.
            method (str): The HTTP method to use for the request.
            json (dict, optional): The JSON payload to send with the request.
            data (bytes, optional): The data to send with the request.
            headers (dict, optional): Additional headers to send with the request.
            params (dict, optional): Parameters to include in the query string.
            retry (int): Number of retry attempts left.

        Returns:
            dict: The server's response as a dictionary.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            from urllib.parse import urlencode
            url = f"{url}?{urlencode(params)}"
        
        headers = headers or {}
        headers.update(self.get_auth_header())
        
        try:
            resp = requests.request(method, url, headers=headers, json=json, data=data, timeout=10)
            if resp.status_code in [401, 400] and retry > 0:
                logging.info("Token potentially expired or invalid. Attempting to refresh.")
                try:
                    self._refresh_access_token()
                except ConnectionError as e:
                    logging.error("Failed to refresh token: %s", e)
                    logging.info("Creating a new session.")
                    self._create_session()
                headers.update(self.get_auth_header())
                return self.api_call(endpoint, method, json, data, headers, params, retry=retry-1)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logging.error("Error during API call: %s", e)
            raise

    def logout(self):
        """
        Logs out by clearing session tokens and deleting the session file.

        Returns:
            None
        """
        self.access_token = None
        self.refresh_token = None
        self.did = None
        if os.path.exists(self.session_file):
            try:
                os.remove(self.session_file)
                logging.info("Session file deleted.")
            except OSError as e:
                logging.error("Error deleting session file: %s", e)
