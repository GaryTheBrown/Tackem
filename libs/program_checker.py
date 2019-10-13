'''Function to check if a program exists for the use by a plugin'''
from shutil import which


def check_for_required_programs(
        program_list: list,
        plugin: str = None,
        output: bool = True
    ) -> bool:
    '''checks list for required programs and warns if not installed'''
    all_there = True
    missing_program_list = []
    for program in program_list:
        if which(program) is None:
            missing_program_list.append(program)
            all_there = False
    if not all_there and output:
        message = "MISSING THE FOLLOWING PROGRAMS: " + " ".join(missing_program_list)
        if plugin is not None:
            print(plugin.upper(), message)
        else:
            print(message)
    return all_there
