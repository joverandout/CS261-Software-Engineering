import pandas as pd

from multiprocessing.spawn import freeze_support

from flair.data import Corpus
from flair.datasets import ClassificationCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer

#'./sets' is the directory the dataset is in

# reads in data, drops duplicates and shuffles
data = pd.read_csv("./sets/spam.csv", encoding='latin-1')
# drop duplicates
data = data.sample(frac=1).drop_duplicates() 
#renames columns to give more descriptive names
data = data[['v1', 'v2']].rename(columns={"v1":"label", "v2":"text"}) 

# changes the label column to include '__label__' at the front, as required by Flair's FastText format
data['label'] = '__label__' + data['label'].astype(str)
print(data.head(25)) 

# column format indicating which columns hold the text and label(s)
column_name_map = {2: "text", 1: "label_topic"}

# get data for training set (80%)
data.iloc[0:int(len(data)*0.8)].to_csv('./sets/train.txt', sep='\t', index = False, header = False)
# get data for testing set (10%)
data.iloc[int(len(data)*0.8):int(len(data)*0.9)].to_csv('./sets/test.txt', sep='\t', index = False, header = False)
# get data for dev set (10%)
data.iloc[int(len(data)*0.9):].to_csv('./sets/dev.txt', sep='\t', index = False, header = False)

data_folder = './sets'


# 'if' only needed when on Windows
if __name__ == '__main__':
    freeze_support()  

    corpus: Corpus = ClassificationCorpus(data_folder, 
                                     test_file='test.txt',
                                     dev_file='dev.txt',
                                     train_file='train.txt')
    # 2. create the label dictionary
    label_dict = corpus.make_label_dictionary()

    # 3. make a list of word embeddings
    word_embeddings = [WordEmbeddings('glove')]

    # 4. initialize document embedding by passing list of word embeddings
    # Can choose between many RNN types (GRU by default, to change use rnn_type parameter)
    document_embeddings = DocumentRNNEmbeddings(word_embeddings, hidden_size=256)

    # 5. create the text classifier
    classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, multi_label=False)

    # 6. initialize the text classifier trainer
    trainer = ModelTrainer(classifier, corpus)
    #trainer.train('./sets', max_epochs=10, patience = 5)
