import os

def create_file(file_name, content):
  with open(file_name, 'w') as file:
    file.write(content)

def read_file(file_name):
  with open(file_name, 'r') as file:
    content = file.read()
  return content

def read_file_lines(file_name):
  with open(file_name, 'r') as file:
    lines = [l.replace("\n","") for l in file.readlines()]
  return lines

def update_file(file_name, content):
  with open(file_name, 'w') as file:
    file.write(content)

def write_lines_to_file(file_name, lines):
  with open(file_name, 'w') as file:
    for line in lines:
      file.write(line + '\n')

def delete_file(file_name):
  if os.path.exists(file_name):
    os.remove(file_name)
  else:
    print(f"The file {file_name} does not exist.")
