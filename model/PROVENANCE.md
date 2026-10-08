# Metamodel provenance

The vendored files were first imported in PyUML2 commit
`edd94a107c80b226b0ef5d65505a39fafd29c17a` (Add first import of existing code).
They are unchanged at the migration baseline
`bbea7442b2f4ba0870c42c15e4738e86ba90ea49`.

Both declare Eclipse UML2 namespace version **5.0.0**. This is the namespace
version, not evidence of a particular OMG UML specification release.
The `2.0.0/UML` annotation identifies annotation vocabulary, not model version.

| File | SHA-256 |
| --- | --- |
| types.ecore | `9be649cf32f3257d2373ce564d85a24924a6d1268da849b10bdb0e6461888ac8` |
| uml.ecore | `20cd5d8f6a7554052ad156db54b6855fc7eb47c4d9d88af53a896ca434035936` |

The original bytes and repository BSD 3-Clause LICENCE are preserved.
Neither Ecore file contains an individual copyright/license header or an
upstream release tag/download URL. Their exact Eclipse artifact release and
separate upstream license attribution are **unverified**; do not infer that
the repository license establishes the upstream models’ license.
No external model was downloaded or substituted during this migration.

The local example/sysml branch contains `pysysml/sysml14` and the namespace
`http://www.eclipse.org/papyrus/sysml/1.4/SysML`: it is a SysML 1.4 prototype,
not SysML v2 and not part of the shipped base runtime. See the harness
UPSTREAM_BRANCH_INVENTORY.md for the distinct unmerged profile prototypes.
