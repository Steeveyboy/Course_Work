import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    
    print(corpus)
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution = corpus.fromkeys(corpus.keys(), (1-damping_factor) / len(corpus))
    
    links = corpus[page]
    if links:
        for link in links:
            prob_distribution[link] += damping_factor / len(links)
            
    return prob_distribution
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_visits = dict.fromkeys(corpus.keys(), 0)
    
    sample_page = random.choice(list(corpus.keys()))
    page_visits[sample_page] += 1
    
    
    for _ in range(n):
            
        prob_distribution = transition_model(corpus, sample_page, damping_factor)
        
        sample_page = random.choices(list(prob_distribution.keys()), weights=prob_distribution.values(), k=1)[0]
        page_visits[sample_page] += 1

    pagerank = {page: visits / n for page, visits in page_visits.items()}
    return pagerank
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_ranks = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    

    convergence_threshold = 0.0001

    converged = False
    while not converged:
        new_page_ranks = page_ranks.copy()
        
        for page in corpus:
            page_rank_sum = 0
            for other_page in corpus:
                if page in corpus[other_page]:
                    page_rank_sum += page_ranks[other_page] / len(corpus[other_page])
                elif len(corpus[other_page]) == 0:
                    page_rank_sum += page_ranks[other_page] / len(corpus)
            
            new_page_ranks[page] = (1 - damping_factor) / len(corpus) + damping_factor * page_rank_sum
        

        
        converged = all(abs(new_page_ranks[page] - page_ranks[page]) < convergence_threshold for page in corpus)
        
        page_ranks = new_page_ranks.copy()
    return new_page_ranks
    

if __name__ == "__main__":
    main()
