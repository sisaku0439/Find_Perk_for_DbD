import configparser

import wx
import wx.xrc

import character
import perk

# ID設定
SEARCH_TAB_ID = 1001
APPEND_TAB_ID = 1002
DELETE_TAB_ID = 1003

# 色設定
config = configparser.ConfigParser()
config.read('./config.ini')
TEXT_COLOR = config['COLOR']['text']
BACKGROUND_COLOR = config['COLOR']['background']
RESULT_COLOR = config['COLOR']['result']
try:
    RATIO = config['DISPLAY'].getfloat('ratio')
except:
    RATIO = 1.0
FONT_SIZE = int(10 * RATIO)



class MainFrame (wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ (self,
                            parent,
                            id = wx.ID_ANY,
                            title = 'Find Perk for DbD',
                            pos = wx.DefaultPosition,
                            size = wx.Size(int(875*RATIO),int(755*RATIO)),
                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetIcon(wx.Icon('./Find_Perk_for_DbD.exe', wx.BITMAP_TYPE_ICO))
        self.status_bar = self.CreateStatusBar()
        self.FONT = wx.Font(FONT_SIZE,
               wx.FONTFAMILY_TELETYPE,
               wx.FONTSTYLE_NORMAL,
               wx.FONTWEIGHT_NORMAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.character_class = character.Character()
        self.perk_class = perk.Perk()
        
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.search_tab = wx.Panel(self.notebook, SEARCH_TAB_ID)
        self.append_tab = wx.Panel(self.notebook, APPEND_TAB_ID)
        self.delete_tab = wx.Panel(self.notebook, DELETE_TAB_ID)
        self.search_panel = Base_Panel(self.search_tab, self.character_class, self.perk_class, self.status_bar)
        self.append_panel = Base_Panel(self.append_tab, self.character_class, self.perk_class, self.status_bar)
        self.delete_panel = Base_Panel(self.delete_tab, self.character_class, self.perk_class, self.status_bar)

        self.notebook.InsertPage(0, self.search_tab, '検索')
        self.notebook.InsertPage(1, self.append_tab, '追加')
        self.notebook.InsertPage(2, self.delete_tab, '削除')

        self.bind()
        self.style()
        self.Centre(wx.BOTH)


    def bind(self):
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.page_changed)
    
    # フォント、色設定
    def style(self):
        self.search_tab.SetBackgroundColour(BACKGROUND_COLOR)
        self.search_tab.SetForegroundColour(TEXT_COLOR)
        self.append_tab.SetBackgroundColour(BACKGROUND_COLOR)
        self.append_tab.SetForegroundColour(TEXT_COLOR)
        self.delete_tab.SetBackgroundColour(BACKGROUND_COLOR)
        self.delete_tab.SetForegroundColour(TEXT_COLOR)
        self.notebook.SetBackgroundColour(BACKGROUND_COLOR)
        self.notebook.SetForegroundColour(TEXT_COLOR)
        self.notebook.SetFont(self.FONT)
        
    # タブ切り替え
    def page_changed(self, event):
        tab = event.GetSelection()
        if tab == 0:
            self.search_panel.perk_list = sorted(self.character_class.json_data[self.search_panel.side][self.search_panel.char]['perks'])
            self.search_panel.candidate_list.SetItems(self.search_panel.perk_list)
            self.search_panel.filter_textctrl.Clear()
        elif tab == 1:
            all_perk = self.perk_class.get_jp_name(self.append_panel.side)
            self.append_panel.perk_list = self.character_class.dont_have_perks(self.append_panel.side, self.append_panel.char, all_perk)
            self.append_panel.candidate_list.SetItems(self.append_panel.perk_list)
            self.append_panel.filter_textctrl.Clear()
        else:
            self.delete_panel.perk_list = sorted(self.character_class.json_data[self.delete_panel.side][self.delete_panel.char]['perks'])
            self.delete_panel.candidate_list.SetItems(self.delete_panel.perk_list)
            self.delete_panel.filter_textctrl.Clear()



class Base_Panel(wx.Panel):
    def __init__(self, parent, character_class, perk_class, status_bar):
        super().__init__(parent, wx.ID_ANY)
        self.main_sizer = wx.GridBagSizer(0, 0)
        self.main_sizer.SetFlexibleDirection(wx.BOTH)
        self.main_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.static_box = wx.StaticBox(parent, wx.ID_ANY, 'キャラクター選択')
        self.label_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        self.scroll_window = wx.ScrolledWindow(parent, wx.ID_ANY, wx.DefaultPosition, (int(480*RATIO),int(640*RATIO)), wx.VSCROLL)
        self.scroll_window.SetScrollRate(5, 5)
        self.radio_sizer = wx.GridBagSizer(0, 0)
        self.radio_sizer.SetFlexibleDirection(wx.BOTH)
        self.radio_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED) 
        self.char_sizer = wx.GridBagSizer(0, 0)
        self.char_sizer.SetFlexibleDirection(wx.BOTH)
        self.char_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.search_radio_sizer = wx.GridBagSizer(0, 0)
        self.search_radio_sizer.SetFlexibleDirection(wx.BOTH)
        self.search_radio_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.perk_sizer = wx.GridBagSizer(0, 0)
        self.perk_sizer.SetFlexibleDirection(wx.BOTH)
        self.perk_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.character_class = character_class
        self.perk_class = perk_class
        self.status_bar = status_bar

        self.FONT = wx.Font(FONT_SIZE,
                            wx.FONTFAMILY_TELETYPE,
                            wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_NORMAL)
        self.result_font = wx.Font(int(FONT_SIZE*1.5),
                                   wx.FONTFAMILY_TELETYPE,
                                   wx.FONTSTYLE_NORMAL,
                                   wx.FONTWEIGHT_BOLD)

        self.char_bitmap = wx.StaticBitmap(parent,
                                           wx.ID_ANY,
                                           wx.Bitmap(self.character_class.json_data['survivor']['サバイバー']['image_path']),
                                           wx.DefaultPosition,
                                           (260,360),
                                           0)
        # キャラクター選択ラジオボタン
        self.survivor_radio_button = []
        self.killer_radio_button = []
        for i,c in enumerate(list(self.character_class.survivor_list)):
            if i == 0:
                self.survivor_radio_button.append(wx.RadioButton(self.scroll_window, wx.ID_ANY, c,style=wx.RB_GROUP))
            else:
                self.survivor_radio_button.append(wx.RadioButton(self.scroll_window, wx.ID_ANY, c))
        for c in  list(self.character_class.killer_list):
            self.killer_radio_button.append(wx.RadioButton(self.scroll_window, wx.ID_ANY, c))
        self.survivor_radio_button[0].SetValue(True)
        self.char = 'サバイバー'
        self.side = self.character_class.get_char_side(self.char)
        self.perk_bitmap = wx.StaticBitmap(parent, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, (int(128*RATIO),int(128*RATIO)), 0)
        self.search_radio_button = [wx.RadioButton(parent, wx.ID_ANY, 'パーク検索',style=wx.RB_GROUP),
                                    wx.RadioButton(parent, wx.ID_ANY, '固有パーク検索')]
        self.filter_textctrl = wx.TextCtrl(parent, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)

        self.parent_id = parent.Id
        if self.parent_id == SEARCH_TAB_ID:
            self.result_text = wx.StaticText(parent, wx.ID_ANY, '', wx.DefaultPosition, wx.DefaultSize, 0)
            self.result_text.Wrap(-1)
            self.perk_list = sorted(self.character_class.json_data[self.side][self.char]['perks'])
            self.candidate_list = wx.ListBox(parent, wx.ID_ANY, wx.DefaultPosition, (int(200*RATIO),int(128*RATIO)), self.perk_list, style=wx.LB_SINGLE)
        elif self.parent_id == APPEND_TAB_ID:
            all_perk = self.perk_class.get_jp_name(self.side)
            self.perk_list = self.character_class.dont_have_perks(self.side, self.char, all_perk)
            self.button_sizer = wx.GridBagSizer(0, 0)
            self.append_button = wx.Button(parent, wx.ID_ANY, '追加')
            self.candidate_list = wx.ListBox(parent, wx.ID_ANY, wx.DefaultPosition, (int(200*RATIO),int(128*RATIO)), self.perk_list, style=wx.LB_EXTENDED)
        else:
            self.perk_list = sorted(self.character_class.json_data[self.side][self.char]['perks'])
            self.button_sizer = wx.GridBagSizer(0, 0)
            self.delete_button = wx.Button(parent, wx.ID_ANY, '削除')
            self.clear_button = wx.Button(parent, wx.ID_ANY, 'すべて削除')
            self.candidate_list = wx.ListBox(parent, wx.ID_ANY, wx.DefaultPosition, (int(200*RATIO),int(128*RATIO)), self.perk_list, style=wx.LB_EXTENDED)
        self.layout(parent)
        self.bind()
        self.style()
        

    # 配置
    def layout(self, parent):
        self.char_sizer.Add(self.char_bitmap, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        for i,radio in enumerate(self.survivor_radio_button):
            self.radio_sizer.Add(radio, wx.GBPosition(i,0), wx.GBSpan(1, 1), wx.ALL, 5)
        for i,radio in enumerate(self.killer_radio_button):
            self.radio_sizer.Add(radio, wx.GBPosition(i,1), wx.GBSpan(1, 1), wx.ALL, 5)
        self.perk_sizer.Add(self.perk_bitmap, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        for i,radio in enumerate(self.search_radio_button):
            self.search_radio_sizer.Add(radio, wx.GBPosition(0,i), wx.GBSpan(1, 1), wx.ALL, 5)
        self.perk_sizer.Add(self.filter_textctrl, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALL, 5)
        self.perk_sizer.Add(self.candidate_list, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        if self.parent_id == SEARCH_TAB_ID:
            self.perk_sizer.Add(self.result_text, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        elif self.parent_id == APPEND_TAB_ID:
            self.button_sizer.Add(self.append_button, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
            self.perk_sizer.Add(self.button_sizer, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        elif self.parent_id == DELETE_TAB_ID:
            self.button_sizer.Add(self.delete_button, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
            self.button_sizer.Add(self.clear_button, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
            self.perk_sizer.Add(self.button_sizer, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        self.scroll_window.SetSizer(self.radio_sizer)
        self.radio_sizer.Fit(self.scroll_window)
        self.label_sizer.Add(self.scroll_window)
        self.main_sizer.Add(self.label_sizer, wx.GBPosition(0, 0), wx.GBSpan(3, 2), wx.ALL, 5)
        self.main_sizer.Add(self.char_sizer, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        self.main_sizer.Add(self.search_radio_sizer, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        self.main_sizer.Add(self.perk_sizer, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        parent.SetSizer(self.main_sizer)

    # イベント設定
    def bind(self):
        self.scroll_window.Bind(wx.EVT_RADIOBUTTON,self.selected_radio)
        self.filter_textctrl.Bind(wx.EVT_TEXT, self.perk_filter)
        for radio in self.search_radio_button:
            radio.Bind(wx.EVT_RADIOBUTTON,self.clear_display)
        if self.parent_id == SEARCH_TAB_ID:
            self.candidate_list.Bind(wx.EVT_LISTBOX,self.search_position)
        elif self.parent_id == APPEND_TAB_ID:
            self.candidate_list.Bind(wx.EVT_LISTBOX,self.show_perk_img)
            self.append_button.Bind(wx.EVT_BUTTON, self.add_perk)
        else:
            self.candidate_list.Bind(wx.EVT_LISTBOX,self.show_perk_img)
            self.delete_button.Bind(wx.EVT_BUTTON, self.delete_perk)
            self.clear_button.Bind(wx.EVT_BUTTON, self.clear_perk)
        
    # フォント、色設定
    def style(self):
        for radio in self.survivor_radio_button:
            radio.SetBackgroundColour(BACKGROUND_COLOR)
            radio.SetForegroundColour(TEXT_COLOR)
            radio.SetFont(self.FONT)
        for radio in self.killer_radio_button:
            radio.SetBackgroundColour(BACKGROUND_COLOR)
            radio.SetForegroundColour(TEXT_COLOR)
            radio.SetFont(self.FONT)
        self.static_box.SetForegroundColour(TEXT_COLOR)
        self.static_box.SetFont(self.FONT)
        for radio in self.search_radio_button:
            radio.SetBackgroundColour(BACKGROUND_COLOR)
            radio.SetForegroundColour(TEXT_COLOR)
            radio.SetFont(self.FONT)
        self.filter_textctrl.SetBackgroundColour(BACKGROUND_COLOR)
        self.filter_textctrl.SetForegroundColour(TEXT_COLOR)
        self.filter_textctrl.SetFont(self.FONT)
        self.candidate_list.SetBackgroundColour(BACKGROUND_COLOR)
        self.candidate_list.SetForegroundColour(TEXT_COLOR)
        self.candidate_list.SetFont(self.FONT)
        if self.parent_id == SEARCH_TAB_ID:
            self.result_text.SetBackgroundColour(BACKGROUND_COLOR)
            self.result_text.SetForegroundColour(RESULT_COLOR)
            self.result_text.SetFont(self.result_font)
        elif self.parent_id == APPEND_TAB_ID:
            self.append_button.SetBackgroundColour(BACKGROUND_COLOR)
            self.append_button.SetForegroundColour(TEXT_COLOR)
            self.append_button.SetFont(self.FONT)
        elif self.parent_id == DELETE_TAB_ID:
            self.delete_button.SetBackgroundColour(BACKGROUND_COLOR)
            self.delete_button.SetForegroundColour(TEXT_COLOR)
            self.delete_button.SetFont(self.FONT)
            self.clear_button.SetBackgroundColour(BACKGROUND_COLOR)
            self.clear_button.SetForegroundColour(TEXT_COLOR)
            self.clear_button.SetFont(self.FONT)

    # キャラ切替
    def selected_radio(self, event):
        self.char = event.GetEventObject().Label
        self.side = self.character_class.get_char_side(self.char)
        # キャラ画像変更
        self.char_bitmap.SetBitmap(wx.Bitmap(self.character_class.json_data[self.side][self.char]['image_path']))
        # テキストクリア
        self.filter_textctrl.Clear()
        if self.parent_id == SEARCH_TAB_ID:
            self.result_text.SetLabel('')
        self.perk_bitmap.SetBitmap(wx.NullBitmap)
        # perk_list切り替え
        if self.parent_id == APPEND_TAB_ID:
            all_perk = self.perk_class.get_jp_name(self.side)
            self.perk_list = self.character_class.dont_have_perks(self.side, self.char, all_perk)
            self.candidate_list.SetItems(self.perk_list)
        else:
            self.perk_list = self.character_class.json_data[self.side][self.char]['perks']
            self.candidate_list.SetItems(self.perk_list)

    # 絞り込み
    def perk_filter(self, event):
        filter_name = self.filter_textctrl.GetValue()
        perk_radio_flag = self.search_radio_button[0].GetValue()
        self.perk_bitmap.SetBitmap(wx.NullBitmap)
        # 入力があるとき
        if filter_name:
            # パーク名検索
            if perk_radio_flag:
                filtered_perks = [s for s in self.perk_list if filter_name in s]
            # 固有パーク検索
            else:
                tags = self.perk_class.get_tag_list(self.side)
                filter_tags = [s for s in tags if filter_name in s]
                # タグがあるとき
                if filter_tags:
                    self.status_bar.SetStatusText(f'{filter_tags[0]}の固有パーク')
                else:
                    self.status_bar.SetStatusText(f'{filter_name}は存在しません')
                    filtered_perks = []
                    self.candidate_list.SetItems(filtered_perks)
                    return False
                unique_perks = self.perk_class.get_unique_perk(self.side, filter_tags[0])
                filtered_perks = []
                # パークリストにある固有パークを取得
                for unique_perk in unique_perks:
                    if unique_perk in self.perk_list:
                        filtered_perks.append(unique_perk)
            self.candidate_list.SetItems(filtered_perks)
            # 絞り込んだパークが1つのときそれを選択
            if len(filtered_perks) == 1:
                self.candidate_list.SetSelection(0)
                if self.parent_id == SEARCH_TAB_ID:
                    self.search_position(None)
                else:
                    self.show_perk_img(None)
        else:
            self.candidate_list.SetItems(self.perk_list)
        

    # パーク位置検索
    def search_position(self, event):
        perk_name = self.candidate_list.GetStringSelection()
        perk_img_path = self.perk_class.get_img_path(self.side, perk_name)
        bitmap = self.image_resize(perk_img_path)
        self.perk_bitmap.SetBitmap(bitmap)
        page, rows, columns = self.character_class.get_position(self.side, self.char, perk_name)
        self.result_text.SetLabel(f'{page}ページ\n{rows}行\n{columns}列')

    # パーク画像表示
    def show_perk_img(self, event): 
        perk_index = self.candidate_list.GetSelections()
        perk_name = self.candidate_list.GetString(perk_index[-1])
        perk_img_path = self.perk_class.get_img_path(self.side, perk_name)
        bitmap = self.image_resize(perk_img_path)
        self.perk_bitmap.SetBitmap(bitmap)
        if self.parent_id == SEARCH_TAB_ID:
            self.result_text.SetLabel('')
        
    # パーク追加
    def add_perk(self, event):
        perk_index = self.candidate_list.GetSelections()
        perk_names = []
        for i in perk_index:
            perk_names.append(self.candidate_list.GetString(i))
        self.character_class.append_perk(self.side, self.char, perk_names)
        all_perk = self.perk_class.get_jp_name(self.side)
        self.perk_list = self.character_class.dont_have_perks(self.side, self.char, all_perk)
        self.candidate_list.SetItems(self.perk_list)
        self.status_bar.SetStatusText(f'{self.char}の所持パークに\"{perk_names}\"追加しました')
        self.filter_textctrl.Clear()
        self.perk_bitmap.SetBitmap(wx.NullBitmap)
    
    # パーク削除
    def delete_perk(self,event):
        perk_index = self.candidate_list.GetSelections()
        perk_names = []
        for i in perk_index:
            perk_names.append(self.candidate_list.GetString(i))
        self.character_class.remove_perk(self.side, self.char, perk_names)
        self.perk_list = sorted(self.character_class.json_data[self.side][self.char]['perks'])
        self.status_bar.SetStatusText(f'{self.char}の所持パークから\"{perk_names}\"を削除しました')
        self.candidate_list.SetItems(self.perk_list)
        self.filter_textctrl.Clear()
        self.perk_bitmap.SetBitmap(wx.NullBitmap)

    # 所持パーククリア
    def clear_perk(self, event):
        self.character_class.renew_perks(self.side, self.char, [])
        self.perk_list = self.character_class.json_data[self.side][self.char]['perks']
        self.status_bar.SetStatusText(f'{self.char}の所持パークからすべてのパークを削除しました')
        self.candidate_list.SetItems(self.perk_list)
        self.filter_textctrl.Clear()
        self.perk_bitmap.SetBitmap(wx.NullBitmap)
    
    # パーク画像リサイズ
    def image_resize(self, path):
        bitmap = wx.Bitmap(path)
        image = bitmap.ConvertToImage()
        image = image.Scale(int(128*RATIO), int(128*RATIO), wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)

        return result

    # 表示クリア
    def clear_display(self, event):
        self.perk_bitmap.SetBitmap(wx.NullBitmap)
        self.filter_textctrl.Clear()
        self.result_text.SetLabel('')

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()
