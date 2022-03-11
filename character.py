import json


class Character:
    def __init__(self):
        self.char_json_path = './character.json'

        with open(self.char_json_path, encoding='utf-8') as f:
            self.json_data = json.load(f)
        
        self.survivor_list = self.json_data['survivor']
        self.killer_list = self.json_data['killer']
        
    # キャラクターの所持パークにパークを追加する
    def append_perk(self, side, char_name, perk_names):
        have_perks = self.json_data[side][char_name]['perks']
        for perk in perk_names:
            # 既にあるか
            if perk in have_perks:
                pass
            else:
                have_perks.append(perk)
                have_perks = sorted(have_perks)

        self.json_data[side][char_name]['perks'] = have_perks

        with open(self.char_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)
        
        return True
    
    # キャラクターの所持パークを更新する
    def renew_perks(self, side, char_name, perks):
        self.json_data[side][char_name]['perks'] = perks

        with open(self.char_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)
        
        return perks

    # パークを１つ削除
    def remove_perk(self, side, char_name, perk_names):
        have_perks = self.json_data[side][char_name]['perks']
        for perk in perk_names:
            if perk in have_perks:
                have_perks.remove(perk)
        self.json_data[side][char_name]['perks'] = have_perks

        with open(self.char_json_path, 'w', encoding='utf-8') as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)
        
        return True

    # キャラクターのサイドを返す
    def get_char_side(self, char_name):
        if char_name in self.killer_list:
             side = 'killer'
        else:
            side = 'survivor'

        return side

    # パークの位置を返す	
    def get_position(self, side, char_name, jp_perk_name):
        have_perks = self.json_data[side][char_name]['perks']
        sorted_have_perks = sorted(have_perks)

        index = sorted_have_perks.index(jp_perk_name)

        page = int(index / 15 + 1)
        rows = int((index % 15) / 5 + 1)
        columns = int((index % 15) % 5 + 1)

        return page, rows, columns

    # 所持していないパークを返す
    def dont_have_perks(self, side, char_name, all_perk):
        have_perks = self.json_data[side][char_name]['perks']
        perk_list = all_perk
        if have_perks:
            for perk in have_perks:
                perk_list.remove(perk)

        return sorted(perk_list)