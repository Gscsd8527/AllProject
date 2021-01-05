import requests
import json
from loguru import logger
import redis


pool = redis.ConnectionPool(host='*********', port=6378, db=13, decode_responses=True)
r = redis.Redis(connection_pool=pool)


class Nomad:
    def __init__(self):
        self.url = 'https://nomad-lab.eu/prod/rae/api/repo/?page=1&per_page=10&order_by=upload_time&order=-1&domain=dft&owner=public&statistics=atoms&exclude=atoms,only_atoms,dft.files,dft.quantities,dft.optimade,dft.labels,dft.geometries'
        # self.atoms = self.get_all_type()
        self.base_url = 'https://nomad-lab.eu/prod/rae/api/repo/?page=1&per_page=10&order_by=upload_time&order=-1&domain=dft&owner=public&atoms={atmon}&statistics=atoms&exclude=atoms,only_atoms,dft.files,dft.quantities,dft.optimade,dft.labels,dft.geometries'
        # self.materials_url = self.base_url + '&encyclopedia.material.materials_grouped=true'
        self.grouped_ectries_url = self.base_url + '&dft.groups_grouped=true'
        self.datasets_url = self.base_url + '&datasets_grouped=true'
        self.page_num = 10  # 一页的数量
        self.token = ''


    def get_all_type(self):
        """
        获取所有类型
        :return:
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            text = response.text
            json_data = json.loads(text)
            atoms = json_data['statistics']['atoms']
            return atoms
        else:
            logger.info(f'错误响应码为： {response.status_code}')


    def get_atom_nums(self, url, atmon):
        """
        获取各元素的个数
        :param url:
        :return:
        """
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
            try:
                r.lpush('nomad_data', text)
            except:
                with open('data.json', 'a+', encoding='utf-8') as f:
                    f.write('{}\n'.format(text))
            data_json = json.loads(text)
            if 'datasets_grouped' in url:
                nums = data_json['statistics']['total']['all']['datasets']
                code = data_json['datasets_grouped']['after']
                type = 'datasets_grouped'
            # elif 'materials_grouped' in url:
            #     nums = data_json['statistics']['total']['all']['encyclopedia.material.materials']
            elif 'groups_grouped' in url:
                nums = data_json['statistics']['total']['all']['dft.groups']
                code = data_json['dft.groups_grouped']['after']
                type = 'groups_grouped'
            else:
                nums = 100

            pages = nums // self.page_num
            ys = nums % self.page_num
            if ys > 0:
                pages += 1
            # 最多1000页
            if pages > 1000:
                pages = 1000
            print(f'元素 {atmon}  的   {type}  有  {nums} 个, 共 {pages} 页')
            return url, pages, type, code
        else:
            logger.info(f'错误响应码为： {response.status_code}', )


    def request(self, url, pages, type, code, atom):
        self.token = code
        js = 1
        while pages:
            logger.info(f'这是{atom} 类型为 {type} 的 第 {js} 页, token = {self.token}')
            if type == 'groups_grouped':
                next_url = url + f'&dft.groups_grouped_after={self.token}'
            elif type == 'datasets_grouped':
                next_url = url + f'&datasets_grouped_after={self.token}'
            # elif type == 'materials':
            #     next_url = url + f'&datasets_grouped_after={self.token}'
            # print('next_url = ', next_url)
            response = requests.get(next_url)
            if response.status_code == 200:
                text = response.text
                if type == 'datasets_grouped':
                    self.token = json.loads(text)['datasets_grouped']['after']
                elif type == 'groups_grouped':
                    self.token = json.loads(text)['dft.groups_grouped']['after']
                try:
                    r.lpush('nomad_data', text)
                except:
                    with open('data.json', 'a+', encoding='utf-8') as f:
                        f.write('{}\n'.format(json.dumps(json.loads(text), ensure_ascii=False)))
            else:
                logger.info(f'错误响应码为： {response.status_code}', )
            pages -= 1
            js += 1


def main():
    """
    https://nomad-lab.eu/prod/rae/gui/search
    :return:
    """
    nomad = Nomad()
    # 第一步： 获取url
    atmons = nomad.get_all_type()
    atmons = list(atmons.keys())
    index_ = 1
    print(atmons)
    for atmon in atmons:
        try:
            logger.info(f'共有 {len(atmons)}  个， 这是 第 {index_}  个')
            # url_1, pages_1, type_1, code_1 = nomad.get_atom_nums(nomad.materials_url.format(atmon=atmon), atmon=atmon, type='materials')  # 不能翻页
            url_2, pages_2, type_2, code_2 = nomad.get_atom_nums(nomad.grouped_ectries_url.format(atmon=atmon), atmon=atmon)
            url_3, pages_3, type_3, code_3 = nomad.get_atom_nums(nomad.datasets_url.format(atmon=atmon),  atmon=atmon)
            jobs = [[url_2, pages_2, type_2, code_2], [url_3, pages_3, type_3, code_3]]
            for job in jobs:
                nomad.request(job[0], job[1], job[2], job[3], atmon)
        except:
            # with open('eror.txt', 'a+') as f:
            with open('error.txt', 'a+') as f:
                f.write('{}\n'.format(atmon))
        index_ += 1


if __name__ == '__main__':
    main()
    # atmons = ['Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Bk', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Co', 'Cr', 'Cs', 'Cu', 'Dy', 'Er', 'Eu', 'F', 'Fe', 'Fr', 'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'I', 'In', 'Ir', 'K', 'Kr', 'La', 'Li', 'Lu', 'Mg', 'Mn', 'Mo', 'N', 'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'Np', 'O', 'Os', 'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U', 'V', 'W', 'X', 'Xe', 'Y', 'Yb', 'Zn', 'Zr']
    # print(atmons.index('Zr'))