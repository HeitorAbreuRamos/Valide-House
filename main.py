from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import sqlite3

def init_db():
    conn = sqlite3.connect('valide_house.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_validade DATE NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT DEFAULT 'ativo'
        )
    ''')
    conn.commit()
    conn.close()

class ValideHouseApp(App):
    def build(self):
        init_db()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(Label(text='VALIDE-HOUSE (ODS 12)', font_size=24, size_hint_y=None, height=50))
        
        self.input_nome = TextInput(hint_text='Nome do Alimento', multiline=False)
        self.input_qtd = TextInput(hint_text='Quantidade', input_filter='int', multiline=False)
        self.input_data = TextInput(hint_text='Validade (AAAA-MM-DD)', multiline=False)
        self.input_cat = TextInput(hint_text='Categoria', multiline=False)
        
        self.layout.add_widget(self.input_nome)
        self.layout.add_widget(self.input_qtd)
        self.layout.add_widget(self.input_data)
        self.layout.add_widget(self.input_cat)
        
        btn_cadastrar = Button(text='Cadastrar Alimento', size_hint_y=None, height=50)
        btn_cadastrar.bind(on_press=self.cadastrar)
        self.layout.add_widget(btn_cadastrar)
        
        self.lbl_status = Label(text='Status: Aguardando ações...')
        self.layout.add_widget(self.lbl_status)
        
        return self.layout

    def cadastrar(self, instance):
        nome = self.input_nome.text.strip()
        qtd = self.input_qtd.text.strip()
        data_val = self.input_data.text.strip()
        cat = self.input_cat.text.strip()

        if nome and qtd and data_val and cat:
            conn = sqlite3.connect('valide_house.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alimentos (nome, quantidade, data_validade, categoria)
                VALUES (?, ?, ?, ?)
            ''', (nome, int(qtd), data_val, cat))
            conn.commit()
            conn.close()
            
            self.lbl_status.text = f"✅ '{nome}' cadastrado com sucesso!"
            self.input_nome.text = ""
            self.input_qtd.text = ""
            self.input_data.text = ""
            self.input_cat.text = ""
        else:
            self.lbl_status.text = "❌ Preencha todos os campos!"

if __name__ == '__main__':
    ValideHouseApp().run()
