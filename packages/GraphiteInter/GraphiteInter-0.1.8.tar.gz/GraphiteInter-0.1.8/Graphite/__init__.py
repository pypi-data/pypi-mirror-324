import threading
import time
import tkinter as tk
from tkinter import  Checkbutton, Entry, Frame, IntVar, Label, OptionMenu, Radiobutton, StringVar, Text, ttk
from PIL import Image, ImageTk

class GraphiteInter:
    _root = None
    _bg_image_label = None
    _buttons = {}
    _texts = []
    _comboboxes = {}
    _sliders = {}
    _inputs = {} 
    _texts = {}  # Usado para armazenar os textos com seus IDs
    _state = {}  # Variável para armazenar o estado
    _width =  None
    _height = None 
    _bgi = None
    _tabs = {}
    @staticmethod
    def create_window(title="GraphiteInter App"):
        """Cria uma janela principal com título e configurações padrão."""
        GraphiteInter._root = tk.Tk()
        GraphiteInter._root.title(title)
        GraphiteInter._root.geometry("800x600")  # Dimensões padrão
        GraphiteInter._root.configure(bg="white")  # Cor de fundo padrão
        GraphiteInter._width = 800
        GraphiteInter._height = 600

    @staticmethod
    def setdimensions(width, height):
        """Define as dimensões da janela e armazena nas variáveis de classe."""
        if GraphiteInter._root:
            GraphiteInter._root.geometry(f"{width}x{height}")
            
            # Armazenar as dimensões nas variáveis de classe
            GraphiteInter._width = width
            GraphiteInter._height = height
            
            return width, height
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def setbackground(color):
        """Define a cor de fundo da janela."""
        if GraphiteInter._root:
            GraphiteInter._root.configure(bg=color)
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def setbgimage(image_path):
        """Define uma imagem de fundo na janela."""
        
        if GraphiteInter._root:
        
            try:
                image = Image.open(image_path)
                bg_image = ImageTk.PhotoImage(image)
                
                if GraphiteInter._bg_image_label:
                    GraphiteInter._bg_image_label.destroy()  # Remove o antigo label da imagem

                # Criar e posicionar a imagem de fundo
                GraphiteInter._bg_image_label = tk.Label(GraphiteInter._root, image=bg_image)
                GraphiteInter._bg_image_label.image = bg_image  # Mantém uma referência para a imagem
                GraphiteInter._bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche toda a janela
                GraphiteInter._bgi=image_path
            except Exception as e:
                raise RuntimeError(f"Erro ao carregar a imagem: {e}")
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def create_button(text, button_id, command):
     """Cria um botão e adiciona ao estado."""
     if GraphiteInter._root:
        if button_id in GraphiteInter._buttons:
            raise ValueError(f"Já existe um botão com o ID '{button_id}'.")
        
        # Cria o botão
        button = tk.Button(GraphiteInter._root, text=text, command=command)
        GraphiteInter._buttons[button_id] = button
        
        # Inicializa o botão no estado
        GraphiteInter._state.setdefault("buttons", {})
        GraphiteInter._state["buttons"][button_id] = {
            "text": text,
            "bg": button.cget("bg"),
            "fg": button.cget("fg"),
            "position": [0, 0]  # Posição padrão inicial
        }
     else:
        raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def buttonposition(button_id, x, y):
     """Define a posição de um botão na interface."""
     if button_id in GraphiteInter._buttons:
        button = GraphiteInter._buttons[button_id]
        button.place(x=x, y=y)  # Altera a posição visual do botão
        GraphiteInter._state["buttons"][button_id]["position"] = [x, y]  # Atualiza a posição no estado interno
     else:
        raise KeyError(f"Botão com ID '{button_id}' não encontrado.")

    @staticmethod
    def inserttext(text_id, text, font_size, position, color):
        """Insere texto em uma posição específica com uma cor personalizada e tamanho de fonte, agora com ID."""
        if GraphiteInter._root:
            x, y = position
            label = tk.Label(GraphiteInter._root, text=text, fg=color, font=("Arial", font_size))
            label.place(x=x, y=y)
            GraphiteInter._texts[text_id] = label  # Armazena o texto com o ID especificado
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def update_text(text_id, new_text):
        """Atualiza o texto de um Label existente, dado o ID."""
        if text_id in GraphiteInter._texts:
            GraphiteInter._texts[text_id].config(text=new_text)
        else:
            raise ValueError(f"O texto com ID '{text_id}' não foi encontrado.")
      
    @staticmethod
    def insertcombo(combo_id, options, position, size=(20, 3)):
     """Cria uma ComboBox (caixa de seleção) e a armazena com seu ID."""
     if GraphiteInter._root:
        if combo_id in GraphiteInter._comboboxes:
            raise ValueError(f"A ComboBox com ID '{combo_id}' já existe.")
        
        # Cria a ComboBox
        combo = ttk.Combobox(GraphiteInter._root, values=options.split(','), width=size[0], height=size[1])
        x, y = position
        combo.place(x=x, y=y)
        
        # Armazena a ComboBox no dicionário com seu ID
        GraphiteInter._comboboxes[combo_id] = combo
     else:
        raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    @staticmethod
    def get_combo_value(combo_id):
     """Retorna o valor selecionado da ComboBox com o ID especificado."""
     if combo_id in GraphiteInter._comboboxes:
        return GraphiteInter._comboboxes[combo_id].get()
     else:
        raise ValueError(f"A ComboBox com ID '{combo_id}' não foi encontrada.")
    @staticmethod
    def update_combo_options(combo_id, new_options):
     """Atualiza as opções de uma ComboBox existente."""
     if combo_id in GraphiteInter._comboboxes:
        combo = GraphiteInter._comboboxes[combo_id]
        combo['values'] = new_options.split(',')
     else:
        raise ValueError(f"A ComboBox com ID '{combo_id}' não foi encontrada.")
    @staticmethod
    def remove_combo(combo_id):
     """Remove uma ComboBox da interface."""
     if combo_id in GraphiteInter._comboboxes:
        GraphiteInter._comboboxes[combo_id].destroy()
        del GraphiteInter._comboboxes[combo_id]
     else:
        raise ValueError(f"A ComboBox com ID '{combo_id}' não foi encontrada.")

    @staticmethod
    def insertslider(slider_id, position, orient="horizontal", sliderlength=20, slider_color="blue", width=10):
        """Cria um slider e o armazena no dicionário com seu ID."""
        if GraphiteInter._root:
            slider = tk.Scale(GraphiteInter._root, orient=orient, sliderlength=sliderlength, length=300, width=width)
            x, y = position
            slider.place(x=x, y=y)
            GraphiteInter._sliders[slider_id] = slider
            # Estilo para o slider (cor)
            slider.config(troughcolor="lightgray", sliderrelief="solid", bg=slider_color)
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    @staticmethod
    def Getslidervalue(slider_id):
        """Obtém o valor atual do slider."""
        if slider_id in GraphiteInter._sliders:
            return GraphiteInter._sliders[slider_id].get()
        else:
            raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
    @staticmethod
    def setmaximum(slider_id, max_value):
        """Define o valor máximo de um slider."""
        if GraphiteInter._root:
            if slider_id in GraphiteInter._sliders:
                GraphiteInter._sliders[slider_id].config(to=max_value)  # Corrigir para 'to' em vez de 'max'
            else:
                raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    @staticmethod
    def sliderpos(slider_id, position):
        """Define a posição do slider."""
        if slider_id in GraphiteInter._sliders:
            GraphiteInter._sliders[slider_id].set(position)
        else:
            raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
    @staticmethod
    def removebutton(button_id):
        """Remove um botão da interface."""
        if button_id in GraphiteInter._buttons:
            GraphiteInter._buttons[button_id].destroy()
            del GraphiteInter._buttons[button_id]
    @staticmethod
    def removeslider(Slider_id):
        """Remove um slider da interface."""
        if Slider_id in GraphiteInter._sliders:
            GraphiteInter._sliders[Slider_id].destroy()
            del GraphiteInter._sliders[Slider_id]
    @staticmethod
    def removeText(_texts):
        """Remove um texto da interface."""
        if _texts in GraphiteInter._texts:
            GraphiteInter._texts[_texts].destroy()
            del GraphiteInter._texts[_texts]
    @staticmethod
    def removeInput(_inputs):
        """Remove um input da interface."""
        if _inputs in GraphiteInter._inputs:
            GraphiteInter._inputs[_inputs].destroy()
            del GraphiteInter._inputs[_inputs]
    @staticmethod
    def removeBgImage():
      """Remove a imagem de fundo da interface."""
      if GraphiteInter._bg_image_label:
          GraphiteInter._bg_image_label.destroy()  # Remove o widget da imagem de fundo
          GraphiteInter._bg_image_label = None
      else:
          raise ValueError("Nenhuma imagem de fundo foi definida.")         
    @staticmethod
    def sliderOrientation(slider_id, orientation):
        """Define a orientação do slider (horizontal ou vertical)."""
        if slider_id in GraphiteInter._sliders:
            GraphiteInter._sliders[slider_id].config(orient=orientation)
        else:
            raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
    @staticmethod
    def sliderthickness(slider_id, thickness):
        """Define a espessura do slider."""
        if GraphiteInter._root:
            if slider_id in GraphiteInter._sliders:
                GraphiteInter._sliders[slider_id].config(width=thickness)  # Corrigir para 'width' em vez de 'thickness'
            else:
                raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    @staticmethod
    def slidercolor(slider_id, color):
        """Define a cor do slider."""
        if slider_id in GraphiteInter._sliders:
            GraphiteInter._sliders[slider_id].config(bg=color)
        else:
            raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado.")
    @staticmethod
    def addtextinput(input_id, position, size=(20, 3)):
        """Cria uma caixa de entrada de texto (Text) e a armazena com seu ID."""
        if GraphiteInter._root:
            text = tk.Text(GraphiteInter._root, width=size[0], height=size[1])
            x, y = position
            text.place(x=x, y=y)
            GraphiteInter._inputs[input_id] = text  # Armazena a entrada criada
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    @staticmethod
    def inputposition(input_id, position):
        """Define a posição de um campo de entrada."""
        if input_id in GraphiteInter._inputs:
            entry = GraphiteInter._inputs[input_id]
            x, y = position
            entry.place(x=x, y=y)
        else:
            raise ValueError(f"O campo de entrada com ID '{input_id}' não foi encontrado.")
    @staticmethod
    def inputsize(input_id, size):
        """Define o tamanho do campo de entrada (largura, altura)."""
        if input_id in GraphiteInter._inputs:
            entry = GraphiteInter._inputs[input_id]
            entry.config(width=size[0], height=size[1])
        else:
            raise ValueError(f"O campo de entrada com ID '{input_id}' não foi encontrado.")
    @staticmethod
    def buttonaction(button_id, command):
        """Define a ação de um botão."""
        if GraphiteInter._root:
            if button_id in GraphiteInter._buttons:
                button = GraphiteInter._buttons[button_id]
                button.config(command=command)
            else:
                raise ValueError(f"O botão com ID '{button_id}' não foi encontrado.")
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
    
    @staticmethod
    def run():
        """Inicia o loop principal da interface gráfica."""
        if GraphiteInter._root:
            GraphiteInter._root.mainloop()
        else:
            raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")
  
    @staticmethod
    def show_notification(message, duration, color, font):
     """
    Exibe uma notificação temporária na janela principal.
    :param message: Texto da notificação.
    :param duration: Duração em milissegundos (default: 3000ms).
    :param color: Cor de fundo da notificação (default: "yellow").
    :param font: Fonte do texto (default: "Arial", 12).
    """
     if GraphiteInter._root:
        notification_label = tk.Label(
            GraphiteInter._root,
            text=message,
            bg=color,
            fg="black",
            font=font,
            relief="solid",
            padx=10,
            pady=5,
        )
        notification_label.place(relx=0.5, rely=0, anchor="n")
        
        # Remove a notificação após o tempo definido
        GraphiteInter._root.after(duration, notification_label.destroy)
     else:
        raise RuntimeError("A janela principal ainda não foi criada. Use GraphiteInter.create_window() primeiro.")

    @staticmethod
    def create_tab(tab_id, label):
        """
        Cria uma nova aba com o rótulo especificado.
        :param tab_id: ID único para a aba.
        :param label: Rótulo visível da aba.
        """
        if not hasattr(GraphiteInter, "_notebook"):
            GraphiteInter._notebook = ttk.Notebook(GraphiteInter._root)
            GraphiteInter._notebook.pack(expand=True, fill="both")
            GraphiteInter._tabs = {}
    
        if tab_id in GraphiteInter._tabs:
            raise ValueError(f"Uma aba com o ID '{tab_id}' já existe.")
    
        tab_frame = tk.Frame(GraphiteInter._notebook)
        GraphiteInter._notebook.add(tab_frame, text=label)
        GraphiteInter._tabs[tab_id] = tab_frame
    @staticmethod
    def tabwidget(tab_id, widget):
     """
    Adiciona um widget a uma aba específica.
    :param tab_id: ID da aba onde o widget será adicionado.
    :param widget: Widget a ser adicionado.
    """
     if tab_id in GraphiteInter._tabs:
        widget.pack(in_=GraphiteInter._tabs[tab_id], padx=10, pady=5)
     else:
        raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
    @staticmethod
    def remove_tab(tab_id):
        """
        Remove uma aba existente.
        :param tab_id: ID da aba a ser removida.
        """
        if tab_id in GraphiteInter._tabs:
            tab_frame = GraphiteInter._tabs[tab_id]
            GraphiteInter._notebook.forget(tab_frame)  # Remove a aba do Notebook
            del GraphiteInter._tabs[tab_id]  # Remove a referência
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
    @staticmethod
    def create_tab_button(tab_id, button_id, button_text, buttonposx, buttonposy, action, button_color=None, text_color=None):
        """
        Cria um botão dentro de uma aba específica.
        :param tab_id: ID da aba onde o botão será adicionado.
        :param button_id: ID único para o botão.
        :param button_text: Texto exibido no botão.
        :param buttonposx: Espaçamento horizontal do botão.
        :param buttonposy: Espaçamento vertical do botão.
        :param action: Função que será executada quando o botão for clicado.
        :param button_color: Cor de fundo do botão.
        :param text_color: Cor do texto do botão.
        """
        if tab_id not in GraphiteInter._tabs:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")

        if button_id in GraphiteInter._buttons:
            raise ValueError(f"Já existe um botão com o ID '{button_id}'.")

        # Criar o botão
        button = tk.Button(GraphiteInter._tabs[tab_id], text=button_text, command=action, bg=button_color, fg=text_color)
        button.pack(padx=buttonposx, pady=buttonposy)  # Posiciona o botão dentro da aba

        # Armazenar o botão com seu ID
        GraphiteInter._buttons[button_id] = button

    @staticmethod
    def tabbackground(tab_id, background):
        """
        Define o plano de fundo de uma aba específica.
        :param tab_id: ID da aba onde o plano de fundo será alterado.
        :param background: Cor (ex.: "blue") ou caminho para uma imagem (ex.: "path/to/image.png").
        """
        if tab_id not in GraphiteInter._tabs:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
    
        tab = GraphiteInter._tabs[tab_id]
    
        # Se for uma cor, define como fundo da aba
        if isinstance(background, str) and not background.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            tab.configure(bg=background)
        else:
            # Caso seja uma imagem, carrega e define como fundo
            try:
                image = Image.open(background)
                bg_image = ImageTk.PhotoImage(image)
    
                # Cria um label com a imagem de fundo
                bg_label = tk.Label(tab, image=bg_image)
                bg_label.image = bg_image  # Mantém a referência à imagem
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
                # Coloca o label como fundo da aba
                bg_label.lower()  # Move para trás de outros widgets
            except Exception as e:
                raise RuntimeError(f"Erro ao carregar a imagem: {e}")
            
