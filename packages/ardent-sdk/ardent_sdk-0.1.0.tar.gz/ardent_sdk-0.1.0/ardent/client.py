import httpx
import time
import hmac
import hashlib
from uuid import uuid4
from typing import Dict, Any, Optional
from .exceptions import ArdentAPIError, ArdentAuthError, ArdentValidationError
import json

class ArdentClient:
    def __init__(
        self, 
        public_key: str,
        secret_key: str,
        base_url: str = "https://ardentbackendwebappfinal.azurewebsites.net"
    ):
        if not public_key or not secret_key:
            raise ArdentValidationError("Both public and secret keys are required")
            
        self.public_key = public_key
        self.secret_key = secret_key
        self.base_url = base_url.rstrip('/')
        self.session_id = str(uuid4())
        self._client = httpx.Client(timeout=3000.0)

    def _sign_request(self, method: str, path: str, body: str = "") -> Dict[str, str]:
        timestamp = str(int(time.time()))
        message = f"{timestamp}{method}{path}{body}"
        
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            "X-API-Key": self.public_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp,
            "X-Session-ID": self.session_id,
            "Content-Type": "application/json"
        }

    def create_job(self, message: str) -> Dict[str, Any]:
        path = "/v1/jobs/createJob"
        body = {
            "userMessage": message,
        }
        
        try:
            json_body = json.dumps(body, separators=(',', ':'))
            
            headers = self._sign_request(
                method="POST",
                path=path,
                body=json_body
            )
            
            response = self._client.post(
                f"{self.base_url}{path}",
                headers=headers,
                json=body
            )


            
            response.raise_for_status()
            
            if response.status_code == 201:  # Handle 201 Created specifically
                response_data = response.json()
                if not response_data:
                    raise ArdentAPIError("API returned empty response")
                
                # Ensure required fields are present
                required_fields = ['id', 'files_share_name', 'userID']
                if not all(field in response_data for field in required_fields):
                    # Generate an ID if missing
                    if 'id' not in response_data:
                        response_data['id'] = str(uuid4())
                    # Use empty string for missing share name
                    if 'files_share_name' not in response_data:
                        response_data['files_share_name'] = ''
                    # Use provided userID if missing

                        
                return response_data
                
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ArdentAuthError("Invalid API key or signature")
            raise ArdentAPIError(
                f"API request failed: {str(e)}", 
                status_code=e.response.status_code,
                response=e.response
            )
        except json.JSONDecodeError as e:
            raise ArdentAPIError(f"Invalid JSON response from API: {str(e)}")

    def execute_job(
        self, 
        jobID: str, 
        message: str, 
        files_share_name: str, 
        userID: str,
        safe_mode: bool = False
    ) -> Dict[str, Any]:
        """Execute a job with the given parameters."""
        path = "/v1/jobs/APIChat"  # Updated endpoint path
        body = {
            "jobID": jobID,
            "userMessage": message,
            "files_share_name": files_share_name,
            "userID": userID,
            "safeMode": safe_mode
        }
        
        try:
            json_body = json.dumps(body, separators=(',', ':'))
            headers = self._sign_request(
                method="POST",
                path=path,
                body=json_body
            )
            
            response = self._client.post(
                f"{self.base_url}{path}",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ArdentAuthError("Invalid API key or signature")
            elif e.response.status_code == 402:
                raise ArdentAPIError("Out of credits")
            elif e.response.status_code == 403:
                raise ArdentAuthError("Missing required scope: job:execute")
            raise ArdentAPIError(
                f"API request failed: {str(e)}", 
                status_code=e.response.status_code,
                response=e.response
            )

    def create_and_execute_job(
        self, 
        message: str,
        safe_mode: bool = False
    ) -> Dict[str, Any]:
        """Create and execute a job in one operation."""
        # First create the job
        path = "/v1/jobs/createJob"
        create_body = {
            "userMessage": message,
        }
        
        try:
            # Create job
            json_body = json.dumps(create_body, separators=(',', ':'))
            headers = self._sign_request(
                method="POST",
                path=path,
                body=json_body
            )
            
            create_response = self._client.post(
                f"{self.base_url}{path}",
                headers=headers,
                json=create_body
            )
            create_response.raise_for_status()
            job = create_response.json()
            
            if not job:
                raise ArdentAPIError("Job creation failed - empty response")
                
            # Then execute the job
            execute_path = "/v1/jobs/APIChat"
            execute_body = {
                "jobID": job["id"],
                "userMessage": message,
                "files_share_name": job["files_share_name"],
                "safeMode": safe_mode
            }
            
            json_body = json.dumps(execute_body, separators=(',', ':'))
            headers = self._sign_request(
                method="POST",
                path=execute_path,
                body=json_body
            )
            
            execute_response = self._client.post(
                f"{self.base_url}{execute_path}",
                headers=headers,
                json=execute_body
            )
            execute_response.raise_for_status()
            return execute_response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise ArdentAuthError("Invalid API key or signature")
            elif e.response.status_code == 402:
                raise ArdentAPIError("Out of credits")
            elif e.response.status_code == 403:
                raise ArdentAuthError("Missing required scope: job:execute")
            raise ArdentAPIError(
                f"API request failed: {str(e)}", 
                status_code=e.response.status_code,
                response=e.response
            )

    def close(self):
        """Close the underlying HTTP client and clean up resources."""
        if hasattr(self, '_client'):
            self._client.close()