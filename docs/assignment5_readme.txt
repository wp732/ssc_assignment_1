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

## Part 1: CI

# With the citool container in place, I then created .github/workflows/ci.yml that makes
# use of the this container during the test: job that gets trigger when a push to main
# branch occurs. The test job will launch the container in a GitHub runner (you will
# note I use ubuntu-24.04-arm for the runner since I built my container on my
# Raspberry PI system and didn't want to worry about any quirks with it running on an
# x64 runner).  

# Once the container is launched, the test job steps that follow clone the repo into
# the container and then run the requisite verification tools are per the assignment
# rubric. The step called "Add missing import packages" runs a script of similar name
# whose job is to run a poetry add -D for any source project under packages directory
# in order to ensure that packages for imports in those package level pyproject.toml
# files get installed prior to running tools like pytest which will fail to execute
# tests properly if those import dependency packages are not installed prior to testing.

# Note that the requirements for Part 1 of this assignment were to trigger CI on a
# push to main branch. During development of Part 1 I did all the work on a
# feature branch called testci as I did not want to pollute the main branch with a
# ton of commits. Once I was done testing to completion on testci branch I merged it
# all to main but then in order to test the push to main I needed to temporarily
# disable the main branch protection ruleset that was in place.

## Part 2: CD

# The .github/workflows/cd.yml also makes use of the citool container. Since one of the
# requirements for the assignment was to have the release version tag be based off of
# the version assigned to the package during poetry build, I modified the container to
# include poetry-dynamic-versioning plugin and git (which is used to fetch the latest
# git tag and set it to POETRY_DYNAMIC_VERSIONING_BYPASS envrionment variable. This
# variable is used by poetry build to override the default version declaration in the
# package level pyproject.toml). The with: fetch-depth: 0 and fetch-tags: true added to
# the git checkout step in cd.yml ensure that the latest tag (which triggered the flow)
# is pulled in during the clone (see bin/get_package_version.sh which was modified to 
# get version from git tag as opposed to version variable in pyproject.toml and
# bin/build.sh which now sets POETRY_DYNAMIC_VERSIONING_BYPASS from it).

# Taking care of the cosign attestation requirement was solved using the script I had
# created in assignment 4 (bin/whl_create_attest.sh), but with the need to have cd.yml
# install cosign via sigstore/cosign-installer@v4.0.0 and some stdin redirect magic
# and disablement of cosign interactive mode so that bin/whl_create_attest.sh could
# work without manual intervention (see cd.yml for details).

# In addition to the cosign atestation processing, it also seemed from the rubric
# that additional GitHub attestation processing was needed (although it was not
# clear if this was a requirement I added it any way using a git action via
# actions/attest-build-provenance@v3 which published an attestation of the whl
# file to https://github.com/wp732/ssc_assignment_1/attestations

# Finally I added a step in the workflow to upload the whl, source tar.gz and
# SBOM json file to the release assests.
