import logging

from emma.embedding.embedding_model_metadata_handler import (
    EmbeddingModelMetadataHandler,
)
# from emma.embedding.esm3 import Esm3
from emma.embedding.t5 import T5
from emma.embedding.esm_fair import EsmFair
from emma.embedding.ankh_models import Ankh


def select_embedding_handler(
    model_id: str, logger: logging.Logger, no_gpu: bool = False
):
    """
    Factory function to select the appropriate embedding handler
    based on model name.

    Args:
        model_id (str): Name of the embedding model to be used.

    Returns:
        EmbeddingHandler: An instance of the appropriate embedding
            handler class.
    """
    model_metadata = EmbeddingModelMetadataHandler()
    model_metadata.validate_model_id(model_id)
    model_handler = model_metadata.get_model_handler_per_model_id(model_id)
    if model_handler == "T5":
        return T5(logger=logger, no_gpu=no_gpu)
    elif model_handler == "EsmFair":
        return EsmFair(logger=logger, no_gpu=no_gpu)
    elif model_handler == "Ankh":
        return Ankh(logger = logger, no_gpu=no_gpu)
    # elif model_handler == "Esm3":
    #     return Esm3(logger=logger, no_gpu=no_gpu)
