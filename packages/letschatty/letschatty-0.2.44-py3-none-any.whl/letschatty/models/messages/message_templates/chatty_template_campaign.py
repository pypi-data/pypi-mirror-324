from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from ...base_models.chatty_asset_model import ChattyAssetModel
from ...utils.types.identifier import StrObjectId
from ...utils.definitions import Area
from ...utils.types.serializer_type import SerializerType
from .recipient_of_template_campaign import RecipientOfTemplateCampaign
from bson import ObjectId
from zoneinfo import ZoneInfo
import logging
from enum import StrEnum
logger = logging.getLogger(__name__)

class CampaignStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"
    ERROR = "ERROR"

class TemplateCampaign(ChattyAssetModel):
    template_name: str
    name: str
    area: Area
    agent_email: str
    recipients: Optional[List[RecipientOfTemplateCampaign]] = None
    assign_to_agent: Optional[str] = None
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    description: Optional[str] = None
    forced_send: bool = Field(default=False)
    date: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    q_recipients: Optional[int] = None
    q_processed_recipients: Optional[int] = None
    q_recipients_succesfully_sent: Optional[int] = None
    status: CampaignStatus = Field(default=CampaignStatus.PENDING)
    progress: float = 0.0
    observations: Optional[str] = None
    
    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"recipients", "tags", "products", "flow", "agent_email", "assign_to_agent", "description", "forced_send", "date"}
    }

    class ConfigDict:
        arbitrary_types_allowed = True

    @field_validator('recipients')
    def validate_recipients(cls, v):
        if len(v) == 0:
            raise ValueError("No recipients specified")
        return v

    @field_validator('q_recipients')
    def set_q_recipients(cls, v, values):
        if v is None:
            return len(values.data.get('recipients', []))
        return v

    @model_validator(mode="after")
    def check_status(self):
        if self.status == CampaignStatus.PENDING:
            pass
        elif self.status == CampaignStatus.PROCESSING and self.q_processed_recipients == self.q_recipients:
            self.status = CampaignStatus.COMPLETED
        elif self.status == CampaignStatus.PROCESSING and self.q_processed_recipients < self.q_recipients:
            self.status = CampaignStatus.INCOMPLETE
        return self

    def pause(self):
        if self.status in [CampaignStatus.PROCESSING, CampaignStatus.PENDING]:
            self.status = CampaignStatus.PAUSED
        else:
            raise ValueError(f"Campaign {self.name} can't be paused because its status is {self.status}")

    def is_processing(self) -> bool:
        return self.status == CampaignStatus.PROCESSING
    
    def start_processing(self):
        if self.status == CampaignStatus.PENDING or self.status == CampaignStatus.PAUSED or self.status == CampaignStatus.INCOMPLETE:
            self.status = CampaignStatus.PROCESSING
        else: 
            raise ValueError(f"Campaign {self.name} can't be started because its status is {self.status}")

    def finish(self):
        if self.status != CampaignStatus.PROCESSING:
            raise ValueError(f"Campaign {self.name} can't be finished because its status is {self.status}")
        
        self.status = CampaignStatus.COMPLETED if self.q_recipients == self.q_processed_recipients else CampaignStatus.INCOMPLETE

    def error(self, observations: Optional[str] = None):
        self.status = CampaignStatus.ERROR
        self.observations = observations