proj_dir=${thisdir}/..
src_dir="${SSC_SRC_DIR}"

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
	echo "ERROR: must supply -srcdir or export SSC_SRC_DIR" >&2
	exit 255
fi

CNAME=`cat ${src_dir}/CNAME`
CTAG=`cat ${src_dir}/CTAG`
