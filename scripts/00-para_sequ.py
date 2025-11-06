# This is a self-contained python script that answers,
# "How much of the QA is fully parallel, and how much of the QA is fully sequential?"
# Parallel here means that to answer the questions, one aggregates information from different Wikipedia pages,
# and the pages contains the group truth directly answering one small part of the questions
# Sequential means that to answer the questions, one ask another question, and follow the logic of that questions...

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Self, TypeAlias, no_type_check
import json
import logging
import urllib.parse
from functools import cached_property

logging.basicConfig(
    filename="data/runtime.log",
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s'
)
logger = logging.getLogger(__name__)

ID: TypeAlias = str


@dataclass
class Evidence:
    page_id: int
    rev_id: int
    title: str

    safe_chars: ClassVar[str] = "/():,-#"

    @property
    def url(self) -> str:
        return f"https://en.wikipedia.org/wiki/{urllib.parse.quote(self.title.replace(' ','_'), safe=self.safe_chars)}"

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
                logger.debug(f"URL is not correctly parsed, {result.url}, {raw_json.get("url")}")
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
    categories: list[str] = field(default_factory=list)

    # Class variables
    categories_all: ClassVar[set[str]] = set()

    @classmethod
    @no_type_check
    def from_json(cls, raw_json: dict) -> Self:
        # Basic info
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

        # Entry hierarchy
        try:
            decomposition = raw_json.get("decomposition")
        except KeyError:
            logger.debug(f"Cannot find answer decomposition")
        else:
            if decomposition:
                # Create all entries
                child_entries: Dict[ID, Entry] = {ent._id: ent \
                    for ent in [cls.from_json(entry) for entry in decomposition]}
                child_entries_inferred: Dict[ID, Entry] = {}

                # Build hierarchy based on dependency
                for _id, entry in child_entries.items():
                    # Assume a single path dependency
                    if len(entry.depends_on) == 1:
                        parent_id = entry.depends_on[0]
                        # Move it to the new place
                        child_entries_inferred[parent_id].decomposition.append(entry)
                    elif len(entry.depends_on) > 1:
                        # Only log, do nothing else
                        logger.warning(f"Multi-path dependency detected, {result.question}")
                        for parent_id in entry.depends_on:
                            logger.warning(f"It depends on {child_entries[parent_id].question}")
                    else:
                        # Do nothing when all are parallel
                        pass

        # Additional info
        try:
            categories: list[str] = raw_json.get("categories")
        except KeyError:
            logger.debug(f"No category information included.")
        else:
            if categories:
                cls.categories_all.update(categories)
                result.categories.extend(categories)

        # Source
        try:
            evidence = Evidence.from_json(raw_json.get("evidence"))
        except (AttributeError, KeyError):
            logger.debug(f"Cannot get evidence")
        else:
            result.evidence = evidence

        return result

    def __repr__(self) -> str:
        """
        recursively create indented string
        """
        last_level: str = ""
        for level in self.decomposition:
            last_level += f"{'\n    '.join(str(level).split('\n'))}"
        this_level: str = f"\n- {self.question}{last_level}"
        return this_level

    @cached_property
    def hop_simple(self) -> int:
        """
        return number of hop to get to the answer
        """
        hop: int = 1
        if not self.decomposition:
            """
            recursion ends: no more decomposition -> answer reached
            """
            return hop

        """
        recursion: find the deepest, we assume all entry in decomposition is at the same level
        """
        child_hops: list[int] = [_.hop_simple for _ in self.decomposition]
        hop += max(*child_hops) if len(child_hops) > 1 else child_hops[0]
        return hop

    @cached_property
    def hop_inferred(self) -> int:
        """
        return number of hop to get to the answer
        """
        hop: int = 1
        if self.depends_on:
            """
            Assume entry only has one path of dependency
            """
            hop += 1

            if len(self.depends_on) > 1:
                logger.warning(f"Encounter multi-path dependency, {self}")

        if not self.decomposition:
            """
            recursion ends: no more decomposition -> answer reached
            """
            return hop

        """
        recursion: find the deepest, we infer the dependency in decomposition
        """
        child_hops: list[int] = [_.hop_inferred for _ in self.decomposition]
        hop += max(*child_hops) if len(child_hops) > 1 else child_hops[0]
        return hop



def main() -> None:
    entries: list[Entry] = []
    with open("data/raw/fanout-dev.json", "r", encoding="utf-8") as f:
        raw = json.load(f)
        for entry in raw:
            entries.append(Entry.from_json(entry))

    logger.info(f"Total entry based on JSON: {len(raw)}")
    logger.info(f"Total entry: {len(entries)}")

    entries_by_hop: dict[int, list[Entry]] = {}
    for entry in entries:
        if not entry.hop_simple in entries_by_hop:
            entries_by_hop[entry.hop_simple] = [entry]
        else:
            entries_by_hop[entry.hop_simple].append(entry)

    for hop, entries_same_hop in entries_by_hop.items():
        logger.info(f"Now visualizing entries with hop {hop}")
        logger.info(f"{len(entries_same_hop)} entries in total")
        for entry in entries_same_hop:
            logger.info(f"Simple visualization: {entry}")


    # logger.info(f"All categories: \n{"\n".join([f"{category}"\
    #     for i, category in enumerate(Entry.categories_all)])}")

if __name__ == "__main__":
    main()