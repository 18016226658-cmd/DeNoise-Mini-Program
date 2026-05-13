"""
大整数分解核心算法实现（Python 版本）
"""
import random
import math
import time

def mod_pow(base, exponent, modulus):
    """快速幂取模 (a^b mod m)"""
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def miller_rabin(n, k=5):
    """
    Miller-Rabin素性测试
    :param n: 待测试的数
    :param k: 测试轮数，默认5轮（大数字自动增加）
    :return: True表示可能是素数，False表示合数
    """
    # 对于大数字，自动增加测试轮数以提高准确性
    num_digits = len(str(n))
    if num_digits > 100 and k < 10:
        k = 10  # 100位以上至少10轮
    elif num_digits > 150 and k < 15:
        k = 15  # 150位以上至少15轮
    elif num_digits > 180 and k < 20:
        k = 20  # 180位以上至少20轮

    # 限制最大测试轮数，避免卡住
    k = min(k, 20)  # 最多20轮

    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    # 对于非常大的数字，限制测试时间
    if num_digits > 100:
        # 减少测试轮数，避免卡住
        k = min(k, 10)

    # 将 n-1 写成 d * 2^r 的形式
    d = n - 1
    r = 0
    while d % 2 == 0:
        d = d // 2
        r += 1

    # 进行k轮测试
    for i in range(k):
        # 随机选择 a ∈ [2, n-2]
        # 对于大数字，限制随机数范围，避免计算过慢
        if num_digits > 50:
            max_a = min(n - 2, 1000000)  # 限制随机数范围
            a = random.randint(2, max_a)
        else:
            a = random.randint(2, n - 2)

        try:
            x = mod_pow(a, d, n)
        except Exception:
            # 如果计算出错，假设是合数
            return False

        if x == 1 or x == n - 1:
            continue

        composite = True
        for j in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break

        if composite:
            return False  # 确定是合数

    return True  # 可能是素数

def gcd(a, b):
    """最大公约数 (GCD)"""
    while b != 0:
        a, b = b, a % b
    return a

def pollard_rho(n):
    """
    Pollard's Rho算法（Brent变体）
    :param n: 待分解的数
    :return: 返回一个因子，如果失败返回None
    """
    if n % 2 == 0:
        return 2
    if miller_rabin(n):
        return None  # 如果是素数，无法分解

    # 尝试多个初始值和多项式函数，提高成功率
    num_digits = len(str(n))
    max_attempts = 3 if num_digits > 100 else 1

    # 根据数字大小动态调整最大迭代次数
    if num_digits <= 20:
        max_iterations = 100000
    elif num_digits <= 40:
        max_iterations = 500000
    elif num_digits <= 50:
        max_iterations = 1000000
    elif num_digits <= 70:
        max_iterations = 2000000
    elif num_digits <= 100:
        max_iterations = 5000000
    elif num_digits <= 150:
        max_iterations = 10000000
    else:
        max_iterations = 20000000

    for attempt in range(max_attempts):
        # Brent循环检测算法
        x = random.randint(2, min(n - 1, 1000000))
        y = x
        d = 1
        m = 100
        r = 1
        q = 1

        # 尝试不同的多项式函数
        if attempt == 0:
            # f(x) = (x^2 + 1) mod n
            def f(x_val):
                return ((x_val * x_val) % n + 1) % n
        elif attempt == 1:
            # f(x) = (x^2 + 2) mod n
            def f(x_val):
                return ((x_val * x_val) % n + 2) % n
        else:
            # f(x) = (x^2 + 3) mod n
            def f(x_val):
                return ((x_val * x_val) % n + 3) % n

        iterations = 0
        while d == 1 and iterations < max_iterations:
            iterations += 1
            x = f(x)
            d = gcd(abs(x - y), n)

            if d != 1 and d != n:
                return d  # 找到因子

            # Brent的循环检测优化
            if iterations == r:
                y = x
                r = r * 2
            elif iterations % 128 == 0:
                # 定期检查
                d = gcd(q, n)
                if d > 1 and d != n:
                    return d
                q = 1
            else:
                q = (q * abs(x - y)) % n

    return None  # 未找到因子

def trial_division(n):
    """试除法（用于小因子）"""
    small_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
        53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
        151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199
    ]
    for prime in small_primes:
        if n % prime == 0:
            return prime
    return None

def factorize(n, mode='standard'):
    """
    完整的大整数分解函数
    :param n: 待分解的数
    :param mode: 分解模式 ('standard' 或 'fast')
    :return: 因子数组
    """
    if n < 2:
        return []

    # 设置最大计算时间（秒）
    max_time = 180 if mode == 'standard' else 60  # standard: 3分钟, fast: 1分钟
    start_time = time.time()

    factors = []
    recursion_depth = 0
    max_recursion_depth = 50  # 最大递归深度

    # 先尝试试除法
    while True:
        # 检查时间限制
        if time.time() - start_time > max_time:
            # 如果已经找到一些因子，返回部分结果
            if factors:
                return sorted(factors)
            # 否则返回原数（表示无法分解）
            return [n]

        trial_factor = trial_division(n)
        if trial_factor:
            factors.append(trial_factor)
            n = n // trial_factor
            if n == 1:
                break
        else:
            break

    if n == 1:
        return sorted(factors)

    # 递归分解函数（带深度和时间限制）
    def recursive_factor(num, depth=0):
        nonlocal recursion_depth
        recursion_depth = max(recursion_depth, depth)

        # 检查递归深度
        if depth > max_recursion_depth:
            factors.append(num)  # 将剩余部分作为因子
            return

        # 检查时间限制
        if time.time() - start_time > max_time:
            # 如果已经找到一些因子，返回部分结果
            if not factors or num not in factors:
                factors.append(num)  # 将剩余部分作为因子
            return

        if num == 1:
            return

        # 检查是否为素数
        num_digits = len(str(num))
        mr_rounds = 10 if num_digits > 100 else (15 if num_digits > 150 else 5)
        if miller_rabin(num, mr_rounds):
            factors.append(num)
            return

        # 使用Pollard's Rho找因子
        factor = pollard_rho(num)
        if factor and factor != num:
            factors.append(factor)
            other_factor = num // factor
            recursive_factor(factor, depth + 1)
            recursive_factor(other_factor, depth + 1)
        else:
            # 如果Pollard's Rho失败，将原数作为因子
            factors.append(num)
    
    recursive_factor(n)
    
    # 排序并返回
    return sorted(factors)

