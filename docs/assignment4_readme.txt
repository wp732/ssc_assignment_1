## Part 1: Publishing packages to PyPi via poetry publish

# NOTE 1: The directory structure of the repo has changes from assignment3.
#         Since the location of the rekor/src files where moved to
#         packages/wp732-rekor-tools/src/wp732/rekor_tools so that they can
#         reside in a tree structure amenable to package publishing, changes
#         were made to the directory discovery functions in tests/run_test_wrappers.py

# NOTE 2: In order to not bloat the package to be published with test tool dependencies,
#         two separate pyproject.toml files now exist in this repo. The one at the top
#         level of the repo was refactored to only deal with test tooling and another
#         one was placed in the packages/wp732-rekor-tools dedicated to the package
#         build and dependencies configuration. It is important to note that the top
#         level pyproject.toml be configured with package-mode = false under the
#         [tool.poetry] section so that it is not considered as part of any poetry
#         package builds.

# NOTE 3: Due to the bifurcation of pyproject.toml files mentioned above, in order for
#         the test tools to work I needed to run the following command at repo top level
#         directory which executes a poetry "editable install" (basically a symlink of
#         the package source into the top level venv created by poetry when poetry install
#         was run at repo top level.
 
			poetry add -D ./packages/wp732-rekor-tools

# NOTE 4: If you want to include a license file as part of the package to be published
#         to PyPi, you will need to have include = ["LICENSE"] under the [tool.poetry]
#         section of the package level pyproject.toml but you will also need to copy the
#         LICENSE file to the same directory as unfortunately include directives cannot
#         use relative path addressing (i.e. you can't have ../../LICENSE or use a
#         symlink), so annoying as it is, you will need to maintain a license file per
#         package.

# NOTE 5: The symlink of packages/wp732-rekor-tools/README.md to
#         packages/wp732-rekor-tools/src/wp732/rekor_tools/README.md was done because
#         the only way to get the README.md to show up in the whl file but still be
#         found by PyPi when published was to keep it in the source level directory
#         and specify a relative path to it in the pyproject.toml, but I also wanted
#         github to display it at the top level of the package so the symlink was the solution.

# NOTE 6: Prior to directory structure refactoring, pytest-cov was yielding 80%, but
#         after refactoring I was only getting 50% because merkle_proof.py and utils.py
#         were yielding 0% coverage! I discovered I needed to change PYTHONPATH from using
#         just dot (".") to the following in the top level pyproject.toml:

			[tool.pytest.ini_options]
			env = ["PYTHONPATH=packages/wp732-rekor-tools/src:tests"]

# NOTE 7: The screenshot in the assignment 4 pdf showed an example of the Rekor commands
#         being run via a wrapper script as opposed to via python main.py so I wanted to
#         include a wrapper script but wasn't sure if making a bash wrapper was wise
#         since that assumes bash is available on target systems. I was considering using
#         a /usr/bin/env python shebang top line but what if python3 was not aliased to
#         python or vice versa? I then discovered this very cool method of having poetry
#         inject and entry_points.txt with a [console_scripts] section into the package
#         whl that instructs pip on an install to generate the proper wrapper script
#         shebang and bootstrap code! I just included the following in the package's
#         pyproject.toml file:         

				[tool.poetry.scripts]
				wp732_rekor_tool = "wp732.rekor_tools.main:main"

# That generated the following script called wp732_rekor_tool when I did a pip install
# from the whl file in a venv python (not even a poetry venv):
# 

			#!/home/user/.penv/test/bin/python3
			# -*- coding: utf-8 -*-
			import re
			import sys
			from wp732.rekor_tools.main import main
			if __name__ == '__main__':
				sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
				sys.exit(main())

# Then from my venv activated environment I could run wp732_rekor_tool -h
# or wp732_rekor_tool -c and it all worked. Very cool :-)

# Note 8: In order to not have to entry very long PyPi token during each poetry publish
#         Add to securely store it locally, I developed scripts to install and use
#         keepassxc as a local password manager. Note that keepassxc uses the terms
#         username and password for key and value to be stored in the database.
#         Also note that for each script you will be prompted to enter a database password.

			bin/keepass_create_db.sh			# Install keepassxc and create its database

			bin/keepass_add_pair.sh pypitok		# Create key pypitok and prompt you for value

			bin/keepass_get_value.sh pypitok	# Get back the token for key pypitok

# NOTE 9: I created a wrapper script for poetry publish that fetches the token into
#         the environment variable.

# So after all this setup work, here were the steps to build and publish:

# Building the package

	cd packages/wp732-rekor-tools
	poetry build

# Once the build completes, there will be a dist/ directory with the build package to be
# published.

# To do a local test of the package using a non-poetry python venv pip install, I created
# a python venv and then activated it and then ran the following command (where
# <repo path> was the directory path to the root of my local cloned git repo):

	pip install \
		--force-reinstall \
		<repo path>/packages/wp732-rekor-tools/dist/wp732_rekor_tools-4.0.0-py3-none-any.whl

# The --force-reinstall was needed to re-test multiple times.

# Publishing

# From the packages/wp732-rekor-tools directory I ran the following:

	../../bin/publish.sh 
	Enter password to unlock /home/user/.config/keepass/myvault.kdbx: 

	Publishing wp732-rekor-tools (4.0.0) to PyPI
	 - Uploading wp732_rekor_tools-4.0.0-py3-none-any.whl 100%
	 - Uploading wp732_rekor_tools-4.0.0.tar.gz 100%

# Testing

# Now that the package has been published, you can simply pip install it to any local python
# environment (be it venv or not). Just run the following:

	pip install wp732-rekor-tools

# After the install complete you can simply run the tool (for example: wp732_rekor_tool -h)

## Part 2: SBOM generation and package attestation

# First cd to top level of the repo so the following commands are acting on the top level
# pyproject.toml file.

# Install CycloneDX software to generate SBOM

	poetry add --dev cyclonedx-bom	# run where repo top level pyproject.toml resides

# Install plugin to enable poetry to generate a requirements.txt file

	poetry self add poetry-plugin-export

# Generate a requirements.txt
# NOTE: I could not find a way with the version of cyclonedx-bom installed (7.2.1) to instruct
#       it to only create an SBOM pertaining to the package level pyproject.toml declarations.
#       It seemed to only be designed to handle repos structured to use a single pyproject.toml
#       and not the bifurcation approach I took as explained above. The workaround I found was
#       to configure poetry to generate a transient requirements.txt file from the package
#       level pyproject.toml and use that to create the scoped SBOM I desired. What follows
#       are the steps to do that:

	pushd packages/wp732/	# move from repo top level to package level
	poetry export -f requirements.txt --output requirements.txt

# Add a .gitignore as we don't care about preserving these package level files in GitHub
# since we already preserve the package level pyproject.toml.

	cat<<EOF > .gitignore
	requirements.txt
	poetry.lock
	EOF

# Generate the SBOM from the transient requirements.txt

	popd	# go back to top level of repo
	poetry run cyclonedx-py requirements packages/wp732-rekor-tools/requirements.txt --of JSON -o packages/wp732-rekor-tools/dist/cyclonedx-sbom.json
	git add packages/wp732-rekor-tools/dist/cyclonedx-sbom.json

