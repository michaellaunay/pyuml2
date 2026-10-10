Unreleased — Python 3.14 migration (release decision pending)
=============================================================

- CPython >=3.12 metadata; qualified 3.12/3.13/3.14 standard with GIL on Linux x86_64 only.
- Build backend setuptools >=83.0.0 and test extra pytest >=9.0.3. Project/module names, nsURI, licenses and author credits are retained.
- Modern packaging retains the historical generated UML API, runtime mixins, skeletons and metamodel resources.
- Installed UML instances pass XMI/JSON round-trips with the generic PyEcore JSON opposite-reference correction.
- An isolated, deterministic and importable regeneration candidate is compared but not integrated.

Do not replace the shipped UML code with the candidate: 197 constructors become keyword-only and ActivityContent.__init__ loses **kwargs. Profiles, SysML and OCL-derived operations remain separate, unmerged work. Model release/license provenance limits are retained in model/PROVENANCE.md.
