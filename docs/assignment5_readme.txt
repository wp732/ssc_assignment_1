# NOTE 1: For assignment 5, I did not want to incur the overhead of git actions
#         having to install all of the tools needed for CI processing each time a push
#         was invoked, so I decided to design a solution where the CI tooling was
#         pre-built into a Docker container that could be used by the GitHub runner
#         in the git actions workflow. The idea is at workflow time, the container
#         would start up and the actions would clone this repo into the container and
#         execute the tests required.
#         The cicd/citool directory contains the Dockerfile used to build this container.
#         There are docker helper scripts in the bin directory of this project to build
#         and publish the container to the GitHub ghcr.io container registry.
#         Documentation for using ghcr.io can be found here:
#         https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

# NOTE 2: Please refer to docs/assignment4_readme.txt for details on using keepass vault.

# Here are the steps to build and publish the container:

# Create an admin GitHub PAT (classic) for publishing to ghcr.io

# Add the admin PAT to local keepassxc vault (this will be used by bin/dockerghpublish.sh)

	bin/keepass_add_pair.sh ghcr_admin

# Note: The following labels were added to cicd/citool/Dockerfile so it could be
# published properly:

	LABEL org.opencontainers.image.source=https://github.com/wp732/ssc_assignment_1
	LABEL org.opencontainers.image.description="Container for Python CI tooling"
	LABEL org.opencontainers.image.licenses="Apache-2.0"

# Run the command to build the container

	SSC_SRC_DIR=cicd/citool bin/dockerbuild.sh

# Run the command to publish the container to ghcr.io 

	SSC_SRC_DIR=cicd/citool bin/dockerghpublish.sh

# After publication I change permissions for the container to read only 
# via Package Settings at https://github.com/wp732/ssc_assignment_1/pkgs/container/citool

# With the citool container in place, I then cretaed .github/workflows/ci.yml that makes
# use of the this container during the test: job that gets trigger when a push to main
# branch occurs. The test job will launch the container in a GitHub runner (you will
# note I use ubuntu-24.04-arm for the runner since I built my container on my
# Raspberry PI system and didn't want to worry about any quirks with it running on an
# x64 runner.  

# Once the container is launched, the test job steps that follow clone the repo into
# the contianer and then run the requisite verifiaction tools are per the assignment
# rubric. The step called "Add missing import packages" runs a script of similar name
# whose job is to run a poetry add -D for any source project under packages directory
# in order to ensure that packages for imports in those package level pyproject.toml
# files get installed prior to running tools like pytest which will fail to execute
# tests properly if those import dependecy packages are not installed prior to testing.
