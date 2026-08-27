#!/bin/bash
find . \
  -path './.git' -prune -o \
  -path './.venv' -prune -o \
  -print | sort
