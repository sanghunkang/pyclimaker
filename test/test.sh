# Maybe it's more sensible to test on command line environments (i.e shell or cmd)
echo "yes\n" | python ./example.py << EOF
foo
bar
    some other input
spam
1
exit
EOF