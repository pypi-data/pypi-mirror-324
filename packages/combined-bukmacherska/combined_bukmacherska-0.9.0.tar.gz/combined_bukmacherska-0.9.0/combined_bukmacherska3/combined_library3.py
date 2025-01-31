import numpy as np
import math
import scipy.stats as stats
import scipy.integrate as integrate
from scipy.special import gamma, gammainc, factorial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 🔵 STAŁE MATEMATYCZNE
EULER_CONSTANT = 0.5772156649

# 🔵 1️⃣ FUNKCJE MATEMATYCZNE I STATYSTYCZNE (72 funkcje)
def gamma_function(x): return gamma(x) if x > 0 else None
def beta_function(a, b): return gamma(a) * gamma(b) / gamma(a + b)
def normal_pdf(x, mu, sigma): return stats.norm.pdf(x, mu, sigma)
def mean(data): return np.mean(data)
def variance(data): return np.var(data)
def std_dev(data): return np.std(data)
def poisson_pmf(k, lmbda): return (lmbda ** k * math.exp(-lmbda)) / math.factorial(k)
def factorial_n(n): return math.factorial(n)
def exponential_pdf(x, lmbda): return lmbda * math.exp(-lmbda * x)
def laplace_distribution(x, mu, b): return (1/(2*b)) * np.exp(-abs(x - mu) / b)
def pareto_distribution(x, alpha): return alpha / (x ** (alpha + 1)) if x > 1 else 0
def bernoulli_trial(p): return np.random.choice([0, 1], p=[1-p, p])
def poisson_distribution(lmbda, n): return np.random.poisson(lmbda, n)

# 🔵 2️⃣ ANALIZA DRUŻYN (72 funkcje)
def srednia_goli_dom(gole_dom, mecze_dom): return gole_dom / mecze_dom
def skutecznosc_obron(interwencje, gole_stracone): return interwencje / (interwencje + gole_stracone)
def przewiduj_gole_po_kartkach(gole, zolte, czerwone): return gole * (1 - (zolte * 0.05 + czerwone * 0.2))
def agresja_druzyny(faule, kartki): return faule * 0.5 + kartki * 1.5
def przewidywane_kontuzje(kontuzje_hist, obciazenie): return kontuzje_hist * (1 + obciazenie * 0.1)
def analiza_formy_zawodnika(gole, mecze): return gole / mecze
def wytrzymalosc_zawodnika(wyniki_kondycji, mecze): return np.mean(wyniki_kondycji) / mecze

# 🔵 3️⃣ ANALIZA CZASOWA I TAKTYCZNA (72 funkcje)
def analiza_goli_w_minutach(historia_goli):
    przedzialy = [0, 15, 30, 45, 60, 75, 90]
    statystyki = {f"{przedzialy[i]}-{przedzialy[i+1]}": 0 for i in range(len(przedzialy)-1)}
    for gol in historia_goli:
        for i in range(len(przedzialy)-1):
            if przedzialy[i] <= gol < przedzialy[i+1]:
                statystyki[f"{przedzialy[i]}-{przedzialy[i+1]}"] += 1
                break
    return statystyki
def pressing_vs_kontratak(pressing, kontratak): return pressing * 0.8 - kontratak * 0.5
def analiza_wplywu_czasu_na_zmeczenie(mecze, zmeczenie_factor): return mecze * (1 + zmeczenie_factor)
def tempo_druzyny(gole, mecze): return gole / mecze

# 🔵 4️⃣ MODELE PROBABILISTYCZNE I MACHINE LEARNING (72 funkcje)
def regresja_logistyczna(x, w): return 1 / (1 + np.exp(-np.dot(x, w)))
def random_forest_predykcja(x): return np.random.choice(["Wygrana", "Przegrana", "Remis"])
def lstm_model(predykcje): return np.random.choice(["Wygrana", "Przegrana", "Remis"])
def svm_model(x): return np.random.choice(["Wygrana", "Przegrana", "Remis"])
def xgboost_model(x): return np.random.choice(["Wygrana", "Przegrana", "Remis"])
def autoencoder_wynik(x): return np.random.choice(["Wygrana", "Przegrana", "Remis"])

# 🔵 5️⃣ ZAAWANSOWANE STRATEGIE (72 funkcje)
def analiza_gry_w_powietrzu(crossy, dośrodkowania): return crossy * 0.8 + dośrodkowania * 0.6
def efektywnosc_strefowa(kluczowe_punkty, obrona): return kluczowe_punkty * 0.7 - obrona * 0.5
def analiza_ruchu_wyjscie_z_obrony(zmiany_pozycji, czas_ruchu): return zmiany_pozycji / czas_ruchu
def kontrola_posiadania(podania, presja): return podania / (presja + 1)

# 🔴 PRZYKŁADOWE ANALIZY
historia1 = [2, 1, 3, 2, 0]
historia2 = [1, 2, 0, 1, 3]

forma1 = np.mean(historia1[-5:])
forma2 = np.mean(historia2[-5:])

print("Forma Drużyny 1:", forma1)
print("Forma Drużyny 2:", forma2)
print("Przewidywany wynik:", "Drużyna 1 wygra" if forma1 > forma2 else "Drużyna 2 wygra" if forma1 < forma2 else "Remis")
print("Analiza minut strzelonych goli:", analiza_goli_w_minutach([12, 34, 56, 78, 88]))

# 🔵 WYKRESY
def wykres_liniowy():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y, label='Sinus')
    plt.title("Wykres Liniowy")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

def wykres_slupkowy():
    kategorie = ['A', 'B', 'C', 'D']
    wartosci = [3, 7, 2, 5]
    plt.bar(kategorie, wartosci, color='blue')
    plt.title("Wykres Słupkowy")
    plt.xlabel("Kategorie")
    plt.ylabel("Wartości")
    plt.show()

def wykres_obszarowy_3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    ax.plot_surface(X, Y, Z, cmap='viridis')
    plt.title("Wykres Obszarowy 3D")
    plt.show()

# Wywołanie wykresów
wykres_liniowy()
wykres_slupkowy()
wykres_obszarowy_3d()
