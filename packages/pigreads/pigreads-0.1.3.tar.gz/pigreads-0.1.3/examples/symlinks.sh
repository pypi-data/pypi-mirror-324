#!/bin/sh
set -ex
ln -s ../src/pigreads pigreads
ln -s ../../src/main.cpython-313-x86_64-linux-gnu.so pigreads/_core.cpython-313-x86_64-linux-gnu.so
