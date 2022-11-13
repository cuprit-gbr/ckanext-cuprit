import json
import pickle

# load data from thesauri.json file
with open("thesauri.json", "r") as f:
    data = json.load(f)

# keys defining relations
parent_relation = "http://www.w3.org/2004/02/skos/core#broader"
child_relations = "http://www.w3.org/2004/02/skos/core#narrower"
top_level_parent_id = "http://thesauri.dainst.org/_fe65f286"
names = "http://www.w3.org/2004/02/skos/core#prefLabel"
exclude_terms = ["Donald", "Trump"]


# Todo: maybe merge with find_relations() and use generator instead
def find_parents(data: dict) -> list:
    """
    Find all parents of the given data.
    """
    flattened_data = {}
    mapping_dict = {}
    for element in data:
        if parent_relation in element:
            if element[parent_relation][0]["@id"] == top_level_parent_id:
                for e in element[names]:
                    if e["@language"] == "de":
                        de_term = e["@value"]
                        element_id = element["@id"]
                        flattened_data[de_term] = []
                        mapping_dict[element_id] = de_term
    return [flattened_data, mapping_dict]


def find_relations(parent_key: str, data: dict, childs: list) -> list:
    """
    Find all partent child relations
    """
    for element in data:
        if element["@id"] == parent_key:
            has_relations = element.get(child_relations)
            if has_relations is None:
                for e in element[names]:
                    if e["@language"] == "de" and e["@value"] not in exclude_terms:
                        childs.append(e["@value"])
                    continue
            else:
                for relation in has_relations:
                    find_relations(relation["@id"], data, childs)

    return childs


def main():
    # iter parent child relations
    flattened_data, mapping_dict = find_parents(data)
    for k, v in mapping_dict.items():
        flattened_data[mapping_dict[k]] = find_relations(k, data, [])
    print(flattened_data)

    # pickle object to store
    with open("tags.pickle", "wb") as file:
        pickle.dump(flattened_data, file, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
