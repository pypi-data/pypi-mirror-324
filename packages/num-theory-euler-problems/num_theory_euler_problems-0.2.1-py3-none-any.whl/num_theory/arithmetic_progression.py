def arithmetic_progression(a, d, n, compute_sum=False, nth_term=False):
    """
    Generate terms of an arithmetic progression (AP), compute the nth term, or calculate the sum of the first n terms.

    Parameters
    ----------
    a : float
        The first term of the AP.
    d : float
        The common difference between consecutive terms.
    n : int
        The number of terms, the term to compute, or the term index.
    compute_sum : bool, optional
        If True, computes the sum of the first n terms. Default is False.
    nth_term : bool, optional
        If True, computes the nth term of the AP instead of generating terms. Default is False.

    Returns
    -------
    list or float
        - If `compute_sum` and `nth_term` are both False, returns a list of the first n terms of the AP.
        - If `nth_term` is True, returns the nth term as a float.
        - If `compute_sum` is True, returns the sum of the first n terms as a float.
        - If both `nth_term` and `compute_sum` is True, it will return the nth term as a float.

    Examples
    --------
    >>> arithmetic_progression(a=2, d=3, n=5)
    [2, 5, 8, 11, 14]

    >>> arithmetic_progression(a=2, d=3, n=5, compute_sum=True)
    40.0

    >>> arithmetic_progression(a=2, d=3, n=5, nth_term=True)
    14

    >>> arithmetic_progression(a=1, d=2, n=5, nth_term=True)
    9
    """
    if n <= 0:
        raise ValueError("The number of terms 'n' must be a positive integer.")
    
    if not isinstance(n, (int)):
        raise TypeError("Input n must be a int value.")
    
    if not isinstance(a, (int, float)):
        raise TypeError("Input a must be a numeric value (int or float).")

    if not isinstance(d, (int, float)):
        raise TypeError("Input d must be a numeric value (int or float).")
    
    if nth_term:
        # Compute the nth term
        term = a + (n - 1) * d
        return term
    elif compute_sum:
        # Calculate the sum of the first n terms
        sum_n = (n / 2) * (2 * a + (n - 1) * d)
        return sum_n
    else:
        # Generate the terms of the AP
        ap_terms = [a + i * d for i in range(n)]
        return ap_terms
