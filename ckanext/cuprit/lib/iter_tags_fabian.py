import json
import pickle
from typing import Dict

# load data from thesauri.json file
with open(r"tags_export.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# keys defining relations
parent_relation = "http://www.w3.org/2004/02/skos/core#broader"
child_relations = "http://www.w3.org/2004/02/skos/core#narrower"
top_level_parent_id = "http://thesauri.dainst.org/_fe65f286"
names = "http://www.w3.org/2004/02/skos/core#prefLabel"
exclude_parent_terms = [
    "http://thesauri.dainst.org/_8cb35559",
    "http://thesauri.dainst.org/_e140fe64",
    "http://thesauri.dainst.org/_474fdc79",
    "http://thesauri.dainst.org/_4dc296b2",
    "http://thesauri.dainst.org/_5c891c93",
    "http://thesauri.dainst.org/_4fa4ce58",
    "http://thesauri.dainst.org/_17b15592",
    "http://thesauri.dainst.org/_b724c3f2",
    "http://thesauri.dainst.org/_5a1e0444",
    "http://thesauri.dainst.org/_49676276",
]


def get_label(id: str) -> str:
    """
    Find the german label for a given ID.
    """
    for element in data:
        if element["@id"] != id:
            continue
        for e in element[names]:
            if e["@language"] != "de":
                continue
            de_term = e["@value"].strip()
    return de_term


def flatten_two(parent_key: str, prefix: str, tags: Dict[str, list]) -> Dict[str, list]:
    """
    Flatten DAG into dict with parents as key and children as values.
    """
    if parent_key in exclude_parent_terms:
        return tags
    for element in data:
        if element["@id"] != parent_key:
            continue
        if child_relations in element:
            children = [child["@id"] for child in element[child_relations]]
            label = (
                f"{prefix} - {get_label(parent_key)}"
                if parent_key != top_level_parent_id
                else get_label(parent_key)
            )
            tags[label] = children
            for c in children:
                flatten_two(c, label, tags)
        return tags


def main():
    tags = flatten_two(top_level_parent_id, "", {})
    for k, v in tags.items():
        tags[k] = [get_label(term) for term in v]

    print(json.dumps(tags, indent=4, ensure_ascii=False))

    with open("tags.pickle", "wb") as file:
        pickle.dump(tags, file, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
