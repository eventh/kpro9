/*
 * Sample header file for testing Lua C structs script
 * Copyright 2011, Stig Bjorlykke <stig@bjorlykke.org>
 */

#include "time.h"

#define INTERNALRCV 2
#define STRING_LEN 26

struct internal_rcv {
   int    type;
   time_t time;
   char   data[STRING_LEN];
};
