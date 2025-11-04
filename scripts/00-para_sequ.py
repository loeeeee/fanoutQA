# This is a self-contained python script that answers,
# "How much of the QA is fully parallel, and how much of the QA is fully sequential?"
# Parallel here means that to answer the questions, one aggregates information from different Wikipedia pages,
# and the pages contains the group truth directly answering one small part of the questions
# Sequential means that to answer the questions, one ask another question, and follow the logic of that questions...

from dataclasses import dataclass, field
from enum import Enum
from typing import Self, TypeAlias, TypedDict
import json

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

@dataclass
class Entry:
    _id: ID
    question: str
    decomposition: list[Self]
    answer: list[str]
    depends_on: list[ID]
    evidence: Evidence
    categories: list[Categories]

def main() -> None:
    with open("raw/fanout-dev.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        