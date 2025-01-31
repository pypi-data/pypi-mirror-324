# import dtr_utils.beam

import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords
import string


import stanza
import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

stanza.download("en")  # Download the English model if not already downloaded
# Check if GPU is available
use_gpu = torch.cuda.is_available()

# Initialize the Stanza pipeline with GPU if available
nlp_stanza = stanza.Pipeline(
    "en",
    processors="tokenize,ner",
    use_gpu=use_gpu,  # Set GPU usage based on availability
    batch_size=50,
    tokenize_batch_size=5000000,
)

# Initialize Stanza pipeline and NLTK stop words
# stanza_nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")
stop_words = set(stopwords.words("english"))


# import dtr_utils.ecd_score
# import dtr_utils.n_gram_utils
# import dtr_utils.web_ret_utils
# import dtr_utils.tree_processing
