typedef enum traffic_light{ red, yellow, green } traffic_light;

enum BOOL{ true, false };

struct cenum_test2 {
	int id;
	enum BOOL correct;
	traffic_light light;
	int percent;
};
