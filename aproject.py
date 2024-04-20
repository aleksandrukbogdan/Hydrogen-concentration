import math
from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Рассчет характеристик центробежного компрессора(ЦК) на смешанном хладагенте.")
root.geometry("500x400")
lbl1 = Label(root, text="Введите давление на входе P1, МПа")
entry1 = ttk.Entry()
lbl1.pack(anchor=NW, padx=6, pady=3)
entry1.pack(anchor=NW, padx=6, pady=6)

lbl2 = Label(root, text="Введите давление на выходе P2, МПа")
entry2 = ttk.Entry()
lbl2.pack(anchor=NW, padx=6, pady=9)
entry2.pack(anchor=NW, padx=6, pady=12)

lbl3 = Label(root, text="Введите КПД компрессора")
entry3 = ttk.Entry()
lbl3.pack(anchor=NW, padx=6, pady=15)
entry3.pack(anchor=NW, padx=6, pady=18)


# btn = ttk.Button(text="Click", command=show_message)
# btn.pack(anchor=NW, padx=6, pady=6)


class Window(Tk):
    def __init__(self, people):
        super().__init__()

        self.title("Рассчет характеристик центробежного компрессора(ЦК) на смешанном хладагенте.")
        self.geometry("800x600")

        # определяем данные для отображения
        self.people = people

        # определяем столбцы
        self.columns = ("param", "value1", "value2", "value3", "value4", "value5", "value6")

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(fill=BOTH, expand=1)

        # определяем заголовки с выпавниваем по левому краю
        self.tree.heading("param", text="Угол выхода лопаток", anchor=W)
        self.tree.heading("value1", text="22,5\u00b0", anchor=W)
        self.tree.heading("value2", text="32\u00b0", anchor=W)
        self.tree.heading("value3", text="48\u00b0", anchor=W)
        self.tree.heading("value4", text="60\u00b0", anchor=W)
        self.tree.heading("value5", text="70\u00b0", anchor=W)
        self.tree.heading("value6", text="90\u00b0", anchor=W)

        # настраиваем столбцы
        self.tree.column("#1", stretch=NO, width=200)
        self.tree.column("#2", stretch=NO, width=100)
        self.tree.column("#3", stretch=NO, width=100)
        self.tree.column("#4", stretch=NO, width=100)
        self.tree.column("#5", stretch=NO, width=100)
        self.tree.column("#6", stretch=NO, width=100)
        self.tree.column("#7", stretch=NO, width=100)

        # добавляем данные
        for person in self.people:
            self.tree.insert("", END, values=person)


