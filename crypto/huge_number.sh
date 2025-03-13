SIZE=10

[[ "$1" -gt 0 ]] && SIZE=$1

od -An -N6400000 -tu8 /dev/urandom | tr -d ' \n' | head -c "$SIZE"
echo
