from scipy.optimize import linprog
# ======================================

bounds = [
    (0, None),
    (0, None),
    (0, None)
]



c = [30, 32, 45]



A_ub = [
    [20, 12, 7],
    [0.8, 1.3, 0.25],
    [-1.3, -1.1, -4],
    [-0.2, -1.1, -0.5]
]

b_ub = [12, 1, -2, -0.5]

A_eq = [
    [1, 1, 1]
]

b_eq = [1]



result = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method='highs'
)



if result.success:
    print('Znaleziono rozwiązanie optymalne')
    print()

    print(f'x1 = {result.x[0]:.4f}')
    print(f'x2 = {result.x[1]:.4f}')
    print(f'x3 = {result.x[2]:.4f}')

    print()
    print(f'Minimalna wartość funkcji celu = {result.fun:.4f}')

else:
    print('Brak rozwiązania')
    print(result.message)