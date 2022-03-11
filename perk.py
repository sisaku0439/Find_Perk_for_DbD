import enum
import json

class Perk:
    def __init__(self):
        self.perk_json_path = './perk_list.json'

        with open(self.perk_json_path, encoding='utf-8') as f:
            self.json_data = json.load(f)
        
        self.tag_dict = [{},{}]
        self.make_tag_dict()

    # タグ逆引き辞書の作成
    def make_tag_dict(self):
        for i,side in enumerate(['killer','survivor']):
            tags = self.get_tag_list(side)
            for tag in tags:
                self.tag_dict[i].setdefault(tag,[])
            for key in self.json_data[side]:
                tag = self.json_data[side][key]['tag']
                perk_list = self.tag_dict[i][tag]
                perk_list.append(key)
                self.tag_dict[i][tag] = sorted(perk_list)

    # 日本語名リストを返す
    def get_jp_name(self, side):
        jp_name = list(self.json_data[side])
        
        return jp_name
        
    # 画像パスを返す
    def get_img_path(self, side, jp_perk_name):
        img_path = self.json_data[side][jp_perk_name]['image_path']
        
        return img_path
    
    # タグを取得
    def get_tag_list(self, side):
        tags = []
        for key in self.json_data[side]:
            tags.append(self.json_data[side][key]['tag'])
        tags = sorted(set(tags))

        return tags

    # 固有パーク取得
    def get_unique_perk(self, side, tag):
        if side == 'killer':
            return self.tag_dict[0][tag]
        else:
            return self.tag_dict[1][tag]