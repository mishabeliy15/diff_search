import sys
from bs4 import BeautifulSoup
from bs4.element import Tag

TARGET_ID = 'make-everything-ok-button'


def find_target(file, id):
    soup = BeautifulSoup(open(file, 'r').read(), 'html.parser')
    return soup.find(attrs={'id': id})


def calculate_similarity(a, b):
    equals = int(a.name == b.name)
    params = len(a.attrs) + 1
    for i in a.attrs:
        if i in b.attrs:
            if isinstance(a.attrs[i], (list,  tuple)) and len(a.attrs[i]):
                s1, s2 = set(a.attrs[i]), set(b.attrs[i])
                equals += len(s1.intersection(s2)) / len(s1)
            else:
                equals += int(a.attrs[i] == b.attrs[i])
    return equals / params


def find_similar(target_dom, node):
    similarity = -1
    best_node = node
    for i in node.contents:
        if isinstance(i, Tag):
            if len(target_dom) == 1:
                temp_sim = calculate_similarity(target_dom[-1], i)
                if temp_sim > similarity:
                    best_node = i
                    similarity = temp_sim
            else:
                node_sim = [find_similar(target_dom, i), find_similar(target_dom[:-1], i)]
                maxi = int(node_sim[1][1] > node_sim[0][1])
                if node_sim[maxi][1] > similarity:
                    best_node = node_sim[maxi][0]
                    similarity = node_sim[maxi][1]
    return best_node, similarity


if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) == 3:
        TARGET_ID = params[2]
    target = find_target(params[0], TARGET_ID)
    dom_parents_target = [target] + list(target.parents)[:-1]
    search_html = BeautifulSoup(open(params[1], 'r').read(), 'html.parser')
    found, sim = find_similar(dom_parents_target, search_html)
    print(f'Similarity: {sim}')
    print(' > '.join(list(map(lambda x: f'{x.name}[{x.attrs}]',
                              reversed([target] + list(found.parents)[:-1])))))