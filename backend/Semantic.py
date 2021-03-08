# @inproceedings{akbik2018coling,
#   title={Contextual String Embeddings for Sequence Labeling},
#   author={Akbik, Alan and Blythe, Duncan and Vollgraf, Roland},
#   booktitle = {{COLING} 2018, 27th International Conference on Computational Linguistics},
#   pages     = {1638--1649},
#   year      = {2018}
# }

from flair.tokenization import SegtokSentenceSplitter
from flair.models import TextClassifier
from flair.models import SequenceTagger
from flair.data import Sentence


# load classifier (either 'sentiment' or 'sentiment-fast')
classifier = TextClassifier.load('sentiment-fast')

# initialize sentence splitter
splitter = SegtokSentenceSplitter()

class Semantic():
    input = ""
    __semValues = []
    __confScores = []
    __evaluation = []

    def __init__(self, stringfeedback):
        self.input = stringfeedback
        self.__semValues = []
        self.__confScores = []
        self.__evaluation = []

    def update_semValues_and_confScores(self): 
        # use splitter to split text into list of sentences
        sentences = splitter.split(self.input)

        # make the prediction
        classifier.predict(sentences)

        #print out the predictions
        for sentence in sentences:
            self.__semValues.append(sentence.labels[0].value) 
            self.__confScores.append(sentence.labels[0].score)

    def get_scores(self):
        for i in range(len(self.__confScores)):
            if self.__semValues[i]=="NEGATIVE":
                self.__confScores[i] = -self.__confScores[i]
        return self.__confScores


# example usage

feedbackEval = Semantic("Groupwork was okay. There were no fireworks. I think you were on time. Overall, an avergae workshop")
feedbackEval.update_semValues_and_confScores()
s = feedbackEval.get_scores()
print(s)
#
