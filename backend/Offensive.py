from flair.data import Sentence
from flair.models import TextClassifier
from flair.tokenization import SegtokSentenceSplitter

# load classifier 
classifier = TextClassifier.load('best-model.pt')

# initialize sentence splitter
splitter = SegtokSentenceSplitter()

# create example sentence
# sentence = Sentence('You are a piece of shit. I hate your faggot ass. I have to admit you are an expert in PR. You dress like a champion. I was bored the whole time. I can see you put a lot of effort into this.')

class Offensive():
    input = ""
    __offValues = []
    __confScores = []
    __evaluation = []

    def __init__(self, stringfeedback):
        self.input = stringfeedback
        self.__offValues = []
        self.__confScores = []
        self.__evaluation = []

    def update_rating(self): 
        # use splitter to split text into list of sentences
        sentences = splitter.split(self.input)

        # make the prediction
        classifier.predict(sentences)

        #print out the predictions
        for sentence in sentences:
            self.__offValues.append(sentence.labels[0].value) 
            self.__confScores.append(sentence.labels[0].score)
            
    #the higher the score the more offensive the sentence
    def get_scores(self):
        for i in range(len(self.__confScores)):
            if self.__offValues[i]=="NOT":
                self.__confScores[i] = -self.__confScores[i]
        return self.__confScores

# offEval = Offensive('You suck balls. Fuck. I love you')
# print('You suck balls. Fuck. I love you')
# offEval.update_rating()
# a = offEval.get_scores()
# print(a)
#for each in a:
#    if each > 0.5:
#        print("OFFENSIVE")