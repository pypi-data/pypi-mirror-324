# DuckDuck Search Library

DuckDuck Search Library is a Python library that allows you to perform searches using [DuckDuckGo](https://duckduckgo.com/). With a simple and clean API, you can quickly and easily retrieve relevant documents and links from the internet. The library supports features like rate limiting, domain filtering, and optional answer retrieval directly from DuckDuckGo.

---

## Features

- **Easy Integration:**
  Provides a simple and intuitive API for performing searches.

- **Rate Limiting:**
  Built-in rate limiting helps to avoid making requests too frequently.

- **Domain Filtering:**
  Restrict search results to a specific domain if required.

- **Optional Answer Retrieval:**
  Optionally fetch direct answers from DuckDuckGo.

- **Flexible Configuration:**
  Customizable parameters such as region, safe search settings, time limits, and more.

- **Python 3.7+ Compatible:**
  Designed to work with modern versions of Python.

---

## Installation

You can install the library via pip:

### From PIP

```bash
pip install duckducksearch
```

### From Source

```bash
pip install git+https://github.com/bes-dev/duckducksearch.git
```

## Usage

```python
from duckduck_search_lib import DuckDuckSearch

# Initialize the searcher with your desired configuration.
searcher = DuckDuckSearch(
    top_k=10,
    max_results=20,
    region="wt-wt",
    safesearch="moderate",
    allowed_domain="",  # Leave empty for no domain restriction
    use_answers=False   # Set to True if you want to retrieve direct answers from DuckDuckGo
)

# Define your search query and number of results to retrieve.
query = "What is Python?"
num_results = 5

# Perform the search.
results = searcher.search(query, num_results)

# Output the results.
print("Documents:")
for doc in results["documents"]:
    print(f"Title: {doc.title}")
    print(f"Content: {doc.content}")
    print(f"Link: {doc.link}")
    print("------------")

print("Links:")
for link in results["links"]:
    print(link)

```
