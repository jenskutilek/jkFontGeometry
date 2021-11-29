#!/bin/sh

# cargo rustc --release -- -C link-arg=-undefined -C link-arg=dynamic_lookup
# cp target/release/libfastgeometry.dylib ../fastgeometry.so

python3 ./setup.py develop