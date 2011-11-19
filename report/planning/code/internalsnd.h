#include <time.h>

#define STRING_LEN 30

struct internal_snd {
   int    type;
   char   name[STRING_LEN];
   time_t time;
};
