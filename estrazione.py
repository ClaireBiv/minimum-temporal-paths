import csv

diamRow, distRow = [], []
diamMatrix, distMatrix = [], []
for n in range(100,1001,100):
    for i in range(3,11):
        with open(f"EAP_ErdosRenyi/output{n}_{i}.txt", "r") as file:
            for line in file:
                if line.startswith("Diametro medio ="):
                    valore = line.split("=")[1].strip()
                    diamRow.append(round(float(valore),2))
                if line.startswith("Distanza media ="):
                    valore = line.split("=")[1].strip()
                    distRow.append(round(float(valore),2))
    diamMatrix.append([n] + diamRow)
    distMatrix.append([n] + distRow)
    diamRow, distRow = [], []

with open("diam_eap_er.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(['n/p'] + [str(i) for i in range(3,11)])
        for row in diamMatrix:
             writer.writerow(row)

with open("dist_eap_er.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(['n/p'] + [str(i) for i in range(3,11)])
        for row in distMatrix:
             writer.writerow(row)