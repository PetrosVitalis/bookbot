# from functions.get_files_info import get_files_info

# def run_tests():
#     print("Result for current directory:")
#     print(get_files_info("calculator", "."))
#     print()
#     print("Result for 'pkg' directory:")
#     print(get_files_info("calculator", "pkg"))
#     print()
#     print("Result for '/bin' directory:")
#     print(get_files_info("calculator", "/bin"))
#     print()
#     print("Result for '../' directory:")
#     print(get_files_info("calculator", "../"))

# if __name__ == "__main__":
#     run_tests()

# from functions.write_file import write_file

# def run_tests():
#     print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
#     print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#     print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

# if __name__ == "__main__":
#     run_tests()

from functions.run_python_file import run_python_file

def run_tests():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    run_tests()