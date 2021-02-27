# @inproceedings{zampierietal2019, 
# title={{Predicting the Type and Target of Offensive Posts in Social Media}}, 
# author={Zampieri, Marcos and Malmasi, Shervin and Nakov, Preslav and Rosenthal, Sara and Farra, Noura and Kumar, Ritesh}, 
# booktitle={Proceedings of NAACL}, 
# year={2019}, 
# }

import pandas as pd 
from multiprocessing.spawn import freeze_support

from flair.data import Corpus
from flair.datasets.document_classification import ClassificationCorpus
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentRNNEmbeddings
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models.text_classification_model import TextClassifier
from flair.trainers.trainer import ModelTrainer
from torch.optim.adam import Adam

#reads data into dataframe, drops redundant columns and duplicates
data = pd.read_csv("off_or_not.tsv", encoding='latin-1', delimiter='\t')
data = data.drop(columns=['id','subtask_b','subtask_c']).drop_duplicates()

#renames columns to give more descriptive names
data = data[['subtask_a', 'tweet']].rename(columns={"subtask_a":"label", "tweet":"text"}) 

# changes the label column to include '__label__' at the front, ei into FastText format
data['label'] = '__label__' + data['label'].astype(str)

#remove '@USER' from text
data["text"] = [' '.join([item for item in x.split() 
                        if item != '@USER']) 
                        for x in data["text"]]

# remove emoji from text                  
data = data.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
print(data)

#get data for training
data.iloc[0:int(len(data)*0.8)].to_csv('train.txt', sep='\t', index = False, header = False)
# get data for testing set (10%)
data.iloc[int(len(data)*0.8):int(len(data)*0.9)].to_csv('test.txt', sep='\t', index = False, header = False)
# get data for dev set (10%)
data.iloc[int(len(data)*0.9):].to_csv('dev.txt', sep='\t', index = False, header = False)

data_folder = '.'

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
    word_embeddings = [WordEmbeddings('glove'), FlairEmbeddings('news-forward-fast'),
                                        FlairEmbeddings('news-backward-fast'),]

    # 4. initialize document embedding by passing list of word embeddings
    # Can choose between many RNN types (GRU by default, to change use rnn_type parameter)
    document_embeddings = TransformerDocumentEmbeddings('distilbert-base-uncased', fine_tune=True)

    stacked_embeddings = StackedEmbeddings([
                                        WordEmbeddings('glove'),
                                        FlairEmbeddings('news-forward-fast'),
                                        FlairEmbeddings('news-backward-fast'),
                                       ])

    # 5. create the text classifier
    classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, multi_label=False)

    # 6. initialize the text classifier trainer
    trainer = ModelTrainer(classifier, corpus, optimizer=Adam)
    trainer.train('.', 
                  learning_rate=3e-5, # use very small learning rate
                  mini_batch_size=16,
                  max_epochs=5,)


# DONT FORGET THIS
# create a StackedEmbedding object that combines glove and forward/backward flair embeddings
