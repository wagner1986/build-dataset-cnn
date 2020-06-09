import glob, os
import re
# Current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
print(current_dir)

def list_files(basepath, ext):
    # List all files in a directory using scandir()
    print(os.path.exists(basepath), basepath)
    lista = [basepath + os.sep +x for x in os.listdir(basepath) if x.endswith(ext)]
    lista.sort()
    return lista


def recover_associated_image(filename, image_path, new_ext='.jpg'):
    # recupera imagem associada ao arquivo de labels
    simple_name = os.path.basename(filename)
    simple_name = os.path.splitext(simple_name)
    return image_path + os.sep + simple_name[0] + new_ext


def read_lines_file(file_name):
    # List all lines of a file
    list = []
    # print(os.path.isfile(file_name))
    with open(file_name) as fp:
        for cnt, line in enumerate(fp):
            # print("Line {}: {}".format(cnt, line))
            list.append(line.rstrip())  # remove quebra de linha
    return list


def convert_lines(list_lines):
    new_list = []
    for line in list_lines:
        new_list.append(re.sub("[ ]", ",", line))
    new_line = ' '.join(new_list)
    return new_line


def write_file_to_yolo(output_file_name, list_lines):
    file = open(output_file_name, "w")
    for line in list_lines:
        file.write(line+"\n")
    file.close()



def convert_yolo(images_path="dataset/testdonout/images", labels_path="bbox_txt", class_file="class_list.txt",filename_out="class_train.txt"):
    list_arq = list_files(labels_path, '.txt')
    list_class = read_lines_file(class_file)
    print(" lista de arquivos " + str(list_arq))
    print(" lista de class " + str(list_class))

    all_data=[]
    for arq_label in list_arq:
        list_lines = read_lines_file(arq_label)
        new_line = convert_lines(list_lines)
        all_data.append(recover_associated_image(arq_label, images_path) + " " + new_line)
    print(all_data)
    write_file_to_yolo(filename_out, all_data)

def separa_foto_das_classes(line):
    lista=line.strip().split()
    nome_foto=lista[0]
    arry_restante=lista[1:]
    labels=[int(box.split(',')[4]) for box in arry_restante]
    return nome_foto,labels

if __name__ == '__main__':
    convert_yolo(images_path="images", labels_path="bbox_txt", class_file="class_list.txt",filename_out="condor_train_data_yolo.txt")


    # Using readlines()
    file1 = open('condor_train_data_yolo.txt', 'r')
    lines = file1.readlines()

    file1 = open('class_list.txt', 'r')
    todas_classes = file1.readlines()

    obj = {}
    data = []
    for line in lines:
        nome, labels = separa_foto_das_classes(line)
        classe=list(todas_classes[label].strip() for label in labels)
        #vetor = binarizar_classes(labels)
        temp = [nome, classe]
        data.append(temp)

    print('binarizar_classes ', data)
    df = pd.DataFrame(data, columns=['filename', 'labels'])
    print(df.head())
    df.to_csv('condor_data.csv')
