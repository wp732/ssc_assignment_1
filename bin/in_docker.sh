if [ -f /.dockerenv ]; then
	echo "HERE"
	echo "HOME=${HOME}"
	pwd
	ls -a /github/home
	source `cat ${HOME}/.path_to_toplevel_poetry_venv.txt` 
fi
