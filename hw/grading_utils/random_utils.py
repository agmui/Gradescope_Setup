import os.path

SUBMISSION_BASE = '/autograder/submission/'


def submitted_files(files_to_check: list, base=SUBMISSION_BASE):
    """Check submitted files"""
    missing_files = len(files_to_check)

    # r=fullpath, d=directories, f = files
    for r, d, f in os.walk(SUBMISSION_BASE):  # os.walk returns list of directory and files
        file_relative_path = r.replace(SUBMISSION_BASE, '')  # removes the first part of the full path
        for file in f:
            file_joined_path = os.path.join(file_relative_path, file)  # adds the remaking part of the path
            if file_joined_path in files_to_check:  # check if the file is needed
                print("found:", file)
                files_to_check.remove(file_joined_path)
                missing_files -= 1
            else:
                print("????:", file)
    for file in files_to_check:
        print(f'MISSING: {file}')

    print('---')
    print(f'missing {missing_files} files')
    return missing_files


# Define a wrapper function to capture the output
def capture_output(func):
    import io
    from contextlib import redirect_stdout

    # Create an in-memory buffer to capture output
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()  # Call the original function

    return buffer.getvalue()
