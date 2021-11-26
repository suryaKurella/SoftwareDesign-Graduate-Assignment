# -----------------------------------------------------------
# Clones the GitHub repository identifies the identifiers in files with extension py, js, go and ruby
# then writes identifiers to Output1.txt with locations and then validates the identifiers to Output2.txt
#
# (C) 2021 Suryateja Kurella, Houston, Texas
# Released under No License
# email skurella@cougarnet.uh.edu
# -----------------------------------------------------------

import os
import stat

from tree_sitter import Language
from main_code import parser_run_function
from git import Repo
import sys

github_url = sys.argv[1]
file_extension = sys.argv[2].replace('.', '').strip()
language = sys.argv[3].lower().strip()

print(sys.argv)

cwd = os.getcwd()
print(cwd)
file_path = './cloned_git_folder'
flag = False


# This function deletes the existing cloned git repository in the local if any exists
def delete_cloned_git(file_path):
    for root, dirs, files in os.walk(file_path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(file_path)


if os.path.isdir(file_path):
    path = os.path.join(os.getcwd(), 'cloned_git_folder')
    delete_cloned_git(path)
Repo.clone_from(github_url, "cloned_git_folder")

# Language bindings fro py, js, go and ruby
Language.build_library(
    'build/my-languages.so',
    [
        'vendor/tree-sitter-python',
        'vendor/tree-sitter-go',
        'vendor/tree-sitter-ruby',
        'vendor/tree-sitter-javascript'
    ]
)

try:
    if language == 'python':
        if file_extension == 'py':
            pass
    else:
        raise Exception('ValueTooSmallError')

except:
    print("File extension does not match the language")

switch = {
    "py": "python",
    "js": "javascript",
    "rb": "ruby",
    "go": "go"
}

try:
    if switch[file_extension] != language:
        print(f'File extension {file_extension} does not match the language {language}')
    else:
        flag = True

except:
    print(f'Invalid file_extension {file_extension} provided')

# setting up the language
PY_LANGUAGE = Language('build/my-languages.so', 'python')
JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
RB_LANGUAGE = Language('build/my-languages.so', 'ruby')
GO_LANGUAGE = Language('build/my-languages.so', 'go')
#
# # The following functions run the cloned extension files for identifier
# matching and validations only if the file extension and language matches in input cmd line args
if flag:
    parser_run_function(PY_LANGUAGE, file_extension)
# parser_run_function(JS_LANGUAGE, "js")
# parser_run_function(RB_LANGUAGE, "ruby")
# parser_run_function(GO_LANGUAGE, "go")
