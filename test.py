# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:30:21 2022

@author: ameli
"""

class Student:
    course = ''
    grade = ''
    
    def __init__ (self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = [float(m) for m in marks.split(',')]
        self.final_mark = self.get_final_mark()
        
    def get_final_mark (self):
      weighted_sum = (round(self.marks[0]*0.2,2) 
                     + round(self.marks[1]*0.4,2)
                     + round(self.marks[2]*0.4,2))
      return -(-weighted_sum//1)
  
    def __str__(self):
        return f'{self.id}\t{self.name}\t{self.course}\t{self.final_mark}\t{self.grade}'
    
class BIT(Student):
    grade_point = {'HD': 4.0, 'D': 3.0, 'C': 2.0, 'P': 1.0, 'SP': 0.5, 'F': 0}
    course = 'BIT'
    
    def __init__(self, student_id, name, marks):
        super().__init__(student_id, name, marks)
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
    grade_point = {'CP': 4.0, 'NC': 0}
    course = 'DIT'
    
    def __init__(self, student_id, name, marks):
        super().__init__(student_id, name, marks)
        self.grade = self.get_grade
        
    def get_grade(self):
        return 'NYC' if self.final_mark < 50 else 'CP'
    
    def update_marks(self, new_marks):
        self.marks = [float(m) for m in new_marks.split(',')]
        self.final_mark = self.final_mark()
        self.grade = 'NC' if self.final_mark < 50 else 'CP'
        
class PerformanceStats:
    
    def __init__(self, students):
        self.students = set(students)
        self.size = len(self.students)
        self.grades = [s.grade for s in self.students]
        self.courses = [s.course for s in self.students]
        
    def total_bit(self):
        return self.courses.count('BIT')
    
    def total_dit(self):
        return self.courses.count('DIT')
    
    def get_pass_rate(self):
       pass_rate = sum([self.grades.count(grade)
                        for grade in ('HD','D','C','P','SP','CP')/self.size])
       return pass_rate      
   
    def get_pass_rate_adj(self):
        adj_pass_rate = sum([self.grades.count(grade)
                         for grade in ('HD','D','C','P','SP','CP')
                         / (self.size - self.grades.count('AF'))])
        return adj_pass_rate
    
    def get_avg_marks(self):
        avg_marks = []
        for i in range(3):
            avg_marks.append(sum([s.marks[i]
                             for s in self.students])/self.size)
            
        return avg_marks
    
    def get_avg_final(self):
        return sum(s.final_marks for s in self.students)/self.size
    
    def get_avg_gp(self):
        # dict (grade:point)
        gp_dict = {}
        gp_dict.update(BIT.grade_point)
        gp_dict.update(DIT.grade_point)
        
        return len(self.grades)/self.size
    
    def grade_count(self):
        grade_count = {}
        grade_count.update({grade: self.grades.count(
            grade) for grade in 'HD D C P SP CP NC'.split()})  
        return grade_count
    
    def print_grade(self, order):
        if order == 'asc':
            list = sorted(self.students, reverse=False)
        else:
            list = sorted(self.students, reverse=True)
        
        for s in list:
            print(s)
    
    def print_stats(self):
        print("Number of students:", self.size)
        print("Number of BIT students:", [self.total_bit()])
        print("Number of DIT students:", [self.total_dit()])
        print("Student pass rate: {:.2f}%".format(self.get_pass_rate()*100))
        try:
            print("Student pass rate (adjusted): {:.2f}%".format(self.get_pass_rate_adj()*100))
        except ZeroDivisionError:
            print("All the BIT students has failed with AF grade")
        
        for i in range(3):
            print("Average mark for Assessment {i+1}: {:.2f}", {self.get_avg_marks()[i]})
        print("Average final mark:", round(self.get_avg_final(),2))
        print("Average grade point:", round(self.get_avg_gp(),2))
        for grade in "HD D C P SP F".split():
            print(f'Number of {grade}s: {self.grade_count[grade]}')
        
# marks validatition
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
        print('Student ID can not be empty')
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
        print('Student name can not be empty')
        return False, '', '', ''
    marks = input(
        'Enter student assessment marks (separated by comma):\n')
    if not validated_marks(marks):
        print('InputError: Student assessment marks (separated by comma)')
        return False, '', '', ''
    return validate, id, name, marks

def main_menu():
    return("""Choose one of the following options:
    1 - Enter student grade information
    2 - Print all student grade information
    3 - Print class performance statistics
    4 - Exit
    Enter your choice here: """)
    
def option1():
    return("""Choose one of the following options:
    1.1 - Enter a BIT student information   
    1.2 - Enter a DIT student information   
    1.3 - Go back to the main menu          
    Enter your choice here: """)
    
def option2():
    return("""Choose one of the following options: 
    2.1 - Print all student grade information ascendingly by final mark
    2.2 - Print all student grade information descendingly by final mark
    2.3 - Go back to the main menu        
    Enter your choice here: """)
    
def option3():
    PerformanceStats.print_stats()

def main():
    student_list = []
    performance = PerformanceStats(student_list)
    while True:
        user_choice = int(input(main_menu()))
        if user_choice == 1:
            while True:
                user_choice = float(input(option1()))
                if user_choice == 1.1:
                    while  True:
                        validate, id, name, marks = record_input()
                        if validate:
                            student = BIT(id,name,marks)
                            if student.grade in ['SE','SA']:
                                subject = 'exam' if student.marks[2] < 50 else 'assessment'
                                new_mark = input(
                                    f"What is this student's supplementary {subject} mark: \n")
                                student.update_marks(new_mark)
                            student_list.append(student)
                            break
                elif user_choice == 1.2:
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
                elif user_choice == 1.3:
                    performance = PerformanceStats(student_list)
                    break
                else:
                    print("Please select 1.1, 1.2, or 1.3: ")

        elif user_choice == 2:
            while True:
                user_choice = float(input(option2()))
                if user_choice == 2.1:
                    if student_list:
                        performance.print_grade('asc')
                    else:
                        print("Can't find any student record.")
                elif option2 == 2.2:
                    if student_list:
                        performance.print_grade('desc')
                    else:
                        print("Can't find any student record.")
                elif option2 == 2.3:
                    break
                else:
                    print('Input should only be "2.1" or "2.2" or "2.3"')
        elif user_choice == 3:
            if student_list:
                option3()
            else:
                print("No records found. Please enter student record.")
        elif user_choice == 4:
            break
        else:
            print('Input should only be a whole number between 1 and 4')
            

if __name__ == '__main__':
    main()