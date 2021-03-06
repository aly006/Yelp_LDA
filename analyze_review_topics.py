from gensim.models import LdaModel
from gensim import corpora
import nltk
import string
import Config

dictionary = corpora.Dictionary.load(Config.DICTIONARY_LOCAL)
lda = LdaModel.load(Config.LDA_LOCAL)

def clean_review(review):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    wnl = nltk.WordNetLemmatizer()

    counter = 0
    cleaned_review_words = []

    # lower case and remove punctiation
    punctuation = set(string.punctuation)
    review_text = (''.join([c for c in review.lower() if not c in punctuation]))

    sentences = nltk.sent_tokenize(review_text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for w in words:
            if w not in stopwords:
                # consider tagging POS, but decreases performance drastically
                cleaned_review_words.append(wnl.lemmatize(w))

    return cleaned_review_words

def find_topics_in_review(cleaned_text):
    topics = lda[dictionary.doc2bow(cleaned_text)]

    sorted_percentage = [(x[1], x[0]) for x in topics]
    sorted_percentage.sort()
    sorted_percentage.reverse()

    return sorted_percentage

def predict_topics(review):
    cleaned_text = clean_review(review)
    sorted_topics = find_topics_in_review(cleaned_text)

    for percentage, topic_number in sorted_topics:
        #print lda.print_topic(topic_number)
        print str(round(percentage * 100, 2)) + "%" + "\t T:" + str(topic_number) + "\t" + lda.print_topic(topic_number)

if __name__ == "__main__":
    print "Vallartas Review"
    vallartas_review = "This is my go-to Mexican place. First off, it has a drive through so my lazy butt doesn't have to change out of pajamas if I'm having a craving for a Cali Burrito. Fast service, good quality and good prices. Their tacos are also really good! I got the carne aside taco combo plate (with rice and beans) and loved it. Also if you order the chips and quac they give you a huge box full of hot crispy tortilla chips smothered in fresh guacamole. Big enough to share between at least 3-4 people, I can never finish it all because the portion is so big."

    predict_topics(vallartas_review)

    print "Mcdonalds Review"
    mcdonalds_review = "Went to their drive through at midnight to satisfy some late night munchies. Ordered two hot & spicy Mcchicken, chipotle BBQ snack wrap, and medium fries. Everything just went wrong. They gave us regular Mcchicken instead of the hot & spicy one which sucks because the regular ones are boring AF and has no flavor. They put way too much BBQ sauce in the snack wrap. Very unproportional amount. Lastly the fries were even salted.. A very sad sad late night snack from McDonalds."

    predict_topics(mcdonalds_review)


