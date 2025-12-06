if [ -f /.dockerenv ]; then
	toplevel_venv=`cat /home/user/.path_to_toplevel_poetry_venv.txt`
	if [ "${VIRTUAL_ENV}" != "${toplevel_venv}" ]; then
		source ${toplevel_venv}/bin/activate
	fi
fi
