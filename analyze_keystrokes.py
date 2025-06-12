import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def load_data(filename):
    try:
        if filename.endswith('.xlsx'):
            data = pd.read_excel(filename)
        else:
            data = pd.read_csv(filename)
        print(f"Wczytano {len(data)} naciśnięć z pliku {filename}")
        return data
    except:
        print(f"Nie można otworzyć {filename}")
        return None

def clean_data(data):
    time_cols = ['Czas naciśnięcia', 'Czas trzymania', 'Czas między naciśnięciami', 'Czas od zwolnienia do naciśnięcia']
    
    for col in time_cols:
        if col in data.columns:
            data[col] = data[col].astype(str).str.replace(' sec', '').str.replace('--- (pierwszy klawisz)', '')
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    return data

def show_stats(data):
    print("\nPodstawowe informacje:")
    print(f"Liczba naciśnięć: {len(data)}")
    print(f"Różnych klawiszy: {data['Klawisz'].nunique()}")
    
    key_counts = data['Klawisz'].value_counts()
    print("\nNaciśnięte klawisze:")
    for key, count in key_counts.items():
        print(f"  {key}: {count} razy")
    
    if 'Czas trzymania' in data.columns:
        hold_times = data['Czas trzymania'].dropna()
        if len(hold_times) > 0:
            print(f"\nŚredni czas trzymania: {hold_times.mean():.3f} sec")
            print(f"Najkrótszy: {hold_times.min():.3f} sec")
            print(f"Najdłuższy: {hold_times.max():.3f} sec")

def make_charts(data):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Analiza pisania na klawiaturze')
    
    if 'Czas trzymania' in data.columns:
        hold_data = data['Czas trzymania'].dropna()
        if len(hold_data) > 0:
            axes[0, 0].hist(hold_data, bins=20, color='blue', alpha=0.7)
            axes[0, 0].set_title('Czas trzymania klawiszy')
            axes[0, 0].set_xlabel('Sekundy')
    
    if 'Czas między naciśnięciami' in data.columns:
        between_data = data['Czas między naciśnięciami'].dropna()
        if len(between_data) > 0:
            axes[0, 1].hist(between_data, bins=20, color='green', alpha=0.7)
            axes[0, 1].set_title('Czas między naciśnięciami')
            axes[0, 1].set_xlabel('Sekundy')
    
    key_counts = data['Klawisz'].value_counts().head(10)
    if len(key_counts) > 0:
        axes[1, 0].bar(range(len(key_counts)), key_counts.values, color='red', alpha=0.7)
        axes[1, 0].set_title('Najczęściej używane klawisze')
        axes[1, 0].set_xticks(range(len(key_counts)))
        axes[1, 0].set_xticklabels(key_counts.index, rotation=45)
    
    if len(data) > 1:
        axes[1, 1].plot(range(len(data)), data.index, 'o-', alpha=0.6)
        axes[1, 1].set_title('Kolejność naciśnięć')
        axes[1, 1].set_xlabel('Numer naciśnięcia')
    
    plt.tight_layout()
    plt.show()

def test_recognition(data):
    print("\nTest rozpoznawania użytkownika:")
    
    time_cols = ['Czas trzymania', 'Czas między naciśnięciami', 'Czas od zwolnienia do naciśnięcia']
    available_cols = [col for col in time_cols if col in data.columns]
    
    if len(available_cols) == 0:
        print("Brak danych czasowych do analizy")
        return
    
    clean_data = data.dropna(subset=available_cols)
    
    if len(clean_data) < 5:
        print("Za mało danych do testu")
        return
    
    clean_data = clean_data.copy()
    clean_data['user'] = 1
    
    X = clean_data[available_cols]
    y = clean_data['user']
    
    if len(X) >= 4:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"Dokładność: {accuracy:.1%}")
        print(f"Użyto {len(X_train)} próbek do nauki")

def save_report(data):
    try:
        with pd.ExcelWriter('raport.xlsx', engine='openpyxl') as writer:
            stats = data.describe().round(3)
            stats.to_excel(writer, sheet_name='Statystyki')
            
            key_stats = data.groupby('Klawisz').size().reset_index(name='Liczba_naciśnięć')
            key_stats.to_excel(writer, sheet_name='Klawisze', index=False)
            
            data.to_excel(writer, sheet_name='Wszystkie_dane', index=False)
        
        print("\nZapisano raport do pliku raport.xlsx")
    except:
        print("\nBłąd podczas zapisywania raportu")

if __name__ == "__main__":
    print("Analiza danych z klawiatury")
    
    data = load_data('keystroke_data.xlsx')
    
    if data is None:
        data = load_data('keystroke_data.csv')
    
    if data is not None:
        data = clean_data(data)
        show_stats(data)
        make_charts(data)
        test_recognition(data)
        save_report(data)
        print("\nAnaliza zakończona")
    else:
        print("Nie znaleziono pliku z danymi")
        