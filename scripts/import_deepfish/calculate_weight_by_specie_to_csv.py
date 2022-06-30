def calcula_peso(specie, talla):
    if specie in coef_a:
        # W = a * L ^ b
        a = coef_a[specie] * talla ** coef_b[specie]
        return a
    else:
        return "Undefined"


coef_a = {
    "Dentex dentex": 0.018,
    "Diplodus annularis": 0.0217,
    "Diplodus sargus": 0.0175,
    "Mullus surmuletus": 0.0104,
    "Mullus barbatus": 0.0077,
    "Merluccius merluccius": 0.0046,
    "Pagellus acarne": 0.0069,
    "Pagellus erythrinus": 0.0096,
    "Pagrus pagrus": 0.0179,
    "Sarda sarda": 0.001,
    "Scorpaena porcus": 0.061,
    "Symphodus tinca": 0.0212,
    "Sphyraena sphyraena": 0.0066,
    "Spicara maena": 0.013,
    "Serranus scriba": 0.012,
    "Seriola dumerili": 0.019,
    "Sparus aurata": 0.0109,
    "Sepia officinalis": 0.1884,
}

coef_b = {
    "Dentex dentex": 3.029,
    "Diplodus annularis": 2.84,
    "Diplodus sargus": 2.921,
    "Mullus surmuletus": 3.0617,
    "Mullus barbatus": 3.1095,
    "Merluccius merluccius": 3.1191,
    "Pagellus acarne": 3.221,
    "Pagellus erythrinus": 3.118,
    "Pagrus pagrus": 2.95,
    "Sarda sarda": 3.593,
    "Scorpaena porcus": 2.652,
    "Symphodus tinca": 2.8351,
    "Sphyraena sphyraena": 2.89,
    "Spicara maena": 2.988,
    "Serranus scriba": 2.963,
    "Seriola dumerili": 2.8726,
    "Sparus aurata": 3.091,
    "Sepia officinalis": 2.81,
}

data = []
with open("./Medidas_entrada_con_h.csv", "r") as f:
    for line in f:
        data.append(line)

first = True
with open("./Medidas_entrada_con_h_con_peso.csv", "w") as f:
    for line in data:
        if first:
            first = False
        else:
            splited_line = line.split(",")
            try:
                line = (
                    line[: len(line) - 1]
                    + ","
                    + str(
                        calcula_peso(
                            splited_line[8][: len(splited_line[8]) - 1],
                            float(
                                splited_line[2][1::]
                                + "."
                                + splited_line[3][: len(splited_line[3]) - 1]
                            ),
                        )
                    )
                    + "\n"
                )
                f.write(line)
            except Exception:
                continue
