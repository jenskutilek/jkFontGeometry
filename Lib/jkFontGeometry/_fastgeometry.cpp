#include <Python.h>
#include "fastgeometry.h"


static char module_docstring[] =
    "Fast geometry functions.";
static char intersect_docstring[] =
    "Find the intersection point between two lines defined by two points each.";
static char get_cubic_point_docstring[] =
    "Return the point at time t on the cubic Bezier given by its four control points.";
static char get_quadratic_point_docstring[] =
    "Return the point at time t on the quadratic Bezier given by its three control points.";
//static char fastgeometry_get_closest_point_index_docstring[] =
//    "Return the index of the point of the list that is closest to the given point.";


static PyObject *fastgeometry_intersect(PyObject *self, PyObject *args);
static PyObject *fastgeometry_get_cubic_point(PyObject *self, PyObject *args);
static PyObject *fastgeometry_get_quadratic_point(PyObject *self, PyObject *args);
//static PyObject *fastgeometry_get_closest_point_index(PyObject *self, PyObject *args);


static PyMethodDef module_methods[] = {
    {"intersect", fastgeometry_intersect, METH_VARARGS, intersect_docstring},
    {"get_cubic_point", fastgeometry_get_cubic_point, METH_VARARGS, get_cubic_point_docstring},
    {"get_quadratic_point", fastgeometry_get_quadratic_point, METH_VARARGS, get_quadratic_point_docstring},
//    {"get_closest_point_index", fastgeometry_get_closest_point_index, METH_VARARGS, fastgeometry_get_closest_point_index_docstring},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC init_fastgeometry(void)
{
    PyObject *m = Py_InitModule3("_fastgeometry", module_methods, module_docstring);
    if (m == NULL)
        return;
}


static PyObject *fastgeometry_intersect(PyObject *self, PyObject *args)
{

    float p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y;
    
    /* Parse the input tuple */
    if (
        !PyArg_ParseTuple(
            args,
            "(ff)(ff)(ff)(ff)",
            &p0x, &p0y, &p1x, &p1y, &p2x, &p2y, &p3x, &p3y
        )
    ) {
        PyErr_SetString(PyExc_RuntimeError, "Error parsing the arguments.");
        return NULL;
    }

    point p0 = {p0x, p0y};
    point p1 = {p1x, p1y};
    point p2 = {p2x, p2y};
    point p3 = {p3x, p3y};

    /* Call the external C function to compute the intersection. */
    point * ip = intersect(&p0, &p1, &p2, &p3);

    if (ip == NULL) {
        free(ip);
        PyObject *ret = Py_BuildValue("", NULL);
        return ret;
    } else {
        /* Build the output tuple */
        PyObject *ret = Py_BuildValue("(ff)", ip->x, ip->y);
        free(ip);
        return ret;
    }    
}


static PyObject *fastgeometry_get_cubic_point(PyObject *self, PyObject *args)
{

    double t;
    float p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y;
    
    /* Parse the input tuple */
    if (
        !PyArg_ParseTuple(
            args,
            "d(ff)(ff)(ff)(ff)",
            &t, &p0x, &p0y, &p1x, &p1y, &p2x, &p2y, &p3x, &p3y
        )
    ) {
        PyErr_SetString(PyExc_RuntimeError, "Error parsing the arguments.");
        return NULL;
    }

    point p0 = {p0x, p0y};
    point p1 = {p1x, p1y};
    point p2 = {p2x, p2y};
    point p3 = {p3x, p3y};

    /* Call the external C function to compute the point on the cubic. */
    point * p = get_cubic_point(t, &p0, &p1, &p2, &p3);

    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("(ff)", p->x, p->y);
    return ret;    
}


static PyObject *fastgeometry_get_quadratic_point(PyObject *self, PyObject *args)
{

    double t;
    float p0x, p0y, p1x, p1y, p2x, p2y;
    
    /* Parse the input tuple */
    if (
        !PyArg_ParseTuple(
            args,
            "d(ff)(ff)(ff)",
            &t, &p0x, &p0y, &p1x, &p1y, &p2x, &p2y
        )
    ) {
        PyErr_SetString(PyExc_RuntimeError, "Error parsing the arguments.");
        return NULL;
    }

    point p0 = {p0x, p0y};
    point p1 = {p1x, p1y};
    point p2 = {p2x, p2y};
    
    /* Call the external C function to compute the point on the quadratic. */
    point * p = get_quadratic_point(t, &p0, &p1, &p2);

    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("(ff)", p->x, p->y);
    return ret;    
}


//static PyObject *fastgeometry_get_closest_point_index(PyObject *self, PyObject *args)
//{
//
//    float px, py;
//    PyObject list;
//    
//    /* Parse the input tuple */
//    if (
//        !PyArg_ParseTuple(
//            args,
//            "(ff)O",
//            &px, &py, &list
//        )
//    ) {
//        PyErr_SetString(PyExc_RuntimeError, "Error parsing the arguments.");
//        return NULL;
//    }
//
//    point p = {px, py};
//
//    /* Call the external C function to compute the index of the closest point. */
//    int i = get_closest_point_index(&p, &list);
//
//    /* Build the output tuple */
//    PyObject *ret = Py_BuildValue("i", i);
//    return ret;    
//}
