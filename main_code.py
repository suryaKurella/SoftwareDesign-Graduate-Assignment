import os
import random
import re
import sys
from pathlib import Path
from tree_sitter import Language, Parser
from validations import final_validator

v_errors_list = []
file_path_op1 = sys.argv[4]
file_path_op2 = sys.argv[5]

# This functions parses the input file based on the file's extension, run validations and identify the identifiers
def parser_run_function(language, language_extension):
    parser = Parser()
    parser.set_language(language)
    dict = {}

    def treeParser(node, unique, file_path):
        leaves = node.children
        for i in range(len(leaves)):
            if leaves[i].type == 'statement_block':
                with open(rf'{file_path}', encoding="utf8") as read_file:
                    k = read_file.readlines()[leaves[i].start_point[0]]
                    enum_lis = k[leaves[i].start_point[1]: leaves[i].end_point[1]]
                    lis = re.findall("[a-zA-Z0-9]+", enum_lis)
                    enum_lis = lis
                    sorted_lis = sorted(lis)

                    if enum_lis != sorted_lis:
                        v_errors_list.append("Enumeration Identifier Declaration Order")

            if leaves[i].type == 'identifier':
                dict[unique] = [leaves[i].start_point, leaves[i].end_point]
            treeParser(leaves[i], random.randint(1, sys.maxsize), file_path)

    cwd = os.getcwd() + os.path.sep + "cloned_git_folder"

    pathlist = Path(cwd).rglob(f'*.{language_extension}')
    for path in pathlist:
        path_in_str = str(path)
        basename = os.path.basename(path_in_str)
        print(f' File names = {path_in_str}')
        text_file = open(path_in_str, encoding="utf8")
        data = text_file.read()
        text_file.close()
        tree = parser.parse(bytes(data, "utf8"))
        root_node = tree.root_node
        treeParser(root_node, 0, path_in_str)
        f = open(file_path_op1, "a")
        f2 = open(file_path_op2, "a")
        f.write(
            f'\n----------------------Identifiers for file {basename}-----------------------------------\n\n')

        for key, value in dict.items():
            start, end = value
            with open(rf'{path_in_str}', encoding="utf8") as fp:
                x = fp.readlines()[start[0]]
                ident = (x[start[1]: end[1]]).strip()
                row_no = start[0]
                col_no = [start[1], end[1]]

                errors_list = final_validator(ident.strip())
                if len(v_errors_list) != 0:
                    errors_list.append(v_errors_list)
                if len(errors_list) != 0:
                    f2.write(
                        f'identifier = {ident}, Row = {row_no}, Col = {col_no} Failed Reason : {errors_list}\n')

                f.write(f'identifier = {ident}, Row = {row_no}, Col = {col_no}\n')

        f.write(
            f'\n------------------------------------------------------------------------------------------\n')

        f2.write(
            f'\n-----------------------------------------------------------------------------------------------------------------------------\n')

        f2.write(f'File writing done for file {basename}')
        f2.write(
            f'\n-----------------------------------------------------------------------------------------------------------------------------\n')

        f.close()
        dict.clear()
