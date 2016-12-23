import pysftp
import os
import filecmp
import math

work_remote = False


if work_remote:
    print("Connecting...")
    sftp = pysftp.Connection(
        "ucx.dei.uc.pt",
        "guest",
        None,
        "ucXception$user")


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
        inputs = os.listdir("source/" + i + "/inputs/")
        inputs.sort()
        outputs = os.listdir("source/" + i + "/outputs/")
        outputs.sort()
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


def run_tests(directories):
    statistics = {}
    print("generating statistics...")
    keys = list(directories.keys())
    keys.sort()
    for i in keys:
        patches = directories[i]['patches']
        inputs = directories[i]['inputs']
        outputs = directories[i]['outputs']
        statistics[i] = {'_name': i, 'patches': {}, 'defect_patch_detected': 0, 'defect_patch_not_detected': 0}
        defect_patch_detected = 0
        defect_patch_not_detected = 0
        type_patches = {}
        for j in patches:
            patch_type = j.split('_')
            patch_type = patch_type[1]
            type_patches[patch_type] = {'not_detected': 0, 'detected': 0}
        statistics[i]['type_patches'] = type_patches
        for j in patches:
            defect = False
            os.system("gcc -w source/" + i + "/patches/" + j + " -o source/" + i + "/" + i)
            detected = 0
            not_detected = 0
            out_tests = []
            patch_type = j.split('_')
            patch_type = patch_type[1]
            print("patch: " + j)
            for count in range(len(inputs)):
                os.system("./source/" + i + "/" + i + " < source/" + i + "/inputs/" + inputs[count] + " > source/" + i + "/out.tmp")
                if filecmp.cmp("source/" + i + "/out.tmp", "source/" + i + "/outputs/" + outputs[count]):
                    out_tests.append([outputs[count], True])
                    detected += 1
                else:
                    out_tests.append([outputs[count], False])
                    not_detected += 1
                    defect = True
                os.system("rm source/" + i + "/out.tmp")
            statistics[i]['type_patches'][patch_type]['detected'] += detected
            statistics[i]['type_patches'][patch_type]['not_detected'] += not_detected
            statistics[i]['patches'][j] = {'out_test': out_tests, 'defect': defect, 'detected': detected, 'not_detected': not_detected}
            if defect:
                defect_patch_detected += 1
            else:
                defect_patch_not_detected += 1
            os.system("rm source/" + i + "/" + i)
        statistics[i]['defect_patch_detected'] = defect_patch_detected
        statistics[i]['defect_patch_not_detected'] = defect_patch_not_detected
        print("number of patches: " + str(len(patches)))
        print("" + i + ":\n\tdefect_patch_detected: " + str(defect_patch_detected) + "\n\tdefect_patch_not_detected: " + str(defect_patch_not_detected))
        type_patches = statistics[i]['type_patches']
        for j in type_patches.keys():
            detected = statistics[i]['type_patches'][j]['detected']
            not_detected = statistics[i]['type_patches'][j]['not_detected']
            print("\t" + j + ":\n\t\tdetected: " + str(detected) + "\n\t\tnot_detected: " + str(not_detected) + "\n\t\tpercentage: " + str(math.floor((detected/(detected + not_detected)) * 100)) + "%")
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
        sftp.get(
            remotepath="source-temp.tar.gz"
        )
    remote_command("rm source-temp.tar.gz")
    remote_command("rm -r source-temp")
    if work_remote:
        read_shipping(directories)
        directories = crawl_directory()
    else:
        statistics = run_tests(directories)

if __name__ == "__main__":
    main()
    if work_remote:
        print("Closing...")
        sftp.close()