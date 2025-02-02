from typing import Any, Optional, List, Dict, Literal
from pydantic import HttpUrl
import json
from PIL.Image import Image
from pathlib import Path
from io import IOBase

from ..._resource import SyncAPIResource, AsyncAPIResource

from ...types.documents.image_settings import ImageSettings
from ...types.mime import MIMEData, EmailData
from ...types.modalities import Modality
from ...types.automations.automations import Mailbox, UpdateMailboxRequest, AutomationLog

from ..._utils.mime import prepare_mime_document
from ..._utils.ai_model import assert_valid_model_extraction




class Mailboxes(SyncAPIResource):
    """Emails API wrapper for managing email automation configurations"""

    def __init__(self, client: Any) -> None:
        super().__init__(client=client)
        self.tests = TestMailboxes(client=client)

    def create(
        self,
        email: str,

        json_schema: Dict[str, Any],
        webhook_url: HttpUrl,

        # email specific opitonals Fields
        authorized_domains: List[str] = [],
        authorized_emails: List[str] = [],
        # HTTP Config Optional Fields
        webhook_headers: Dict[str, str] = {},

        # DocumentExtraction Config
        image_settings: Optional[Dict[str, Any]] = None,
        modality: Modality = "native",
        model: str = "gpt-4o-mini",
        temperature: float = 0,

    ) -> Mailbox:
        """Create a new email automation configuration.
        
        Args:
            email: Email address for the mailbox
            json_schema: JSON schema to validate extracted email data
            webhook_url: Webhook URL to receive processed emails
            webhook_headers: Webhook headers to send with processed emails
            authorized_domains: List of authorized domains for the mailbox
            authorized_emails: List of authorized emails for the mailbox
            image_settings: Optional image preprocessing operations
            modality: Processing modality (currently only "native" supported)
            model: AI model to use for processing
            temperature: Model temperature setting
            
        Returns:
            Mailbox: The created mailbox configuration
        """

        assert_valid_model_extraction(model)

        data = {
            "email": email,
            "webhook_url": webhook_url,
            "webhook_headers": webhook_headers,
            "json_schema": json_schema,
            "authorized_domains": authorized_domains,
            "authorized_emails": authorized_emails,
            "image_settings": image_settings or ImageSettings(),
            "modality": modality,
            "model": model,
            "temperature": temperature,
        }

        request = Mailbox.model_validate(data)
        response = self._client._request("POST", "/v1/automations/mailboxes", data=request.model_dump(mode="json"))

        return Mailbox.model_validate(response)

    def list(self,
            before: str | None = None,
            after: str | None = None,
            limit: int = 10,
            order: Literal["asc", "desc"] | None = "desc",
            email: Optional[str] = None,
            webhook_url: Optional[str] = None,
            schema_id: Optional[str] = None,
            schema_data_id: Optional[str] = None,
            ) -> List[Mailbox]:
        """List all email automation configurations.

        Args:
            before: Optional cursor for pagination - get results before this log ID
            after: Optional cursor for pagination - get results after this log ID  
            limit: Maximum number of logs to return (1-100, default 10)
            order: Sort order by creation time - "asc" or "desc" (default "desc")
            email: Optional email address filter
            webhook_url: Optional webhook URL filter
            schema_id: Optional schema ID filter
            schema_data_id: Optional schema data ID filter
        
        Returns:
            List[Mailbox]: List of mailbox configurations
        """
        params = {
            "email": email,
            "webhook_url": webhook_url,
            "schema_id": schema_id,
            "schema_data_id": schema_data_id,
            "before": before,
            "after": after,
            "limit": limit,
            "order": order,
        }

        response = self._client._request("GET", "/v1/automations/mailboxes", params=params)

        return [Mailbox.model_validate(mailbox) for mailbox in response]

    def get(self, email: str) -> Mailbox:
        """Get a specific email automation configuration.
        
        Args:
            email: Email address of the mailbox
            
        Returns:
            Mailbox: The mailbox configuration
        """
        response = self._client._request("GET", f"/v1/automations/mailboxes/{email}")
        return Mailbox.model_validate(response)

    def update(
        self,
        email: str,
        webhook_url: Optional[HttpUrl] = None,
        webhook_headers: Optional[Dict[str, str]] = None,
        authorized_domains: Optional[List[str]] = None,
        authorized_emails: Optional[List[str]] = None,
        image_settings: Optional[Dict[str, Any]] = None,
        modality: Optional[Modality] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        json_schema: Optional[Dict[str, Any]] = None
    ) -> Mailbox:
        """Update an email automation configuration.
        
        Args:
            email: Email address of the mailbox to update
            webhook_url: New webhook configuration
            webhook_headers: New webhook configuration
            max_file_size: New webhook configuration
            file_payload: New webhook configuration
            follow_up: New webhook configuration
            authorized_domains: New webhook configuration
            authorized_emails: New webhook configuration
            image_settings: New image preprocessing operations
            modality: New processing modality
            model: New AI model
            temperature: New temperature setting
            json_schema: New JSON schema
            
        Returns:
            Mailbox: The updated mailbox configuration
        """
        data: dict[str, Any] = {}
        if webhook_url is not None:
            data["webhook_url"] = webhook_url
        if webhook_headers is not None:
            data["webhook_headers"] = webhook_headers
        if authorized_domains is not None:
            data["authorized_domains"] = authorized_domains
        if authorized_emails is not None:
            data["authorized_emails"] = authorized_emails
        if image_settings is not None:
            data["image_settings"] = image_settings
        if modality is not None:
            data["modality"] = modality
        if model is not None:
            assert_valid_model_extraction(model)
            data["model"] = model
        if temperature is not None:
            data["temperature"] = temperature
        if json_schema is not None:
            data["json_schema"] = json_schema

        update_mailbox_request = UpdateMailboxRequest.model_validate(data)

        response = self._client._request("PUT", f"/v1/automations/mailboxes/{email}", data=update_mailbox_request.model_dump())

        return Mailbox(**response)

    def delete(self, email: str) -> None:
        """Delete an email automation configuration.
        
        Args:
            email: Email address of the mailbox to delete
        """
        response = self._client._request("DELETE", f"/v1/automations/mailboxes/{email}")



    def logs(self, 
                before: str | None = None,
                after: str | None = None,
                limit: int = 10,
                order: Literal["asc", "desc"] | None = "desc",
                email: Optional[str] = None,
                webhook_url: Optional[str] = None,
                schema_id: Optional[str] = None,
                schema_data_id: Optional[str] = None,
                ) -> List[AutomationLog]:
        """Get logs for a specific email automation.
        
        Args:
            before: Optional cursor for pagination - get results before this log ID
            after: Optional cursor for pagination - get results after this log ID  
            limit: Maximum number of logs to return (1-100, default 10)
            order: Sort order by creation time - "asc" or "desc" (default "desc")
            email: Optional email address filter
            webhook_url: Optional webhook URL filter
            schema_id: Optional schema ID filter
            schema_data_id: Optional schema data ID filter
            
        Returns:
            List[Dict[str, Any]]: List of log entries
        """
        params = {
            "email": email,
            "webhook_url": webhook_url,
            "schema_id": schema_id,
            "schema_data_id": schema_data_id,
            "before": before,
            "after": after,
            "limit": limit,
            "order": order,
        }
        response = self._client._request("GET", f"/v1/automations/mailboxes/{email}/logs", params=params)

        return [AutomationLog.model_validate(log) for log in response]



