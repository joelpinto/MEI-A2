import pysftp
import os
import filecmp
import math
import subprocess

work_remote = False
timeout_time = 2
domain = input()
username = input()
password = input()

if work_remote:
    print("Connecting...")
    sftp = pysftp.Connection(
        domain,
        username,
        None,
        password)


def remote_command(command):
    if work_remote:
        out = sftp.execute(command)
        to_print = 'Remote: '
        for i in out:
            to_print += str(i) + ' '
        if len(out) > 0:
            to_print.replace('b\'', '')
            to_print.replace('\\n\'', '')
            print(to_print)


def crawl_directory():
    ret = {}
    program_dirs = os.listdir("source/")
    for i in program_dirs:
        _path = 'source/' + i + "/"
        insuits = os.listdir("source/" + i + "/inputs/")
        insuits.sort()
        inputs = {}
        for j in insuits:
            inputslist = os.listdir("source/" + i + "/inputs/" + j + "/")
            inputslist.sort()
            inputs[j] = inputslist
        outsuits = os.listdir("source/" + i + "/outputs/")
        outsuits.sort()
        outputs = {}
        for j in outsuits:
            outputslist = os.listdir("source/" + i + "/outputs/" + j + "/")
            outputslist.sort()
            outputs[j] = outputslist
        patches = os.listdir("source/" + i + "/patches/")
        patches.sort()
        ret[i] = {'_name': i, '_path': _path, 'inputs': inputs, 'outputs': outputs, 'patches': patches}
    return ret


def create_shipping(directories):
    # tar -zxvf tar-archive-name.tar.gz  TO EXTRACT
    # tar -zcvf tar-archive-name.tar.gz source-folder-name  TO COMPRESS
    os.system("mkdir source-temp")
    os.system("cp -a source/. source-temp/")
    for i in directories.keys():
        os.system("rm -r source-temp/" + directories[i]['_name'] + "/inputs/")
        os.system("rm -r source-temp/" + directories[i]['_name'] + "/outputs/")
        os.system("rm -r source-temp/" + directories[i]['_name'] + "/patches/*")
        os.system("rm -r source-temp/" + directories[i]['_name'] + "/" + directories[i]['_name'])
    os.system("tar -zcvf source-temp.tar.gz source-temp")
    os.system("rm -r source-temp")


def read_shipping(directories):
    # tar -zxvf tar-archive-name.tar.gz  TO EXTRACT
    # tar -zcvf tar-archive-name.tar.gz source-folder-name  TO COMPRESS
    os.system("tar -zxvf source-temp.tar.gz")
    for i in directories.keys():
        os.system("cp -a source-temp/" + directories[i]['_name'] + "/patches/ source/" + directories[i]['_name'] + "/")
    os.system("rm -r source-temp/")
    os.system("rm -r source-temp.tar.gz")


def generate_outputs(directories):
    print("generating outputs...")
    keys = list(directories.keys())
    keys.sort()
    for i in keys:
        insuits = directories[i]['inputs']
        insuits = list(insuits.keys())
        insuits.sort()
        outsuits = directories[i]['outputs']
        outsuits = list(outsuits.keys())
        outsuits.sort()
        if i == "huffman":
            os.system("make -C source/" + i + "/")
        else:
            os.system("gcc -w source/" + i + "/" + i + ".c -lm -o source/" + i + "/" + i)
        for j in range(len(insuits)):
            inputs = directories[i]['inputs'][insuits[j]]
            outputs = directories[i]['outputs'][outsuits[j]]
            for z in range(len(inputs)):
                file_extension = inputs[z].split('.')
                #print("generating '" + "source/" + i + "/outputs/" + outsuits[j] + "/output" + str(z + 1) + ".png")
                if i == "huffman":
                    if (z + 1) < 10:
                        cmd = "./source/" + i + "/" + i + " compress source/" + i + "/outputs/" + outsuits[j] + "/output0" + str(z + 1) + ".huff" + " source/" + i + "/inputs/" + insuits[j] + "/" + inputs[z]
                    else:
                        cmd = "./source/" + i + "/" + i + " compress source/" + i + "/outputs/" + outsuits[
                            j] + "/output" + str(z + 1) + ".huff" + " source/" + i + "/inputs/" + insuits[
                                  j] + "/" + inputs[z]
                else:
                    cmd = "./source/" + i + "/" + i + " < source/" + i + "/inputs/" + insuits[j] + "/" + inputs[z] + \
                          " > source/" + i + "/outputs/" + outsuits[j] + "/output" + str(z + 1) + "." + file_extension[1]
                try:
                    subprocess.run(cmd, timeout=timeout_time, shell=True)
                except subprocess.TimeoutExpired:
                    print("timeout in input" + str(z) + " after " + str(timeout_time) + " seconds...")
                    os.system("pkill source")
        os.system("rm source/" + i + "/" + i)
        os.system("rm source/" + i + "/*.o")


