from datetime import datetime
import logging
from typing import Optional

import requests
from pydantic import BaseModel

from t_reporting_sdk.repositories.api_clients.fabric.auth import JWTAuth


logger = logging.getLogger(__name__)


class FabricClientConfig(BaseModel):
    user_email: str
    user_otp_secret: str
    base_url: str


class FabricClient:
    def __init__(
        self, 
        config: FabricClientConfig,
    ):
        fabric_auth = JWTAuth(
            email=config.user_email,
            otp_secret=config.user_otp_secret,
            auth_url=config.base_url + "/verify",
            refresh_url=config.base_url + "/refresh-token",
        )
        self._session = requests.Session()
        self._session.auth = fabric_auth

        # Using the /me endpoint as a temporary solution for reporting.
        # This should be replaced with the actual reporting endpoint when available.
        self._base_url = config.base_url

    def create_agent_run(self, run_id: int, run_date: Optional[datetime] = None) -> None:
        url = f"{self._base_url}/apt/agent-runs"
        json_body = {"run_id": run_id, "run_date": run_date}
        response = self._session.post(
            url=url,
            json=json_body
        )
        try:
            # Expecting 201 or 409 status code
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 409:
                # Gracefully handle the case where the agent run already exists
                logger.warning(f"Agent Run already exists: {run_id}")
                return
            else:
                raise e
        if response.status_code != 201:
            raise RuntimeError("Failed to create agent run.")

    def create_eva_record(
        self,
        run_id: int,
        status: str,
        exception_type: Optional[str],
        message: str,
        customer_id: str,
        patient_id: str,
        payer_id: Optional[str],
        portal: str,
        insurance_eligibility: Optional[str],
    ) -> None:
        url = f"{self._base_url}/apt/records/eva"
        json_body = {
            "agent_run_id": run_id,
            "status": status,
            "exception_type": exception_type,
            "message": message,
            "customer_id": customer_id,
            "patient_id": patient_id,
            "payer_id": payer_id,
            "portal": portal,
            "description": "placeholder",  # TODO: remove this once no longer required by Fabric API
            "insurance_eligibility": insurance_eligibility,
        }
        response = self._session.post(
            url=url,
            json=json_body,
        )
        response.raise_for_status()
        if response.status_code != 202:
            raise RuntimeError("Failed to eva record.")
