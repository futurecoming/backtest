import base64
import os

root_path = os.path.abspath(os.path.join(os.getcwd()))


def read_file(file_path):
    file_path = root_path + file_path
    with open(file_path) as f:
        content = f.read()
    f.close()
    return content


def img2base64():
    file_path = root_path + '/output/cumulative_return.png'
    with open(file_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read())
    f.close()
    return img_base64


def write2file(name, content):
    relative_path = '/engine/strategies/' + name + '.py'
    file_path = root_path + relative_path
    with open(file_path, 'w') as f:
        f.write(content)
    f.close()
    return relative_path


if __name__ == '__main__':
    pass
