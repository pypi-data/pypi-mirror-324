from typing import List, Optional

from pydantic import BaseModel, model_validator


# Action Input Models
class SearchGoogleAction(BaseModel):
    query: str


class GoToUrlAction(BaseModel):
    url: str


class ClickElementAction(BaseModel):
    index: int


class InputTextAction(BaseModel):
    index: int
    text: str


class DoneAction(BaseModel):
    text: str


class SwitchTabAction(BaseModel):
    page_id: int


class OpenTabAction(BaseModel):
    url: str


class GetPageContentAction(BaseModel):
    include_links: bool


class ScrollAction(BaseModel):
    amount: Optional[int] = None  # The number of pixels to scroll. If None, scroll down/up one page


class SendKeysAction(BaseModel):
    keys: str


class ScrollToTextAction(BaseModel):
    text: str


class GetDropdownOptionsAction(BaseModel):
    index: int


class SelectDropdownOptionAction(BaseModel):
    index: int
    text: str


class UploadFilesAction(BaseModel):
    index: int
    file_names: List[str]


class NoParamsAction(BaseModel):
    """
    Accepts absolutely anything in the incoming data
    and discards it, so the final parsed model is empty.
    """

    @model_validator(mode='before')
    def ignore_all_inputs(cls, values):
        # No matter what the user sends, discard it and return empty.
        return {}

    class Config:
        # If you want to silently allow unknown fields at top-level,
        # set extra = 'allow' as well:
        extra = 'allow'
