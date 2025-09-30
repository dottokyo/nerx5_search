import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import pandas as pd
import ast
import random

nlp = spacy.load("ru_core_news_md")

#upload data
csv = pd.read_csv('services/data/train.csv', sep=';')

train_data = []
for index, row in csv.iterrows():
    text = row['sample']
    annotations = ast.literal_eval(row['annotation'])
    entities = [(start, end, label) for start, end, label in annotations]
    train_data.append((text, {'entities': entities}))

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in train_data:
    for _, _, label in annotations['entities']:
        ner.add_label(label)

#or begin_training()
optimizer = nlp.resume_training()

for epoch in range(20):
    print(f"Epoch {epoch+1}")
    losses = {}
    random.shuffle(train_data)
    examples = [Example.from_dict(nlp.make_doc(text), ann) for text, ann in train_data]

    batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        nlp.update(batch, drop=0.5, losses=losses, sgd=optimizer)
    print("losses", losses)

nlp.to_disk('x5-ner')

