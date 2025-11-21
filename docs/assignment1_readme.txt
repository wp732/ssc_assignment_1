# Sign the data blob 

# Note: First login to GitHub via a web browser on the same computer
#       that you will run the cosign sign-blob command on. When it runs,
#       it will authenticate you via OIDC to GitHub.

cd data/
cosign sign-blob artifact.md --bundle artifact.bundle

# Test funcitonality of rekor verification code

cd rekor/src/

# create checkpoint (when run with -d it creates ~/checkpoint.json)
python3 ./main.py -d -c

# get logIndex of entry
logindex=`jq -r '.rekorBundle.Payload.logIndex' ../../data/artifact.bundle`

# test for inclusion of artifact entry in rekor log
python3 ./main.py --inclusion $logindex --artifact ../../data/artifact.md

# test for consistency of current checkpoint against previous captured checkpoint
python3 ./main.py `../bin/consistency_args.sh ~/checkpoint.json` 
