from multiprocessing.spawn import freeze_support

from flair.data import Corpus
from flair.datasets.document_classification import ClassificationCorpus
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models.text_classification_model import TextClassifier
from flair.trainers.trainer import ModelTrainer
from torch.optim.adam import Adam

data_folder = '.'

# 'if' only needed when on Windows
if __name__ == '__main__':
    freeze_support()  

    corpus: Corpus = ClassificationCorpus(data_folder, 
                                     test_file='test.txt',
                                     dev_file='dev.txt',
                                     train_file='train.txt').downsample(0.7)
    # 2. create the label dictionary
    label_dict = corpus.make_label_dictionary()
    
    # 3. initialize transformer document embeddings
    embedding = TransformerDocumentEmbeddings('distilbert-base-uncased', 
                                              fine_tune=True)

    # 5. create the text classifier
    classifier = TextClassifier(embedding, label_dictionary=label_dict, multi_label=False)

    # 6. initialize the text classifier trainer
    trainer = ModelTrainer(classifier, corpus, optimizer=Adam)
    trainer.train('.', 
                  learning_rate=3e-5, #learning rate must be small
                  mini_batch_size=16,
                  max_epochs=8,  #terminate after 8 epochs
                  mini_batch_chunk_size=4, #this is so as not to overwhelm the CPU
                  shuffle=True,
                  )

