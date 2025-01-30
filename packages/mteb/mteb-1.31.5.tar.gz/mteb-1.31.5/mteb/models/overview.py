from __future__ import annotations

import logging
from collections.abc import Iterable
from functools import lru_cache
from typing import Any

from huggingface_hub import ModelCard
from sentence_transformers import SentenceTransformer

from mteb.abstasks.AbsTask import AbsTask
from mteb.encoder_interface import Encoder
from mteb.model_meta import ModelMeta
from mteb.models import (
    arctic_models,
    bedrock_models,
    bge_models,
    bm25,
    cde_models,
    cohere_models,
    colbert_models,
    e5_instruct,
    e5_models,
    gme_models,
    google_models,
    gritlm_models,
    gte_models,
    ibm_granite_models,
    inf_models,
    jasper_models,
    jina_models,
    lens_models,
    linq_models,
    llm2vec_models,
    misc_models,
    model2vec_models,
    moka_models,
    mxbai_models,
    no_instruct_sentence_models,
    nomic_models,
    nvidia_models,
    openai_models,
    piccolo_models,
    promptriever_models,
    repllama_models,
    rerankers_custom,
    rerankers_monot5_based,
    ru_sentence_models,
    salesforce_models,
    sentence_transformers_models,
    stella_models,
    text2vec_models,
    uae_models,
    voyage_models,
)

logger = logging.getLogger(__name__)

model_modules = [
    arctic_models,
    bge_models,
    bm25,
    cde_models,
    cohere_models,
    colbert_models,
    e5_instruct,
    e5_models,
    google_models,
    google_models,
    gritlm_models,
    gte_models,
    gme_models,
    ibm_granite_models,
    inf_models,
    jina_models,
    lens_models,
    linq_models,
    llm2vec_models,
    mxbai_models,
    model2vec_models,
    moka_models,
    misc_models,
    nomic_models,
    no_instruct_sentence_models,
    nvidia_models,
    openai_models,
    piccolo_models,
    promptriever_models,
    repllama_models,
    rerankers_custom,
    rerankers_monot5_based,
    ru_sentence_models,
    salesforce_models,
    sentence_transformers_models,
    voyage_models,
    google_models,
    repllama_models,
    promptriever_models,
    jina_models,
    jasper_models,
    uae_models,
    text2vec_models,
    stella_models,
    bedrock_models,
    uae_models,
    voyage_models,
]
MODEL_REGISTRY = {}

for module in model_modules:
    for mdl in vars(module).values():
        if isinstance(mdl, ModelMeta):
            MODEL_REGISTRY[mdl.name] = mdl


def get_model_metas(
    model_names: Iterable[str] | None = None,
    languages: Iterable[str] | None = None,
    open_weights: bool | None = None,
    frameworks: Iterable[str] | None = None,
    n_parameters_range: tuple[int | None, int | None] = (None, None),
    use_instructions: bool | None = None,
    zero_shot_on: list[AbsTask] | None = None,
) -> list[ModelMeta]:
    """Load all models' metadata that fit the specified criteria."""
    res = []
    model_names = set(model_names) if model_names is not None else None
    languages = set(languages) if languages is not None else None
    frameworks = set(frameworks) if frameworks is not None else None
    for model_meta in MODEL_REGISTRY.values():
        if (model_names is not None) and (model_meta.name not in model_names):
            continue
        if languages is not None:
            if (model_meta.languages is None) or not (
                languages <= set(model_meta.languages)
            ):
                continue
        if (open_weights is not None) and (model_meta.open_weights != open_weights):
            continue
        if (frameworks is not None) and not (frameworks <= set(model_meta.framework)):
            continue
        if (use_instructions is not None) and (
            model_meta.use_instructions != use_instructions
        ):
            continue
        lower, upper = n_parameters_range
        n_parameters = model_meta.n_parameters
        if upper is not None:
            if (n_parameters is None) or (n_parameters > upper):
                continue
        if lower is not None:
            if (n_parameters is None) or (n_parameters < lower):
                continue
        if zero_shot_on is not None:
            if not model_meta.is_zero_shot_on(zero_shot_on):
                continue
        res.append(model_meta)
    return res


