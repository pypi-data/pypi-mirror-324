from pydantic import BaseModel, Field,  HttpUrl, EmailStr, field_validator, computed_field
from typing import Any, Optional, Literal, List, Dict, ClassVar
import uuid
import datetime
import os
import re 
import copy
import json

from ...types.documents.image_settings import ImageSettings
from ...types.documents.parse import DocumentExtractResponse
from ...types.pagination import ListMetadata
from ...types.modalities import Modality
from ...types.mime import MIMEData, BaseMIMEData

from ...types.usage import Amount
from ..._utils.usage.usage import compute_cost_from_model
from ..._utils.json_schema import clean_schema
from ..._utils.mime import generate_sha_hash_from_string

# Never used anywhere in the logs, but will be useful
class HttpOutput(BaseModel): 
    extraction: dict[str,Any]
    payload: Optional[MIMEData] # MIMEData forwarded to the mailbox, or to the link
    user_email: Optional[EmailStr] # When the user is logged or when he forwards an email

class AutomationConfig(BaseModel):
    object: str
    id: str
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    # HTTP Config
    webhook_url: HttpUrl = Field(..., description = "Url of the webhook to send the data to")
    webhook_headers: Dict[str, str] = Field(default_factory=dict, description = "Headers to send with the request")

    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")

    # New attributes
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])

    

domain_pattern = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")

class Mailbox(BaseModel):
    EMAIL_PATTERN: ClassVar[str] = f".*@{os.getenv('EMAIL_DOMAIN', 'devmail.uiform.com')}$"
    object: Literal['mailbox'] = "mailbox"
    id: str = Field(default_factory=lambda: "mb_" + str(uuid.uuid4()), description="Unique identifier for the mailbox")
    
    # Email Specific config
    email: str = Field(..., pattern=EMAIL_PATTERN)
    authorized_domains: list[str] = Field(default_factory=list, description = "List of authorized domains to receive the emails from")
    authorized_emails: List[EmailStr] = Field(default_factory=list, description = "List of emails to access the link")

    # Automation Config
    webhook_url: HttpUrl = Field(..., description = "Url of the webhook to send the data to")
    webhook_headers: Dict[str, str] = Field(default_factory=dict, description = "Headers to send with the request")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    # DocumentExtraction Config
    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])


    # Normalize email fields (case-insensitive)
    @field_validator("email", mode="before")
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("authorized_emails", mode="before")
    def normalize_authorized_emails(cls, emails: List[str]) -> List[str]:
        return [email.strip().lower() for email in emails]
    
    @field_validator('authorized_domains', mode='before')
    def validate_domain(cls, list_domains: list[str]) -> list[str]:
        for domain in list_domains:
            if not domain_pattern.match(domain):
                raise ValueError(f"Invalid domain: {domain}")
        return list_domains
    
    @computed_field   # type: ignore
    @property
    def schema_data_id(self) -> str:
        """Returns the SHA1 hash of the schema data, ignoring all prompt/description/default fields.
        
        Returns:
            str: A SHA1 hash string representing the schema data version.
        """
        return "sch_data_id_" + generate_sha_hash_from_string(
            json.dumps(
                clean_schema(copy.deepcopy(self.json_schema), remove_custom_fields=True, fields_to_remove=["description", "default", "title", "required", "examples", "deprecated", "readOnly", "writeOnly"]),
                sort_keys=True).strip(), 
            "sha1")

    # This is a computed field, it is exposed when serializing the object
    @computed_field   # type: ignore
    @property
    def schema_id(self) -> str:
        """Returns the SHA1 hash of the complete schema.
        
        Returns:
            str: A SHA1 hash string representing the complete schema version.
        """
        return "sch_id_" + generate_sha_hash_from_string(json.dumps(self.json_schema, sort_keys=True).strip(), "sha1")





