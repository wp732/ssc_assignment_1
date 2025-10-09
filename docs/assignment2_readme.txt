cd rekor/src/

# use black to reformat code to be PEP-8 compliant
black --verbose ./main.py 2>&1 | tee ../../logs/black_main_py.log

# create docstring skeletons in code, then edit the code to fill in the details
doq -f main.py --formatter google -w

