from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

LangCodeDescription = {
  'es': 'Spanish',
  'en': 'English',
  'it': 'Italian',
  'pt': 'Portuguese',
  'fr': 'French',
}

class CharacterCardData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    first_mes: Optional[str] = None
    creator_notes: Optional[str] = None
    mes_example: Optional[str] = None
    alternate_greetings: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    post_history_instructions: Optional[str] = None
    character_version: Optional[str] = None
    appearance: Optional[str] = None



class CharacterCardDC(BaseModel):
    spec: str = Field(default='chara_card_v2')
    spec_version: str = Field(default='2_v_dc')
    data: CharacterCardData



class Assets(BaseModel):
    image: Any



class TTS(BaseModel):
    voice: str
    secondaryVoice: str
    speed: str
    speedRate: float



class MetaApp(BaseModel):
    isPublished: bool
    isPublic: Any
    authorId: str
    authorEmail: str
    createdAt: datetime
    updatedAt: datetime
    takenCount: int



class IConversationCard(BaseModel):
    version: str
    _id: str
    id: str
    title: str
    assets: Assets
    characterCard: CharacterCardDC
    textEngine: str
    conversationType: str
    lang: str
    tts: TTS
    metaApp: MetaApp



class TranslationRequest(BaseModel):
    idCard: str
    currentLang: str
    targetLang: str


class ChatRole(str, Enum):
    Assistant = "assistant",
    System = "system",
    User = "user",


class LLMProvider(str, Enum):
    OpenAI = "openai",
    Groq = "groq",
    Anthropic = "anthropic",
    Google = "google",
    OpenRouter = "openrouter",


class ChatMessage(BaseModel):
    role: ChatRole
    content: str

class ConversationMessagesDTO(BaseModel):
    messages: Optional[List[ChatMessage]] = None
    modelName: Optional[str] = None
    provider: Optional[str] = None
    type: Optional[str] = None

    class Config:
        extra = "allow"

class ChatResponseDTO(BaseModel):
    role: ChatRole
    content: str
    metadata: dict


class ListModelsResponse(BaseModel):
    name: str
    id: str

    class Config:
        extra = "allow"
    

