import os
from github import Github


def makeDirs(dirpath):
    '''
    创建目录
        支持多级目录，若目录已存在自动忽略
        Updated: 2020-05-12
        GitHub: https://github.com/NodeWee/OpenSnippets/tree/master/Python
    '''

    # 去除首尾空白符和右侧的路径分隔符
    dirpath = dirpath.strip().rstrip(os.path.sep)

    if dirpath:
        if not os.path.exists(dirpath):  # 如果目录已存在, 则忽略，否则才创建
            os.makedirs(dirpath)


def copy_folder_from_github_repo(repo, folder_path):
    makeDirs(folder_path)
    file_objects = repo.get_contents(folder_path)

    for obj in file_objects:
        if obj.type == 'file':
            # print(obj.path)
            # save file
            with open(obj.path, 'wb') as fh:
                fh.write(obj.decoded_content)
        elif obj.type == 'dir':
            makeDirs(obj.path)
            copy_folder_from_github_repo(repo, obj.path)


def main():
    gh = Github(os.environ['API_TOKEN_GITHUB'])
    repo = gh.get_repo('NodeWee/FeedGenerator')

    # copy programs
    copy_folder_from_github_repo(repo, 'programs')
    print('Copy programs finished.')


if not os.environ.get('GITHUB_ACTIONS'):
    # run on local
    os.environ['API_TOKEN_GITHUB'] = open('../github-api-key.txt','rt').read()
    

main()
