import json
import urllib
from .models import UvaProblems


def title_match(title):
    titles = ['Divide and Conquer', 'Dynamic Programming', 'String Processing with Dynamic Programming',
              'Network Flow', 'Game Theory', 'Graph Traversal', 'Single-Source Shortest Paths (SSSP)', 'Problem Decomposition',
              'Introduction', 'Mathematics', '(Computational) Geometry', 'Combinatorics', 'Probability Theory', 'Number Theory']
    if title in titles:
        return True
    return False


def RefreshProblem():
    # all problems with catagory
    url = "http://uhunt.felix-halim.net/api/cpbook/3"
    result = json.load(urllib.urlopen(url))

    for r in result:
        fm = 0
        mtitle = r["title"]
        if title_match(mtitle):
            fm = 1
        for rr in r["arr"]:
            fs = 0
            stitle = rr["title"]
            if title_match(stitle):
                fs = 1
        if fm == 1 or fs == 1:
            for rrr in rr["arr"]:
                for rrrr in rrr:
                    if fm == 1:
                        if rrrr < 0:
                            rrrr *= -1
                        p_url = "http://uhunt.felix-halim.net/api/p/num/" + \
                            str(rrrr)
                        problem = json.load(urllib.urlopen(p_url))
                        print problem
