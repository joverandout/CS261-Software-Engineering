from flair.models import TextClassifier
from flair.data import Sentence

classifier = TextClassifier.load('en-sentiment')
sentence = Sentence('Flask is annoying!')
classifier.predict(sentence)# print sentence with predicted labels

print('Sentence above is: ', sentence.labels)