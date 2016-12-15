import pysftp
import os

work_remote = True


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
        outputs = os.listdir("source/" + i + "/outputs/")
        patches = os.listdir("source/" + i + "/patches/")
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

def main():
    if work_remote:
        print("Successful connected!")

    directories = crawl_directory()
    create_shipping(directories)

    if work_remote:
        sftp.put(
            localpath="source-temp.tar.gz"
        )
    remote_command("tar -zxvf source-temp.tar.gz")
    remote_command("rm source-temp.tar.gz")
    for i in directories.keys():
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
    read_shipping(directories)


if __name__ == "__main__":
    main()
    if work_remote:
        print("Closing...")
        sftp.close()