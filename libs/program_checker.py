'''Function to check if a program exists for the use by a plugin'''
import platform
from shutil import which

def check_for_required_programs(
        program_list: list,
        plugin: str = None,
        output: bool = True
) -> tuple:
    '''checks list for required programs and warns if not installed'''
    if platform.system() == 'Linux':
        return __linux(program_list, plugin, output)
    return "OTHER OS's NOT IMPLEMENTET", 1

def __linux(
        program_list: list,
        plugin: str = None,
        output: bool = True
) -> tuple:
    '''checks list for required programs and warns if not installed'''
    all_there = True
    missing_program_list = []
    for program in program_list:
        if which(program) is None:
            missing_program_list.append(program)
            all_there = False
    if not all_there:
        message = "MISSING THE FOLLOWING PROGRAMS: {}".format(" ".join(missing_program_list))
        if plugin is not None:
            if output:
                print(plugin.upper(), message)
            return "{} {}".format(plugin.upper(), message), 1
        else:
            if output:
                print(message)
            return message, 1
    return True, 0
