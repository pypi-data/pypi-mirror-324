# Bukmacherska Lib – Biblioteka do Analizy Zakładów Bukmacherskich

## 📌 Opis

**Bukmacherska Lib** to kompleksowa biblioteka do analizy wyników meczów piłkarskich z wykorzystaniem zaawansowanych narzędzi matematycznych, statystycznych i algorytmów uczenia maszynowego. Dzięki tej bibliotece możesz przewidywać wyniki meczów, analizować statystyki drużyn, a także generować wykresy i wizualizacje do dalszej analizy.

Biblioteka zawiera cztery główne modele:
- **Model 12** – Zaawansowane modele machine learning (12 algorytmów)
- **Model 24** – 24 modele machine learning do predykcji wyników meczów
- **Model 360** – Analiza matematyczna i statystyczna z narzędziami predykcyjnymi
- **Bukmacherska** – Podstawowe narzędzia do obliczania stawek, analizy wyników i rysowania wykresów

## 🔹 Kluczowe funkcjonalności

- **Zaawansowana analiza statystyczna**: Obliczanie średnich, wariancji, funkcji gamma, beta, Poissona, i innych.
- **Modele predykcyjne**: Regresja logistyczna, SVM, XGBoost, LSTM, random forest, itp.
- **Analiza drużyn i meczów**: Analiza skuteczności obrony, przewidywanie goli, analiza agresji i kondycji drużyn.
- **Wizualizacje**: Generowanie wykresów liniowych, słupkowych, 3D i innych wizualizacji.
- **Podstawowe narzędzia bukmacherskie**: Obliczanie stawek, tabele bramek, rysowanie wykresów dla różnych danych meczowych.

## 🛠 Instalacja

Aby zainstalować bibliotekę, uruchom poniższe polecenie:

```bash
pip install bukmacherska_lib

pip install -r requirements.txt

from bukmacherska_lib.models.model_360 import mean, poisson_pmf, normal_pdf

# Przykładowe dane
data =[[1, 2],[3, 4, 5]]

# Oblicz średnią
print("Średnia:", mean(data))

# Oblicz prawdopodobieństwo Poissona
print("Prawdopodobieństwo Poissona:", poisson_pmf(2, 3.5))

# Oblicz prawdopodobieństwo z rozkładu normalnego
print("Prawdopodobieństwo z rozkładu normalnego:", normal_pdf(2, 0, 1))

from bukmacherska_lib.models.model_24 import train_models, predict_with_models, plot_results

import numpy as np

# Przykładowe dane
X_train = np.array([[1, 2], [2, 3], [3, 4]])
y_train = np.array([0, 1, 1])
X_test = np.array([[2, 3], [3, 4]])

# Trening modeli
models = train_models(X_train, y_train)

# Predykcja
predictions = predict_with_models(models, X_test)
print("Predykcje:", predictions)

# Wizualizacja
plot_results(predictions, x_min=1.5, x_max=1.2, y_min=1.0, y_max=0.9)

from bukmacherska_lib.models.model_12 import train_models, predict_with_models, plot_results

import numpy as np

# Przykładowe dane
X_train = np.array([[1, 2], [2, 3], [3, 4]])
y_train = np.array([0, 1, 1])
X_test = np.array([[2, 3], [3, 4]])

# Trening modeli
models = train_models(X_train, y_train)

# Predykcja
predictions = predict_with_models(models, X_test)
print("Predykcje:", predictions)

# Wizualizacja
plot_results(predictions, x_min=1.5, x_max=1.2, y_min=1.0, y_max=0.9)

from bukmacherska_lib.bukmacherska import oblicz_stawki, rysuj_wykresy_stawki, tabela_bramek

# Dane wejściowe
stawka_poczatkowa = 100
gole_zdobyte_druzyna1 = 1.8
gole_stracone_druzyna1 = 1.2
gole_zdobyte_druzyna2 = 1.5
gole_stracone_druzyna2 = 1.7
czas = [0, 15, 30, 45, 60, 75, 90]

# Oblicz stawki
stawki_druzyna1, stawki_druzyna2 = oblicz_stawki(
    stawka_poczatkowa, 
    gole_zdobyte_druzyna1, gole_stracone_druzyna1, 
    gole_zdobyte_druzyna2, gole_stracone_druzyna2, 
    czas
)

# Rysuj wykresy
rysuj_wykresy_stawki(stawki_druzyna1, stawki_druzyna2, czas)

# Tabela bramek
gamma_values = [1, 2, 3, 4, 5]
tabela = tabela_bramek(gamma_values)
print("Tabela bramek:", tabela)
