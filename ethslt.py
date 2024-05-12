from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField

class CalculatorApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        
        # Create text field to display input and result
        self.input_field = MDTextField(hint_text="0", size_hint_y=None, height=100)
        self.screen.add_widget(self.input_field)
        
        # Create grid layout for buttons
        button_grid = MDGridLayout(cols=4, spacing=10)
        
        # Create number buttons
        for i in range(1, 10):
            button = MDRaisedButton(text=str(i), on_release=self.on_button_press)
            button_grid.add_widget(button)
        
        # Create operation buttons
        operations = ["+", "-", "*", "/"]
        for op in operations:
            button = MDRaisedButton(text=op, on_release=self.on_button_press)
            button_grid.add_widget(button)
        
        # Create clear and equals buttons
        clear_button = MDRaisedButton(text="C", on_release=self.clear_input)
        equals_button = MDRaisedButton(text="=", on_release=self.calculate_result)
        button_grid.add_widget(clear_button)
        button_grid.add_widget(equals_button)
        
        self.screen.add_widget(button_grid)
        
        return self.screen
    
    def on_button_press(self, instance):
        self.input_field.text += instance.text
    
    def clear_input(self, instance):
        self.input_field.text = ""
    
    def calculate_result(self, instance):
        try:
            result = eval(self.input_field.text)
            self.input_field.text = str(result)
        except Exception as e:
            self.input_field.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()

