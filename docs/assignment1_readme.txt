cd rekor/src/

# create checkpoint (when run with -d it creates ~/checkpoint.json)
python3 ./main.py -d -c

# get logIndex of entry
logindex=`jq -r '.rekorBundle.Payload.logIndex' ../../data/artifact.bundle`

# test for inclusion of artifact entry in rekor log
python3 ./main.py --inclusion $logindex --artifact ../../data/artifact.md

# test for consistency of current checkpoint against previous captured checkpoint
python3 ./main.py `../bin/consistency_args.sh ~/checkpoint.json` 
