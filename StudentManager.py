"""Python 命令行学生管理系统：学生信息管理、成绩排名及 JSON 数据保存。"""

import json


class Student:
    """表示一名学生，保存姓名、成绩，并根据成绩计算等级。"""
    def __init__(self, name, score):
        """创建学生对象。

        参数：
            name：学生姓名。
            score：0～100 分之间的数值，允许有小数。

        给 self.score 赋值时会调用下面的 setter；成绩超出范围时抛出 ValueError。
        """
        self.name = name
        # 使用公开属性赋值，让新建学生也经过成绩范围检查。
        self.score = score

    @property
    def score(self):
        """读取学生成绩，返回内部保存的 _score。"""
        return self._score

    @score.setter
    def score(self, new_score):
        """设置学生成绩。new_score 必须是 0～100 分之间的数值。

        成绩超出范围时抛出 ValueError，不会覆盖原成绩。
        """
        if 0<=new_score<=100:
            self._score = new_score
        else:
            raise ValueError("成绩必须在0到100之间")

    @property
    def level(self):
        """根据当前成绩返回等级：90 分起优秀、80 分起良好、60 分起及格，其余不及格。"""
        if 90<=self.score<=100:
            return "优秀"
        elif 80<=self.score<90:
            return "良好"
        elif 60<=self.score<80:
            return "及格"
        else:
            return "不及格"

class StudentManager:
    """管理一组 Student 对象，提供查询、修改、排名和文件读写功能。"""
    def __init__(self):
        """创建管理器，并用空列表保存学生对象。"""
        self.students = []

    def add_student(self, student):
        """把一个 Student 对象加入学生列表。

        参数 student 是学生对象。本方法不检查姓名是否重复，也没有显式返回值。
        """
        self.students.append(student)

    def average_score(self):
        """返回所有学生的平均分；列表为空时返回 0，避免除以零。"""
        if len(self.students) == 0:
            return 0
        else:
            sum_score = 0
            for student in self.students:
                   sum_score += student.score
            return sum_score/len(self.students)

    def find_student(self, name):
        """按姓名查找学生。

        参数 name 是待查找的姓名；找到时返回第一个匹配的 Student 对象，否则返回 None。
        """
        for student in self.students:
            if student.name == name:
                return student
        return None

    def remove_student(self, name):
        """按姓名删除第一个匹配的学生。删除成功返回 True，未找到返回 False。"""
        student = self.find_student(name)
        if student is not None:
            self.students.remove(student)
            return True
        return False

    def update_student_score(self, name, new_score):
        """按姓名修改第一个匹配学生的成绩。

        参数 name 是姓名，new_score 是新成绩。修改成功返回 True，未找到返回 False。
        赋值时会调用 Student.score 的 setter，成绩超出范围时抛出 ValueError。
        """
        student = self.find_student(name)
        if student is not None:
            student.score = new_score
            return True
        return False

    def get_ranking(self):
        """返回按成绩从高到低排列的新列表，原学生列表的顺序保持不变。"""
        sorted_students = sorted(self.students, key=lambda student: student.score, reverse=True)
        return sorted_students

    def save_to_json(self, filename):
        """把学生姓名和成绩保存到 filename 指定的 JSON 文件。

        以 UTF-8 编码写入，保留中文并缩进显示；如果文件已存在，会覆盖原文件。
        参数 filename 可以是路径；相对路径以程序运行时的当前目录为起点。
        """
        data = []
        for student in self.students:
            data.append({"name": student.name, "score": student.score})
        with open(filename, "w" ,encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename):
        """从 filename 指定的 JSON 文件加载学生，成功返回 True，已处理的失败返回 False。

        文件应是列表，每条记录包含 name 和 score。全部学生创建成功后才替换当前列表。
        本方法处理文件不存在、JSON 语法错误和成绩范围错误；其他结构或类型错误可能抛出异常。
        """
        try:
            with open(filename ,"r",encoding="utf-8") as f:
                data = json.load(f)
            # 先在临时列表中创建全部学生，成功后再更新管理器中的列表。
            new_students = []
            for student in data:
                new_students.append(Student(student["name"], student["score"]))
        except FileNotFoundError:
            print("文件不存在")
            return False
        except json.JSONDecodeError:
            print("JSON文件格式错误")
            return False
        except ValueError:
            print("学生成绩不合法")
            return False
        self.students = new_students
        return True

def run_menu(manager):
    """运行命令行菜单，操作传入的 StudentManager 对象，输入 0 时结束。

    增删改操作首先影响内存中的学生列表；需要选择 6 才会保存到 students.json。
    退出时不会自动保存。本函数没有显式返回值。
    """
    while True:
        print("\n===== 学生管理系统 =====")
        print("1. 查看所有学生")
        print("2. 添加学生")
        print("3. 删除学生")
        print("4. 修改学生成绩")
        print("5. 查看成绩排名")
        print("6. 保存学生数据")
        print("7. 加载学生数据")
        print("0. 退出系统")
        choice = input("请输入选项：").strip()

        if choice == "1":
            for student in manager.students:
                print(student.name,student.score,student.level)
        elif choice == "2":
            try:
                name=input("请输入姓名:").strip()
                score=float(input("请输入成绩:").strip())
                # is_integer() 判断浮点数是否没有小数部分，例如 90.0；转换后显示为 90。
                if score.is_integer():
                    score=int(score)
                student=Student(name,score)
                manager.add_student(student)
                print("添加成功！")
            except ValueError as e  :
                print(f"添加失败：{e}")
        elif choice == "3":
            name=input("请输入要删除的学生姓名：")
            if manager.remove_student(name):
                print("删除成功")
            else:
                print("没有找到该学生")
        elif choice == "4":
            try:
                name = input("请输入要修改的学生姓名：")
                score = float(input("请输入新成绩:").strip())
                # is_integer() 判断浮点数是否没有小数部分，例如 90.0；转换后显示为 90。
                if score.is_integer():
                    score=int(score)
                if manager.update_student_score(name,score):
                    print("成绩修改成功！")
                else:
                    print("没有找到该学生")
            except ValueError as e :
                print(f"修改失败：{e}")
        elif choice == "5":
            rank_manage=manager.get_ranking()
            for i,student in enumerate(rank_manage,start=1):
                print(f"第{i}名：{student.name} ，{student.score}分")
        elif choice == "6":
            manager.save_to_json("students.json")
            print("保存成功！")
        elif choice == "7":
            if manager.load_from_json("students.json"):
                print("加载成功！")
            else:
                print("加载失败！")
        elif choice == "0":
            print("系统已退出")
            break

        else:
            print("无效选项，请重新输入")


# 程序入口：从运行时的当前目录加载数据，再启动菜单。
manager = StudentManager()
manager.load_from_json("students.json")
run_menu(manager)