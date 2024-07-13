This should identify all module inter-dependencies on our system, create a
graph structure out of that, and maybe even visualise that graph. Mostly for
fun, but this could be useful if we ever wish to *replace* one module with
another completely or identify modules affected by a severe vulnerability.

## Setup
You should have conda configured already. Create the environment with

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
