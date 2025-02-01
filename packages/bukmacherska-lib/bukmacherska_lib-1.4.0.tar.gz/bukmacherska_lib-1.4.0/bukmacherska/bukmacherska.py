import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma as gamma_function

def oblicz_stawki(stawka_poczatkowa, gole_zdobyte_druzyna1, gole_stracone_druzyna1, 
                  gole_zdobyte_druzyna2, gole_stracone_druzyna2, czas):
    """
    Oblicza zmiany stawek na podstawie średniej zdobytych i straconych goli drużyn.
    """
    stawka_druzyna1 = [stawka_poczatkowa]
    stawka_druzyna2 = [stawka_poczatkowa]

    # Oblicz prawdopodobieństwo wygranej dla obu drużyn
    prawdopodobienstwo_druzyna1 = gole_zdobyte_druzyna1 / (gole_zdobyte_druzyna1 + gole_stracone_druzyna2)
    prawdopodobienstwo_druzyna2 = gole_zdobyte_druzyna2 / (gole_zdobyte_druzyna2 + gole_stracone_druzyna1)

    # Przekształć prawdopodobieństwo na proporcje zmian stawki
    proporcja1 = prawdopodobienstwo_druzyna1 / (prawdopodobienstwo_druzyna1 + prawdopodobienstwo_druzyna2)
    proporcja2 = 1 - proporcja1

    for t in czas[1:]:
        stawka_druzyna1.append(stawka_poczatkowa * proporcja1)
        stawka_druzyna2.append(stawka_poczatkowa * proporcja2)

    return stawka_druzyna1, stawka_druzyna2

def rysuj_wykresy_stawki(stawki_druzyna1, stawki_druzyna2, czas):
    """
    Rysuje wykresy: liniowy, słupkowy i obszarowy 3D dla stawek obu drużyn.
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Wykres Liniowy
    axs[0, 0].plot(czas, stawki_druzyna1, label='Drużyna 1')
    axs[0, 0].plot(czas, stawki_druzyna2, label='Drużyna 2')
    axs[0, 0].set_title('Wykres Liniowy - Zmiana Stawek')
    axs[0, 0].set_xlabel('Czas')
    axs[0, 0].set_ylabel('Stawki')
    axs[0, 0].legend()

    # Wykres Słupkowy
    axs[0, 1].bar(['Drużyna 1', 'Drużyna 2'], [stawki_druzyna1[-1], stawki_druzyna2[-1]], color=['blue', 'orange'])
    axs[0, 1].set_title('Wykres Słupkowy - Końcowe Stawki')

    # Wykres Obszarowy 3D
    ax = fig.add_subplot(223, projection='3d')
    X, Y = np.meshgrid(czas, [1, 2])
    Z = np.array([stawki_druzyna1, stawki_druzyna2])
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title('Wykres 3D - Zmiany Stawek')

    plt.tight_layout()
    plt.show()

def tabela_bramek(gamma_values):
    """
    Generuje tabelę bramek na podstawie wartości gamma.
    """
    tabela = {}
    for gamma in gamma_values:
        tabela[gamma] = gamma_function(gamma)
    return tabela
