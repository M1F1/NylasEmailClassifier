# NylasEmailClassifier
  Project contains simple text binary classifier (MultinomiaL Naive Bayes) which categorize email messages from your inbox. It uses API provided by Nylas to leverage messages from email account and create/add new labels to the recived message. If you want to try it, check the instructions below:
1. Clone repo and install requiremets: 
  ```sh
  git clone 
  cd /NylasEmailClassifier
  pip install -r requirements.txt
  ```

2. Copy all required credentials from your [Nylas account](https://www.nylas.com/) to `.env` file (disclaimer - only gmail is supported).
3. Decide what is the new category/label which you want add to some of received messages.
4. Create training dataset from current messages in your mail account (you can specify number of messages, default is 100):
  ```sh
  python create_train_predict.py -l {new_label_name} -nt 50 -c
  ```
5. In the next step you will be training binary classifier, so tag messages either with 0 or 1 (1 means that message should have chosen new label).
   Save tagged data as `{new_label_name}_train_labeled_dataset.csv`.

6. Train classifier on tagged data:
  ```sh
  python create_train_predict.py -l {new_label_name} -t
  ```
7. Classify the newest received email message:
  ```sh
  python create_train_predict.py -l {new_label_name} -p
  ```
