from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from .filled_data_from_frontend import FilledRecipientParameter
from .raw_meta_template import WhatsappTemplate
from .required_for_frontend_templates import RequiredTemplateParameter
from enum import StrEnum

class RecipientStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    
class RecipientOfTemplateCampaign(BaseModel):
    phone_number: str
    new_contact_name: Optional[str] = None
    parameters: List[FilledRecipientParameter] = Field(default_factory=list)
    status: RecipientStatus = Field(default=RecipientStatus.PENDING)
    details: Optional[str] = None
    message_id: Optional[str] = None
    
    @model_validator(mode="after")
    def validate_new_contact_name(self) -> RecipientOfTemplateCampaign:
        if self.new_contact_name is None:
            self.new_contact_name = self.phone_number
        return self

    @classmethod
    def example_recipient(cls, whatsapp_template : WhatsappTemplate) -> RecipientOfTemplateCampaign:
        required_parameters = RequiredTemplateParameter.from_whatsapp_template(whatsapp_template)
        return cls(phone_number="5491166317681", new_contact_name="Axel Example", parameters=[FilledRecipientParameter(id=parameter.id, text=parameter.example) for parameter in required_parameters])
    
    @property
    def is_example_recipient(self) -> bool:
        return self.new_contact_name == "Axel Example"
    
    def to_row(self, just_columns_and_example) -> dict:
        parameters = {}
        for parameter in self.parameters:
            parameters[parameter.id] = parameter.text
        parameters["phone_number"] = self.phone_number
        parameters["new_contact_name"] = self.new_contact_name
        if not just_columns_and_example:
            parameters["status"] = self.status
            parameters["details"] = self.details
            parameters["message_id"] = self.message_id
        return parameters
