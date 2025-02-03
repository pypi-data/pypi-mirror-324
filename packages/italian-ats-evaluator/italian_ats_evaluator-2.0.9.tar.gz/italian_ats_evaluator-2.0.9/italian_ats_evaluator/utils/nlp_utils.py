import re

import spacy
import pyphen
import pkgutil
from sentence_transformers import SentenceTransformer

DEFAULT_SPACY_MODEL = "it_core_news_lg"
DEFAULT_SENTENCE_TRANSFORMERS_MODEL = "intfloat/multilingual-e5-base"

dic = pyphen.Pyphen(lang='it')

difficult_connectives = [c for c in pkgutil.get_data('italian_ats_evaluator', 'resources/difficult_connectives.txt').decode('utf-8').replace('\r', '').split('\n')]
difficult_connectives = [c + "\\b" for c in difficult_connectives if (not c.endswith("*")) or (not c.endswith("]"))]
difficult_connectives = [c.replace("a\\w*", "(a|al|allo|alla|ai|agli|alle|all')\\b") for c in difficult_connectives]
difficult_connectives  = [c.replace("d\\w*", "(di|del|dello|dell'|della|dei|degli|delle|dal|dallo|dall'|dalla|dai|dagli|dalle')\\b") for c in difficult_connectives]

latinisms = [l for l in pkgutil.get_data('italian_ats_evaluator', 'resources/latinisms.txt').decode('utf-8').replace('\r', '').split('\n')]
latinisms = ["\\b" + l + "\\b" for l in latinisms]

italian_vdb_fo = {a for a in pkgutil.get_data('italian_ats_evaluator', 'resources/nvdb_FO.txt').decode('utf-8').replace('\r', '').split('\n')}
italian_vdb_au = {a for a in pkgutil.get_data('italian_ats_evaluator', 'resources/nvdb_AU.txt').decode('utf-8').replace('\r', '').split('\n')}
italian_vdb_ad = {a for a in pkgutil.get_data('italian_ats_evaluator', 'resources/nvdb_AD.txt').decode('utf-8').replace('\r', '').split('\n')}
italian_vdb = italian_vdb_fo.union(italian_vdb_au).union(italian_vdb_ad)


spacy_model = None
sentence_transformers_model = None


def get_spacy_model(model_name: str) -> spacy.language.Language:
    global spacy_model
    if spacy_model is None:
        try:
            spacy_model = spacy.load(model_name)
        except OSError:
            spacy.cli.download(model_name)
            spacy_model = spacy.load(model_name)
    return spacy_model


def get_sentence_transformers_model(model_name) -> SentenceTransformer:
    global sentence_transformers_model
    if sentence_transformers_model is None:
        sentence_transformers_model = SentenceTransformer(model_name)
    return sentence_transformers_model


def clean_text(text: str) -> str:
    text = text.strip()
    text = text.replace("\r\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    return " ".join(text.split())


def eval_syllables(token: str):
    return dic.inserted(token).split('-')


def find_difficult_connectives(text: str):
    connectives_found = []
    for conn in difficult_connectives:
        results = [m.group() for m in re.finditer(conn, text, re.IGNORECASE)]
        connectives_found.extend(results)
    return connectives_found


def find_latinisms(text: str):
    latinisms_found = []
    for lat in latinisms:
        results = [m.group() for m in re.finditer(lat, text, re.IGNORECASE)]
        latinisms_found.extend(results)
    return latinisms_found


def is_vdb(lemma: str):
    return lemma in italian_vdb


def is_vdb_fo(lemma: str):
    return lemma in italian_vdb_fo


def is_vdb_au(lemma: str):
    return lemma in italian_vdb_au


def is_vdb_ad(lemma: str):
    return lemma in italian_vdb_ad