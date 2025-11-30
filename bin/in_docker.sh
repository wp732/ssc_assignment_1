if [ -f /.dockerenv ]; then
	echo "HERE"
	ls -a /github/home
	source `cat ${HOME}/.path_to_toplevel_poetry_venv.txt` 
fi
