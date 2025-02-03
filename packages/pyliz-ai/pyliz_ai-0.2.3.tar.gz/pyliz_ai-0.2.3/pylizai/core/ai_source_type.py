from enum import Enum

from pylizai.model.ai_model_list import AiModelList


class AiSourceType(Enum):
    OLLAMA_SERVER = "Ollama server"
    LMSTUDIO_SERVER = "LMM studio server"
    LOCAL_LLAMACPP = "Local (Llamacpp)"
    LOCAL_WHISPER = "Local (Whisper)"
    API_MISTRAL = "Mistral API"
    API_GEMINI = "Gemini API"


