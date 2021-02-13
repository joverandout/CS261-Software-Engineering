from flair.models import TextClassifier
from flair.models import SequenceTagger
from flair.data import Sentence

# load tagger
classifier = TextClassifier.load('sentiment')
# predict for example sentence

sentence1 = Sentence("That is fantastic")
sentence2 = Sentence("I've never seen anyone mess up a presentation like this before")
sentence3 = Sentence("I wish I could leave")
sentence4 = Sentence("I miss my cats")



classifier.predict(sentence1)
classifier.predict(sentence2)
classifier.predict(sentence3)
classifier.predict(sentence4)

# check prediction
print(sentence1)
print(sentence2)
print(sentence3)
print(sentence4)


#setup required
#pip install flair
#it may be necessary to install ms visual C++ 2015-2019 Redistributable (x64)