def run_tests(directories):
    statistics = {}
    print("generating statistics...")
    keys = list(directories.keys())
    keys.sort()
    print_statistics = ""
    out_tsv = 'code_name\tpatch\ttest_suite\ttest_case\tdefect\n'
    for i in keys:
        patches = directories[i]['patches']
        inputs = directories[i]['inputs']
        outputs = directories[i]['outputs']
        type_patches = {}
        for j in patches:
            if i == "huffman":
                os.system("cp source/" + i + "/patches/" + j + " source/" + i + "/huffman.c")
                os.system("make -C source/" + i + "/")
            else:
                os.system("gcc source/" + i + "/patches/" + j + " -o source/" + i + "/" + i)
            patch_type = j.split('_')
            patch_type = patch_type[1]
            insuits = list(inputs.keys())
            insuits.sort()
            outsuits = list(outputs.keys())
            outsuits.sort()
            count = 0
            for test_suite in insuits:
                count2 = 0
                for test_case in inputs[test_suite]:
                    defect = 0
                    if i == "huffman":
                        cmd = "./source/" + i + "/" + i + " compress source/" + i + "/out.huff source/" + i + "/inputs/" + test_suite + "/" + test_case
                        try:
                            subprocess.run(cmd, timeout=timeout_time, shell=True)
                        except subprocess.TimeoutExpired:
                            print("timeout in patch " + j + " after " + str(timeout_time) + " seconds...")
                            os.system\
                                ("pkill " + i)
                            defect = -1
                        try:
                            if not filecmp.cmp("source/" + i + "/out.huff",
                                               "source/" + i + "/outputs/" + outsuits[count] + "/" + outputs[outsuits[count]][count2]):
                                defect = 1
                        except FileNotFoundError:
                            defect = 1
                            os.system("rm source/" + i + "/out.huff")
                    else:
                        cmd = "./source/" + i + "/" + i + " < source/" + i + "/inputs/test_suite" + test_case + " > source/" + i + "/out.tmp"
                        try:
                            subprocess.run(cmd, timeout=timeout_time, shell=True)
                        except subprocess.TimeoutExpired:
                            print("timeout in patch " + j + " after " + str(timeout_time) + " seconds...")
                            os.system("pkill " + i)
                            defect = -1
                        if not filecmp.cmp("source/" + i + "/out.tmp",
                                           "source/" + i + "/outputs/" + test_case):
                            defect = 1
                        os.system("rm source/" + i + "/out.tmp")
                    out_tsv += '' + i + '\t' + j + '\t' + test_suite + '\t' + test_case + '\t' + str(defect) + '\n'
                    count2 += 1
                count += 1
            os.system("rm source/" + i + "/" + i)
            os.system("rm soutce/" + i + "/*.o")
    f = open('out.tsv', 'w')
    f.write(out_tsv)
    f.close()
    return statistics


def main():
    if work_remote:
        print("Successful connected!")

    directories = crawl_directory()
    if work_remote:
        create_shipping(directories)

    if work_remote:
        sftp.put(
            localpath="source-temp.tar.gz"
        )
    remote_command("tar -zxvf source-temp.tar.gz")
    remote_command("rm source-temp.tar.gz")
    if work_remote:
        for i in directories.keys():
            print("Generating patches for " + i + "...")
            remote_command("swfi source-temp/" + directories[i]['_name'] + "/" + directories[i]['_name'] + ".c > /dev/null")
            list = sftp.listdir("source-temp/" + directories[i]['_name'] + "/")
            for j in list:
                if (j != directories[i]['_name'] + ".c") and (j != directories[i]['_name'] + ".c._FORMATTED_") and (j != directories[i]['_name'] + ".origin.c") and (j != "patches"):
                    remote_command("patch -d source-temp/" + directories[i]['_name'] + "/ < source-temp/" + directories[i]['_name'] + "/" + j)
                    remote_command("cp source-temp/" + directories[i]['_name'] + "/" + directories[i]['_name'] + ".c source-temp/" + directories[i]['_name'] + "/" + "patches/")
                    remote_command("cp source-temp/" + directories[i]['_name'] + "/" + "patches/" + directories[i]['_name'] + ".c source-temp/" + directories[i]['_name'] + "/" + "patches/" + j + ".c")
                    remote_command("rm source-temp/" + directories[i]['_name'] + "/" + "patches/" + directories[i]['_name'] + ".c")
                    remote_command("patch -R -d source-temp/" + directories[i]['_name'] + "/ < source-temp/" + directories[i]['_name'] + "/" + j)
        remote_command("tar -zcvf source-temp.tar.gz source-temp")
    if work_remote:
        print("downloading...")
        sftp.get(
            remotepath="source-temp.tar.gz"
        )
    remote_command("rm source-temp.tar.gz")
    remote_command("rm -r source-temp")
    if work_remote:
        read_shipping(directories)
        directories = crawl_directory()
    else:
        #generate_outputs(directories)
        #directories = crawl_directory()
        statistics = run_tests(directories)

if __name__ == "__main__":
    main()
    if work_remote:
        print("Closing...")
        sftp.close()