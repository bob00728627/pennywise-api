from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Serializes as camelCase so payloads match the React frontend."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)
