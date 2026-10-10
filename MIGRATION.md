# Migration to the Python 3.14 fork line

This is an unreleased documentation draft, not a publication or version decision.
The existing distribution name `pyuml2` and version `0.0.1.dev0`
remain unchanged. A PyPI fork name and release/prerelease version require a separate
human decision; no ownership of upstream names is implied.

CPython 3.12, 3.13 and 3.14 standard with GIL are qualified on Linux x86_64.
Python <3.12 is outside this line. Windows, macOS, other architectures, PyPy and
free-threaded Python are NOT_RUN. Metadata >=3.12 is not a promise about future
Python versions.

Do not replace the shipped UML code with the candidate: 197 constructors become keyword-only and ActivityContent.__init__ loses **kwargs. Profiles, SysML and OCL-derived operations remain separate, unmerged work. Model release/license provenance limits are retained in model/PROVENANCE.md.

Use local, provenance-checked ecosystem wheels together. The accepted T12 closure
passes 911 tests per environment for both supported-minimum and recent profiles,
each on 3.12/3.13/3.14 source and wheel. The supported closure uses setuptools
83.0.0, pytest 9.0.3, lxml 6.1.0, Jinja2 3.1.6, ordered-set 4.0.1, autopep8 2.0.0
and build 1.0.0; exact transitives are in the qualification locks. Historical
setuptools 77.0.1/pytest 8.0.0 compatibility results are not supported minimums.
Audits on 2026-10-09 reported no known advisories for the two supported profiles;
this is dated evidence, not a security guarantee.

For rollback, create a separate checkout at known qualified commit
`a3071ed2276a581a469408ff3c920b85d2605d5d` and reinstall the matching complete
closure from its hashed locks in a fresh environment. Do not mix isolated old
components with new ones or overwrite a dirty checkout. Back up models and
application-generated code before migration. The original upstream baseline
`bbea7442b2f4ba0870c42c15e4738e86ba90ea49` is historical, not qualified for Python
3.14 and not a safe default rollback environment.

Keep `LICENCE` and existing author/copyright notices with redistributed code.
The ecosystem delivery guide lives in the separate pyecore-codex-harness pilot
repository (`docs/MIGRATION_GUIDE.md`, `docs/PYTHON_SUPPORT.md`,
`docs/RELEASE_PLAN.md`). Documentation drafts are separate from the frozen T12
artifacts until reviewed and committed.
