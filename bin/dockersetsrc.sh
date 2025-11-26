src_dir=""

while [ $# -ne 0 ]; do
	case $1 in
		-srcdir )
			shift
			src_dir=$1
			;;	
		* )
			break
			;;
	esac
	shift
done

if [ -z "${src_dir}" ]; then
	echo "ERROR: must supply -srcdir" >&2
	exit 255
fi

cd $src_dir
[[ $? -ne 0 ]] && exit 255

CNAME=`cat ./CNAME`
CTAG=`cat ./CTAG`
