This is quite the spaghetti code.

    scripts/bench/thp-build/run 

calls 

    scripts/bench/thp-build/measure-thp.py

which calls

    lakeprof 

(which needs to be installed independently)

which thinks it calls `lean`, but actually calls

    scripts/bench/thp-build/fake-root/bin/lean

which calls

    scripts/bench/thp-build/measure-thp.py

again, which calls `lean`.


I think.