def get_model(model_name: str, revision: str | None = None, **kwargs: Any) -> Encoder:
    """A function to fetch a model object by name.

    Args:
        model_name: Name of the model to fetch
        revision: Revision of the model to fetch
        **kwargs: Additional keyword arguments to pass to the model loader

    Returns:
        A model object
    """
    meta = get_model_meta(model_name, revision)
    model = meta.load_model(**kwargs)

    # If revision not available in the modelmeta, try to extract it from sentence-transformers
    if meta.revision is None and isinstance(model, SentenceTransformer):
        _meta = model_meta_from_sentence_transformers(model)
        meta.revision = _meta.revision if _meta.revision else meta.revision

    model.mteb_model_meta = meta  # type: ignore
    return model


def get_model_meta(model_name: str, revision: str | None = None) -> ModelMeta:
    """A function to fetch a model metadata object by name.

    Args:
        model_name: Name of the model to fetch
        revision: Revision of the model to fetch

    Returns:
        A model metadata object
    """
    if model_name in MODEL_REGISTRY:
        if revision and (not MODEL_REGISTRY[model_name].revision == revision):
            raise ValueError(
                f"Model revision {revision} not found for model {model_name}. Expected {MODEL_REGISTRY[model_name].revision}."
            )
        return MODEL_REGISTRY[model_name]
    else:  # assume it is a sentence-transformers model
        logger.info(
            "Model not found in model registry, assuming it is on HF Hub model."
        )
        logger.info(
            f"Attempting to extract metadata by loading the model ({model_name}) using HuggingFace."
        )
        meta = model_meta_from_hf_hub(model_name)
        meta.revision = revision
        meta.name = model_name
    return meta


@lru_cache
def model_meta_from_hf_hub(model_name: str) -> ModelMeta:
    try:
        card = ModelCard.load(model_name)
        card_data = card.data.to_dict()
        frameworks = ["PyTorch"]
        if card_data.get("library_name", None) == "sentence-transformers":
            frameworks.append("Sentence Transformers")
        return ModelMeta(
            name=model_name,
            revision=card_data.get("base_model_revision", None),
            # TODO
            release_date=None,
            # TODO: We need a mapping between conflicting language codes
            languages=None,
            license=card_data.get("license", None),
            framework=frameworks,
            training_datasets=card_data.get("datasets", None),
            similarity_fn_name=None,
            n_parameters=None,
            max_tokens=None,
            embed_dim=None,
            open_weights=True,
            public_training_code=None,
            public_training_data=None,
            use_instructions=None,
        )
    except Exception as e:
        logger.warning(f"Failed to extract metadata from model: {e}.")
        return ModelMeta(
            name=model_name,
            revision=None,
            languages=None,
            release_date=None,
            n_parameters=None,
            max_tokens=None,
            embed_dim=None,
            license=None,
            open_weights=True,
            public_training_code=None,
            public_training_data=None,
            similarity_fn_name=None,
            use_instructions=None,
            training_datasets=None,
            framework=[],
        )


def model_meta_from_sentence_transformers(model: SentenceTransformer) -> ModelMeta:
    try:
        name = (
            model.model_card_data.model_name
            if model.model_card_data.model_name
            else model.model_card_data.base_model
        )
        languages = (
            [model.model_card_data.language]
            if isinstance(model.model_card_data.language, str)
            else model.model_card_data.language
        )
        meta = ModelMeta(
            name=name,
            revision=model.model_card_data.base_model_revision,
            release_date=None,
            languages=languages,
            framework=["Sentence Transformers"],
            similarity_fn_name=model.similarity_fn_name,
            n_parameters=None,
            max_tokens=None,
            embed_dim=None,
            license=None,
            open_weights=True,
            public_training_code=None,
            public_training_data=None,
            use_instructions=None,
            training_datasets=None,
        )
    except AttributeError as e:
        logger.warning(
            f"Failed to extract metadata from model: {e}. Upgrading to sentence-transformers v3.0.0 or above is recommended."
        )
        meta = ModelMeta(
            name=None,
            revision=None,
            languages=None,
            release_date=None,
            n_parameters=None,
            max_tokens=None,
            embed_dim=None,
            license=None,
            open_weights=True,
            public_training_code=None,
            public_training_data=None,
            similarity_fn_name=None,
            use_instructions=None,
            training_datasets=None,
            framework=[],
        )
    return meta
