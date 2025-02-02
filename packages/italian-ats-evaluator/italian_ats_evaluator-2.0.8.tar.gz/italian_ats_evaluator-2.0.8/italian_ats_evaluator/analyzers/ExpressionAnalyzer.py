from ..utils import nlp_utils


class ExpressionAnalyzer:

    def __init__(self, text: str):
        self.difficult_connectives = nlp_utils.find_difficult_connectives(text)
        self.latinisms = nlp_utils.find_latinisms(text)

        self.n_difficult_connectives = len(self.difficult_connectives)
        self.n_latinisms = len(self.latinisms)