import numpy as np

def calculate_total_resources(allocation_matrix, available_vector):
    """
    全リソース数を計算

    Args:
        allocation_matrix (numpy.ndarray): 割当済みリソース行列 (P x R)
        available_vector (numpy.ndarray): 利用可能リソースベクトル (1 x R)

    Returns:
        numpy.ndarray: 全リソースベクトル (1 x R)
    """
    allocated = allocation_matrix.sum(axis=0)  # 割り当て済みリソースの合計
    total_resources = allocated + available_vector  # 全リソースを計算
    return total_resources

def calculate_available_from_graph(resource_nodes, allocation_matrix):
    """
    グラフ情報から利用可能リソースを計算

    Args:
        resource_nodes (list): 各リソースノードに残っているリソース数
        allocation_matrix (numpy.ndarray): 割当済みリソース行列 (P x R)

    Returns:
        numpy.ndarray: 利用可能リソースベクトル (1 x R)
    """
    allocated = allocation_matrix.sum(axis=0)  # 割り当て済みリソースの合計
    available = np.array(resource_nodes) - allocated  # 未割り当てリソースを計算
    return available

def detect_deadlock(request_matrix, allocation_matrix, available_vector):
    """
    デッドロック検出アルゴリズムを実装

    Args:
        request_matrix (numpy.ndarray): プロセスのリソース要求行列 (P x R)
        allocation_matrix (numpy.ndarray): 割当済みリソース行列 (P x R)
        available_vector (numpy.ndarray): 利用可能なリソースベクトル (1 x R)

    Returns:
        list: デッドロック状態にあるプロセスのインデックス
    """
    num_processes = request_matrix.shape[0]
    finish = np.array([False] * num_processes)  # 各プロセスの完了状態
    available = available_vector.copy()        # 利用可能なリソースのコピー

    print("\n=== デッドロック検出開始 ===")
    print(f"初期状態:")
    print(f"- 利用可能リソース: {available}")
    print(f"- プロセス完了状態: {finish}")

    round_count = 0
    # デッドロック検出アルゴリズム
    while True:
        round_count += 1
        print(f"\nラウンド {round_count}")
        # 実行可能なプロセスを探す
        process_found = False

        for i in range(num_processes):
            if finish[i]:
                continue

            print(f"\nプロセスP{i+1}の確認:")
            print(f"- 要求リソース: {request_matrix[i]}")
            print(f"- 利用可能リソース: {available}")
            print(f"- 要求 <= 利用可能?: {request_matrix[i] <= available}")

            if np.all(request_matrix[i] <= available):
                # 実行可能なプロセスが見つかった場合
                process_found = True
                finish[i] = True
                available += allocation_matrix[i]  # 割り当てリソースを解放
                print(f">>> P{i+1}が実行可能:")
                print(f"   - P{i+1}の保持リソース解放: {allocation_matrix[i]}")
                print(f"   - 新しい利用可能リソース: {available}")
                print(f"   - 更新された完了状態: {finish}")
                break
            else:
                print(f">>> P{i+1}は実行不可（リソース不足）")

        if not process_found:
            print("\n=== 実行可能なプロセスが見つからない ===")
            break  # 実行可能なプロセスがない場合終了

    # デッドロック状態にあるプロセスを抽出
    deadlocked_processes = [i+1 for i in range(num_processes) if not finish[i]]
    print("\n=== 検出結果 ===")
    if deadlocked_processes:
        print(f"デッドロック発生: プロセス {deadlocked_processes} がデッドロック状態")
    else:
        print("デッドロックなし: 全プロセスが実行可能")

    return deadlocked_processes

if __name__ == '__main__':
    # テストデータ1（オリジナル）
    print("=== システム初期状態 ===")
    resource_nodes = [2, 2, 1]  # 各リソースノードに格納されているリソース数
    print(f"リソース総数: {resource_nodes}")

    allocation_matrix = np.array([
                                [0, 1, 0],
                                [1, 0, 0],
                                [0, 1, 0],
                                [1, 0, 1]
                                ])
    print("\n割り当て状態:")
    for i in range(len(allocation_matrix)):
        print(f"P{i}の保持リソース: {allocation_matrix[i]}")

    request_matrix = np.array([
                            [1, 0, 0],
                            [0, 0, 0],
                            [0, 0, 1],
                            [0, 1, 0]
                            ])
    deadlock_request_matrix = np.array([
                                [1, 0, 0], # NOTE P4がR2に要求するリソースを2つにするとP3, P4がデッドロックする
                                [0, 0, 0],
                                [0, 0, 1],
                                [0, 2, 0]
                                ])

    print("\nリソース要求:")
    for i in range(len(request_matrix)):
        print(f"P{i+1}の要求リソース: {request_matrix[i]}")

    # 利用可能リソースを計算
    available_vector = calculate_available_from_graph(resource_nodes, allocation_matrix)
    print(f"\n利用可能リソース: {available_vector}")

    # デッドロック検出
    deadlocked = detect_deadlock(request_matrix, allocation_matrix, available_vector)
