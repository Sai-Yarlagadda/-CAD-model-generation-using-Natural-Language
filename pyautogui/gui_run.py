import pyautogui
import time
import pyperclip

def get_mouse_coordinates():

    """
    This function constantly gives you mouse coordinates until you do a keyboard interrupt
    """
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: X = {x}, Y = {y}")
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")


def script_on_text_editor(macro_script, file_name):

    """
    Save the generated script by LLM code on a text editor.
    File path should be complete with the .FCMacro file extension at the end.
    """
    with open(file_name, 'w') as file:
        file.write(macro_script)


def generate_CAD_design(file_name):

    """
    Opening the FreeCAD software. And running the macro
    """
    pyautogui.hotkey('win') #Open Run in windows
    time.sleep(.5)
    pyautogui.typewrite('FreeCAD')  
    time.sleep(.5)
    pyautogui.press('enter')  #Enter the pyautogui
    print('Opened FreeCAD software')
    time.sleep(8)
    pyautogui.hotkey('ctrl', 'o') #open the macro generated
    time.sleep(.5)
    pyautogui.typewrite(f'{file_name}')
    time.sleep(.1)
    pyautogui.press('enter')
    print('Opened the macros')
    time.sleep(.1)
    pyautogui.moveTo(622, 75)
    pyautogui.hotkey('ctrl', 'f6')#run the macro
    '''time.sleep(2)
    pyautogui.leftClick()'''
    

def CAD_screenshots(filepath_images):

    """
    Takes screenshots of the isometric view of the model generated on FreeCAD
    """

    pyautogui.hotkey('v', 'f')
    time.sleep(.1)
    pyautogui.hotkey('0')#orient the CAD model in isometric view
    time.sleep(.1)
    screenshot = pyautogui.screenshot(region=(343, 147, 1850, 675))

    #TODO - Save in a valid location
    screenshot.save('Isometric_view.png')

def get_error_msg():

    """
    This function returns the error message
    If no error returns an empty string  
    """
    pyperclip.copy('') #erases whatever is copied into clipboard initially

    pyautogui.moveTo(1278, 929)
    pyautogui.leftClick()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    error_msg = pyperclip.paste() #if no error returns an empty string. 
    return error_msg

def close_freecad_window():

    """
    Closes the whole model
    """
    pyautogui.hotkey('alt', 'f4')
    pyautogui.press('left')
    pyautogui.press('enter')#shuts down the freecad software


if __name__ == '__main__':


    #check for sample macro below. 
    macro = r'''
import FreeCAD as App
import Part

# Create a new document
doc = App.newDocument()

# Define the dimensions of the cube
length = 10
width = 10
height = 10

# Create a cube shape
cube = Part.makeBox(length, width, height)

# Add the cube to the document
doc.addObject("Part::Feature", "Cube").Shape = cube

# Refresh the 3D view
App.ActiveDocument.recompute()

'''
    macro_name = 'cube.FCMacro'
    macro_path  = f'C:\\Users\\saisr\\AppData\\Roaming\\FreeCAD\\Macro\\{macro_name}'
    script_on_text_editor(macro_script=macro, file_name=macro_path)
    time.sleep(2)
    generate_CAD_design(file_name = macro_name)
    time.sleep(1)
    #print('getting error msg')
    #get_error_msg()
    #get_mouse_coordinates()
    CAD_screenshots('zz')#give a valid location
    close_freecad_window()
