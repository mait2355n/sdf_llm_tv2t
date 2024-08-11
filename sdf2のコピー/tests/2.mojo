from time import now


fn ackermann(m: Int, n: Int) -> Int:
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))


fn main() -> None:
    let m = 3
    let n = 12
    let start = now()
    let result = ackermann(m, n)
    let exec_time = (now() - start) / 1_000_000_000
    print("result:", result)
    print("time:", exec_time, "sec")