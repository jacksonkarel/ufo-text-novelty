import os

import praw
from sentence_transformers import SentenceTransformer, util
import torch

from punctuation import segment_sents


def file_to_corpus(filename):
    with open(filename) as f:
        punct_text = f.read()
    corpus = punct_text.split("\n")
    return corpus

def get_reddit():
    client_id = os.environ.get("REDDIT_ID")
    client_secret = os.environ.get("REDDIT_SEC")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="macintosh:com.example.ufocompanies:v1.0.0 (by u/boo_hooray)",
    )

    subreddit = reddit.subreddit("UFOs")
    queries = []
    for submission in subreddit.top("hour"):
        sub_sents = segment_sents(submission.title)
        for sub_sent in sub_sents:
            queries.append(sub_sent)

    """
    This is a simple application for sentence embeddings: semantic search

    We have a corpus with various sentences. Then, for a given query sentence,
    we want to find the most similar sentence in this corpus.

    This script outputs for various queries the top 5 most similar sentences in the corpus.
    """
    corpus = file_to_corpus("punct.txt")

    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    # Query sentences:
    # queries = ['A man is eating pasta.', 'Someone in a gorilla costume is playing a set of drums.', 'A cheetah chases prey on across a field.']
    # queries = ['A man is eating pasta.']

    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(1, len(corpus))
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        if len(corpus) < 1000000:
            # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
            hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=1)
            hit = hits[0][0]
            # if hit['score'] < .4:
            #     print(query, "(Score: {:.4f})".format(hit['score']))
            print(query, "(Score: {:.4f})".format(hit['score']))
        
        else:
            # We use cosine-similarity and torch.topk to find the highest 5 scores
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            top_results = torch.topk(cos_scores, k=top_k)

            # print(top_results[0], top_results[1])
            
            for score, idx in zip(top_results[0], top_results[1]):
                print(corpus[idx], "(Score: {:.4f})".format(score))
                # if score < .4:
                    # print(corpus[idx], "(Score: {:.4f})".format(score))
        
        with open("punct.txt", 'a') as f:
            f.write(query)
        