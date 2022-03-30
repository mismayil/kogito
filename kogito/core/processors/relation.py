from abc import ABC, abstractmethod
from typing import List, Tuple

import numpy as np
import torch
import spacy
from torch import nn
import pytorch_lightning as pl
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence

from kogito.core.head import KnowledgeHead
from kogito.core.relation import HEAD_TO_RELATION_MAP, PHYSICAL_RELATIONS, EVENT_RELATIONS, SOCIAL_RELATIONS

RELATION_CLASSES = [PHYSICAL_RELATIONS, EVENT_RELATIONS, SOCIAL_RELATIONS]


class MaxPool(nn.Module):
    def forward(self, X):
        values, _ = torch.max(X, dim=1)
        return values


class AvgPool(nn.Module):
    def forward(self, X):
        return torch.mean(X, dim=1)


class SWEMRelationClassifier(pl.LightningModule):
    def __init__(self, num_classes=3, pooling="max"):
        super().__init__()
        self.embedding = nn.Embedding(num_embeddings=400002, embedding_dim=100)
        self.pool = MaxPool() if pooling == "max" else AvgPool()
        self.linear = nn.Linear(100, num_classes)
        self.model = nn.Sequential(self.embedding, self.pool, self.linear)
    
    def forward(self, X):
        outputs = self.model(X)
        probs = F.sigmoid(outputs)
        return probs


class KnowledgeRelationMatcher(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def match(
        self, heads: List[KnowledgeHead], relations: List[str] = None
    ) -> List[Tuple[KnowledgeHead, str]]:
        raise NotImplementedError


class SimpleRelationMatcher(KnowledgeRelationMatcher):
    def match(
        self, heads: List[KnowledgeHead], relations: List[str] = None
    ) -> List[Tuple[KnowledgeHead, str]]:
        head_relations = []

        for head in heads:
            rels_to_match = HEAD_TO_RELATION_MAP[head.type]
            if relations:
                rels_to_match = set(HEAD_TO_RELATION_MAP[head.type]).intersection(
                    set(relations)
                )
            for relation in rels_to_match:
                head_relations.append((head, relation))

        return head_relations


class SWEMRelationMatcher(KnowledgeRelationMatcher):
    def match(
        self, heads: List[KnowledgeHead], relations: List[str] = None
    ) -> List[Tuple[KnowledgeHead, str]]:
        nlp = spacy.load("en_core_web_sm")
        vocab = np.load("./relation_modeling/data/vocab_glove_100d.npy", allow_pickle=True).item()
        head_inputs = pad_sequence([torch.tensor([vocab.get(token.text, 1) for token in nlp(head.text)], dtype=torch.int) for head in heads],
                                    batch_first=True)
        model = SWEMRelationClassifier()
        model.load_state_dict(torch.load('./relation_modeling/models/swem_multi_label_finetune_state_dict.pth'))
        probs = model.forward(head_inputs).detach().numpy()
        predictions = np.where(probs >= 0.5, 1, 0).tolist()
        head_relations = []

        for head, prediction in zip(heads, predictions):
            pred_rel_classes = [RELATION_CLASSES[idx] for idx, pred in enumerate(prediction) if pred == 1]
            if pred_rel_classes:
                for rel_class in pred_rel_classes:
                    rels_to_match = rel_class
                    if relations:
                        rels_to_match = set(rels_to_match).intersection(set(relations))
                    for relation in rels_to_match:
                        head_relations.append((head, relation))

        return head_relations