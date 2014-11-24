__author__ = 'christopherallison'

import os
import nltk, re, pprint
import csv
from nltk import word_tokenize
from nltk.corpus import stopwords
import time


# Load target file and supporting documents

path = '/Users/christopherallison/Documents/Work/User Study/'
print('\nFILES:\n')
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for f in files:
    print(f)

ftarget = 'User Study 2013'  #input("\nPlease enter file name: ")

recommendations = ['should', 'make', 'improve', 'recommend', 'could', 'change', 'need',
                   'adjust', 'suggest', 'propose', 'advise', 'urge', 'want', 'must', 'desire', 'fix']

components = ['interface', 'search', 'groups', 'notifications', 'messaging', 'files', 'video', 'performance', 'post',
              'registration', 'display', 'editor', 'upload', 'download']

tools = ['gcpedia', 'gcconnex', 'gcforums', 'blueprint', 'tool']


with open(path + 'positive.txt', 'r') as f:
    pos = f.read()
    pos = pos.strip()
    positive_words = pos.split('\n')

with open(path + 'negative.txt', 'r') as f:
    neg = f.read()
    neg = neg.strip()
    negative_words = neg.split('\n')

with open(path + ftarget, 'rU') as f:
    raw = f.read()

# Process text

tokens = word_tokenize(raw)
text = nltk.Text(tokens)
sens = nltk.sent_tokenize(raw)


def text_analysis(text):

    options = ['Find collocations', 'Find Concordance', 'Run a frequency distribution', 'Display Hapaxes',
               'Display frequently occurring long words', 'Run a sentiment analysis',
               'Clean text and run frequency distribution', 'Recommendations & Concordance',
               'Search for 3 word phrases']

    # Select options

    finished = False

    while not finished:

        i = 1
        print("\n\nChoose an option:")
        for option in options:
            print('{}: {}'.format(i, option))
            i += 1

        option_select = input("\nEnter the number for your choice or type q to quit: ")

        if option_select == str(1):
            collocation(text, 40, 5)

        elif option_select == str(2):
            concordance(text)

        elif option_select == str(3):
            frequency_distribution(text)

        elif option_select == str(4):
            hapaxes(text)

        elif option_select == str(5):
            freq_long(text)

        elif option_select == str(6):
            sentiment_analysis(text, positive_words, negative_words)

        elif option_select == str(7):
            clean_up_text(text)

        elif option_select == str(8):
            recommend_concordance(text)

        elif option_select == str(9):
            pos_trigrams(sens)

        elif option_select in ['q', 'Q', 'Quit', 'quit']:
            break

        else:
            print("Invalid selection.  Please try again")

        cont = input("\nPerform another operation? (y/n): ")
        if cont in ['Y', 'y', 'yes']:
            pass
        else:
            finished = True


def collocation(text, number, win):

    print("Collocations:")
    text.collocations(num=number, window_size=win)

def concordance(text):

    target = input("Which word would you like to search concordance for? ")
    print('\nConcordance: {}'.format(target))
    text.concordance(target, width=140)
    #csv_write(target, text.concordance(target, width=140))
    print('\nSentences:')
    for sentence in sens:
        if target.lower() in sentence.lower():
            print(sentence)

def frequency_distribution(text):

    #min_len = input("Please set a minimum length for the frequency distribution: ")
    #number = input("Please enter the number of raw results to process (the longer the minimum length, the higher"
    #               " this can be): ")

    print('\nFrequency Distribution:')
    fdist1 = nltk.FreqDist(text)
    V = fdist1.most_common(n=50)
    print([y for y in V if len(y) > 7])
    text.dispersion_plot(recommendations)

def hapaxes(text):

    print('\nHapaxes')
    fdist1 = nltk.FreqDist(text)
    print(fdist1.hapaxes())

def freq_long(text):
    fdist1 = nltk.FreqDist(text)
    min_len = input("Please set a minimum length for the for the words: ")
    number = input("Please enter the minimum number of times the word should appear: ")
    print('\nFrequently Occurring Long Words:')
    print(sorted(w for w in set(text) if len(w) > int(min_len) and fdist1[w] > int(number)))

def sentiment_analysis(text, positive, negative):
    V = set(text)
    pos = [w for w in V if w.lower() in positive]
    print(sorted(pos), '\nNumber of positive words: {} ({}%)'.format(len(pos), round(len(pos)/len(text), 3)))
    neg = [w for w in V if w.lower() in negative]
    print(sorted(neg), '\nNumber of negative words: {} ({}%)'.format(len(neg), round(len(neg)/len(text), 3)))


def clean_up_text(text):
    print("\nCleaning text.\n")

    x = [w for w in set(text) if w.lower() not in stopwords.words('english') and
            w.lower() not in stopwords.words('french')]
    print(x)

    fdist2 = nltk.FreqDist(x)
    fdist2.plot(50, cumulative=True)


def recommend_concordance(text):
    print("Printing concordance by recommendations")

    save_file = open('Recommendation.txt', 'w')
    save_file.write("Printing concordance by recommendations {}".format(time.strftime("%d/%m/%Y")))
    save_file.write('\n')
    #for t in tools:
    for c in components:
        for w in recommendations:
            print(c.upper(), w.upper())

            save_file.write(c.upper() + " " + w.upper())
            save_file.write("\n")

            for sentence in sens:
                if all(x in sentence for x in [c, w]):
                    print(sentence)

                    save_file.write(sentence)
                    save_file.write("\n")

            print('')
            save_file.write("\n")

    save_file.close()
        #print('{}\n'.format(w))
        #text.concordance(w, width=120, lines=100)



def process(sentence):
    for (w1,t1), (w2,t2), (w3,t3) in nltk.trigrams(sentence):
        if t1.startswith('V') and t2 == 'TO' and t3.startswith('V'):
            print(w1, w2, w3)

def pos_trigrams(text):
    # tags sentences with POS and runs three word phrases

    for sentence in text:
        trans = word_tokenize(sentence)
        final = nltk.pos_tag(trans)
        process(final)

def csv_write(file_name, text):
    writer = csv.writer(open(file_name + '.csv', 'wb'))
    writer.writerow(['Instances of {}'.format(str(file_name))])
    writer.writerows(text)

if __name__ == "__main__":
    text_analysis(text)