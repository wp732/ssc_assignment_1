# Repository for Software Supply Chain security assignments  

[![release](https://github.com/wp732/ssc_assignment_1/actions/workflows/cd.yml/badge.svg)](https://github.com/wp732/ssc_assignment_1/actions/workflows/cd.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/wp732/ssc_assignment_1/badge)](https://scorecard.dev/viewer/?uri=github.com/wp732/ssc_assignment_1)

# SSC assignment 1 (using Sigstore tools)   

The release entitled "Working version of assignment 1" was the snapshot of this assignment  
The instructions for how the commands were run are in docs/assignment1_readme.txt  
The Python source code for assignments 1,2, and 3 were in the rekor/src directory,  
but that changed with assignment 4 (so if you are trying to follow along, then do so  
by downloading the per assignment release source packages.   
The artifact.md used for testing is in the data directory  
The artifact.bundle that was create for the artifact.md file is in the data directory  

# SSC assignment 2 (using code quality tools)    

The release entitled "v2.0.0" was the snapshot of this assignment  
The instructions for how the commands were installed and run are in docs/assignment2_readme.txt  
The log output for commands run (ruff, mypy, black, etc.) are in the logs directory  
The file rekor/src/initial_py_files.tar.gz is a save of original *.py files used for the tooling runs that produced the logs/*.inital.txt outputs.  
The *.py files that exist in rekor/src at time of assignment 2 submission are the final modified files.  
The *.final.txt logs are the outputs of the *.py cleaned files.  

# SSC assignment 3 (git project best practices; secrets scanning and back-out; build system config; testing and code coverage)  

The release entitled "v3.0.0" was the snapshot of this assignment  

Part 1: Git Best Practices   
- Add README.md, SECURITY.md, CONTRIBUTING.md, LICENSE, CODEOWNERS, .gitignore files.  
- Enable Branch Protection in GitHub.  

For the following parts, the instructions for how the commands were installed and run are in docs/assignment3_readme.txt  

Part 2: Prevent Secrets Leakage   

Part 3: Scrub Old Secrets ( see part3-writeup.txt submitted to Brightspace ) 

Part 4: Build System Configuration  

Part 5: Testing and Coverage   

# SSC assignment 4 (package publishing and SBOMs)  

The instructions for how the commands were installed and run for following are in docs/assignment4_readme.txt  

Part 1: Publishing packages to PyPi via poetry publish  

Part 2: SBOM generation and package attestation  

# SSC assignment 5 (CI, CD, Repo assessment)  

The instructions for how the commands were installed and run for following are in docs/assignment5_readme.txt  

Part 1: Continuous Integration  

Part 2: Continuous Deployment  

Part 3: Repository Assessment  
