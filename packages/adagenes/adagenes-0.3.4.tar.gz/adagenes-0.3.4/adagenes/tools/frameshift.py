import re


def is_frameshift_ins(var):
        # Regular expression to match the insertion format
        pattern = re.compile(r'ins([A-Za-z0-9_]?)')

        # Find the insertion part
        match = pattern.search(var)
        if not match:
            #raise ValueError("Invalid insertion identifier format")
            print("invalid insertion identifier: ",var)
            return ""

        insertion = match.group(1)

        # Check if the insertion is defined as letters or numbers
        if insertion.isdigit():
            # If it's a number, it represents the number of nucleotides directly
            num_nucleotides = int(insertion)
        elif '_' in insertion:
            # If it's a range, calculate the number of nucleotides
            start, end = map(int, insertion.split('_'))
            num_nucleotides = end - start + 1
        else:
            # If it's letters, calculate the number of nucleotides
            num_nucleotides = len(insertion)

        # Check if the number of nucleotides is divisible by 3
        if num_nucleotides % 3 == 0:
            return "frameshift"
        else:
            return "in-frame"


def is_frameshift_del(var):
    # Regular expression to match the insertion format
    pattern = re.compile(r'del([A-Za-z0-9_]?)')

    # Find the insertion part
    match = pattern.search(var)
    if not match:
        #raise ValueError("Invalid insertion identifier format")
        print("invalid deletion identifier: ", var)
        return ""

    insertion = match.group(1)

    # Check if the insertion is defined as letters or numbers
    if insertion.isdigit():
        # If it's a number, it represents the number of nucleotides directly
        num_nucleotides = int(insertion)
    elif '_' in insertion:
        # If it's a range, calculate the number of nucleotides
        start, end = map(int, insertion.split('_'))
        num_nucleotides = end - start + 1
    else:
        # If it's letters, calculate the number of nucleotides
        num_nucleotides = len(insertion)

    # Check if the number of nucleotides is divisible by 3
    if num_nucleotides % 3 == 0:
        return "frameshift"
    else:
        return "in-frame"