def validate_input(input_str):
    """
    验证输入是否为有效的大整数
    :param input_str: 输入字符串
    :return: {valid: bool, number: int|None, error: str|None}
    """
    if input_str is None:
        return {'valid': False, 'number': None, 'error': '请输入数字'}
    
    if not isinstance(input_str, str):
        input_str = str(input_str)
    
    trimmed = input_str.strip()
    
    if trimmed == '':
        return {'valid': False, 'number': None, 'error': '请输入数字'}
    
    # 只允许0-9，移除所有非数字字符
    cleaned = ''.join(c for c in trimmed if c.isdigit())
    
    if cleaned == '':
        return {'valid': False, 'number': None, 'error': '请输入数字（0-9）'}
    
    # 检查前导零（允许单个0）
    if len(cleaned) > 1 and cleaned[0] == '0':
        return {'valid': False, 'number': None, 'error': '数字不能有前导零'}
    
    # 检查位数
    if len(cleaned) > 200:
        return {'valid': False, 'number': None, 'error': '数字位数不能超过200位'}
    
    # 检查是否全为相同数字（可能是异常输入）
    if len(cleaned) > 50 and len(set(cleaned)) == 1:
        return {'valid': False, 'number': None, 'error': '检测到异常输入模式，请检查输入'}
    
    try:
        num = int(cleaned)
        if num < 0:
            return {'valid': False, 'number': None, 'error': '数字不能为负数'}
        return {'valid': True, 'number': num, 'error': None}
    except (ValueError, OverflowError) as e:
        return {'valid': False, 'number': None, 'error': '数字过大或格式错误，最大支持200位'}

def get_number_type(n, factors):
    """
    判断数字类型
    :param n: 原数
    :param factors: 已分解的因子数组
    :return: {type: str, type_name: str, description: str}
    """
    if n == 0:
        return {'type': 'zero', 'type_name': '非素非合', 'description': '0既不是素数也不是合数'}
    if n == 1:
        return {'type': 'unit', 'type_name': '非素非合', 'description': '1既不是素数也不是合数'}
    if not factors or len(factors) == 0:
        return {'type': 'unknown', 'type_name': '未知', 'description': '无法确定数字类型'}
    if len(factors) == 1 and factors[0] == n:
        # 只有一个因子且等于自身，可能是素数
        if miller_rabin(n, 5):
            return {'type': 'prime', 'type_name': '素数', 'description': '只能被1和自身整除的正整数'}
        else:
            return {'type': 'composite', 'type_name': '合数', 'description': '有多个因子的正整数'}
    # 有多个因子，是合数
    return {'type': 'composite', 'type_name': '合数', 'description': '有多个因子的正整数'}

def get_factorization_level(original_number, factors):
    """
    判断分解程度
    :param original_number: 原数
    :param factors: 已分解的因子数组
    :return: {level: str, level_name: str, description: str}
    """
    if original_number == 0:
        return {'level': 'complete', 'level_name': '完全分解', 'description': '0的分解已完成'}
    if original_number == 1:
        return {'level': 'complete', 'level_name': '完全分解', 'description': '1的分解已完成'}
    if not factors or len(factors) == 0:
        return {'level': 'failed', 'level_name': '不能分解', 'description': '无法分解该数字'}
    
    # 计算所有因子的乘积
    product = 1
    try:
        for f in factors:
            if f is not None:
                product = product * f
    except Exception as e:
        return {'level': 'failed', 'level_name': '不能分解', 'description': '计算因子乘积时发生错误'}
    
    # 检查是否为部分分解
    if product < original_number and len(factors) > 0:
        percentage = (product * 100) / original_number
        return {
            'level': 'partial',
            'level_name': '部分分解',
            'description': f'已分解 {len(factors)} 个因子，覆盖原数的 {percentage:.2f}%'
        }
    
    if product == original_number:
        # 验证是否所有因子都是素数
        all_prime = True
        for factor in factors:
            if factor == 0 or factor == 1:
                continue
            try:
                if not miller_rabin(factor, 3):
                    all_prime = False
                    break
            except Exception:
                all_prime = False
                break
        
        if all_prime:
            return {'level': 'complete', 'level_name': '完全分解', 'description': '已分解为所有素因子的乘积'}
        else:
            return {'level': 'partial', 'level_name': '部分分解', 'description': '已找到部分因子，但可能还有未分解的因子'}
    elif product < original_number:
        return {'level': 'partial', 'level_name': '部分分解', 'description': '已找到部分因子，但乘积小于原数'}
    else:
        return {'level': 'failed', 'level_name': '不能分解', 'description': '因子乘积不等于原数，分解失败'}

