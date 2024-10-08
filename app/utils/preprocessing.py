import json

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from natasha import MorphVocab, Doc, Segmenter, NewsMorphTagger, NewsEmbedding

def data_to_text(data: dict) -> (str, list):
    """
    Convert dataset to text
    """
    texts = []
    for answer in data["answers"]:
        texts.extend(answer)
    question = data["question"]
    return question, texts

def to_lowercase(sentence: str) -> str:
    """
    Convert sentence to lowercase
    """
    return sentence.lower()

def remove_stopwords(sentence: str) -> str:
    """
    Remove stopwords from sentence
    """
    stop_words = set(stopwords.words('russian'))

    words = word_tokenize(sentence)

    filtered_sentence = [word for word in words if word.lower() not in stop_words]
    
    return ' '.join(filtered_sentence)

def lemmatize(sentence: str) -> str:
    """
    Lemmatize sentence
    """
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    morph_vocab = MorphVocab()

    lemmatized = ''
    doc = Doc(sentence)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        #print(token.text, token.lemma)
        lemmatized += token.lemma + ' '
    return lemmatized.strip()

def lemmatize_texts(texts: list):
    """
    Lemmatize texts
    """
    lemmatized_texts = []
    lemmatize_dict = {}

    for sentence in texts:
        lemmatized_sentence = lemmatize(remove_stopwords(sentence))
        lemmatize_dict[lemmatized_sentence] = sentence
        lemmatized_texts.append(lemmatized_sentence)

    return lemmatize_dict, lemmatized_texts

def lemma_replacement(lemma: str, lemmatize_dict: dict) -> str:
    """
    Replacement for lemmatization
    """
    if lemma in lemmatize_dict.keys():
        return lemmatize_dict[lemma]
    return lemma