#!/usr/bin/env bash

##### emoji section #####
checkmark=$'\xE2\x9C\x85'
weary_cat_face=$'\xF0\x9F\x99\x80'
police_red_light=$'\xF0\x9F\x9A\xA8'
beer=$'\xF0\x9F\x8D\xBA'
############
RED='\033[0;31m'
GREEN='\033[0;32m'
NOCOLOR='\033[0m'

execute_tests() {
  fullFeaturePath=./features/
  behave /tests/features
  if [ $? -ne 0 ]; then
    print_error && return 1
  else
    print_success
  fi
}

print_success() {
  printf $checkmark'%.0s' {1..10}
  printf $beer'%.0s' {1..3}
  echo -e " ${GREEN} ---> SUCCESS!"
}

print_error() {
  printf $police_red_light'%.0s' {1..10}
  printf $weary_cat_face'%.0s' {1..10}
  echo -e " ${RED} ---> TEST FAILED!"
}

execute_tests
