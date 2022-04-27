# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:07:13 2022

@author: ameli
"""

class Student:
    course = ''
    grade = ''

    def __init__(self, id, name, marks):
        self.id = id
        self.name = name
        self.marks = [float(m) for m in marks.split(',')]
        self.final_mark = ceil(self.get_final_mark())

    def get_final_mark(self):
        return self.marks[0] * 0.2 + self.marks[1] * 0.4 + self.marks[2] * 0.40

    def __str__(self):
        return f'{self.id}\t{self.name}\t{self.course}\t{self.final_mark}\t{self.grade}'


class BIT(Student):
    GP = {'HD': 4.0, 'D': 3.0, 'C': 2.0, 'P': 1.0, 'SP': 0.5, 'F': 0}
    course = 'BIT'

    def __init__(self, id, name, marks):
        Student.__init__(self, id, name, marks)
        self.grade = self.get_grade()

    def get_grade(self):
        if self.final_mark < 45:
            return 'AF' if self.marks.count(0) > 1 else 'F'
        elif self.final_mark < 50:
            if self.marks.count(0.0) == 0 and len(list(x for x in self.marks if x < 50)) == 1:
                return 'SE' if self.marks[2] < 50 else 'SA'
            else:
                return 'F'
        elif self.final_mark < 65:
            return 'P'
        elif self.final_mark < 75:
            return 'C'
        elif self.final_mark < 85:
            return 'D'
        else:
            return 'HD'

    def update_marks(self, new_mark):
        # marks wont affect final_mark/avg_mark
        # for i in range(len(self.marks)):
        #     if self.marks[i] < 50:
        #         self.marks[i] = float(new_mark)
        self.grade = 'SP' if float(new_mark) >= 50 else 'F'


class DIT(Student):
    GP = {'CP': 4.0, 'NC': 0}
    course = 'DIT'

    def __init__(self, id, name, marks):
        Student.__init__(self, id, name, marks)
        self.grade = self.get_grade()

    def get_grade(self):
        return 'NYC' if self.final_mark < 50 else 'CP'

    def update_marks(self, new_marks):
        self.marks = [float(m) for m in new_marks.split(',')]
        self.final_mark = ceil(self.get_final_mark())
        self.grade = 'NC' if self.final_mark < 50 else 'CP'


class ClassPerformance():
    def __init__(self, students):
        self.students = set(students)
        self.size = len(self.students)
        self.grades = [s.grade for s in self.students]
        self.courses = [s.course for s in self.students]

        self.grade_number_dict = self.get_grade_number_dict()

    def size_bit(self):
        return self.courses.count('BIT')

    def size_dit(self):
        return self.courses.count('DIT')

    def get_pass_rate(self):
        s = sum([self.grades.count(grade)
                for grade in 'HD D C P SP CP'.split()])
        return s/self.size

    def get_pass_rate_adj(self):
        s = sum([self.grades.count(grade)
                for grade in 'HD D C P SP CP'.split()])
        return s / (self.size - self.grades.count('AF'))

    def get_avg_marks(self):
        avg_marks = []
        for i in range(3):
            avg_marks.append(sum([s.marks[i]
                             for s in self.students])/self.size)
        return avg_marks

    def get_avg_final(self):
        return sum([s.final_mark for s in self.students])/self.size

    def get_avg_gp(self):
        # init dict(grade:point)
        gp_dict = {}
        gp_dict.update(BIT.GP)
        gp_dict.update(DIT.GP)
        total = sum(self.grades.count(grade) * point for grade,
                    point in gp_dict.items() if grade in self.grades)
        return total/self.size

    def get_grade_number_dict(self):
        grade_number_dict = {}
        grade_number_dict.update({grade: self.grades.count(
            grade) for grade in 'HD D C P SP CP NC'.split()})
        grade_number_dict.update(
            {'F': self.grades.count('F')+self.grades.count('AF')})
        return grade_number_dict

    def print_grade(self, order):
        if order == 'ASC':
            l = sorted(self.students, reverse=False,
                       key=lambda x: x.final_mark)
        else:
            l = sorted(self.students, reverse=True,
                       key=lambda x: x.final_mark)
        for s in l:
            print(s)

    def print_performances(self):
        print(f'Number of students: {self.size}')
        print(f'Number of BIT students: {self.size_bit()}')
        print(f'Number of DIT students: {self.size_dit()}')
        print(f'Student pass rate: {self.get_pass_rate()*100:.2f}%')
        try:
            print(
                f'Student pass rate (adjusted): {self.get_pass_rate_adj()*100:.2f}%')
        except ZeroDivisionError:
            print('All the BIT students have received Absent Fail final grade')
        for i in range(3):
            print(
                f'Average mark for Assessment {i+1}: {self.get_avg_marks()[i]:.2f}')
        print(f'Average final mark: {self.get_avg_final():.2f}')
        print(f'Average grade point: {self.get_avg_gp():.1f}')
        for grade in 'HD D C P SP CP F'.split():
            print(
                f'Number of {grade}s: {self.grade_number_dict[grade]}')


# ceil func to get student mark
def ceil(n):
    return int(-1 * n // 1 * -1)


# marks validation
def validated_marks(marks):
    mark_list = marks.split(',')
    if len(mark_list) != 3:
        return False
    else:
        try:
            for i in mark_list:
                if not (0 <= float(i) <= 100):
                    return False
        except ValueError:
            return False
    return True


# student id validation
def validated_id(id):
    if not id:
        print('Student ID can not be empty, please enter capital A followed by 8 digits ')
        return False
    if len(id) != 9 or id[0] != 'A':
        print('Invalid Student ID, please enter capital A followed by 8 digits')
        return False
    for c in id[1::]:
        if c not in [str(n) for n in range(10)]:
            print('Invalid Student ID, please enter capital A followed by 8 digits')
            return False
    return True


# take input and validate
def record_input():
    validate = True
    id = input('Enter student ID:\n')
    if not validated_id(id):
        return False, '', '', ''
    name = input('Enter student name:\n')
    if not name:
        print('InputError: Student name can not be empty')
        return False, '', '', ''
    marks = input(
        'Enter student assessment marks (separated by comma):\n')
    if not validated_marks(marks):
        print('InputError: Student assessment marks (separated by comma)')
        return False, '', '', ''
    return validate, id, name, marks


def main():
    student_list = []
    performance = ClassPerformance(student_list)
    while True:
        option0 = input(
            """Choose one of the following options:
