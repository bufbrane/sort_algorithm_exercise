#!/usr/bin/env python3

# 考研常见排序算法的小练习

import random

class sort:
    '''常见排序算法类'''

    @staticmethod
    def direct_search_insert_sort(elementlist: list)-> list:
        '''直接插入排序'''

        # 列表在逻辑上分为有序区[0:i]和无序区[i,len(elementlist)-1]，
        # 每次循环将第i个元素（也就是无序区的第一个元素）插入到有序区的适当位置
        for i in range(len(elementlist)):

            # 取出第i个元素
            temp = elementlist[i] 

            # 记录其插入有序区的位置
            insert_index = 0

            # 顺序查找适当的插入位置
            for j in range(i):
                
                # 升序查找
                if temp >= elementlist[j]:
                    # 当前元素比temp小，记录当前查找位置（当查找失败时插入位置是有序区末尾），然后继续向后查找
                    insert_index = i
                else:
                    # 当前元素是比temp大的第一个元素，则插入位置在j，查找成功
                    insert_index = j
                    break

            # 将有序区的插入位置及其之后的元素向后移动一格，给插入元素腾出位置
            for k in range(i, insert_index, -1):
                elementlist[k] = elementlist[k-1]
                
            # 然后插入元素
            elementlist[insert_index] = temp

        return elementlist


    @staticmethod
    def __binary_search_algorithm(elementlist: list, element: int, first_index: int, last_index: int)->int:
        '''
        二分查找算法，仅供折半查找排序算法使用
        
        Args:
            elementlist: 待查找的数组，数组中存在一个有序区，查找即在有序区中进行
            element: 查找的元素
            first_index: 待查找数组有序区的起始元素下标
            last_index: 带查找数组有序区的末尾元素（含）下标
        
        Returns:
            介于first_index和last_index的一个整数，即使查找失败也会返回
        '''

        # 计算有序区的元素个数（当first_index==0 and last_index==-1时即为第一个元素排序，此时有序区为空）
        num_of_element = last_index - first_index + 1

        # 有序区为空或给出的范围错误时直接返回，通常是对第一个元素排序
        if num_of_element <= 0:
            return first_index

        # 递归退出条件：有序区只有一个元素，插入位置不是在其左就是在其右
        elif num_of_element == 1:
            if element <= elementlist[first_index]:
                return first_index
            else:
                return first_index + 1

        # 有序区元素个数大于1，可以将其分成两部分（递归二分查找）
        else:

            # 计算中位数下标，以中位数为分界线（除法向下舍入，因此当有序区只有两个元素时中位数一定是第一个元素）
            mid_index = (first_index + last_index) // 2
            
            # 如果查找元素不大于中位数，则查找区域缩小到中位数（含）的左侧
            if element <= elementlist[mid_index]:
                return sort.__binary_search_algorithm(elementlist, element, first_index, mid_index)
            
            # 如果查找元素大于中位数，则查找区域缩小到中位数（不含）的右侧
            else:
                return sort.__binary_search_algorithm(elementlist, element, mid_index + 1, last_index)


    @staticmethod
    def binary_search_insert_sort(elementlist: list)->list:
        '''折半查找排序算法'''

        # 列表在逻辑上分为有序区[0:i]和无序区[i,len(elementlist)-1]，
        # 每次循环将第i个元素（也就是无序区的第一个元素）插入到有序区的适当位置
        for i in range(len(elementlist)):

            # 取出第i个元素
            temp = elementlist[i] 

            # 折半查找适当的插入位置
            insert_index = sort.__binary_search_algorithm(elementlist, temp, 0, i-1)

            # 从后往前移动插入位置之后的元素
            for k in range(i, insert_index, -1):
                elementlist[k] = elementlist[k-1]
                
            # 插入元素
            elementlist[insert_index] = temp

        return elementlist


    @staticmethod
    def shell_sort(elementlist: list)->list:
        '''希尔（Shell）排序算法，又称缩小增量排序算法'''

        # 数组长度，后面用的比较多，就单独存放一个变量
        elementlist_len = len(elementlist)

        # Shell排序到目前为止尚未求得一个最好的增量序列，Shell本人给出的方法是
        # d(1) = n/2，d(i+1) = d(i)//2，且最后一个增量等于1
        dk = len(elementlist) // 2

        # 每一次循环都缩小一次增量dk，直到增量缩小到1则排序完成
        while dk >= 1:

            # 对dk个增量序列分别进行排序
            for shift in range(dk):
                
                # Shell排序理论上空间复杂度为O(1)，但为了复用上面的折半查找排序的代码，就用一个辅助列表来存储每一个增量序列的元素吧
                grouplist = list()

                # 从原列表里取出一个增量的所有元素
                elementlist_index = shift
                while elementlist_index < elementlist_len:
                    grouplist.append(elementlist[elementlist_index])
                    elementlist_index = elementlist_index + dk

                # 对增量序列进行排序（暂且用折半查找排序吧）
                grouplist = sort.binary_search_insert_sort(grouplist)

                # 将排好序的元素放回原位置
                elementlist_index = shift
                grouplist_index = 0
                while elementlist_index < elementlist_len:
                    elementlist[elementlist_index] = grouplist[grouplist_index]
                    
                    # 加上偏移量
                    elementlist_index = elementlist_index + dk
                    grouplist_index = grouplist_index + 1

                # 清空辅助列表
                grouplist.clear()

            # 增量减半
            dk = dk // 2

        return elementlist


    @staticmethod   
    def bubble_sort(elementlist: list)->list:
        '''冒泡排序算法'''

        # 原理很简单，但是却很慢，平均时间复杂度O(n^2)

        # 数组长度，后面用的比较多，就单独存放一个变量
        elementlist_len = len(elementlist)

        # 外层循环，每一趟确定一个元素的最终位置（从最大到最小）
        for i in range(elementlist_len - 1):

            # 内层循环，完成具体的冒泡过程
            for j in range(elementlist_len - i - 1):

                # 若前一个数比后一个数大，则交换位置
                if elementlist[j] > elementlist[j+1]:
                    temp = elementlist[j+1]
                    elementlist[j+1] = elementlist[j]
                    elementlist[j] = temp

        return elementlist


    @staticmethod
    def quick_sort(elementlist: list, first_index: int = 0, last_index: int = -2)->list:
        '''快速排序算法'''

        # 快速排序算法是一个分治算法（使用递归实现），因而需要用first_index和last_index指出递归范围

        # -2是个定义域外的值，此处用来表示默认的最后一个元素的下标（因为静态方法无法直接通过形参获取数组长度，只能自己计算）
        if last_index == -2:
            last_index = len(elementlist) - 1

        # 防止递归时数组越界（当分界元素处于0号位置时，其左子序列的last_index就会等于-1，要对其进行修正）
        if last_index == -1:
            last_index = 0

        # 只有当元素个数不少于1个时才能划分递归范围
        if first_index < last_index:

            # 选出一个分界元素（默认第一个吧）
            element = elementlist[first_index]

            # 从两端起扫描的指针
            less_index = first_index
            greater_index = last_index

            # 对数组进行一趟划分
            while less_index < greater_index:

                # greater_index指针从后向前寻找小于element的元素
                while less_index < greater_index and elementlist[greater_index] >= element:
                    greater_index = greater_index - 1
                    
                # 将找到的元素与less_index指针指向的元素交换位置
                if elementlist[less_index] != elementlist[greater_index]:
                    temp = elementlist[less_index]
                    elementlist[less_index] = elementlist[greater_index]
                    elementlist[greater_index] = temp

                # less_index指针从前向后寻找大于element的元素
                while less_index < greater_index and elementlist[less_index] <= element:
                    less_index = less_index + 1
                
                # 将找到的元素与greater_index指针指向的元素交换位置
                if elementlist[less_index] != elementlist[greater_index]:
                    temp = elementlist[less_index]
                    elementlist[less_index] = elementlist[greater_index]
                    elementlist[greater_index] = temp

            # 当less_index和greater_index指针相遇之后，该位置即为分界元素的位置（这一行代码似乎多余）
            #elementlist[less_index] = element
            
            # 这一趟划分得到了两个子区间，再分别对子区间递归划分
            return sort.quick_sort(sort.quick_sort(elementlist, first_index, less_index - 1), less_index + 1, last_index)
        
        return elementlist


    @staticmethod
    def select_sort(elementlist: list)->list:
        '''简单选择排序算法'''

        # 每一趟遍历确定一个元素的位置
        for i in range(len(elementlist)):

            # 存放无序区最小的元素的下标
            min_index = i

            # 找到无序区最小的元素
            for j in range(i, len(elementlist)):
                if elementlist[j] < elementlist[min_index]:
                    min_index = j

            # 交换最小元素和当前元素位置
            temp = elementlist[i]
            elementlist[i] = elementlist[min_index]
            elementlist[min_index] = temp

        return elementlist

    @staticmethod
    def __build_max_heap(elementlist: list, last_index: int)->list:
        '''大根堆建堆算法，对last_index（含）之前的列表元素建立大根堆'''

        # 方便起见使用非递归算法，需要一个栈，放入初始元素的下标
        stack = [last_index // 2]

        while len(stack) > 0:

            # 取出当前需要调整的根节点下标，计算其左右子树下标
            index = stack.pop()
            left_child_index = index * 2 + 1
            right_child_index = index * 2 + 2

            # 若根节点需要与左子树节点交换
            if left_child_index <= last_index and elementlist[left_child_index] > elementlist[index]:
                temp = elementlist[index]
                elementlist[index] = elementlist[left_child_index]
                elementlist[left_child_index] = temp

                # 左子树节点入栈，检查其性质是否被破坏
                stack.append(left_child_index)

            # 若根节点需要与右子树节点交换
            if right_child_index <= last_index and elementlist[right_child_index] > elementlist[index]:
                temp = elementlist[index]
                elementlist[index] = elementlist[right_child_index]
                elementlist[right_child_index] = temp

                # 右子树节点入栈，检查其性质是否被破坏
                stack.append(right_child_index)
            
            # 若栈空且排序尚未完成，则继续扫描前一个根节点
            if len(stack) == 0 and index > 0:
                stack.append(index - 1)

        return elementlist


    @staticmethod
    def heap_sort(elementlist: list)->list:
        '''堆排序算法'''

        # 每一趟将[0,i+1]的无序区建立为大根堆
        for i in range(len(elementlist)-1, 0, -1):
            
            # 对前i个元素建立大根堆
            sort.__build_max_heap(elementlist, i)

            # 将堆顶元素与堆底元素交换位置
            temp = elementlist[0]
            elementlist[0] = elementlist[i]
            elementlist[i] = temp

        return elementlist


    @staticmethod
    def merge_sort(elementlist: list, first_index: int=0, last_index: int=-2)->list:
        '''2路归并排序算法'''

        if last_index == -2:
            last_index = len(elementlist) - 1

        # 当列表可分割时
        if last_index - first_index > 1:

            # 计算分割元素下标
            mid_index = (first_index + last_index) // 2

            # 分治获得前后两个有序列表
            elementlist = sort.merge_sort(sort.merge_sort(elementlist, first_index, mid_index), mid_index + 1, last_index)

            # 两个有序列表需要归并为一个有序列表
            if elementlist[mid_index] > elementlist[mid_index + 1]:
                
                # 复制一个副本
                temp_list = elementlist.copy()
                
                # 两个有序列表的下标以及elementlist的下标
                i, j, k = first_index, mid_index + 1, first_index

                # 同时扫描前后两个有序列表，选出小的元素放进副本
                while i <= mid_index and j <= last_index:

                    if temp_list[i] < temp_list[j]:
                        elementlist[k] = temp_list[i]
                        i = i + 1
                    else:
                        elementlist[k] = temp_list[j]
                        j = j + 1

                    k = k + 1

                # 扫描结束，可能会有一个有序表有剩余，将剩余的内容复制到副本
                while i <= mid_index:
                    elementlist[k] = temp_list[i]  
                    i = i + 1
                    k = k + 1

                while j <= last_index:
                    elementlist[k] = temp_list[j] 
                    j = j + 1
                    k = k + 1

                return elementlist


        # 当列表不可分割时（即只有两个元素时），对两个元素排序即可
        if elementlist[first_index] > elementlist[last_index]:
            temp = elementlist[first_index]
            elementlist[first_index] = elementlist[last_index]
            elementlist[last_index] = temp   

        return elementlist



    @staticmethod
    def get_a_random_elementlist(count: int, min=0, max=65535) -> list:
        '''生成一个随机列表'''

        elementlist = list()

        for i in range(count):
            elementlist.append(random.randint(min, max))

        return elementlist


    @staticmethod
    def orderliness_check(elementlist: list, ascending=True)->bool:
        '''检查列表的有序性'''

        # 升序检查
        if ascending:
            for i in range(1, len(elementlist)):
                if elementlist[i] < elementlist[i-1]:
                    return False
        # 降序检查
        else:
            for i in range(1, len(elementlist)):
                if elementlist[i] > elementlist[i-1]:
                    return False

        return True


    @staticmethod
    def reverse(elementlist: list)->list:
        '''将列表元素翻转'''

        # 列表长度
        last_index = len(elementlist) - 1

        # 遍历列表
        index = 0
        while index < last_index - index:

            # 交换列表的第index个元素和倒数第index个元素
            temp = elementlist[index]
            elementlist[index] = elementlist[last_index - index]
            elementlist[last_index - index] = temp

            # 自增数组下标
            index = index + 1

        return elementlist


if __name__ == "__main__":

    #------生成待排序的数组------
 
    # 升序序列
    #elementlist = list(range(0, 1000))

    # 降序序列
    #elementlist = list(range(999, -1, -1))

    # 自动生成若干个随机数序列
    elementlist = sort.get_a_random_elementlist(10000)
   
    # 元素高度重复的序列
    #elementlist = sort.get_a_random_elementlist(1000, 1, 10)

    # 使用python自带的排序算法获得的标准结果
    standard_list = elementlist.copy()
    standard_list.sort()

    # 打印生成的随机数序列
    #print(elementlist)



    # 以下算法按照在本人电脑上实际排序的速度由慢到快排列，测试结果详见附表

    # 堆排序
    #elementlist = sort.heap_sort(elementlist)

    # 冒泡排序
    #elementlist = sort.bubble_sort(elementlist)

    # 直接插入排序
    #elementlist = sort.direct_search_insert_sort(elementlist)

    # 简单选择排序
    #elementlist = sort.select_sort(elementlist)

    # 折半插入排序
    #elementlist = sort.binary_search_insert_sort(elementlist)

    # 2路归并排序
    #elementlist = sort.merge_sort(elementlist)

    # 希尔（Shell）排序
    #elementlist = sort.shell_sort(elementlist)

    # 快速排序，实测平均时间复杂度为O(n log n)
    elementlist = sort.quick_sort(elementlist)

    # 作为对比，list自带的sort()方法（Timsort算法），实测平均时间复杂度为O(n log n)
    #elementlist.sort()


    # 打印排序结果
    #print(elementlist)

    # 将列表元素倒序排列
    #elementlist = sort.reverse(elementlist)

    # 检查排序结果是否为升序
    if not sort.orderliness_check(elementlist):
        print("Orderliness check failed.")

    # 检查排序结果是否与标准结果相等
    for i in range(len(elementlist)):
        if elementlist[i] != standard_list[i]:
            print("Standard check failed at index {}.".format(i))
            break
        
'''
各排序算法测试结果（单位：秒）
测试环境：Dell XPS13 9343, i7-5500U, 8GB, Ubuntu 20.04 64bit, python 3.8.2 64bit
计时工具：linux自带的time命令

+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|   Algorithm   | 1K,asc | 1K,desc | 1K,random | 10K,asc | 10K,desc | 10K,random | 100K,random | 1M,random | 10M,random |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|      heap     |   0.55 |    0.37 |      0.47 |   49.86 |    36.80 |      44.83 |         *** |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|     bubble    |   0.07 |    0.11 |      0.09 |    4.54 |    10.25 |       7.95 |         *** |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
| direct_search |   0.05 |    0.04 |      0.05 |    2.92 |     3.66 |       3.49 |         *** |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|     select    |   0.06 |    0.05 |      0.05 |    3.15 |     3.36 |       3.18 |         *** |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
| binary_search |   0.02 |    0.05 |      0.04 |    0.05 |     3.64 |       2.02 |      291.90 |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|     merge     |   0.02 |    0.02 |      0.02 |    0.02 |     0.28 |       0.27 |       58.55 |       *** |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|     Shell     |   0.03 |    0.04 |      0.02 |    0.36 |     0.33 |       0.37 |        6.34 |     86.94 |        *** |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|   quick_sort  |  *0.06 |   *0.07 |      0.01 |      ** |       ** |       0.06 |        0.49 |      6.21 |     136.29 |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
|  list.sort()  |   0.01 |    0.01 |      0.02 |    0.02 |     0.02 |       0.02 |        0.14 |      1.31 |      16.57 |
+---------------+--------+---------+-----------+---------+----------+------------+-------------+-----------+------------+
注：
-   1K,10K,100K,1M,10M为排序的元素个数，asc为初始升序，desc为初始降序，random为随机序列

*   实际是对998个升序、降序元素进行排序的结果。python虚拟机默认限制递归栈的深度为1000，对1000个升序元素进行
    快速排序时会导致递归栈溢出（除去<module>和quick_sort两层函数栈，最多支持998次递归）。
    当然也可以手动将递归栈的深度限制设置得大一点，可以使用如下代码：
    import sys
    sys.setrecursionlimit = 2000

**  递归栈溢出，无法测试

*** 时间复杂度为O(n^2)，预估运行时间在5分钟以上，没有测试的必要了

'''