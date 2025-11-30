if [ -f /.dockerenv ]; then
	echo "HOME=${HOME}"
	pwd
	ls -a ${HOME}
	source `cat ${HOME}/.path_to_toplevel_poetry_venv.txt` 
fi