class TestMailboxes(SyncAPIResource):

    def forwarding(self, 
                    email: str,
                    document: Path | str | IOBase | HttpUrl | MIMEData,
                    verbose: bool = True
                    ) -> EmailData:
        """Mock endpoint that simulates the complete email forwarding process with sample data.
        
        Args:
            email: Email address of the mailbox to mock
            
        Returns:
            DocumentExtractResponse: The simulated extraction response
        """
        mime_document = prepare_mime_document(document)
        response = self._client._request("POST", f"/v1/automations/mailboxes/tests/forwarding/{email}", data={"document": mime_document.model_dump()})

        email_data = EmailData.model_validate(response)
        
        if verbose:
            print(f"\nTEST EMAIL FORWARDING RESULTS:")
            print(f"\n#########################")
            print(f"Email ID: {email_data.id}")
            print(f"Subject: {email_data.subject}")
            print(f"From: {email_data.sender}")
            print(f"To: {', '.join(str(r) for r in email_data.recipients_to)}")
            if email_data.recipients_cc:
                print(f"CC: {', '.join(str(r) for r in email_data.recipients_cc)}")
            print(f"Sent at: {email_data.sent_at}")
            print(f"Attachments: {len(email_data.attachments)}")
            if email_data.body_plain:
                print("\nBody Preview:")
                print(email_data.body_plain[:500] + "..." if len(email_data.body_plain) > 500 else email_data.body_plain)

        return email_data

    def processing(self, 
                         email: str,
                         document: Path | str | IOBase | HttpUrl | Image | MIMEData,
                         verbose: bool = True
                         ) -> AutomationLog:
        """Mock endpoint that simulates the complete email processing process with sample data.
        
        Args:
            email: Email address of the mailbox to mock
            
        Returns:
            DocumentExtractResponse: The simulated extraction response
        """
        mime_document = prepare_mime_document(document)
        response = self._client._request("POST", f"/v1/automations/mailboxes/tests/processing/{email}", data={"document": mime_document.model_dump()})

        log = AutomationLog.model_validate(response)

        if verbose:
            print(f"\nTEST EMAIL PROCESSING RESULTS:")
            print(f"\n#########################")
            print(f"Status Code: {log.external_request_log.status_code}")
            print(f"Duration: {log.external_request_log.duration_ms:.2f}ms")
            
            if log.external_request_log.error:
                print(f"\nERROR: {log.external_request_log.error}")
            
            if log.external_request_log.response_body:
                print("\n--------------")
                print("RESPONSE BODY:")
                print("--------------")

                print(json.dumps(log.external_request_log.response_body, indent=2))
            if log.external_request_log.response_headers:
                print("\n--------------")
                print("RESPONSE HEADERS:")
                print("--------------")
                print(json.dumps(log.external_request_log.response_headers, indent=2))


        return log
    

    def webhook(self, 
                          email: str,
                          verbose: bool = True
                          ) -> AutomationLog:
        """Mock endpoint that simulates the complete webhook process with sample data.
        
        Args:
            email: Email address of the mailbox to mock
            
        Returns:
            AutomationLog: The simulated webhook response
        """

        response = self._client._request("POST", f"/v1/automations/mailboxes/tests/webhook/{email}")

        log = AutomationLog.model_validate(response)

        if verbose:
            print(f"\nTEST WEBHOOK RESULTS:")
            print(f"\n#########################")
            print(f"Status Code: {log.external_request_log.status_code}")
            print(f"Duration: {log.external_request_log.duration_ms:.2f}ms")
            
            if log.external_request_log.error:
                print(f"\nERROR: {log.external_request_log.error}")
            
            if log.external_request_log.response_body:
                print("\n--------------")
                print("RESPONSE BODY:")
                print("--------------")

                print(json.dumps(log.external_request_log.response_body, indent=2))
            if log.external_request_log.response_headers:
                print("\n--------------")
                print("RESPONSE HEADERS:")
                print("--------------")
                print(json.dumps(log.external_request_log.response_headers, indent=2))

        return log
