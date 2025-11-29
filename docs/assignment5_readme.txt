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

