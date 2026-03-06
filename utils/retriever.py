from rank_bm25 import BM25Okapi


def build_index(pages):
    """
    Builds a BM25Okapi index from the parsed page list.

    Args:
        pages: List of dicts with 'page' and 'text' keys (from parse_pdf).

    Returns:
        A BM25Okapi index object.
    """
    tokenized_corpus = [page["text"].lower().split() for page in pages]
    return BM25Okapi(tokenized_corpus)


def retrieve_pages(bm25, pages, query, top_n=3):
    """
    Retrieves the top-N most relevant pages for the given query.

    Args:
        bm25: BM25Okapi index object.
        pages: Original page list from parse_pdf.
        query: User's question string.
        top_n: Number of top pages to return (default 3).

    Returns:
        List of top-N page dicts sorted by relevance (descending).
    """
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [pages[idx] for idx, _ in ranked[:top_n]]
