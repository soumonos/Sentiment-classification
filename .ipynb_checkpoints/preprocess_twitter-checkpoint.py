from __future__ import print_function
import re, sys

# Script for preprocessing tweets by Romain Paulus
# with small modifications by Jeffrey Pennington
# downloaded from http://nlp.stanford.edu/projects/glove/preprocess-twitter.rb

# adapted to python by Benoit Favre
# - fixed bug on left-facing faces
# - fixed byg on neural faces with a slash
# TODO: <ALLCAPS> marker does not work

def split_hashtag(found):
    hashtag_body = found.group(0)[1:]
    if hashtag_body.upper() == hashtag_body:
        return "<HASHTAG> " + hashtag_body + " <ALLCAPS>"
    else:
        return "<HASHTAG> " + ' '.join(re.split(r'(?=[A-Z])', hashtag_body))
    
def preprocess(text):

    # Different regex parts for smiley faces
    eyes = "[8:=;]"
    nose = "['`\-]?"

    text = re.sub(r'https?:\/\/\S+\b|www\.(\w+\.)+\S*', '<URL>', text)
    text = re.sub(r'/', ' / ', text) # Force splitting words appended with slashes (once we tokenized the URLs, of course)
    text = re.sub(r'@\w+', '<USER>', text)
    text = re.sub(eyes + nose + r'[)dD]+|[(dD]+' + nose + eyes, "<SMILE>", text)
    text = re.sub(eyes + nose + r'[pP]+', "<LOLFACE>", text)
    text = re.sub(eyes + nose + r'\(+|\)+' + nose + eyes, "<SADFACE>", text)
    text = re.sub(eyes + nose + r'( \/|[\\|l*])', "<NEUTRALFACE>", text)
    text = re.sub(r'<3', "<HEART>", text)
    text = re.sub(r'[-+]?[.\d]*[\d]+[:,.\d]*', "<NUMBER>", text)
    text = re.sub(r'#\S+', split_hashtag, text) # Split hashtags on uppercase letters
    text = re.sub(r'([!?.]){2,}', r'\1 <REPEAT>', text) # Mark punctuation repetitions (eg. "!!!" => "! <REPEAT>")
    text = re.sub(r'\b(\S*?)(.)\2{2,}\b', r'\1\2 <ELONG>', text) # Mark elongated words (eg. "wayyyy" => "way <ELONG>")
    #text = re.sub(r'(?<![<A-Z])([^a-z0-9()<>\'`\-]){2,}', lambda x: x.group(1).lower() + ' <ALLCAPS>', text)

    return text.lower()

if __name__ == '__main__':
    for line in sys.stdin:
        print(preprocess(line))
