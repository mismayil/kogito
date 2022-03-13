from kogito.core.head import KnowledgeHeadType


KG_RELATIONS = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "CausesDesire",
    "CreatedBy",
    "DefinedAs",
    "DesireOf",
    "Desires",
    "HasA",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPainCharacter",
    "HasPainIntensity",
    "HasPrerequisite",
    "HasProperty",
    "HasSubEvent",
    "HasSubevent",
    "HinderedBy",
    "InheritsFrom",
    "InstanceOf",
    "IsA",
    "LocatedNear",
    "LocationOfAction",
    "MadeOf",
    "MadeUpOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "NotHasA",
    "NotHasProperty",
    "NotIsA",
    "NotMadeOf",
    "ObjectUse",
    "PartOf",
    "ReceivesAction",
    "RelatedTo",
    "SymbolOf",
    "UsedFor",
    "isAfter",
    "isBefore",
    "isFilledBy",
    "oEffect",
    "oReact",
    "oWant",
    "xAttr",
    "xEffect",
    "xIntent",
    "xNeed",
    "xReact",
    "xReason",
    "xWant",
]

CONCEPTNET_RELATIONS = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "CausesDesire",
    "CreatedBy",
    "DefinedAs",
    "Desires",
    "HasA",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPrerequisite",
    "HasProperty",
    "HasSubevent",
    "InheritsFrom",
    "InstanceOf",
    "IsA",
    "MadeOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "NotHasA",
    "NotHasProperty",
    "NotIsA",
    "NotMadeOf",
    "PartOf",
    "ReceivesAction",
    "SymbolOf",
    "UsedFor",
]

ATOMIC_RELATIONS = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "Desires",
    "HasProperty",
    "HasSubEvent",
    "HinderedBy",
    "MadeUpOf",
    "NotDesires",
    "isAfter",
    "isBefore",
    "isFilledBy",
    "oEffect",
    "oReact",
    "oWant",
    "xAttr",
    "xEffect",
    "xIntent",
    "xNeed",
    "xReact",
    "xReason",
    "xWant",
    "ObjectUse",
]

SENTENCE_RELATIONS = [
    "Causes",
    "CausesDesire",
    "Desires",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPrerequisite",
    "HasSubEvent",
    "HasSubevent",
    "HinderedBy",
    "InheritsFrom",
    "InstanceOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "ReceivesAction",
    "SymbolOf",
    "isAfter",
    "isBefore",
    "isFilledBy",
    "oEffect",
    "oReact",
    "oWant",
    "xAttr",
    "xEffect",
    "xIntent",
    "xNeed",
    "xReact",
    "xReason",
    "xWant",
]

NOUN_PHRASE_RELATIONS = [
    "AtLocation",
    "CapableOf",
    "Causes",
    "CausesDesire",
    "CreatedBy",
    "DefinedAs",
    "Desires",
    "HasA",
    "HasFirstSubevent",
    "HasLastSubevent",
    "HasPrerequisite",
    "HasProperty",
    "HasSubEvent",
    "HasSubevent",
    "HinderedBy",
    "InheritsFrom",
    "InstanceOf",
    "IsA",
    "MadeOf",
    "MadeUpOf",
    "MotivatedByGoal",
    "NotCapableOf",
    "NotDesires",
    "NotHasA",
    "NotHasProperty",
    "NotIsA",
    "NotMadeOf",
    "ObjectUse",
    "PartOf",
    "ReceivesAction",
    "SymbolOf",
    "UsedFor",
    "isAfter",
    "isBefore",
    "isFilledBy",
]

VERB_PHRASE_RELATIONS = SENTENCE_RELATIONS


HEAD_TO_RELATION_MAP = {
    KnowledgeHeadType.SENTENCE: SENTENCE_RELATIONS,
    KnowledgeHeadType.NOUN_PHRASE: NOUN_PHRASE_RELATIONS,
    KnowledgeHeadType.VERB_PHRASE: VERB_PHRASE_RELATIONS
}
