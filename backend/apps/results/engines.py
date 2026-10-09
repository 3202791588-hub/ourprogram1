from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib
from django.conf import settings
from .models import PersonalityTemplate

@dataclass(frozen=True)
class ScoreOutput:
    result_type: str
    scores: dict
    payload: dict
    template_version: str

class ScoringEngine(ABC):
    @abstractmethod
    def calculate(self, session) -> ScoreOutput: ...

class MockScoringEngine(ScoringEngine):
    """MOCK ONLY. NOT SCIENTIFIC. Stable answer hash for UI development."""
    def calculate(self, session) -> ScoreOutput:
        option_ids=list(session.answers.order_by("question__sequence").values_list("option_id",flat=True))
        digest=hashlib.sha256(",".join(map(str,option_ids)).encode()).digest()
        templates=list(PersonalityTemplate.objects.filter(active=True).order_by("key"))
        if not templates: raise RuntimeError("Run seed_demo before scoring")
        template=templates[int.from_bytes(digest[:4],"big") % len(templates)]
        scores={"social_energy":30+digest[4]%61,"sensitivity":30+digest[5]%61,"exploration":30+digest[6]%61}
        return ScoreOutput(template.key,scores,template.payload,template.version)

def get_scoring_engine() -> ScoringEngine:
    if settings.SCORING_ENGINE == "mock": return MockScoringEngine()
    raise RuntimeError(f"Unknown scoring engine: {settings.SCORING_ENGINE}")