class Link(BaseModel):
    object: Literal['link'] = "link"
    id: str = Field(default_factory=lambda: "lnk_" + str(uuid.uuid4()), description="Unique identifier for the extraction link")
    
    # Link Specific Config
    name: str = Field(..., description = "Name of the link")
    password: Optional[str] = Field(None, description = "Password to access the link")

    # Automation Config
    webhook_url: HttpUrl = Field(..., description = "Url of the webhook to send the data to")
    webhook_headers: Dict[str, str] = Field(default_factory=dict, description = "Headers to send with the request")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    # DocumentExtraction Config
    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])

    @computed_field   # type: ignore
    @property
    def schema_data_id(self) -> str:
        """Returns the SHA1 hash of the schema data, ignoring all prompt/description/default fields.
        
        Returns:
            str: A SHA1 hash string representing the schema data version.
        """
        return "sch_data_id_" + generate_sha_hash_from_string(
            json.dumps(
                clean_schema(copy.deepcopy(self.json_schema), remove_custom_fields=True, fields_to_remove=["description", "default", "title", "required", "examples", "deprecated", "readOnly", "writeOnly"]),
                sort_keys=True).strip(), 
            "sha1")

    # This is a computed field, it is exposed when serializing the object
    @computed_field   # type: ignore
    @property
    def schema_id(self) -> str:
        """Returns the SHA1 hash of the complete schema.
        
        Returns:
            str: A SHA1 hash string representing the complete schema version.
        """
        return "sch_id_" + generate_sha_hash_from_string(json.dumps(self.json_schema, sort_keys=True).strip(), "sha1")


    
class ListLinks(BaseModel):
    data: list[Link]
    list_metadata: ListMetadata
    
class CronSchedule(BaseModel):
    second: Optional[int] = Field(0, ge=0, le=59, description="Second (0-59), defaults to 0")
    minute: int = Field(..., ge=0, le=59, description="Minute (0-59)")
    hour: int = Field(..., ge=0, le=23, description="Hour (0-23)")
    day_of_month: Optional[int] = Field(None, ge=1, le=31, description="Day of the month (1-31), None means any day")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month (1-12), None means every month")
    day_of_week: Optional[int] = Field(None, ge=0, le=6, description="Day of the week (0-6, Sunday = 0), None means any day")

    def to_cron_string(self) -> str:
        return f"{self.second or '*'} {self.minute} {self.hour} " \
               f"{self.day_of_month or '*'} {self.month or '*'} {self.day_of_week or '*'}"


class ScrappingConfig(AutomationConfig):
    object: Literal['scrapping_cron'] = "scrapping_cron"
    id: str = Field(default_factory=lambda: "scrapping_" + str(uuid.uuid4()), description="Unique identifier for the scrapping job")
    
    # Scrapping Specific Config
    link: HttpUrl = Field(..., description="Link to be scrapped")
    schedule: CronSchedule


class OutlookConfig(BaseModel):
    object: Literal['outlook_plugin'] = "outlook_plugin"
    id: str = Field(default_factory=lambda: "outlook_" + str(uuid.uuid4()), description="Unique identifier for the outlook account")
    
    authorized_domains: list[str] = Field(default_factory=list, description = "List of authorized domains to connect to the plugin from")
    authorized_emails: List[EmailStr] = Field(default_factory=list, description = "List of emails to connect to the plugin from")

    # Automation Config
    webhook_url: HttpUrl = Field(..., description = "Url of the webhook to send the data to")
    webhook_headers: Dict[str, str] = Field(default_factory=dict, description = "Headers to send with the request")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    # DocumentExtraction Config
    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])




