typedef struct {
  float x;
  float y;
} point;


typedef struct {
  float A;
  float B;
  float C;
} coefficients;


coefficients * line_coefficients(point *p1, point *p2);

point * intersect_coeffs(coefficients *L1, coefficients *L2);

point * intersect(point *p0, point *p1, point *p2, point *p3);

point * get_cubic_point(double t, point *p0, point *p1, point *p2, point *p3);

point * get_quadratic_point(double t, point *p0, point *p1, point *p2);

//int get_closest_point_index(point *p, &list);
