from __future__ import annotations

import json
import logging
import os

import torch
from torch import Tensor, nn

logger = logging.getLogger(__name__)


class WordWeights(nn.Module):
    """This model can weight word embeddings, for example, with idf-values."""

    def __init__(self, vocab: list[str], word_weights: dict[str, float], unknown_word_weight: float = 1):
        """
        Initializes the WordWeights class.

        Args:
            vocab (List[str]): Vocabulary of the tokenizer.
            word_weights (Dict[str, float]): Mapping of tokens to a float weight value. Word embeddings are multiplied
                by this float value. Tokens in word_weights must not be equal to the vocab (can contain more or less values).
            unknown_word_weight (float, optional): Weight for words in vocab that do not appear in the word_weights lookup.
                These can be, for example, rare words in the vocab where no weight exists. Defaults to 1.
        """
        super().__init__()
        self.config_keys = ["vocab", "word_weights", "unknown_word_weight"]
        self.vocab = vocab
        self.word_weights = word_weights
        self.unknown_word_weight = unknown_word_weight

        weights = []
        num_unknown_words = 0
        for word in vocab:
            weight = unknown_word_weight
            if word in word_weights:
                weight = word_weights[word]
            elif word.lower() in word_weights:
                weight = word_weights[word.lower()]
            else:
                num_unknown_words += 1
            weights.append(weight)

        logger.info(
            f"{num_unknown_words} of {len(vocab)} words without a weighting value. Set weight to {unknown_word_weight}"
        )

        self.emb_layer = nn.Embedding(len(vocab), 1)
        self.emb_layer.load_state_dict({"weight": torch.FloatTensor(weights).unsqueeze(1)})

    def forward(self, features: dict[str, Tensor]):
        attention_mask = features["attention_mask"]
        token_embeddings = features["token_embeddings"]

        # Compute a weight value for each token
        token_weights_raw = self.emb_layer(features["input_ids"]).squeeze(-1)
        token_weights = token_weights_raw * attention_mask.float()
        token_weights_sum = torch.sum(token_weights, 1)

        # Multiply embedding by token weight value
        token_weights_expanded = token_weights.unsqueeze(-1).expand(token_embeddings.size())
        token_embeddings = token_embeddings * token_weights_expanded

        features.update({"token_embeddings": token_embeddings, "token_weights_sum": token_weights_sum})
        return features

    def get_config_dict(self):
        return {key: self.__dict__[key] for key in self.config_keys}

    def save(self, output_path):
        with open(os.path.join(output_path, "config.json"), "w") as fOut:
            json.dump(self.get_config_dict(), fOut, indent=2)

    @staticmethod
    def load(input_path):
        with open(os.path.join(input_path, "config.json")) as fIn:
            config = json.load(fIn)

        return WordWeights(**config)