#acabei de criar abaixo

    @staticmethod
    def insert_text_in_tab(tab_id, text_id, text, font_size, position, color):
     """Insere um texto em uma aba específica com um ID.""" 
     if tab_id in GraphiteInter._tabs:
        x, y = position
        try:
            # Forçar conversão correta de cor hexadecimal
            if color.startswith("#") and len(color) == 7:
                tk_color = color.upper()  # Algumas versões do Tkinter podem exigir maiúsculas
            else:
                tk_color = color.lower()  # Garantir que cores por nome sejam minúsculas
                
            label = tk.Label(GraphiteInter._tabs[tab_id], text=text, fg=tk_color, font=("Arial", font_size))
            label.place(x=x, y=y)
            GraphiteInter._texts[text_id] = label
        except tk.TclError:
            raise ValueError(f"Cor '{color}' inválida. Use um nome de cor válido ou um código hexadecimal no formato #RRGGBB.")
     else:
        raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")

    @staticmethod
    def update_text_in_tab(tab_id, text_id, new_text):
        """Atualiza o texto de um Label dentro de uma aba específica, dado o ID."""
        if tab_id in GraphiteInter._tabs:
            if text_id in GraphiteInter._texts:
                GraphiteInter._texts[text_id].config(text=new_text)
            else:
                raise ValueError(f"O texto com ID '{text_id}' não foi encontrado.")
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def remove_text_from_tab(tab_id, text_id):
        """Remove um texto de uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            if text_id in GraphiteInter._texts:
                GraphiteInter._texts[text_id].destroy()
                del GraphiteInter._texts[text_id]
            else:
                raise ValueError(f"O texto com ID '{text_id}' não foi encontrado na aba '{tab_id}'.")
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def insert_slider_in_tab(tab_id, slider_id, position, orient="horizontal", sliderlength=20, slider_color="blue", width=10):
        """Insere um slider em uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            slider = tk.Scale(GraphiteInter._tabs[tab_id], orient=orient, sliderlength=sliderlength, length=300, width=width)
            x, y = position
            slider.place(x=x, y=y)
            GraphiteInter._sliders[slider_id] = slider
            slider.config(troughcolor="lightgray", sliderrelief="solid", bg=slider_color)
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def remove_slider_from_tab(tab_id, slider_id):
        """Remove um slider de uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            if slider_id in GraphiteInter._sliders:
                GraphiteInter._sliders[slider_id].destroy()
                del GraphiteInter._sliders[slider_id]
            else:
                raise ValueError(f"O slider com ID '{slider_id}' não foi encontrado na aba '{tab_id}'.")
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def insert_combo_in_tab(tab_id, combo_id, options, position, size=(20, 3)):
        """Insere uma ComboBox em uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            if combo_id in GraphiteInter._comboboxes:
                raise ValueError(f"A ComboBox com ID '{combo_id}' já existe.")
            combo = ttk.Combobox(GraphiteInter._tabs[tab_id], values=options.split(','), width=size[0], height=size[1])
            x, y = position
            combo.place(x=x, y=y)
            GraphiteInter._comboboxes[combo_id] = combo
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def remove_combo_from_tab(tab_id, combo_id):
        """Remove uma ComboBox de uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            if combo_id in GraphiteInter._comboboxes:
                GraphiteInter._comboboxes[combo_id].destroy()
                del GraphiteInter._comboboxes[combo_id]
            else:
                raise ValueError(f"A ComboBox com ID '{combo_id}' não foi encontrada na aba '{tab_id}'.")
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def insert_input_in_tab(tab_id, input_id, position, size=(20, 3)):
        """Insere uma caixa de entrada de texto (Input) em uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            input_field = tk.Text(GraphiteInter._tabs[tab_id], width=size[0], height=size[1])
            x, y = position
            input_field.place(x=x, y=y)
            GraphiteInter._inputs[input_id] = input_field  # Armazena o input com o ID especificado
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
  
    @staticmethod
    def remove_input_from_tab(tab_id, input_id):
        """Remove uma caixa de entrada de texto de uma aba específica."""
        if tab_id in GraphiteInter._tabs:
            if input_id in GraphiteInter._inputs:
                GraphiteInter._inputs[input_id].destroy()
                del GraphiteInter._inputs[input_id]
            else:
                raise ValueError(f"O input com ID '{input_id}' não foi encontrado na aba '{tab_id}'.")
        else:
            raise ValueError(f"A aba com ID '{tab_id}' não foi encontrada.")
    widgets = {}
    scheduled_events = {}

    @staticmethod
    def schedule_event(event_id, action, delay_ms):
        """Agenda a execução de uma função após um tempo definido."""
        def delayed_execution():
            time.sleep(delay_ms / 1000)
            action()
        
        thread = threading.Thread(target=delayed_execution)
        thread.start()
        GraphiteInter.scheduled_events[event_id] = thread
    
    @staticmethod
    def animate_widget(widget_id, effect="fade_in", duration=500):
        """Aplica uma animação a um widget específico."""
        widget = GraphiteInter.widgets.get(widget_id)
        if not widget:
            return

        if effect == "fade_in":
            for alpha in range(0, 11):
                widget.after(int(duration / 10) * alpha, lambda a=alpha: widget.configure(alpha=a / 10))

        elif effect == "fade_out":
            for alpha in range(10, -1, -1):
                widget.after(int(duration / 10) * (10 - alpha), lambda a=alpha: widget.configure(alpha=a / 10))

    
    @staticmethod
    def create_form(form_id, fields, x=0, y=0):
        """Cria um formulário com base em um dicionário de campos e permite definir a posição."""
        form_frame = Frame()
        GraphiteInter.widgets[form_id] = form_frame
        
        for i, (label_text, field_type) in enumerate(fields.items()):
            label = Label(form_frame, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)
            
            if field_type == "text":
                entry = Entry(form_frame)
            elif field_type == "password":
                entry = Entry(form_frame, show="*")
            elif field_type == "email":
                entry = Entry(form_frame)
            elif field_type == "number":
                entry = Entry(form_frame, validate="key", validatecommand=(form_frame.register(lambda char: char.isdigit()), "%P"))
            elif field_type == "date":
                entry = Entry(form_frame)
            elif field_type == "checkbox":
                var = IntVar()  # Variável para o estado do checkbox
                entry = Checkbutton(form_frame, text=label_text, variable=var)
                GraphiteInter.widgets[f"{form_id}_{label_text}_var"] = var
            elif field_type == "radio":
                var = IntVar()  # Variável para o estado do radio button
                entry = Frame(form_frame)
                options = ["Option 1", "Option 2", "Option 3"]  # Exemplo de opções
                for j, option in enumerate(options):
                    radio = Radiobutton(entry, text=option, variable=var, value=j)
                    radio.grid(row=j, column=0)
                GraphiteInter.widgets[f"{form_id}_{label_text}_var"] = var
            
            elif field_type == "textarea":
                entry = Text(form_frame, height=4, width=30)
            elif field_type == "file":
                entry = Entry(form_frame)  # Placeholder para um botão de upload de arquivo
            elif field_type == "hidden":
                entry = Entry(form_frame, show="")  # Pode ser invisível ou escondido em uma variável
            else:
                entry = Label(form_frame, text=f"Tipo '{field_type}' não suportado")
            
            entry.grid(row=i, column=1, padx=5, pady=5)
            GraphiteInter.widgets[f"{form_id}_{label_text}"] = entry
        
        form_frame.place(x=x, y=y)  # Define a posição do formulário

    @staticmethod
    def get_form_data(form_id):
        """Obtém os dados preenchidos no formulário com base no form_id."""
        form_data = {}
        form_frame = GraphiteInter.widgets.get(form_id)

        if form_frame:
            for widget_key, widget in GraphiteInter.widgets.items():
                if widget_key.startswith(form_id):
                    label_text = widget_key.replace(f"{form_id}_", "")
                    if isinstance(widget, Entry):
                        form_data[label_text] = widget.get()
                    elif isinstance(widget, Text):
                        form_data[label_text] = widget.get("1.0", "end-1c")  # Captura o conteúdo do Text
                    elif isinstance(widget, Checkbutton):
                        # Captura o valor do checkbox diretamente da variável associada
                        var = GraphiteInter.widgets.get(f"{form_id}_{label_text}_var")
                        form_data[label_text] = var.get() if var else None
                    elif isinstance(widget, Radiobutton):
                        form_data[label_text] = widget.var.get()  # Captura a opção selecionada no radio button
                    
        return form_data