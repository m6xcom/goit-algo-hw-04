import random
import timeit

SIZES = [100, 1_000, 5_000, 10_000]
LARGE_SIZES = [50_000, 100_000]
REPEATS = 3


def insertion_sort(arr: list) -> list:
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def timsort(arr: list) -> list:
    return sorted(arr)


ALGORITHMS = {
    "Сортування вставками": insertion_sort,
    "Сортування злиттям": merge_sort,
    "Timsort (sorted)": timsort,
}


def random_data(n: int) -> list:
    return [random.randint(0, n) for _ in range(n)]


def sorted_data(n: int) -> list:
    return list(range(n))


def reversed_data(n: int) -> list:
    return list(range(n, 0, -1))


def nearly_sorted_data(n: int) -> list:
    data = list(range(n))
    for _ in range(max(1, n // 100)):
        i, j = random.randrange(n), random.randrange(n)
        data[i], data[j] = data[j], data[i]
    return data


DATASETS = {
    "Випадкові дані": random_data,
    "Відсортовані дані": sorted_data,
    "Дані у зворотному порядку": reversed_data,
    "Майже відсортовані дані (1% перестановок)": nearly_sorted_data,
}


def measure(func, data: list) -> float:
    """Повертає найкращий час із REPEATS запусків у секундах."""
    timer = timeit.Timer(lambda: func(data))
    return min(timer.repeat(repeat=REPEATS, number=1))


def check_correctness() -> None:
    sample = random_data(500)
    expected = sorted(sample)
    for name, func in ALGORITHMS.items():
        assert func(sample) == expected, f"{name}: неправильний результат"


def print_table(dataset_name: str, sizes: list, algorithms: dict, results: dict) -> None:
    print(f"\n### {dataset_name}\n")
    header = "| n | " + " | ".join(algorithms) + " |"
    print(header)
    print("|" + "---|" * (len(algorithms) + 1))
    for n in sizes:
        cells = [f"{results[(name, n)]:.6f}" for name in algorithms]
        print(f"| {n:,} | " + " | ".join(cells) + " |")


def run_benchmarks() -> None:
    random.seed(42)
    check_correctness()
    print("Усі алгоритми сортують правильно.")
    print(f"Час у секундах, найкращий із {REPEATS} запусків (timeit).")

    for dataset_name, generator in DATASETS.items():
        results = {}
        for n in SIZES:
            data = generator(n)
            for name, func in ALGORITHMS.items():
                results[(name, n)] = measure(func, data)
        print_table(dataset_name, SIZES, ALGORITHMS, results)

    fast = {k: v for k, v in ALGORITHMS.items() if v is not insertion_sort}
    results = {}
    for n in LARGE_SIZES:
        data = random_data(n)
        for name, func in fast.items():
            results[(name, n)] = measure(func, data)
    print_table(
        "Великі масиви, випадкові дані (без сортування вставками)",
        LARGE_SIZES,
        fast,
        results,
    )


if __name__ == "__main__":
    run_benchmarks()
