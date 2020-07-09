from nylas import APIClient
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--new_label_name",
                    help="label name for a new folder in your mail")
parser.add_argument("-nt", "--number_of_training_samples", type=int,
                    default=100, help="decide how many email messages "
                    "will be use for training your classification model")
parser.add_argument("-c", "--create_train_dataset", action='store_true',
                    help="create csv file with processed email messages")
parser.add_argument("-t", "--train_model", action="store_true",
                    help="train binary classifier which will classify new label again rest")
parser.add_argument("-p", "--predict_label", action="store_true",
                    help="predict the newest received email label")
args = parser.parse_args()

load_dotenv()
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN
)

def preprocessing(body_html):
    text = BeautifulSoup(body_html, "lxml").text
    return " ".join(text.split())

if args.create_train_dataset:
    print('Creating training dataset ... ', end='')
    messages = nylas.messages.all(limit=args.number_of_training_samples)
    messages_bodies = [message.body for message in messages]
    tags = [None] * len(messages_bodies)
    df = pd.DataFrame({'text': messages_bodies,
                       'tag': tags})

    df['text'] = df['text'].apply(preprocessing)
    df.to_csv(f'{args.new_label_name}_train_dataset.csv')
    print('done.')
    print(df.info())

    print(f'You have to annotate messages in {args.new_label_name}_train_dataset.csv '
           'either with 0 or 1 tag, where 1 means that message '
          f'should be moved to {args.new_label_name} folder in your email account.')

if args.train_model:
    try:
        df = pd.read_csv(f'{args.new_label_name}_train_labeled_dataset.csv')
    except:
        print(f"You have to create labels per every message in {args.new_label_name}_train_dataset.csv"
              f"and saved it as {args.new_label_name}_train_labeled_dataset.csv")
        raise

    print('Number of samples for each class: ')
    print(df.groupby(['tag']).count())
    df.dropna(subset=['tag'], inplace=True)
    y = df['tag']
    x = df['text']

    text_clf = Pipeline([
      ('vect', CountVectorizer()),
      ('tfidf', TfidfTransformer()),
      ('clf', MultinomialNB()),
    ])

    print('Training Model ... ', end='')
    text_clf.fit(x, y)
    print('done.')

    joblib.dump(text_clf, f'{args.new_label_name}_model.pkl', compress = 1)

if args.predict_label:
    try:
        text_clf = joblib.load(f'{args.new_label_name}_model.pkl')

    except:
        print('First create train dataset, tag it and train model '
              'before making any prediction.')
        raise

    if nylas.account.organization_unit == 'label':

        labels = nylas.labels.all()

        label_list = list(filter(lambda x: x.display_name == args.new_label_name, labels))

        if not label_list:
            my_new_label = nylas.labels.create()
            my_new_label.display_name = args.new_label_name
            my_new_label.save()
        else:
            my_new_label = label_list[0]

        message = nylas.messages.first()
        text =  preprocessing(message.body)

        print('Predicting label for: ')
        print(text)
        predicted_label = text_clf.predict([text])
        print('Predicted label: ', predicted_label[0])

        if predicted_label[0] == 1.:
            print(f'Message now is in {args.new_label_name} folder.')
            message.add_label(my_new_label.id)
    else:
        print('Supporting Gmail API only.')
