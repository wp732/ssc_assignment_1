if [ -f /.dockerenv ]; then
	source `cat ${HOME}/.path_to_toplevel_poetry_venv.txt` 
fi
