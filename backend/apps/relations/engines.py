from abc import ABC, abstractmethod
from dataclasses import dataclass
import hashlib
from django.conf import settings
from .models import RelationTemplate

@dataclass(frozen=True)
class RelationOutput:
    relation_type: str; score: int; scores: dict; payload: dict; version: str
class RelationEngine(ABC):
    @abstractmethod
    def calculate(self,result_a,result_b)->RelationOutput: ...
class MockRelationEngine(RelationEngine):
    """MOCK ONLY. NOT SCIENTIFIC. Symmetric, deterministic relation mapping."""
    def calculate(self,result_a,result_b)->RelationOutput:
        pair="|".join(sorted([result_a.result_type,result_b.result_type])); digest=hashlib.sha256(pair.encode()).digest()
        templates=list(RelationTemplate.objects.filter(active=True).order_by("key"))
        if not templates: raise RuntimeError("Run seed_demo before relation generation")
        t=templates[int.from_bytes(digest[:4],"big")%len(templates)]
        score=65+digest[4]%31
        scores={"emotion":65+digest[5]%31,"communication":65+digest[6]%31,"pace":65+digest[7]%31,"exploration":65+digest[8]%31}
        return RelationOutput(t.key,score,scores,t.payload,t.version)
def get_relation_engine()->RelationEngine:
    if settings.RELATION_ENGINE=="mock": return MockRelationEngine()
    raise RuntimeError(f"Unknown relation engine: {settings.RELATION_ENGINE}")
