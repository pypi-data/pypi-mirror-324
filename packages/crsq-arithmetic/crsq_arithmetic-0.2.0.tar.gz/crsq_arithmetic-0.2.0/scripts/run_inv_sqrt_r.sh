#!/bin/bash -e

. ../../.venv/bin/activate
. ../.env
export PYTHONPATH

SCRIPTDIR=$(dirname $(realpath $0))
python inv_sqrt_r.py
