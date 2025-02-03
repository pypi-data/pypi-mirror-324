# pynewsml

A NewsML parsing library

## Installation

```bash
pip install pynewsml
```

## Usage

```python
from pynewsml import NewsML

newsml = NewsML('path/to/newsml.xml')

news = newsml.news_items[0]

print(news.news_lines.headline)
```
