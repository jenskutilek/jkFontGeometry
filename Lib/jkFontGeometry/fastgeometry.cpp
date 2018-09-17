#include <stddef.h>
//#include <stdio.h>
#include <stdlib.h>
#include "fastgeometry.h"


coefficients * line_coefficients(point *p1, point *p2) {
  coefficients *co;
  co = (coefficients *) malloc(sizeof(coefficients));
  co->A =   p1->y - p2->y;
  co->B =   p2->x - p1->x;
  co->C = - p1->x * p2->y + p2->x * p1->y;
  return co;
}

point * intersect_coeffs(coefficients *L1, coefficients *L2) {
  float D, Dx, Dy;
  D  = L1->A * L2->B - L1->B * L2->A;
  Dx = L1->C * L2->B - L1->B * L2->C;
  Dy = L1->A * L2->C - L1->C * L2->A;
  if (D != 0) {
    point *p;
    p = (point *) malloc(sizeof(point));
    p->x = Dx/D;
    p->y = Dy/D;
    return p;
  } else
    return NULL;
}

point * intersect(point *p0, point *p1, point *p2, point *p3) {
  coefficients *L1 = line_coefficients(p0, p1);
  coefficients *L2 = line_coefficients(p2, p3);
  point *p = intersect_coeffs(L1, L2);
  free(L1);
  free(L2);
  return p;
}

point * half_point(point *p0, point *p1) {
  float x = (p0->x + p1->x) * 0.5;
  float y = (p0->y + p1->y) * 0.5;
  point *p;
  p = (point *) malloc(sizeof(point));
  p->x = x;
  p->y = y;
  return p;
}

point * get_cubic_point(double t, point *p0, point *p1, point *p2, point *p3) {
  point *p;
  p = (point *) malloc(sizeof(point));
  if (t == 0) {
    p = p0;
  } else if (t == 1) {
    p = p3;
  } else if (t == 0.5) {
    point *a = half_point(p0, p1);
    point *b = half_point(p1, p2);
    point *c = half_point(p2, p3);
    point *d = half_point(a, b);
    point *e = half_point(b, c);
    p = half_point(d, e);
    free(a);
    free(b);
    free(c);
    free(d);
    free(e);
  } else {
    float cx = (p1->x - p0->x) * 3;
    float cy = (p1->y - p0->y) * 3;
    float bx = (p2->x - p1->x) * 3 - cx;
    float by = (p2->y - p1->y) * 3 - cy;
    float ax = p3->x - p0->x - cx - bx;
    float ay = p3->y - p0->y - cy - by;
    float t3 = t * t * t;
    float t2 = t * t;
    p->x = ax * t3 + bx * t2 + cx * t + p0->x;
    p->y = ay * t3 + by * t2 + cy * t + p0->y;
  }
  return p;
};

point * get_quadratic_point(double t, point *p0, point *p1, point *p2) {
  point *p;
  p = (point *) malloc(sizeof(point));
  if (t == 0) {
    p = p0;
  } else if (t == 1) {
    p = p2;
  } else {
    float a = (1 - t) * (1 - t);
    float b = 2 * t * (1 - t);
    float c = t * t;
    p->x = a * p0->x + b * p1->x + c * p2->x;
    p->y = a * p0->y + b * p1->y + c * p2->y;
  }
  return p;
};

//int main (void) {
//
//  point p0 = {0, 0};
//  point p1 = {1, 1};
//  point p2 = {2, 1};
//  point p3 = {3, 0};
//
//  point *ip = get_cubic_point(0.5, &p0, &p1, &p2, &p3);
//  
//  if (ip == NULL)
//    printf("NULL\n");
//  else {
//    printf("%f %f\n", ip->x, ip->y);
//  }
//}
