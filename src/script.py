# Python
import random


def read_large_file(file_path):
    sample_size = 150
    sample = []
    lista = []

    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            file_iter = iter(file)
            for i, line in enumerate(file_iter):
                if i < sample_size:
                    sample.append(line)
                elif i >= sample_size and random.random() < sample_size / (i+1):
                    replace = random.randint(0, len(sample)-1)
                    sample[replace] = line

        for line in sample:
            values = line.split("|")  # Split the line into values
            lista.append(values[0])

        print(lista)

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except PermissionError:
        print(f"Permission denied to read the file {file_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Replace 'large_file.txt' with the path to your file
read_large_file('C:/Users/israe/Downloads/padron_reducido_ruc.txt')
