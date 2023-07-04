import argparse
import os
import csv
import json


def boolean_string(s):
    if s.lower() not in {'False', 'True', 'y', 'n'}:
        raise ValueError('Not a valid boolean string')
    return s == 'True'


def csv_to_column_dict(csv_matrix, headers, output):
    output_data = csv_matrix
    if headers:
        print("I ran")
        new_array = []
        for data_array in csv_matrix[1:]:
            data_dict = {}
            for element in range(0, len(data_array)):
                if csv_matrix[0][element]:
                    data_dict[csv_matrix[0][element]] = data_array[element]
                else:
                    data_dict[element] = data_array[element]
            new_array.append(data_dict)

        output_data = new_array

    with open(output, 'w') as f:
        json.dump(output_data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a csv file to json')
    parser.add_argument('file', type=str, help='The csv file to convert')
    parser.add_argument('-o', '--output', type=str, default="output.json", help='The output file name')
    parser.add_argument('-t', '--headers', action='store_true',
                        help='If the csv file has headers this will use them as keys in the dictionary')
    parser.add_argument('-d', '--delimiter', type=str, default=',',
                        help='For csv files that are not separated by a comma')

    args = parser.parse_args()

    headers = not args.headers
    if not os.path.isfile(args.file) or os.path.splitext(args.file)[1] != '.csv':
        print('\033[91mInvalid input file, please supply a real csv file\033[00m')
    elif os.path.isfile(args.output):
        print('\033[91mOutput file already exists. Please pick another output name with -o\033[00m')
    else:
        with open("people.csv", 'r') as f:
            csv_reader = csv.reader(f)
            table = [row for row in csv_reader]

        csv_to_column_dict(table, headers, args.output)
