"""Hybrid AI stylist model.

This module provides a small abstraction that combines a rules based stylist with
an optional Large Language Model (LLM).  The goal is to give the rest of the
application a single entry point for generating outfit recommendations.  When an
LLM client is available (for example an OpenAI compatible client) we assemble a
structured prompt and request detailed recommendations.  If the LLM call fails
or is not configured the module falls back to deterministic heuristics so the
feature still works in development and automated tests.

The implementation purposely avoids importing any specific vendor SDK at module
import time.  This keeps the backend light-weight and lets deployments decide if
they want to ship an actual LLM integration or just the local rules engine.
"""

from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Protocol


class LLMClient(Protocol):
    """Protocol for the minimal functionality we need from an LLM client."""

    def complete(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - protocol
        """Return a text completion for *prompt*."""

    async def acomplete(self, prompt: str, **kwargs: Any) -> str:  # pragma: no cover - protocol
        """Asynchronous variant of :meth:`complete`."""


@dataclass(slots=True)
class UserProfile:
    """Normalized representation of the answers collected from the quiz."""

    age: Optional[int] = None
    height_ft: Optional[int] = None
    height_in: Optional[int] = None
    body_type: Optional[str] = None
    gender: Optional[str] = None


@dataclass(slots=True)
class UserPreferences:
    """Holds soft constraints expressed by the user."""

    colors: List[str] = field(default_factory=list)
    occasion: Optional[str] = None
    disliked_items: List[str] = field(default_factory=list)
    budget: Optional[str] = None  # e.g. "<$100", "premium"


@dataclass(slots=True)
class WardrobeItem:
    """Small helper describing what the user already owns."""

    name: str
    category: str
    dominant_color: Optional[str] = None


@dataclass(slots=True)
class Recommendation:
    """Structure returned by the hybrid model."""

    title: str
    summary: str
    items: List[str] = field(default_factory=list)
    accessories: List[str] = field(default_factory=list)


_BODY_TYPE_RULES: Dict[str, List[str]] = {
    "athletic": ["slim fit jeans", "fitted tees", "structured jackets"],
    "curvy": ["high-rise trousers", "wrap dresses", "tailored blazers"],
    "petite": ["cropped jackets", "ankle pants", "monochrome outfits"],
    "tall": ["wide-leg trousers", "layered knits", "longline coats"],
}

_OCCASION_RULES: Dict[str, List[str]] = {
    "work": ["tailored blazer", "button-up shirt", "sleek loafers"],
    "casual": ["straight denim", "relaxed tee", "clean sneakers"],
    "date": ["silk blouse", "dark denim", "ankle boots"],
    "party": ["statement top", "black jeans", "chelsea boots"],
}


class HybridStylistModel:
    """Combine deterministic rules with optional LLM reasoning."""

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        *,
        style_rules: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self._llm = llm_client
        self._body_rules = style_rules or _BODY_TYPE_RULES

    # ------------------------------------------------------------------
    # Public factory helpers
    # ------------------------------------------------------------------
    @classmethod
    def from_env(cls) -> "HybridStylistModel":
        """Instantiate the model using environment variables.

        If ``AI_PROVIDER`` is set to ``openai`` and the ``OPENAI_API_KEY``
        variable exists we lazily create an OpenAI client using the official
        SDK.  Missing configuration results in a purely rules-based model.
        """

        provider = (os.getenv("AI_PROVIDER") or "").lower()
        llm: Optional[LLMClient] = None

        if provider == "openai" and os.getenv("OPENAI_API_KEY"):
            llm = _create_openai_client()

        return cls(llm)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------
    def generate(
        self,
        profile: UserProfile,
        preferences: Optional[UserPreferences] = None,
        wardrobe: Optional[Iterable[WardrobeItem]] = None,
        *,
        max_outfits: int = 3,
    ) -> Dict[str, Any]:
        """Return structured outfit recommendations.

        The response is always JSON serialisable.  When the LLM returns a JSON
        payload it is used directly.  Otherwise the local rule engine is used as
        a fallback.
        """

        prompt = self._build_prompt(profile, preferences, wardrobe, max_outfits)
        if self._llm is None:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)

        try:
            raw = self._llm.complete(prompt)
        except Exception:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)

        parsed = self._safe_json_loads(raw)
        if parsed is None:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)
        return parsed

    async def agenerate(
        self,
        profile: UserProfile,
        preferences: Optional[UserPreferences] = None,
        wardrobe: Optional[Iterable[WardrobeItem]] = None,
        *,
        max_outfits: int = 3,
    ) -> Dict[str, Any]:
        """Asynchronous wrapper mirroring :meth:`generate`."""

        if self._llm is None:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)

        prompt = self._build_prompt(profile, preferences, wardrobe, max_outfits)
        try:
            raw = await self._llm.acomplete(prompt)
        except Exception:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)

        parsed = self._safe_json_loads(raw)
        if parsed is None:
            return self._rule_based_response(profile, preferences, wardrobe, max_outfits)
        return parsed

    # ------------------------------------------------------------------
    # Prompt building / parsing helpers
    # ------------------------------------------------------------------
    def _build_prompt(
        self,
        profile: UserProfile,
        preferences: Optional[UserPreferences],
        wardrobe: Optional[Iterable[WardrobeItem]],
        max_outfits: int,
    ) -> str:
        wardrobe_payload = [item.__dict__ for item in wardrobe or []]
        prompt_data = {
            "instruction": (
                "You are Dressly, an expert fashion stylist. "
                "Return JSON with a `summary` string and an `outfits` array. "
                "Each outfit must include `title`, `summary`, `items`, and optional `accessories`."
            ),
            "profile": profile.__dict__,
            "preferences": preferences.__dict__ if preferences else None,
            "wardrobe": wardrobe_payload,
            "max_outfits": max_outfits,
        }
        return json.dumps(prompt_data, indent=2)

    @staticmethod
    def _safe_json_loads(raw: str) -> Optional[Dict[str, Any]]:
        raw = raw.strip()
        if not raw:
            return None
        if raw[0] != "{" and "{" in raw:
            raw = raw[raw.index("{") :]
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    # ------------------------------------------------------------------
    # Fallback rule engine
    # ------------------------------------------------------------------
    def _rule_based_response(
        self,
        profile: UserProfile,
        preferences: Optional[UserPreferences],
        wardrobe: Optional[Iterable[WardrobeItem]],
        max_outfits: int,
    ) -> Dict[str, Any]:
        body_items = self._body_rules.get((profile.body_type or "").lower(), [])
        occasion_items: List[str] = []
        if preferences and preferences.occasion:
            occasion_items = _OCCASION_RULES.get(preferences.occasion.lower(), [])

        base_palette = (preferences.colors if preferences else []) or ["navy", "white", "black"]
        wardrobe_items = [item.name for item in wardrobe or []]

        outfits: List[Dict[str, Any]] = []
        for idx in range(max_outfits):
            item_selection = list(dict.fromkeys(body_items + occasion_items))
            if not item_selection:
                item_selection = ["tailored trousers", "versatile knit", "layering jacket"]

            accent_color = base_palette[idx % len(base_palette)] if base_palette else "black"
            summary = (
                "Blends Dressly's core rules for "
                f"{profile.body_type or 'balanced'} body types with {accent_color} accents."
            )

            accessories = [f"{accent_color} belt", "minimal watch", "textured bag"]
            if preferences and preferences.disliked_items:
                accessories = [a for a in accessories if all(d not in a for d in preferences.disliked_items)]

            outfits.append(
                {
                    "title": f"Outfit {idx + 1}",
                    "summary": summary,
                    "items": item_selection,
                    "accessories": accessories,
                    "reuse_from_wardrobe": [item for item in wardrobe_items if item in item_selection],
                }
            )

        return {
            "summary": (
                "Generated using Dressly's rules engine. "
                "Configure AI_PROVIDER=openai to enable LLM powered suggestions."
            ),
            "outfits": outfits,
        }


def _create_openai_client() -> LLMClient:
    """Create an OpenAI compatible client at runtime.

    Importing the SDK lazily keeps the dependency optional.  The returned object
    exposes ``complete``/``acomplete`` adapters that map to the Responses API.
    """

    openai_module = importlib.import_module("openai")
    client_class = getattr(openai_module, "OpenAI")
    api_key = os.environ["OPENAI_API_KEY"]
    client = client_class(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    class _ClientAdapter:
        def __init__(self) -> None:
            self._client = client

        def complete(self, prompt: str, **_: Any) -> str:
            response = self._client.responses.create(
                model=model,
                input=prompt,
                response_format={"type": "json_object"},
            )
            return response.output_text

        async def acomplete(self, prompt: str, **_: Any) -> str:
            response = await self._client.responses.create_async(
                model=model,
                input=prompt,
                response_format={"type": "json_object"},
            )
            return response.output_text

    return _ClientAdapter()


__all__ = [
    "HybridStylistModel",
    "LLMClient",
    "Recommendation",
    "UserPreferences",
    "UserProfile",
    "WardrobeItem",
]

