# NOTE 1: The directory structure of the repo has changes from assignment3.
#         Since the location of the rekor/src files where moved to
#         packages/wp732-rekor-tools/src/wp732/rekor_tools so that they can
#         reside in a tree structure amenable to package publishing, changes
#         were made to the directory discovery functions in tests/run_test_wrappers.py

# NOTE 2: In order to not bloat the package to be published with test tool dependencies,
#         two separate pyproject.toml files now exist in this repo. The one at the root
#         level of the repo was refactored to only deal with test tooling and another
#         one was placed in the packages/wp732-rekor-tools dedicated to the package
#         build and dependencies configuration.

# NOTE 3: Due to the bifurcation of pyproject.toml files mentioned above, in order for
#         the test tools to work I needed to run the following command which executes
#         a poetry "editable install" (basically a symlink of package source into
#         the root level venv created by poetry when poetry install was run at repo
#         root level.
 
poetry add -D ./packages/wp732-rekor-tools
