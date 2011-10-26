struct abcde {
	int a;
	int b;
	long c;
	short d;
	char e;
};

struct alignment_test {
	int a;
	short b;
	char c;
	char d;
	char e;
	struct abcde f;
};
