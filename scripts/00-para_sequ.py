# This is a self-contained python script that answers,
# "How much of the QA is fully parallel, and how much of the QA is fully sequential?"
# Parallel here means that to answer the questions, one aggregates information from different Wikipedia pages,
# and the pages contains the group truth directly answering one small part of the questions
# Sequential means that to answer the questions, one ask another question, and follow the logic of that questions...

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Self, TypeAlias, TypedDict, no_type_check
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s'
)
logger = logging.getLogger(__name__)


class Categories(Enum):
    sports = 0
    statistics = 1


ID: TypeAlias = str


@dataclass
class Evidence:
    page_id: int
    rev_id: int
    title: str

    @property
    def url(self) -> str:
        return f"https://en.wikipedia.org/wiki/{self.title.replace(" ","_")}"

    @classmethod
    @no_type_check
    def from_json(cls, raw_json: dict) -> Self:
        try:
            result = cls(
                page_id = raw_json.get("pageid"),
                rev_id = raw_json.get("revid"),
                title = raw_json.get("title")
            )
            if result.url != raw_json.get("url"):
                logger.error(f"URL is not correctly parsed, {result.url}, {raw_json.get("url")}")
                raise
        except KeyError:
            logger.error(f"Incorrect format for {raw_json}")
            raise

        return result


@dataclass
class Entry:
    _id: ID
    question: str
    answer: list[str]
    depends_on: list[ID]
    evidence: Evidence|None = field(default=None)
    decomposition: list[Self] = field(default_factory=list)
    categories: list[Categories] = field(default_factory=list)

    # Class variables
    categories_all: ClassVar[set[str]] = set()

    @classmethod
    @no_type_check
    def from_json(cls, raw_json: dict) -> Self:
        try:
            result: Self = cls(
                _id = raw_json.get("id"),
                question = raw_json.get("question"),
                answer = raw_json.get("answer"),
                depends_on = raw_json.get("depends_on"),
            )
        except KeyError:
            logger.error(f"Incorrect format for {raw_json}")
            raise

        try:
            decomposition = raw_json.get("raw_composition")
        except KeyError:
            logger.debug(f"Find answer composition {len(decomposition)}")

        try:
            categories: list[str] = raw_json.get("categories")
        except KeyError:
            logger.debug(f"No category information included.")
        else:
            if categories not in Categories:
                cls.categories_all.update(categories)

        try:
            evidence = Evidence.from_json(raw_json.get("evidence"))
        except (AttributeError, KeyError):
            logger.debug(f"Cannot get evidence")
        else:
            result.evidence = evidence

        return result



def main() -> None:
    entries: list[Entry] = []
    with open("data/raw/fanout-dev.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        for entry in raw:
            entries.append(Entry.from_json(entry))

    logger.info(f"Total entry: {len(entries)}")
    logger.info(f"All categories: \n{"\n".join([f"    {category} = {i}"\
        for i, category in enumerate(Entry.categories_all)])}")

if __name__ == "__main__":
    main()