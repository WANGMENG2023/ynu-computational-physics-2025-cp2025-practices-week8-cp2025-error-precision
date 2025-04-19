import numpy as np
import matplotlib.pyplot as plt

def sum_up(N):
    """从小到大计算调和级数和"""
    result = 0.0
    for n in range(1, N + 1):
        result += 1.0 / n
    return result

def sum_down(N):
    """从大到小计算调和级数和"""
    result = 0.0
    for n in range(N, 0, -1):
        result += 1.0 / n
    return result

def calculate_relative_difference(N):
    """计算两种方法的相对差异"""
    s_up = sum_up(N)
    s_down = sum_down(N)
    return abs(s_up - s_down) / abs((s_up + s_down) / 2.0)

def plot_differences():
    """绘制相对差异随N的变化"""
    N_values = np.logspace(1, 4, 50, dtype=int)
    differences = [calculate_relative_difference(N) for N in N_values]
    
    plt.figure(figsize=(10, 6))
    plt.loglog(N_values, differences, 'o-', alpha=0.7)
    
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.xlabel('N')
    plt.ylabel('Relative Difference')
    plt.title('Relative Difference vs N')
    
    plt.savefig('harmonic_sum_differences.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_results():
    """打印典型N值的计算结果"""
    N_values = [10, 100, 1000, 10000]
    
    print("\n计算结果:")
    print("N\tS_up\t\tS_down\t\t相对差异")
    print("-" * 60)
    
    for N in N_values:
        s_up = sum_up(N)
        s_down = sum_down(N)
        diff = calculate_relative_difference(N)
        print(f"{N}\t{s_up:.8f}\t{s_down:.8f}\t{diff:.8e}")

def main():
    """主函数"""
    # 打印计算结果
    print_results()
    
    # 绘制误差图
    plot_differences()

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
