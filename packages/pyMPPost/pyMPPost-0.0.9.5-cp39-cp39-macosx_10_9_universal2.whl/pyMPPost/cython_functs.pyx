import numpy as np

cimport cython
cimport numpy as cnp

cnp.import_array()

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.initializedcheck(False)
cpdef calc_pulses(long[:] history, long[:] cell, double[:] time, long[:] detector_mat, double[:] pgt_arr, double[:] dt_arr, double tol):
    """ Groups events into pulses given history, cell, time, and the material properties
    """
    cdef Py_ssize_t N = len(history)
    cdef double begin
    cdef long curr_pulse = 0
    cdef long curr_detect = -1
    cdef long curr_hist = -1

    cdef Py_ssize_t k
    pulses = np.zeros(N, dtype=long)
    cdef long[::1] pulses_view = pulses
    
    for k in range(N):
        if curr_hist != history[k] or curr_detect != cell[k]:
            curr_hist = history[k]
            curr_detect = cell[k]
            curr_pulse = 0
            begin = time[k]
            mat_num = detector_mat[k]
            pgt = pgt_arr[mat_num]
            dt = dt_arr[mat_num]

        
        if (time[k] - begin) - pgt <= tol:
            pulses_view[k] = curr_pulse
        elif (time[k] - begin) - (pgt+dt) > tol:
            begin = time[k]
            curr_pulse += 1
            pulses_view[k] = curr_pulse
        else:
            pulses_view[k] = -1
    return pulses

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
@cython.initializedcheck(False)
cpdef shift_register_counting(long[:] history, double[:] time, double window_width, double tol):
    """ Shift Register counting for multiplicity module
    """
    cdef Py_ssize_t N = len(history)
    cdef double begin
    cdef long curr_hist = -1
    cdef long curr_pulse = -1
    cdef long curr_window = -1

    cdef Py_ssize_t k
    windows = np.zeros(N, dtype=long)
    cdef long[::1] window_view = windows
    
    for k in range(N):
        if curr_hist != history[k]:
            curr_hist = history[k]
            curr_window += 1
            begin = time[k]
        
        if (time[k] - begin) - window_width <= tol:
            window_view[k] = curr_window
        else:
            begin = time[k]
            curr_window += 1
            window_view[k] = curr_window
    return windows