def click():
    global P1
    global P2
    global nu
    P1 = float(entry1.get())
    P2 = float(entry2.get())
    nu = float(entry3.get())
    R = 506.9
    P1 *= 10 ** 6
    T1 = 288.15
    P2 *= 10 ** 6
    Q = 405

    G = P1 * Q / (R * 0.88 * 288.15 * 60)
    Pi = P2 / P1

    b = [22.5, 32, 48, 60, 70, 90]
    phi_r = [0.22, 0.2917, 0.34, 0.36, 0.36, 0.38]
    Z2 = [14, 18, 24, 26, 26, 28]
    bs = [1.05, 1.04, 1.035, 1.03, 1.025, 1.02]
    Kz = [0 for j in range(len(b))]
    j = 0
    phi_u = [0 for j in range(len(b))]
    j = 0
    d_t = [[0 for j in range(len(b))] for k in range(3)]
    j = 0
    U = [[0 for j in range(len(b))] for k in range(3)]
    j = 0
    D = [[0 for j in range(len(b))] for k in range(3)]
    D_u = [[0 for j in range(len(b))] for k in range(3)]
    kv = [[0 for j in range(len(b))] for k in range(3)]
    n = [[0 for j in range(len(b))] for k in range(3)]
    b_u = [[0 for j in range(len(b))] for k in range(3)]
    t_u = [[0 for j in range(len(b))] for k in range(3)]
    om = [[0 for j in range(len(b))] for k in range(3)]

    tau = 0.95
    b2 = 0.07
    H = 58.02
    k0 = 1.31

    for i in range(6):
        Kz[i] = 1 - math.pi / Z2[i] * math.sin(math.radians(b[i]))
        phi_u[i] = Kz[i] - phi_r[i] / math.tan(math.radians(b[i]))
        for x in range(3):
            U[x][i] = round(math.sqrt((H * 10 ** 3) / ((x + 1) * phi_u[i] * bs[i])), 2)
            d_t[x][i] = round((k0 - 1) / k0 * bs[i] / (R * Kz[i]) * phi_u[i] * U[x][i] ** 2, 2)
            om[x][i] = round(1 - ((phi_r[i] ** 2 + phi_u[i] ** 2) / (2 * phi_u[i] * bs[i])), 2)
            kv[x][i] = round((1 + om[x][i] * d_t[x][i] / T1) ** (k0 / (k0 - 1) * nu - 1), 2)
            D[x][i] = round(math.sqrt(Q / (60 * math.pi * tau * phi_r[i] * U[x][i] * b2 * kv[x][i])), 3)
            n[x][i] = round(60 * U[x][i] / math.pi / D[x][i], 0)
            D_u[x][i] = round(60 * U[x][i] / math.pi / n[x][i], 2)
            t_u[x][i] = round(1 - 0.5 * Z2[i] * 9 * 10 ** (-3) / (math.pi * D_u[x][i] * math.sin(math.radians(b[i]))),
                              3)
            b_u[x][i] = round(Q / (60 * math.pi * t_u[x][i] * phi_r[i] * U[x][i] * D_u[x][i] ** 2 * kv[x][i]), 3)


    k0_2 = 1.292

    # для угла = 32 х = 2
    delta_t = (k0_2 - 1) / k0_2 * (bs[1]) / R / Kz[1] * phi_u[1] * U[1][1] ** 2
    Tn = T1 + delta_t
    kv2 = (1 + om[1][1] * delta_t / Tn) ** (k0_2 / (k0_2 - 1) * nu - 1)
    # kv1 = (1 + om[0][1] * delta_t / T1) ** (k0 / (k0 - 1) * nu - 1)
    b_2 = b_u[1][1] * kv[1][1] / kv2

    n_ob = n[1][1]
    kd = 0.025
    N = G * H
    n_kr1 = n_ob / 1.5
    n_kr2 = 3.6 * n_kr1
    d = kd * (2 + 2.3) * D_u[1][1] * math.sqrt(n_kr1 / 1000)

    phi_r.insert(0, "Коэффициент расхода")
    Z2.insert(0, "Число лопаток колеса")
    bs.insert(0, 'Поправка на потери дискового трения')
    U_1 = U[0]
    U_1.insert(0, "Окружная скорость, м/с, Х = 1")
    U_2 = U[1]
    U_2.insert(0, "Окружная скорость, м/с, Х = 2")
    U_3 = U[2]
    U_3.insert(0, "Окружная скорость, м/с, Х = 3")
    om_1 = om[0]
    om_1.insert(0, "Коэффициент реакции")
    d_t_1 = d_t[0]
    d_t_1.insert(0, "Повышение температуры в ступени, K, X = 1")
    d_t_2 = d_t[1]
    d_t_2.insert(0, "Повышение температуры в ступени, K, X = 2")
    d_t_3 = d_t[2]
    d_t_3.insert(0, "Повышение температуры в ступени, K, X = 3")
    kv_1 = kv[0]
    kv_1.insert(0, "Коэффициент изменения удельного объема, X = 1")
    kv_2 = kv[1]
    kv_2.insert(0, "Коэффициент изменения удельного объема, X = 2")
    kv_3 = kv[2]
    kv_3.insert(0, "Коэффициент изменения удельного объема, X = 3")
    D_1 = D[0]
    D_1.insert(0, "Диаметр РК, м, X = 1")
    D_2 = D[1]
    D_2.insert(0, "Диаметр РК, м, X = 2")
    D_3 = D[2]
    D_3.insert(0, "Диаметр РК, м, X = 3")
    n_1 = n[0]
    n_1.insert(0, "Част. вращ. ротора, об/мин , X = 1")
    n_2 = n[1]
    n_2.insert(0, "Част. вращ. ротора, об/мин , X = 2")
    n_3 = n[2]
    n_3.insert(0, "Част. вращ. ротора, об/мин , X = 3")
    D_u_1 = D_u[0]
    D_u_1.insert(0, "Диаметр РК, уточ., м, X = 1")
    D_u_2 = D_u[1]
    D_u_2.insert(0, "Диаметр РК, уточ., м, X = 2")
    D_u_3 = D_u[2]
    D_u_3.insert(0, "Диаметр РК, уточ., м, X = 3")
    tau_1 = t_u[0]
    tau_1.insert(0, "Относительное загромождение, X = 1")
    tau_2 = t_u[1]
    tau_2.insert(0, "Относительное загромождение, X = 2")
    tau_3 = t_u[2]
    tau_3.insert(0, "Относительное загромождение, X = 3")
    b_u_1 = b_u[0]
    b_u_1.insert(0, "Относит. ширина, X = 1")
    b_u_2 = b_u[1]
    b_u_2.insert(0, "Относит. ширина, X = 2")
    b_u_3 = b_u[2]
    b_u_3.insert(0, "Относит. ширина, X = 3")
    data = [tuple(phi_r),
            tuple(Z2),
            tuple(bs),
            tuple(U_1),
            tuple(U_2),
            tuple(U_3),
            tuple(om_1),
            tuple(d_t_1),
            tuple(d_t_2),
            tuple(d_t_3),
            tuple(kv_1),
            tuple(kv_2),
            tuple(kv_3),
            tuple(D_1),
            tuple(D_2),
            tuple(D_3),
            tuple(n_1),
            tuple(n_2),
            tuple(n_3),
            tuple(D_u_1),
            tuple(D_u_2),
            tuple(D_u_3),
            tuple(tau_1),
            tuple(tau_2),
            tuple(tau_3),
            tuple(b_u_1),
            tuple(b_u_2),
            tuple(b_u_3),
            ]

    w = Window(data)


open_button = ttk.Button(root, text="Рассчитать", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()
