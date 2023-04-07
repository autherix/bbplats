# Function replace_content: Replace the content of a file with the content of another file, return true on success, false on failure
def replace_content(source, destination):
    try:
        with open(source, 'r') as f:
            content = f.read()
        with open(destination, 'w') as f:
            f.write(content)
        return True
    except:
        return False