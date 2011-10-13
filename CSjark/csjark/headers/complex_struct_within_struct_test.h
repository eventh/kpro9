#include "cenum_test.h"
#include "simple.h"

struct complex_struct_within_struct_test {
	int prime;
	struct cenum_test astruct;
	int number;
	struct basic astruct2;
	int nend;
};
