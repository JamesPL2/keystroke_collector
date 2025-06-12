from pynput import keyboard
import pandas as pd
import time

data = []
start_time = time.time()
last_keydown_time = None
last_keyup_time = None
press_times = {}

def on_press(key):
    global data, start_time, last_keydown_time, press_times
    
    current_time = time.time()
    
    if hasattr(key, 'char') and key.char:
        key_name = key.char
        print(f"Naciśnięto: {key.char}")
    else:
        key_name = str(key).replace('Key.', '')
        print(f"Naciśnięto: {key_name}")
    
    press_times[key_name] = current_time
    
    keydown_keydown_time = None
    if last_keydown_time:
        keydown_keydown_time = current_time - last_keydown_time
    
    data.append({
        'key': key_name,
        'press_time': current_time - start_time,
        'hold_time': None,
        'keydown_keydown_time': keydown_keydown_time,
        'keyup_keydown_time': None
    })
    
    last_keydown_time = current_time

def on_release(key):
    global data, last_keyup_time, press_times
    
    current_time = time.time()
    
    if hasattr(key, 'char') and key.char:
        key_name = key.char
    else:
        key_name = str(key).replace('Key.', '')
   
    if key_name in press_times:
        hold_time = current_time - press_times[key_name]
     
        for record in reversed(data):
            if record['key'] == key_name and record['hold_time'] is None:
                record['hold_time'] = hold_time
                
                if last_keyup_time:
                    record['keyup_keydown_time'] = press_times[key_name] - last_keyup_time
                break
        
        del press_times[key_name]
    
    last_keyup_time = current_time
    
    if key == keyboard.Key.esc:
        return False

def save_data():
    complete_data = [record for record in data if record['hold_time'] is not None]
    
    if not complete_data:
        print("Brak danych do zapisania")
        return
    
    for record in complete_data:
        record['press_time'] = f"{record['press_time']:.3f} sec"
        record['hold_time'] = f"{record['hold_time']:.3f} sec"
        
        if record['keydown_keydown_time']:
            record['keydown_keydown_time'] = f"{record['keydown_keydown_time']:.3f} sec"
        else:
            record['keydown_keydown_time'] = "--- (pierwszy klawisz)"
            
        if record['keyup_keydown_time']:
            record['keyup_keydown_time'] = f"{record['keyup_keydown_time']:.3f} sec"
        else:
            record['keyup_keydown_time'] = "--- (pierwszy klawisz)"
    
    df = pd.DataFrame(complete_data)
    df.columns = ['Klawisz', 'Czas naciśnięcia', 'Czas trzymania', 
                  'Czas między naciśnięciami', 'Czas od zwolnienia do naciśnięcia']
    
    try:
        with pd.ExcelWriter('keystroke_data.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Dane', index=False)
            
            ws = writer.sheets['Dane']
            
            ws.column_dimensions['A'].width = 12
            ws.column_dimensions['B'].width = 18
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 25
            ws.column_dimensions['E'].width = 30
        
        print(f"Zapisano {len(complete_data)} naciśnięć do pliku keystroke_data.xlsx")
        
    except Exception as e:
        print(f"Błąd zapisu: {e}")

if __name__ == "__main__":
    print("Nagrywanie klawiszy - naciśnij ESC aby zakończyć")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    save_data()