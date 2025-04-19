import numpy as np
import matplotlib.pyplot as plt
import time

def f(x):
    """被积函数 f(x) = sqrt(1-x^2)"""
    return np.sqrt(1 - x**2)

def rectangle_method(f, a, b, N):
    """矩形法（左矩形法）计算积分"""
    h = (b - a) / N
    result = 0.0
    
    for k in range(1, N + 1):
        x_k = a + h * (k - 1)  # 左端点
        y_k = f(x_k)
        result += h * y_k
    
    return result

def trapezoid_method(f, a, b, N):
    """梯形法计算积分"""
    h = (b - a) / N
    result = 0.0
    
    for k in range(1, N + 1):
        x_k_minus_1 = a + h * (k - 1)  # 左端点
        x_k = a + h * k  # 右端点
        result += 0.5 * h * (f(x_k_minus_1) + f(x_k))
    
    return result

def calculate_errors(a, b, exact_value):
    """计算不同N值下各方法的误差"""
    N_values = [10, 100, 1000, 10000]
    h_values = [(b - a) / N for N in N_values]
    
    rect_errors = []
    trap_errors = []
    
    for N in N_values:
        # 矩形法
        rect_result = rectangle_method(f, a, b, N)
        rect_error = abs((rect_result - exact_value) / exact_value)
        rect_errors.append(rect_error)
        
        # 梯形法
        trap_result = trapezoid_method(f, a, b, N)
        trap_error = abs((trap_result - exact_value) / exact_value)
        trap_errors.append(trap_error)
    
    return N_values, h_values, rect_errors, trap_errors

def plot_errors(h_values, rect_errors, trap_errors):
    """绘制误差-步长关系图"""
    plt.figure(figsize=(10, 6))
    
    # 绘制误差曲线
    plt.loglog(h_values, rect_errors, 'o-', label='Rectangle Method', alpha=0.5)
    plt.loglog(h_values, trap_errors, 's-', label='Trapezoid Method', alpha=0.5)
    
    # 添加参考线
    plt.loglog(h_values, np.array(h_values), '--', label='O(h)')
    plt.loglog(h_values, np.array(h_values)**2, '--', label='O(h²)')
    
    # 设置图表
    plt.xlabel('Step Size (h)')
    plt.ylabel('Relative Error')
    plt.title('Error vs Step Size in Numerical Integration')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    
    plt.savefig('error_vs_stepsize_integration.png', dpi=300)
    plt.show()

def print_results(N_values, rect_results, trap_results, exact_value):
    """打印计算结果表格"""
    print("N\t矩形法\t\t梯形法\t\t精确值")
    print("-" * 60)
    
    for i in range(len(N_values)):
        print(f"{N_values[i]}\t{rect_results[i]:.8f}\t{trap_results[i]:.8f}\t{exact_value:.8f}")
    
    print("\n相对误差:")
    print("N\t矩形法\t\t梯形法")
    print("-" * 40)
    
    for i in range(len(N_values)):
        rect_error = abs((rect_results[i] - exact_value) / exact_value)
        trap_error = abs((trap_results[i] - exact_value) / exact_value)
        print(f"{N_values[i]}\t{rect_error:.8e}\t{trap_error:.8e}")

def time_performance_test(a, b, max_time=1.0):
    """测试在限定时间内各方法能达到的最高精度"""
    exact_value = 0.5 * np.pi
    
    methods = [
        ("Rectangle Method", rectangle_method),
        ("Trapezoid Method", trapezoid_method)
    ]
    
    print(f"\n在{max_time}秒内各方法能达到的最高精度:")
    print("方法\t\tN\t\t结果\t\t相对误差\t运行时间(秒)")
    print("-" * 80)
    
    for name, method in methods:
        N = 10
        while True:
            start_time = time.time()
            result = method(f, a, b, N)
            end_time = time.time()
            
            elapsed = end_time - start_time
            error = abs((result - exact_value) / exact_value)
            
            if elapsed > max_time / 10:
                print(f"{name}\t{N}\t{result:.8f}\t{error:.8e}\t{elapsed:.6f}")
                break
            
            N *= 2

