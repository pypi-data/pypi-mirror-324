from dataclasses import dataclass, field
from typing import List
from lxml import etree


@dataclass
class Topic:
    topic_type: str
    formal_name: str
    descriptions: dict


@dataclass
class RevisionId:
    value: str
    update: str
    previous_revision: str

    def __init__(self, elem):
        self.value = elem.text
        self.update = elem.attrib.get("Update")
        self.previous_revision = elem.attrib.get("PreviousRevision")


@dataclass
class NewsIdentifier:
    provider_id: str
    date_id: str
    news_item_id: str
    revision_id: RevisionId
    public_identifier: str


@dataclass
class NewsLines:
    headline: str
    subheadline: str
    byline: str
    dateline: str
    creditline: str
    copyrightline: str
    keywords: List[str]


@dataclass
class ContentItem:
    media_type: str
    word_count: int
    data_content: str


@dataclass
class NewsItem:
    identifier: NewsIdentifier
    news_lines: NewsLines
    topics: List[Topic]
    content: ContentItem


@dataclass
class NewsML:
    news_items: List[NewsItem] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_string: str) -> "NewsML":
        root = etree.fromstring(xml_string.encode('utf-8'))
        news_items = []

        for news_item_elem in root.findall(".//NewsItem"):
            identifier = NewsIdentifier(
                provider_id=news_item_elem.findtext(".//ProviderId"),
                date_id=news_item_elem.findtext(".//DateId"),
                news_item_id=news_item_elem.findtext(".//NewsItemId"),
                revision_id=RevisionId(news_item_elem.find(".//RevisionId")),
                public_identifier=news_item_elem.findtext(
                    ".//PublicIdentifier"),
            )

            news_lines = NewsLines(
                headline=news_item_elem.findtext(".//HeadLine"),
                subheadline=news_item_elem.findtext(".//SubHeadLine"),
                byline=news_item_elem.findtext(".//ByLine"),
                dateline=news_item_elem.findtext(".//DateLine"),
                creditline=news_item_elem.findtext(".//CreditLine"),
                copyrightline=news_item_elem.findtext(".//CopyrightLine"),
                keywords=[kw.text for kw in news_item_elem.findall(
                    ".//KeywordLine")],
            )

            topics = cls._load_topics(news_item_elem)

            content_elem = news_item_elem.find(".//ContentItem")
            content = ContentItem(
                media_type=content_elem.find(
                    ".//MediaType").attrib.get("FormalName"),
                word_count=int(content_elem.find(
                    ".//Property[@FormalName='WordCount']").attrib.get("Value")),
                data_content=content_elem.findtext(".//DataContent"),
            )

            news_items.append(
                NewsItem(identifier, news_lines, topics, content))

        return NewsML(news_items)

    @staticmethod
    def _load_topics(elem) -> List[Topic]:
        topics = []
        for topic_elem in elem.findall(".//Topic"):
            descriptions = {desc.attrib.get(
                "xml:lang"): desc.text for desc in topic_elem.findall(".//Description")}
            topics.append(
                Topic(
                    topic_type=topic_elem.find(
                        ".//TopicType").attrib.get("FormalName"),
                    formal_name=topic_elem.findtext(".//FormalName"),
                    descriptions=descriptions,
                )
            )
        return topics
