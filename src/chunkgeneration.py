import ast
import os
import time
from rich import print as rprint

def extractsublines(lines, start, end):
    sub_lines = lines[start - 1 : end]
    sub_code = "\n".join(sub_lines)
    return sub_code

#creates chunks of a single file
def parsecode(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
            code_lines = code.splitlines()
    except FileNotFoundError:
        rprint("[bright_red]Filepath invalid, try again[/bright_red]")
    except:
        print("[bright_red]Error[/bright_red]")
    
    parsed = ast.parse(code)
    chunks = []
    prev_start = -1
    prev_end = -1
    stored = False

    for node in ast.iter_child_nodes(parsed):
        #we want to group together single lines of code until the next big group of statements
        start = node.lineno
        end = node.end_lineno
        if start == end and not stored:
            prev_start = start
            prev_end = end
            stored = True
        elif start == end and stored:
            prev_end = end
        elif start != end and stored:
            #appending the previous chunk
            sub_code = extractsublines(code_lines, prev_start, prev_end)
            chunks.append(sub_code)
            #appending the current chunk
            sub_code = extractsublines(code_lines, start, end)
            chunks.append(sub_code)
            stored = False
            prev_start = -1
            prev_end = -1
        else:
            sub_code = extractsublines(code_lines, start, end)
            chunks.append(sub_code)
            prev_start = -1
            prev_end = -1

    if prev_start != -1 and prev_end != -1:
        sub_code = extractsublines(code_lines, prev_start, prev_end)
        chunks.append(sub_code)

    #to handle a file full of comments
    if not chunks:
        chunks.append(code)
    
    return chunks

#the chunks generated for the whole codebase, returns a dictionary with the keys being the files in the codebase and the values being the chunks
def generatedchunks(cur_dir):
    log = "file_log.txt"
    cur_log = {}
    file_chunks = {}
    if os.path.exists(log):
        with open(log, 'r') as f:
            for line in f:
                #split a maximum of only one time
                filepath, mtime = line.rstrip('\n').split(",", 1)
                cur_log[filepath] = mtime

    for root, sub, files in os.walk(cur_dir):
        if 'venv' in sub:
            sub.remove('venv')
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                info = os.stat(filepath)
                cur_time = time.ctime(info.st_mtime)
                if filepath not in cur_log or cur_log[filepath] != cur_time:
                    rprint("[blue]Change Noted: [/blue]" , file)
                    cur_log[filepath] = cur_time
                    chunks = parsecode(filepath)
                    file_chunks[filepath] = chunks

    with open(log, 'w') as f:
        for filepath, mtime in cur_log.items():
            text = filepath + "," + mtime + "\n"
            f.write(text)

    return file_chunks

