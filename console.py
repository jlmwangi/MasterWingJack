#!/usr/bin/python3
'''command interpreter to handle the objects creation, update, reading and deletion'''

import cmd
from models import storage
from models.base_model import BaseModel
from models.student import Student
from models.instructor import Instructor
from models.lesson import Lesson
from dotenv import load_dotenv


load_dotenv()


class MWJCommand(cmd.Cmd):
    """entry point of the command interpreter"""
    prompt = "(MWJ) "

    classnames = {
        "BaseModel": BaseModel,
        "Student": Student,
        "Instructor": Instructor,
        "Lesson": Lesson
    }

    """_instances = []

    def __init__(self):
        super().__init__()
        MWJCommand._instances.append(self)"""

    def do_quit(self, arg):
        '''exits the program'''
        print("Exiting Interpreter")
        return True

    def do_EOF(self, arg):
        """exits interpreter"""
        return True

    def emptyline(self):
        """doesnt do anyhting"""
        pass

    def do_create(self, arg):
        """creates a new instance , saves it and prints the id"""
        if arg:
            if len(arg) == 1:
                if arg in self.classnames:
                    cls = self.classnames[arg]
                    instance = cls()
                    instance.save()
                    print(f"{instance.id}")
                else:
                    print("** class doesn't exist **")
            elif len(arg) > 1:
                args = arg.split(" ")
                class_name = args[0]
                params = args[1:]

                param_dict = {}
                for param in params:
                    if "=" in param:
                        key, value = param.split("=", 1)
                        if value.startswith('"') and value.endswith('"'):
                            '''eg 'my"str"ing', escape it to use value as mystring'''
                            value = value.strip('"')  #.replace("_", " ")
                        elif '_' in value:
                            val = value.replace("_", " ")
                        elif '.' in value and '@' not in value:
                            val = float(value)
                        elif value.isdigit():
                            val = int(value)
                        else:
                            val = value.strip('"')

                        param_dict[key] = value
                    else:
                        print(f"** invalid parameter: {param} **")

                # create instance
                if class_name in self.classnames:
                    cls = self.classnames[class_name]
                    instance = cls(**param_dict)

                    session = storage._DBStorage__session

                    #link student with a default instructor and lesson
                    if class_name == "Student":
                        storage.new(instance)

                        # ensure lesson and student are in same session
                        lesson_name = param_dict.get("lesson")
                        if lesson_name:
                            lesson = session.query(Lesson).filter(Lesson.name.ilike(lesson_name)).first()
                            if lesson:
                                instance.lessons.append(lesson)

                        # ensure instructor and student are in the same session
                        instructor_name = param_dict.get("instructor")
                        if instructor_name:
                            """look for instructor with the name"""
                            instructor = session.query(Instructor).filter(Instructor.name.ilike(instructor_name)).first()
                            if instructor:
                                instance.instructors.append(instructor)

                        #commit the links
                        storage.save()

                    elif class_name == "Instructor":
                        # pass STUDENT as kwargs with a value(name) to link to this instructor
                        storage.new(instance)

                        student_name = param_dict.get("student")
                        if student_name:
                            """look for student with the name"""
                            student = session.query(Student).filter(Student.name.ilike(student_name)).first()
                            if student:
                                instance.students.append(student)
                            '''for student in storage.all(Student).values():
                                if getattr(student, "name", "").lower() == student_name.lower():
                                    instance.students.append(student)
                                    break'''

                        lesson_name = param_dict.get("lesson")
                        if lesson_name:
                            lesson = session.query(Lesson).filter(Lesson.name.ilike(lesson_name)).first()
                            if lesson:
                                instance.lessons.append(lesson)
                            '''for lesson in storage.all(Lesson).values():
                                if getattr(lesson, "lesson", "").lower() == lesson_name.lower():
                                    instance.lessons.append(lesson)
                                    break'''

                        # save the linkages
                        storage.save()

                    #link lesson with nstructor and student
                    elif class_name == "Lesson":
                        # pass INSTRUCTOR as kwargs with value(name) to link to this lesson
                        student_name = param_dict.get("student")
                        instructor_name = param_dict.get("instructor")

                        storage.new(instance)

                        if instructor_name:
                            """look for instructor with the name"""
                            for inst in storage.all(Instructor).values():
                                if getattr(inst, "instructor", "").lower() == instructor_name.lower():
                                    instance.instructors.append(inst)
                                    #storage.new(instance)
                                    break

                        if student_name:
                            """look for student with the name"""
                            for student in storage.all(Student).values():
                                if getattr(student, "name", "").lower() == student_name.lower():
                                    instance.students.append(student)
                                    #storage.new(instance)
                                    break

                        # commit relationships after linking
                        storage.save()

                    # save instance
                    instance.save()
                    storage.save()
                    print(f"{instance.id}")
                else:
                    print("** class doesn't exist **")
            else:
                print("** class name missing **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """prints str rep of an instance based on class name and id"""
        args = arg.split()

        if len(args) == 2:
            name = args[0]
            eyed = args[1]

            if name in self.classnames:

                key = f"{name}.{eyed}"

                '''retrieve instance from storage using identified key'''
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            print("** class name missing **")

    def do_destroy(self, arg):
        """deletes an instance based on class name and id"""
        args = arg.split()

        if len(args) == 2:
            name = args[0]
            eyed = args[1]

            if name in self.classnames:

                key = f"{name}.{eyed}"

                '''retrieve instance from storage using identified key'''
                if key in storage.all():
                    del(storage.all()[key])
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            print("** class name missing **")

    def do_all(self, arg):
        """prints all string reps of all instances based or not on the class name"""
        if arg:
            if arg in self.classnames:
                objs = storage.all()
                obj_list = []

                for key, val in objs.items():
                    if key.startswith(arg):
                        obj_list.append(str(val))

                print(str(obj_list))
            else:
                print("** class doesn't exist **")
        else:
            obj_list = []
            objs = storage.all()

            for key, val in objs.items():
                obj_list.append(str(val))

            print(obj_list)

    def do_update(self, arg):
        """updates an instance based on class name and id by adding/updating attribute"""
        args = arg.split()

        if len(args) == 4:
            name = args[0]
            eyed = args[1]
            attr_name = args[2]
            attr_val = args[3]

            if name in self.classnames:

                key = f"{name}.{eyed}"

                '''retrieve instance from storage using identified key'''
                if key in storage.all():
                    accessed_instance = storage.all()[key]
                    setattr(accessed_instance, attr_name, attr_val)
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")

        elif len(args) == 3:
            print("** value missing **")

        elif len(args) == 2:
            print("** attribute name missing **")

        elif len(args) == 1:
            print("** instance id missing **")

        else:
            print("** class name missing **")

    def default(self, line):
        """called when command is not recognized"""
        if "." in line and "(" in line and line.endswith(")"):
            try:
                cls_name, rest = line.split(".", 1)
                command, args = rest.split("(", 1)
                arg_str = args[:-1].strip()

                if cls_name in self.classnames:
                    cls = self.classnames[cls_name]

                    if command == "all":
                        print(cls.all())
                        return
                    elif command == "count":
                        print(len(cls.all()))
                        return
                    elif command =="show":
                        """expecting one argument, id"""
                        if not arg_str:
                            print("** instance id missing **")
                            return

                        instance_id = arg_str.strip('"')  #strip quotes
                        for obj in cls.all():
                            if getattr(obj, "id", None) == instance_id:
                                print(obj)
                                return
                        print("** no instance found **")
                        return

                    elif command == "destroy":
                        """destroy based on the id"""
                        if not arg_str:
                            print("** instance id missing **")
                            return

                        instance_id = arg_str.strip('"')  #strip quotes

                        key = f"{cls.__name__}.{instance_id}"
                        all_objs = storage.all()

                        if key in all_objs:
                            del all_objs[key]
                            storage.save()
                            return
                        print("** no instance found **")
                        return

                    elif command == "update":
                        """update based on id, att name and att value"""
                        args = arg_str.split()
                        instance_id = args[0].strip('"')

                        if len(args) < 1:
                            print("** instance id missing **")
                            return
                        if len(args) < 2:
                            print("** attribute name missing **")
                            return
                        if len(args) < 3:
                            print("** attribute value missing **")
                            return

                        at_name = args[1].strip('"')
                        at_value = args[2].strip('"')

                        key = f"{cls.__name__}.{instance_id}"
                        all_objs = storage.all()

                        if key in all_objs:
                            setattr(all_objs[key], at_name, at_value)
                            storage.save()
                            return
                        print("** no instance found **")


            except Exception as e:
                print(f"Error: {e}")
                return

        print(f"** Unknown syntax: {line}")



if __name__ == "__main__":
    MWJCommand().cmdloop()
