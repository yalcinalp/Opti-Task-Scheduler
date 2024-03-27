# Import the required libraries
import json

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# URL to Search all issues.
url = "https://algorithmicacrobats.atlassian.net/rest/api/2/search"

# Create an authentication object,using
# registered emailID, and, token received.
auth = HTTPBasicAuth(
    "abc@gmail.com",
    "token",
)

# The Header parameter, should mention, the
# desired format of data.
headers = {"Accept": "application/json"}
# Mention the JQL query.
# Here, all issues, of a project, are
# fetched,as,no criteria is mentioned.


class IssueLink:
    def __init__(self, issue_link):
        self.id = issue_link["id"]
        self.type = issue_link["type"]["name"]
        self.blocks = issue_link["outwardIssue"]["key"]


class Issue:
    def __init__(self, issue):
        self.key = issue["key"]
        self.summary = issue["fields"]["summary"]
        self.status = issue["fields"]["status"]["name"]
        self.due_date = issue["fields"]["duedate"]
        self.time_estimate = issue["fields"]["timeestimate"]
        self.issue_links = [
            IssueLink(issue_link)
            for issue_link in issue["fields"]["issuelinks"]
            if "outwardIssue" in issue_link
        ]
        self.eet = None
        self.let = self.due_date
        self.est = None
        self.lst = None

    def __repr__(self):
        return f"{self.key}"

    def __str__(self):
        return f"{self.key}"

    def __eq__(self, other):
        return self.key == other

    def __hash__(self):
        return hash(self.key)


def get_issues(jql: str = "ORDER BY duedate DESC") -> map:
    issues = json.loads(
        requests.request(
            "GET", url, headers=headers, auth=auth, params={"jql": jql}
        ).text
    )["issues"]

    issues = [Issue(issue) for issue in issues]
    graph = make_graph(issues)
    return topological_sort(graph, issues)


def make_graph(issues: list) -> dict:
    graph = {}
    for issue in issues:
        graph[issue] = set()
        for issue_link in issue.issue_links:
            graph[issue].add(issue_link.blocks)
    return graph


def topological_sort_old(graph: dict, nodes: dict) -> (list, dict):
    visited = set()
    stack = []
    nodes_dict = {node.key: node for node in nodes}

    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor)
            stack.append(nodes_dict[node])

    for node in graph:
        dfs(node)

    return stack[::-1]


def topological_sort(graph: dict, nodes_list: list) -> (list, dict):
    nodes_dict = {node.key: node for node in nodes_list}
    ingoing = {node: 0 for node in graph}
    for node in graph:
        for outgoing in graph[node]:
            ingoing[outgoing] += 1
    zeros = [node for node in ingoing if ingoing[node] == 0]

    while zeros:
        node = zeros.pop()
        for outgoing in graph[node]:
            ingoing[outgoing] -= 1
            if ingoing[outgoing] == 0:
                zeros.append(outgoing)
        yield nodes_dict[node]


if __name__ == "__main__":
    print(list(get_issues()))
