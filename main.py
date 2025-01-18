import numpy as np

def is_safe_state(available, max_matrix, allocation):
    # NOTE 行列変換
    available = np.array(available)
    max_matrix = np.array(max_matrix)
    allocation = np.array(allocation)

    n_processes = len(max_matrix)
    n_resources = len(available)

    # NOTE 必要資源行列
    need = max_matrix - allocation
    print("Need matrix:")
    print(need)

    work = available.copy()
    finish = np.zeros(n_processes, dtype=bool)

    # NOTE 安全性アルゴリズム
    safe_sequence = []

    while len(safe_sequence) < n_processes:
        allocated_in_this_round = False
        print("\nCurrent work:", work)
        print("Current finish:", finish)

        for i in range(n_processes):
            if not finish[i]:
                print(f"Checking process {i}:")
                print(f"Need: {need[i]}")
                print(f"Work: {work}")
                print(f"Need <= Work: {(need[i] <= work).all()}")

            if not finish[i] and (need[i] <= work).all():
                print(f"Allocating process {i}")
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(int(i))
                allocated_in_this_round = True
                break

        if not allocated_in_this_round:
            return False, []

    return True, np.array(safe_sequence, dtype=int)

def print_safe_sequence(safe_sequence):
    for i in safe_sequence:
        print(f"P{i+1}", end=" -> ")

if __name__ == '__main__':
    available = [3, 3, 2]
    max_matrix = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    is_safe, safe_sequence = is_safe_state(available, max_matrix, allocation)

    if is_safe:
        print("The system is in a safe state.")
        print_safe_sequence(safe_sequence)
    else:
        print("The system is not in a safe state.")
