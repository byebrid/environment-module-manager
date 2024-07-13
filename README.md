# Environment module manager
This is for managing and inspecting Linux [environment
modules](https://modules.readthedocs.io/en/latest/). The exact feature set is
currently undecided, but this might be used to:
- Identify all modules that depend on some other module, or conversely identify all modules that a module depends on.
- Identify a valid order in which to rebuild a subset of modules, e.g. to backport a security-patched module.
- Produce an image of the network of all modules and their dependences.
- Identify modules that do not load or unload correctly.


## Setup
You should have [conda](https://conda.io/projects/conda/en/latest/index.html) configured already. Create the environment with

```console
$ mamba env create --file=environment.yml --name=environment-module-manager
```

And then activate it with
```console
$ mamba activate module-graph
```


## Desirable features
- [ ] Easily identify `module load`s of *unversioned* modules. E.g. `module load gmp` rather than `module load gmp/6.3.0`.
- [ ] Determine the order in which the entire set of modules could be rebuilt. E.g. you would have to rebuild `hpcx` before rebuilding many other modules.
- [ ] Ensure that the user's environment is identical before loading and after unloading a module.
- [ ] Easily list all dependents of a a module.
- [ ] Easily list all depedencies of a module.
- [ ] Choose maximum depth of dependents/dependencies to list. E.g. you may only want to list *direct* dependencies so would set `--max-depth=1`.
- [ ] Choose whether to analyse a single modulepath or all modulepaths simultaneously.
- [ ] Easily identify modules whose dependencies/dependents exist in distinct modulepaths.
- [ ] Cache a module graph for quicker analysis.
- [ ] Have option to refresh a cached module graph, e.g. when a new modulefile has been created.
- [ ] Export entire module graph to image file.
- [ ] Check if there are any cycles in the graph.
- [ ] List executables from a given module???
