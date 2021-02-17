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


# user feedback (free text input)
feedback = ("The analysis section could have included some more detail. " 
        "Several different avenues of text analysis are described, "
        "but no firm decision is made. The presented timeline seems reasonable. "
        "Having a list of tests is good, but it would have been nice to see a more "
        "formal description of each test. Perhaps include data to use and expected outcomes")

# load tagger (DOWNLOADING THIS TAKES A VERY LONG TIME)
classifier = TextClassifier.load('sentiment-fast')

# initialize sentence splitter
splitter = SegtokSentenceSplitter()

# use splitter to split text into list of sentences
sentences = splitter.split(feedback)

# make the prediction
classifier.predict(sentences)

#print out the predictions
for sentence in sentences:
    print(sentence)
    print(sentence.labels[0].value) #this is a string
    print(sentence.labels[0].score) #this is a float





#setup required
#pip install flair
#it may be necessary to install ms visual C++ 2015-2019 Redistributable (x64)
