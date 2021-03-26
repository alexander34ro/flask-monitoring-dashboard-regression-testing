git show $1^..HEAD |
grep -E '^(@@)' |
sed 's/@@.*@@//' |
sed 's/def //' |
sed '/^$/d' |
sort |
uniq