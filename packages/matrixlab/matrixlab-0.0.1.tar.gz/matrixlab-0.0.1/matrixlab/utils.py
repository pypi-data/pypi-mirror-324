__all__ = ["check_sparse_format"]

import scipy
from scipy.sparse import coo_matrix, _coo

def check_sparse_format(A):
    if not isinstance(A, _coo.coo_matrix):
        A = coo_matrix(A)

    return A