1 - Enter student grade information
2 - Print all student grade information
3 - Print class performance statistics
4 - Exit
""")
        if option0 == '1':
            while True:
                option1 = input(
                    """Choose one of the following options:
1.1 - Enter a BIT student information
1.2 - Enter a DIT student information
1.3 - Go back to the main menu
""")
                if option1 == '1.1':
                    while True:
                        validate, id, name, marks = record_input()
                        if validate:
                            student = BIT(id, name, marks)
                            if student.grade in ['SE', 'SA']:
                                subject = 'exam' if student.marks[2] < 50 else 'assessment'
                                new_mark = input(
                                    f"What is this student's supplementary {subject} mark: \n")
                                student.update_marks(new_mark)
                            student_list.append(student)
                            break
                elif option1 == '1.2':
                    while True:
                        validate, id, name, marks = record_input()
                        if validate:
                            student = DIT(id, name, marks)
                            if student.grade == 'NYC':
                                new_marks = input(
                                    "What is this student's resubmission marks (separated by comma): \n")
                                student.update_marks(new_marks)
                            student_list.append(student)
                            break
                elif option1 == '1.3':
                    performance = ClassPerformance(student_list)
                    break
                else:
                    print('Input should only be "1.1" or "1.2" or "1.3"')

        elif option0 == '2':
            while True:
                option2 = input(
                    """Choose one of the following options:
2.1 - Print all student grade information ascendingly by final mark
2.2 - Print all student grade information descendingly by final mark
2.3 - Go back to the main menu
""")
                if option2 == '2.1':
                    if student_list:
                        performance.print_grade('ASC')
                    else:
                        print("Can't find any student record")
                elif option2 == '2.2':
                    if student_list:
                        performance.print_grade('DESC')
                    else:
                        print("Can't find any student record")
                elif option2 == '2.3':
                    break
                else:
                    print('Input should only be "2.1" or "2.2" or "2.3"')
        elif option0 == '3':
            if student_list:
                performance.print_performances()
            else:
                print('No records found, please enter student record')
        elif option0 == '4':
            break
        else:
            print('Input should only be a whole number between 1 and 4')


if __name__ == '__main__':
    main()