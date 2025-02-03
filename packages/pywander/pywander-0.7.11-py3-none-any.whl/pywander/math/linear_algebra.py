"""
linear algebra

the prefix explanation

a : an array np.array([1, 2, 3])
v : a vector for example row vector row_v1:  np.array([1, 2, 3]) \
    col vector col_v1 np.array([[2],[0],[0]])
m : the linear equation system left matrix 
b : the linear equation right b array 
am : [argumented matrix] combine m and b to a entire linear system matrix 


"""

import numpy as np


def dimension_of_linear_combination(*vec):
    vec_num = len(vec)

    matrix = np.column_stack(vec)
    # 计算矩阵的秩
    rank = np.linalg.matrix_rank(matrix)
    # 判断秩
    if rank == vec_num:
        print(f'这组向量的线性组合组成的向量空间维度为 {rank} ,等于向量数,这组向量是线性无关的.')

    if rank == 1:
        print(f'这组向量的线性组合是向量空间中的一条直线.')
    elif rank == 2:
        print(f'这组向量的线性组合是向量空间中的一个平面.')
    else:
        print(f'这组向量的线性组合是向量空间中的{rank}维空间 $\\mathbb{{R}}^{rank}$ .')


def can_form_plane(vec1, vec2):
    # 将两个向量按列拼接成矩阵
    matrix = np.column_stack((vec1, vec2))
    # 计算矩阵的秩
    rank = np.linalg.matrix_rank(matrix)
    # 判断秩是否为 2
    return bool(rank == 2)


def can_form_3d_space(vec1, vec2, vec3):
    # 将三个向量按列拼接成矩阵
    matrix = np.column_stack((vec1, vec2, vec3))
    # 计算矩阵的秩
    rank = np.linalg.matrix_rank(matrix)
    # 判断秩是否为 3
    return bool(rank == 3)


def is_1d_row_vector(arr):
    # 方法一：使用 ndim 属性判断
    # 方法二：使用 shape 属性判断
    return arr.ndim == 1 or len(arr.shape) == 1


def row_vector_to_col_vector(row_v):
    """
    行向量转成列向量
    """
    if is_1d_row_vector(row_v):
        return row_v.reshape(-1, 1)
    else:
        raise ValueError("please input the row vector.")


def is_column_vector(arr):
    """
    笑死 感觉ai比我会编程
    我准备动几下的脑细胞这下彻底沉睡了
    """
    # 首先检查数组是否为二维数组
    if arr.ndim == 2:
        # 然后检查数组的第二维（列）长度是否为 1
        return arr.shape[1] == 1
    return False


def col_vector_to_row_vector(col_v):
    """
    列向量转成行向量
    """
    if is_column_vector(col_v):
        return col_v.reshape(1, -1)
    else:
        raise ValueError("please input the column vector.")


def swap_rows(m, row_num_1, row_num_2):
    """
    Gaussian elimination basic operation 1
    swap two rows
    """
    m_new = m.copy()
    m_new[[row_num_1, row_num_2]] = m_new[[row_num_2, row_num_1]]
    return m_new


def multiply_row(m, row_num, row_num_multiple):
    """
    Gaussian elimination basic operation 2
    """
    m_new = m.copy()
    m_new[row_num] = m_new[row_num] * row_num_multiple
    return m_new


def add_rows(m, row_num_1, row_num_2, row_num_1_multiple):
    """
    Gaussian elimination basic operation 3
    """
    m_new = m.copy()
    m_new[row_num_2] = row_num_1_multiple * m_new[row_num_1] + m_new[row_num_2]
    return m_new


def solve(m, b):
    """
    solve the linear equation system
    """
    return np.linalg.solve(m, b)


def determinant(m):
    """
    calc the determinant
    """
    return np.linalg.det(m)


def combine_system(m, b):
    """
    combine m and b to system
    """
    return np.hstack((m, b.reshape(b.size, 1)))


def l2norm(v):
    """
    get the l2 norm of a vector
    """
    return np.linalg.norm(v)


def dot_product(v1, v2):
    """
    get the dot product of two vectors
    """
    return np.dot(v1, v2)


def matrix_multiplication(m1, m2):
    """
    notice: ndim=1 array is a vector, can not apply here.
    """
    return np.matmul(m1, m2)


def cos(v1, v2):
    """
    calc the cosine similarity between two vectors.
    Parameters
    ----------
    v1
    v2

    Returns
    -------

    """
    cosine = np.dot(v1, v2) / (l2norm(v1) * l2norm(v2))
    return cosine