def calculate_convergence_rate(h_values, errors):
    """计算收敛阶数"""
    log_h = np.log(h_values)
    log_error = np.log(errors)
    
    n = len(h_values)
    slope = (n * np.sum(log_h * log_error) - np.sum(log_h) * np.sum(log_error)) / \
            (n * np.sum(log_h**2) - np.sum(log_h)**2)
    
    return slope

def main():
    """主函数"""
    a, b = -1.0, 1.0  # 积分区间
    exact_value = 0.5 * np.pi  # 精确值
    
    print(f"计算积分 ∫_{a}^{b} √(1-x²) dx")
    print(f"精确值: {exact_value:.10f}")
    
    # 计算不同N值下的结果
    N_values = [10, 100, 1000, 10000]
    rect_results = []
    trap_results = []
    
    for N in N_values:
        rect_results.append(rectangle_method(f, a, b, N))
        trap_results.append(trapezoid_method(f, a, b, N))
    
    # 打印结果
    print_results(N_values, rect_results, trap_results, exact_value)
    
    # 计算误差
    _, h_values, rect_errors, trap_errors = calculate_errors(a, b, exact_value)
    
    # 绘制误差图
    plot_errors(h_values, rect_errors, trap_errors)
    
    # 计算收敛阶数
    rect_rate = calculate_convergence_rate(h_values, rect_errors)
    trap_rate = calculate_convergence_rate(h_values, trap_errors)
    
    print("\n收敛阶数分析:")
    print(f"矩形法: {rect_rate:.2f}")
    print(f"梯形法: {trap_rate:.2f}")
    
    # 时间性能测试
    time_performance_test(a, b)

if __name__ == "__main__":
    main()import sys
import os
import numpy as np
import pytest

# 添加父目录到路径，以便导入学生代码
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from harmonic_sum import sum_up, sum_down
#from solution.harmonic_sum_solution import sum_up, sum_down

def test_sum_up_basic():
    """测试sum_up基本功能"""
    assert abs(sum_up(1) - 1.0) < 1e-10, "N=1时计算错误"
    assert abs(sum_up(2) - 1.5) < 1e-10, "N=2时计算错误"
    assert abs(sum_up(4) - 2.083333333333333) < 1e-10, "N=4时计算错误"

def test_sum_down_basic():
    """测试sum_down基本功能"""
    assert abs(sum_down(1) - 1.0) < 1e-10, "N=1时计算错误"
    assert abs(sum_down(2) - 1.5) < 1e-10, "N=2时计算错误"
    assert abs(sum_down(4) - 2.083333333333333) < 1e-10, "N=4时计算错误"

def test_sum_consistency():
    """测试两种方法在小N值时结果一致"""
    N = 10
    assert abs(sum_up(N) - sum_down(N)) < 1e-10, "两种方法在N=10时结果应该几乎相同"

def test_sum_monotonicity():
    """测试和的单调性"""
    N_values = [10, 100]
    up_sums = [sum_up(N) for N in N_values]
    down_sums = [sum_down(N) for N in N_values]
    
    # 验证和随N增大而增大
    assert up_sums[1] > up_sums[0], "sum_up结果应随N增大而增大"
    assert down_sums[1] > down_sums[0], "sum_down结果应随N增大而增大"

def test_relative_difference():
    """测试大N值时两种方法的差异"""
    N = 1000000  # 使用更大的N值
    s_up = sum_up(N)
    s_down = sum_down(N)
    
    # 只测试两种方法的差异
    assert abs(s_up - s_down) > 1e-13, "大N值时两种方法应该有差异"
    
    # 验证两个结果都接近理论值的合理范围
    theoretical = np.log(N) + 0.5772156649
    assert abs(s_up - theoretical) < 1e-3, "sum_up结果应在理论值的合理范围内"
    assert abs(s_down - theoretical) < 1e-3, "sum_down结果应在理论值的合理范围内"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
