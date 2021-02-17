# @inproceedings{akbik2018coling,
#   title={Contextual String Embeddings for Sequence Labeling},
#   author={Akbik, Alan and Blythe, Duncan and Vollgraf, Roland},
#   booktitle = {{COLING} 2018, 27th International Conference on Computational Linguistics},
#   pages     = {1638--1649},
#   year      = {2018}
# }

from flair.models import TextClassifier
from flair.models import SequenceTagger
from flair.data import Sentence

# load tagger
classifier = TextClassifier.load('en-sentiment')

#  example sentences
sentence1 = Sentence("Overall, design is good and thoroughly describes most of the processes in the system. The analysis section could have included some more detail, as several different avenues of text analysis are described, but no firm decision is made. Methodology seems sensible, and the presented timeline seems reasonable. Having a list of tests is good, but it would have been nice to see a more formal description of each test (including data to use and expected outcomes)")
sentence2 = Sentence("Your wife should leave you")



# check prediction for first sentence
print(sentence1)
# this modifies the sentence to include the sentiment and confidence of analysis
classifier.predict(sentence1)
print('Sentence above is: ')
print(sentence1.labels[0].value)
print(sentence1.labels[0].score)


# print prediction for second sentence
print(sentence2)
# this modifies the sentence to include the sentiment and confidence of analysis
classifier.predict(sentence2)
print('Sentence above is: ')
print(sentence2.labels[0].value)
print(sentence2.labels[0].score)




#setup required
#pip install flair
#it may be necessary to install ms visual C++ 2015-2019 Redistributable (x64)
