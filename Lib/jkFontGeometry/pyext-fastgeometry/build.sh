#!/bin/sh
cargo rustc --release -- -C link-arg=-undefined -C link-arg=dynamic_lookup