# Optional Solo Builder integration

ReuseForge is standalone. This integration is optional.

When `Solo Builder Dev Orchestrator` is installed, its Reuse Review policy may invoke the minimal ReuseForge chain before Solo Builder DEV Gate C:

`reuseforge-orchestrator -> reuseforge-project-framer -> reuseforge-asset-scout -> reuseforge-candidate-auditor -> reuseforge-solution-architect`

Then control normally returns to Solo Builder DEV Gate C unless the Human explicitly chooses the full ReuseForge path through planning and execution handoff.

Authority remains separate:

- Solo Builder owns the top-level software-development lifecycle and DEV Gates A-E.
- ReuseForge owns the reuse subworkflow and RF Gates A-C.
- ReuseForge does not replace repository execution authority or private runtime orchestration.
