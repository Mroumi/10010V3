from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView
import os
import shutil

class KeyConfigApp(App):
    def build(self):
        font_path = os.path.join(os.getcwd(), '方正小标宋简体.TTF')
        resource_add_path(font_path)
        LabelBase.register(DEFAULT_FONT, '方正小标宋简体.TTF')
        # UI布局
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 文件选择按钮
        select_file_button = Button(text='选择文件', on_press=self.select_file)
        layout.add_widget(select_file_button)

        # 显示选择的文件路径
        self.file_path_label = TextInput(hint_text='选择的文件路径', multiline=False, readonly=True)
        layout.add_widget(self.file_path_label)

        # 游戏ID输入框
        id_input = TextInput(hint_text='输入游戏ID', multiline=False)
        layout.add_widget(id_input)

        # 键位号选择框
        key_config_options = ['1', '2', '3']
        key_config_spinner = Spinner(text='选择键位号', values=key_config_options)
        layout.add_widget(key_config_spinner)

        # 按钮触发创建和复制操作
        create_and_copy_button = Button(text='创建并复制键位文件', on_press=self.create_and_copy_key_config)
        layout.add_widget(create_and_copy_button)

        return layout

    def select_file(self, instance):
        # 打开文件选择器
        file_chooser = FileChooserIconView()
        file_chooser.bind(on_submit=self.file_selected)
        file_chooser.path = os.path.join(os.getcwd(), '键位')

        # 显示文件选择器
        popup = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup.add_widget(file_chooser)

        self.popup = popup

        App.get_running_app().root_window.add_widget(popup)

    def file_selected(self, instance, selection, touch):
        # 获取选择的文件路径
        selected_file = os.path.join(instance.path, selection[0])

        # 更新UI中的文件路径显示
        self.file_path_label.text = selected_file

        # 关闭文件选择器弹窗
        App.get_running_app().root_window.remove_widget(self.popup)

    def create_and_copy_key_config(self, instance):
        try:
            # 获取输入的游戏ID、选择的键位号和选择的文件路径
            game_id = self.root.children[2].text
            key_config_spinner = self.root.children[1]

            # 获取键位号选择框的当前选中值
            key_config = key_config_spinner.text

            # 构造新文件的路径
            new_file_name = f'JoySticksConfig_{key_config}_{game_id}.json'
            assets_folder = os.path.join('Android', 'data', 'com.tencent.tmgp.cf', 'files', 'Assets4')
            new_file_path = os.path.join(os.getcwd(), assets_folder, new_file_name)

            # 输出目标文件夹和源文件的路径
        #  print(f'目标文件夹：{os.path.join(os.getcwd(), assets_folder)}')
        # print(f'源文件路径：{self.file_path_label.text}')

            # 复制选择的文件到新的路径
            shutil.copyfile(self.file_path_label.text, new_file_path)

            print(f'成功复制键位文件到 {new_file_path}')
        except Exception as e:
            print(f'发生错误：{e}')


if __name__ == '__main__':
    KeyConfigApp().run()
