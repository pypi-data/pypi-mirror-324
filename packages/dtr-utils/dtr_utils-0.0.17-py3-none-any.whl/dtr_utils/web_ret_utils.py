# Import necessary libraries
from duckduckgo_search import DDGS
import os
import random
import re
import time
import requests
import numpy as np
import pandas as pd
import math
import pickle
import urllib3
import sys
import ssl
from lxml import html
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from collections import Counter, defaultdict
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

from googlesearch import search
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures

from dtr_utils import nlp_stanza

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load SentenceTransformer model
# model_sent_transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
from dtr_utils import model

model_sent_transformer = model


domains = [
    "wikipedia.org",
    "nytimes.com",
    "cnn.com",
    "bbc.com",
    "theguardian.com",
    "forbes.com",
    "reuters.com",
    "cnbc.com",
    "bloomberg.com",
    "foxnews.com",
    "npr.org",
    "washingtonpost.com",
    "wsj.com",
    "aljazeera.com",
    "ft.com",
    "huffpost.com",
    "nationalgeographic.com",
    "scientificamerican.com",
    "nature.com",
    "time.com",
    "usatoday.com",
    "apnews.com",
    "abcnews.go.com",
    "cbsnews.com",
    "nbcnews.com",
    "news.yahoo.com",
    "theatlantic.com",
    "vox.com",
    "politico.com",
    "economist.com",
    "en.wikipedia.org",
    "nytimes.com",
    "propublica.org",
    "usatoday.com",
    "latimes.com",
    "thehill.com",
    "pbs.org",
    "timesofindia.indiatimes.com",
    "thetimes.com",
    "telegraphindia.com",
    "ft.com",
    "news.sky.com",
    "cbc.ca",
    "ctvnews.ca",
    "abc.net.au",
    "straitstimes.com",
    "hindustantimes.com",
    "thehindu.com",
    "chinadaily.com.cn",
    "aljazeera.com",
    "gulfnews.com",
    "economist.com",
    "foreignpolicy.com",
    "theintercept.com",
    "nature.com",
]


def fetch_webpage(url):
    # Define a list of user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        # Add more User-Agents as needed
    ]

    # Create an unverified SSL context
    context = ssl._create_unverified_context()

    exclude = [
        "Thank you for your patience",
        "Subscribe",
        "subscribe",
        "trouble retrieving the article content",
        "browser settings",
        "Thank you for your patience while we verify access. If you are in Reader mode please exit and log into your Times account, or subscribe for all of The Times.",
        "Thank you for your patience while we verify access.",
        "Already a subscriber? Log in.",
        "Want all of The Times? Subscribe.",
        "Advertisement",
        "Site Index",
        "Thank you for your patience while we verify access. If you are in Reader mode please exit andlog intoyour Times account, orsubscribefor all of The Times.",
        "Already a subscriber?Log in.",
        "Want all of The Times?Subscribe.",
        "Site Information Navigation",
    ]

    """Fetch webpage content with rotating user-agents and bypass SSL verification."""
    try:
        # Randomly select a user-agent
        user_agent = random.choice(user_agents)

        # Set up request with the random user-agent
        req = Request(url, headers={"User-Agent": user_agent})

        # Fetch webpage content, bypassing SSL verification
        with urlopen(req, timeout=10, context=context) as response:
            content = response.read()
            response_encoding = response.headers.get_content_charset() or "utf-8"
            # Decode the content
            content = content.decode(response_encoding)

        if not content.strip():
            return ""

        try:
            # Parse the content using lxml
            tree = html.fromstring(content)
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return ""

        # Extract specified tags and filter content in one loop
        filtered_data = []
        # tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]
        tags = ["p"]
        for tag in tags:
            for element in tree.xpath(f"//{tag}"):
                sentence = element.text_content()
                # Only add the sentence if it does not contain any of the excluded phrases
                if not any(excluded_phrase in sentence for excluded_phrase in exclude):
                    filtered_data.append(sentence)

        return "\n".join(filtered_data)

    except Exception as e:
        print(f"\nURL: {url}\nError: {e}")

        return ""


def clean_text(text):
    """Normalize text by removing extra spaces, tabs, hyphens, and other discrepancies."""
    text = re.sub(
        r"[\s\t]+", " ", text
    )  # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[-–—]", " ", text)  # Replace hyphens and dashes with a space
    text = text.strip()  # Trim leading/trailing spaces
    return text.lower()  # Convert to lowercase


def rank_sentences(sentences, query):
    if not sentences:
        return []  # Return an empty list if no sentences are found

    # Normalize and deduplicate sentences
    sentences = list(set(clean_text(s) for s in sentences))

    # Normalize query
    query = clean_text(query)

    # Encode sentences and query into embeddings
    sentence_embeddings = model_sent_transformer.encode(
        sentences, convert_to_tensor=True
    )
    query_embedding = model_sent_transformer.encode(query, convert_to_tensor=True)

    # Compute cosine similarity between query and each sentence
    similarities = (
        util.pytorch_cos_sim(query_embedding, sentence_embeddings)
        .cpu()
        .numpy()
        .flatten()
    )

    # Rank sentences based on their similarity to the query
    ranked_sentences = sorted(
        zip(sentences, similarities), key=lambda x: x[1], reverse=True
    )

    # Extract the ranked sentences
    ranked_sentences = [sentence for sentence, _ in ranked_sentences]

    return ranked_sentences[: min(len(ranked_sentences), 2000)]


def fetch_content_for_url(url):
    try:
        # Extract base domain
        base_domain = urlparse(url).netloc
        base_domain = re.sub(r"^www\.", "", base_domain)

        # Check if domain is in the list of valid domains
        if base_domain in domains:
            print(f"Fetching content from: {url}")
            # Fetch the content of the webpage
            text = fetch_webpage(url)
            if text:
                # text = text.splitlines()
                return [text]
            else:
                return []  # In case the text is empty
            # else:
            #     return []  # If domain is not in the allowed list

    except Exception as e:
        print(f"Failed to fetch content from {url} due to: {str(e)}")
        return []  # Return empty list on failure


# def get_web_content_parallelize(query, ranker_query, exclude_url, num_urls):
def get_web_content_parallelize(query, num_urls):
    all_results = search(query, num_results=num_urls)
    # all_results = [result for result in all_results if result != exclude_url]
    # all_results = [result for result in all_results]

    # results = DDGS().text(query, max_results=num_urls)
    # all_results = [result["href"] for result in results]

    # print(f"Excluding URL: {exclude_url}")

    t1 = time.time()
    text_combined = []
    web_context = set()
    # web_context = []

    # Use ThreadPoolExecutor to fetch content in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Fetch content for all URLs concurrently
        future_to_url = {
            executor.submit(fetch_content_for_url, result): result
            for result in all_results
        }

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                result_text = future.result()  # Get the result of each completed future
                if result_text:

                    text_combined.extend(result_text)
            except Exception as e:
                print(f"Error processing result: {e}")

    for line in text_combined:
        # if not any(excluded_phrase in line for excluded_phrase in exclude):
        if len(line.split()) > 8:
            web_context.add(line)
            # web_context.append(line)
    # print(web_context)
    # top_sentences = rank_sentences(web_context,query)
    top_sentences = rank_sentences(web_context, query)
    # top_sentences = top_sentences[:30]
    t2 = time.time()
    minutes, seconds = divmod(t2 - t1, 60)

    print(f"{minutes} minutes and {seconds} seconds")

    ans = "\n\n".join(
        sentence.strip() for sentence in top_sentences if sentence.strip()
    )
    return ans
    # return web_context
