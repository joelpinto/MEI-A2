import math




def main():
    with open("out.tsv", "r") as f:
        content = f.readlines()
    content = [x.strip('\t') for x in content]
    table = []
    count = 0
    for x in content:
        line = x.replace('\n', '')
        table.append(line.split('\t'))
        count += 1
    table.pop(0)
    dicio = {}
    for x in table:
        if int(x[4]) > -1:
            if x[0] not in dicio:
                dicio[x[0]] = {}
            if x[1] not in (dicio[x[0]]).keys():
                dicio[x[0]][x[1]] = {}
            if x[2] not in (dicio[x[0]][x[1]]).keys():
                dicio[x[0]][x[1]][x[2]] = 'NOT DETECTED'
            if x[2] in (dicio[x[0]][x[1]]).keys() and int(x[4]) > 0:
                dicio[x[0]][x[1]][x[2]] = 'DETECTED'
    out_tsv = ''
    codes = list(dicio.keys())
    codes.sort()
    for i in codes:
        out_tsv += '\ttest_suite1\ttest_suite2\ttest_suite3\ttest_suite4\n'
        patches = list((dicio[i]).keys())
        patches.sort()
        for j in patches:
            out_tsv += '' + j + '\t' + dicio[i][j]['test_suite1'] + '\t' + dicio[i][j]['test_suite2'] + '\t' + \
                       dicio[i][j]['test_suite3'] + '\t' + dicio[i][j]['test_suite4'] + '\n'
    f = open('patches_test-suite_table.tsv', 'w')
    f.write(out_tsv)
    f.close()
    dic = {}
    for i in codes:
        patches = list((dicio[i]).keys())
        patches.sort()
        dic[i] = {}
        dic[i]['total'] = 0
        for j in patches:
            tmp = j.split('_')
            if tmp[1] not in (dic[i]).keys():
                dic[i][tmp[1]] = 0
            if tmp[1] in (dic[i]).keys():
                if 'NOT DETECTED' == dicio[i][j]['test_suite1'] and 'NOT DETECTED' == dicio[i][j]['test_suite2'] and 'NOT DETECTED' == dicio[i][j]['test_suite3'] and 'NOT DETECTED' == dicio[i][j]['test_suite4']:
                    dic[i][tmp[1]] += 1
                    dic[i]['total'] += 1
    out_tsv = ''
    codes = list(dic.keys())
    codes.sort()
    for i in codes:
        out_tsv += '' + i + '\nTipo de Patch\tPercentagem de nao detetar\n'
        suits = list((dic[i]).keys())
        suits.sort()
        for j in suits:
            if dic[i]['total'] == 0:
                out_tsv += '' + j + '\t' + str(0) + '\n'
            else:
                out_tsv += '' + j + '\t{0:.2f}\n' . format(round((dic[i][j] / dic[i]['total']) * 100, 2))
    f = open('patch-type_notDetected.tsv', 'w')
    f.write(out_tsv)
    f.close()
    dicio = {}
    for x in table:
        if int(x[4]) > -1:
            if x[0] == 'huffman':
                if x[2] == 'test_suite1':
                    if x[0] not in dicio:
                        dicio[x[0]] = {}
                    if x[3] not in (dicio[x[0]]).keys():
                        dicio[x[0]][x[3]] = {'detected': 0, 'notDetected': 0}
                    if x[3] in (dicio[x[0]]).keys() and int(x[4]) > 0:
                        dicio[x[0]][x[3]]['detected'] += 1
                    else:
                        dicio[x[0]][x[3]]['notDetected'] += 1
            if x[0] == 'radix':
                if x[2] == 'test_suite4':
                    if x[0] not in dicio:
                        dicio[x[0]] = {}
                    if x[3] not in (dicio[x[0]]).keys():
                        dicio[x[0]][x[3]] = {'detected': 0, 'notDetected': 0}
                    if x[3] in (dicio[x[0]]).keys() and int(x[4]) > 0:
                        dicio[x[0]][x[3]]['detected'] += 1
                    else:
                        dicio[x[0]][x[3]]['notDetected'] += 1
    out_tsv = ''
    codes = list(dicio.keys())
    codes.sort()
    for i in codes:
        out_tsv += '' + i + '\nTest Case\tProbabilidade de detetar falha\n'
        suits = list((dicio[i]).keys())
        suits.sort()
        for j in suits:
            out_tsv += '' + j + '\t' + str(math.floor(
                (dicio[i][j]['detected'] / (dicio[i][j]['detected'] + dicio[i][j]['notDetected'])) * 100)) + '\n'
    f = open('test-suite_histo_table_test-suite1.tsv', 'w')
    f.write(out_tsv)
    f.close()


if __name__ == "__main__":
    main()