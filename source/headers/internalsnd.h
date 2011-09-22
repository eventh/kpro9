/*
 * Sample header file for testing Lua C structs script
 * Copyright 2011, Stig Bjorlykke <stig@bjorlykke.org>
 */

#define STRING_LEN 30

typedef int time_t;

struct internal_snd {
   int    type;
   char   name[STRING_LEN];
   time_t time;
};
