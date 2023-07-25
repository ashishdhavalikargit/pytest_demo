import argparse
import os
from utils.utility import timestamp_name


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=False, action='store', dest='file',
                        help='Pass "all" if all testcases from all the testcase files needs to be executed together '
                        'or pass filename of the testcase. Multiple filenames can '
                        'be passed by adding ",". Pass "all except [filename]" to execute testcases from all '
                        'the testcase files except the filesnames specified.')
    parser.add_argument('-m', type=str, required=False, action='store', dest='marker',
                        help='Pass marker specified in particular testcases. Multiple markers can '
                        'be passed by adding ",".')
    args = parser.parse_args()
    return args


def main():
    version = "test_o.1"
    args = parse_argument()
    list_dir = os.listdir('tests/')
    list_testcases = ["example"]
    if args.marker == None and args.file == None:
        raise Exception("None of the parameters were passed")
    if args.file:
        if 'all' == args.file:
            split_list = list_testcases
        elif 'except' in args.file:
            split_list = args.file.split('except')
            split_list = [x.strip(' ') for x in split_list]
            split_list = split_list[1].split(',')
            for element in split_list:
                if element in list_testcases:
                    list_testcases.remove(element)
            split_list = list_testcases
        elif ',' in args.file:
            split_list = args.file.split(',')
            split_list = [x.strip(' ') for x in split_list]
        else:
            split_list = [args.file]
    else:
        split_list = [args.file]
    for iter in range(len(split_list)):
        report_name_assigned = False
        command_list = ['python -m pytest -p no:randomly ']
        if args.marker:
            if ',' in args.marker:
                marker_list = args.marker.split(',')
                marker_list = [x.strip(' ') for x in marker_list]
                command_list.append(f'-m "{" or ".join(marker_list)}"')
            else:
                command_list.append(f'-m {args.marker}')
        if split_list[iter]:
            file_name_check = False
            for dir in list_dir:
                if dir in split_list[iter]:
                    command_list.append(f'tests/{dir}/test_{split_list[iter]}.py')
                    file_name_check = True
            if not file_name_check:
                raise Exception("Invalid testcase filename")
        if args.marker and split_list[iter] == None:
            if ',' in args.marker:
                report_name_assigned = True
                report_dir = version + "_" + timestamp_name("_".join(marker_list))
                html_filename = version + "_" + timestamp_name("_".join(marker_list)) + '.html'
            else:
                report_name_assigned = True
                report_dir = version + "_" + timestamp_name(args.marker)
                html_filename = version + "_" + timestamp_name(args.marker) + '.html'
        if split_list[iter] and not report_name_assigned:
            report_name_assigned = True
            report_dir = version + "_" + \
                timestamp_name(split_list[iter].replace("test", ""))
            html_filename = version + "_" + \
                timestamp_name(split_list[iter].replace("test", "")) + '.html'
        os.makedirs(f'report/{report_dir}')
        command_list.append(f'--html=report/{report_dir}/{html_filename}')
        command_list.append(f'--dirname {report_dir}')
        print("Pytest command:", str(' '.join(command_list)))
        os.system(str(' '.join(command_list)))


if __name__ == '__main__':
    main()