class ExtractionEndpointConfig(BaseModel):
    object: Literal['endpoint'] = "endpoint"
    id: str = Field(default_factory=lambda: "endp" + str(uuid.uuid4()), description="Unique identifier for the extraction endpoint")
    
    # Extraction Endpoint Specific Config
    name: str = Field(..., description="Name of the extraction endpoint")

    # Automation Config
    webhook_url: HttpUrl = Field(..., description = "Url of the webhook to send the data to")
    webhook_headers: Dict[str, str] = Field(default_factory=dict, description = "Headers to send with the request")
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    # DocumentExtraction Config
    modality: Modality
    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    model: str = Field(..., description="Model used for chat completion")
    json_schema: dict[str, Any] = Field(..., description="JSON schema format used to validate the output data.")
    temperature: float = Field(default=0.0, description="Temperature for sampling. If not provided, the default temperature for the model will be used.", examples=[0.0])


# ------------------------------
# ------------------------------
# ------------------------------


class ExternalRequestLog(BaseModel):
    webhook_url: Optional[HttpUrl]
    request_body: dict[str, Any]
    request_headers: dict[str, str]
    request_at: datetime.datetime

    response_body: dict[str, Any]
    response_headers: dict[str, str]
    response_at: datetime.datetime

    status_code: int
    error: Optional[str] = None
    duration_ms: float

class InternalLog(BaseModel):
    automation_snapshot:  Optional[Mailbox| Link| ScrappingConfig| ExtractionEndpointConfig]
    file_metadata: BaseMIMEData
    extraction: Optional[DocumentExtractResponse]

    @computed_field # type: ignore
    @property
    def api_cost(self) -> Optional[Amount]:
        if self.extraction and self.extraction.usage:
            try: 
                cost = compute_cost_from_model(self.extraction.model, self.extraction.usage)
                return cost
            except Exception as e:
                print(f"Error computing cost: {e}")
                return None
        return None

class AutomationLog(BaseModel):
    object: Literal['automation_log'] = "automation_log"
    id: str = Field(default_factory=lambda: "log_auto_" + str(uuid.uuid4()), description="Unique identifier for the automation log")
    user_email: Optional[EmailStr] # When the user is logged or when he forwards an email
    organization_id:str
    internal_log: InternalLog
    external_request_log: ExternalRequestLog
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))


class OpenAIRequestConfig(BaseModel):
    model: str
    temperature: float
    json_schema: dict[str, Any]

class OpenAILog(BaseModel): 
    request_config: OpenAIRequestConfig
    extraction: Optional[DocumentExtractResponse]



class ListLinkLogs(BaseModel):
    data: List[AutomationLog]
    list_metadata: ListMetadata

# ------------------------------
# ------------------------------
# ------------------------------

class UpdateMailboxRequest(BaseModel):

    authorized_domains: Optional[list[str]] = None
    authorized_emails: Optional[List[EmailStr]] = None

    # ------------------------------
    # HTTP Config
    # ------------------------------
    webhook_url: Optional[HttpUrl] = None
    webhook_headers: Optional[Dict[str, str]] = None

    # ------------------------------
    # DocumentExtraction Parameters
    # ------------------------------
    # DocumentProcessing Parameters
    image_settings: Optional[ImageSettings] = None
    modality: Optional[Modality] = None
    # Others DocumentExtraction Parameters
    model: Optional[str] = None
    temperature: Optional[float] = None
    json_schema: Optional[Dict] = None

    @field_validator("authorized_emails", mode="before")
    def normalize_authorized_emails(cls, emails: List[str]) -> List[str]:
        return [email.strip().lower() for email in emails]

   

class UpdateLinkRequest(BaseModel):
    id: str

    # ------------------------------
    # Link Config
    # ------------------------------
    name: Optional[str] = None
    password: Optional[str] = None

    # ------------------------------
    # HTTP Config
    # ------------------------------
    webhook_url: Optional[HttpUrl] = None
    webhook_headers: Optional[Dict[str, str]] = None

    # ------------------------------
    # DocumentExtraction Parameters
    # ------------------------------
    # DocumentProcessing Parameters
    image_settings: Optional[ImageSettings] = None
    modality: Optional[Modality] = None
    # Others DocumentExtraction Parameters
    model: Optional[str] = None
    temperature: Optional[float] = None
    json_schema: Optional[Dict] = None

