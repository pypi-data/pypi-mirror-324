#include <Python.h>
#include <math.h>

#include <stdlib.h>
#include <stdbool.h>

#include "entropy.h"


PyObject* binary_entropy(PyObject* self, PyObject* args)
{
    double x;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "d", &x)) return NULL;

    double z = -x * log(x) / log(2.0);
    return Py_BuildValue("d", z);
}

