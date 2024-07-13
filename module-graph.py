#!/usr/bin/env python3
import subprocess
import json
from typing import TypedDict
from pathlib import Path

from tqdm import tqdm


class ModuleDict(TypedDict):
    name: str           # Full "$name/$version" for this module
    type: str           # Think this is always "modulefile"
    symbols: list       # No idea what this is, empty for all of our modules
    tags: list          # List of tags, but don't think we use tags anywhere
    pathname: Path      # Absolute filepath of this modulefile


ModulePathDict = dict[str, ModuleDict]          # Key = "$name/$version" of module, e.g. "minimap2/2.28"
GlobalModuleDict = dict[str, ModulePathDict]    # Key = modulepath, e.g. "/apps/modulefiles"


#def main():
shell_output = subprocess.run("module avail --json", capture_output=True, shell=True)
shell_output = shell_output.stdout.decode("utf-8")
# This has keys which are the module paths, and the values are
global_module_dict: GlobalModuleDict = json.loads(shell_output)
print(f"Module paths are {list(global_module_dict.keys())}")

# For now, let's just pick a single modulepath, can expand later
#module
import networkx as nx
G = nx.DiGraph()
modules = global_module_dict["/apps/modulefiles"]
G.add_nodes_from(modules.keys())

import re
regex = re.compile(r"^\s*module\s+load\s+(?P<loaded_modules>.*)")

for name, module in tqdm(tuple(modules.items())):
    o = subprocess.run(f"module show {name}", capture_output=True, shell=True)
    o = o.stdout.decode("utf-8").split("\n")
    all_loaded_modules = []
    for line in o:
        match = regex.match(line)
        if not match:
            continue
        loaded_modules = match.group("loaded_modules")
        # In case multiple modules are loaded on same line, ensure any whitespace is collapsed into exactly one whitespace character
        loaded_modules = re.sub("\s+", " ", loaded_modules)
        loaded_modules = loaded_modules.split(" ")
        all_loaded_modules.extend(loaded_modules)
    #print(f"* {name:<16} loads: {all_loaded_modules}")
    edges = [(name, loaded) for loaded in all_loaded_modules]
    G.add_edges_from(edges)

# Draw graph
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(24, 24), dpi=600)
nx.draw(G, with_labels=True, arrows=True)
#plt.savefig("module-graph.png")

nx.draw(G, with_labels=True, arrows=True, pos=nx.kamada_kawai_layout(G))
#plt.savefig("module-graph-kamada_kawai_layout.png")

nx.draw(G, with_labels=True, arrows=True, pos=nx.arf_layout(G))
#plt.savefig("module-graph-arf_layout.png")

nx.draw(G, with_labels=True, arrows=True, pos=nx.spectral_layout(G))
#plt.savefig("module-graph-spectral_layout.png")

# Only draw subgraph showing all depencies and dependents of a particular module
def focus_on_module(target: str):
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    subgraph_nodes = [target]
    preds = [n for n in G.predecessors(target)]
    succs = [n for n in G.successors(target)]
    subgraph_nodes.extend(preds)
    subgraph_nodes.extend(succs)
    subgraph = G.subgraph(subgraph_nodes)    
    print(f"Subgraph of {target} has nodes: {subgraph.nodes}")
    # Label all of the nodes
    attrs = {target: {"subset": "target"}}
    attrs.update({n: {"subset": "pred"} for n in preds})
    attrs.update({n: {"subset": "succ"} for n in succs})
    nx.set_node_attributes(subgraph, attrs)
    print(attrs)
    #nx.draw(subgraph, with_labels=True, arrows=True)
    #filename = f"module-graph-{target.replace('/', '_')}.png"
    #print(f"Saving subgraph to '{filename}'")
    #plt.savefig(filename)
    nx.draw(subgraph, with_labels=True, arrows=True, pos=nx.multipartite_layout(subgraph))
    filename = f"module-graph-{target.replace('/', '_')}-multipartite.png"
    print(f"Saving subgraph to '{filename}'")
    plt.savefig(filename)

#if __name__ == "__main__":
#    main()
