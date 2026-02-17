import time

#Dictionary koordinat untuk warna
ColorCoordinate = {}
def MakeColorDict(c):
    n_keys = len(ColorCoordinate)
    ColorCoordinate.update({c.lower(): n_keys})

#Baca posisi warna
def ReadWarna(line, KoorWarna, row):
    j = 0
    for c in line:
        if c.lower() not in ColorCoordinate:
            MakeColorDict(c)
        index = ColorCoordinate[c.lower()]
        KoorWarna[index].append((row, j))
        j += 1

#Read test.txt and paste masing-masing coord warna
def OpenCaseFile(filename):
    with open(filename, "r") as f:
        first_line = f.readline().strip()
        KoorWarna = [[] for _ in range(len(first_line))]
        ReadWarna(first_line, KoorWarna, 0)
        row = 1
        for line in f:
            line = line.strip()
            ReadWarna(line, KoorWarna, row)
            row += 1
    f.close()
    return KoorWarna

def check_Row_and_Col(RowWarna, ColWarna):
    Rows = []
    Cols = []
    for Row in RowWarna:
        if Row in Rows:
            return False
        else:
            Rows.append(Row)
    for Col in ColWarna:
        if Col in Cols:
            return False
        else:
            Cols.append(Col)
    return True

def check_Diagonal(Result):
    DiagKoords = []
    for Koord in Result:
        x = Koord[0]
        y = Koord[1]
        DiagKoords.append((x+1, y+1))
        DiagKoords.append((x+1, y-1))
        DiagKoords.append((x-1, y+1))
        DiagKoords.append((x-1, y-1))
    for Koord in DiagKoords:
        if Koord in Result:
            return False
    return True
                    
def check(RowWarna, ColWarna, KoordWarna, Result):
    global Iteration
    Final_Result = []
    #Check sisa 2 warna atau nggak
    if (len(KoordWarna) < 2):
        last_color = True
    else:
        last_color = False
    for Koord in KoordWarna[0]:
        x = Koord[0]
        y = Koord[1]
        RowWarna.append(x)
        ColWarna.append(y)
        if (last_color):
            Iteration += 1
            Result.append((x, y))
            if (Iteration % 500) == 0:
                print(Result)
            if (check_Row_and_Col(RowWarna, ColWarna)):
                if (check_Diagonal(Result)):
                    Final_Result.append(Result.copy())
        else:
            Result.append((x, y))
            check_result = check(RowWarna, ColWarna, KoordWarna[1:], Result)
            if check_result != []:
                Final_Result.extend(check_result)
        RowWarna.pop()
        ColWarna.pop()
        Result.pop()
        
    return Final_Result

def check_Optimized(RowWarna, ColWarna, KoordWarna, Result):
    global Iteration
    Final_Result = []
    #Check sisa 2 warna atau nggak
    if (len(KoordWarna) < 2):
        last_color = True
    else:
        last_color = False
    for Koord in KoordWarna[0]:
        x = Koord[0]
        y = Koord[1]
        if (last_color):
            Iteration += 1
            Result.append((x, y))
            RowWarna.append(x)
            ColWarna.append(y)
            if (Iteration % 500) == 0:
                print(Result)
            if (check_Row_and_Col(RowWarna, ColWarna)):
                if (check_Diagonal(Result)):
                    Final_Result.append(Result.copy())
            Result.pop()
            RowWarna.pop()
            ColWarna.pop()
        else:
            if (x in RowWarna) or (y in ColWarna):
                continue
            else:
                RowWarna.append(x)
                ColWarna.append(y)
                Result.append((x, y))
                check_result = check_Optimized(RowWarna, ColWarna, KoordWarna[1:], Result)
                if check_result != []:
                    Final_Result.extend(check_result)
                RowWarna.pop()
                ColWarna.pop()
                Result.pop()  
    return Final_Result

def getSolvedLines(Col_Queen, filename):
    with open(filename, "r") as f:
        row = 0
        baris_solve = []
        for line in f:
            string_baris = ""
            line = line.strip()
            col = 0
            for c in line:
                if col == Col_Queen[row]:
                    string_baris += "#"
                else:
                    string_baris += c
                col += 1
            baris_solve.append(string_baris)
            row += 1
    f.close()
    return baris_solve


#Print tiap baris solusi. Koordinat Queen diganti ke array sebesar n, dengan nilai x = indeks col_queen
def printResult(Final_Result, filename):
    num = 1
    all_solution = []
    for Result in Final_Result:
        Col_Queen = [0] * len(Result)
        for Koord in Result:
            x = Koord[0]
            y = Koord[1]
            Col_Queen[x] = y
        print(f"Solusi ke - {num} : \n")
        full_solve = getSolvedLines(Col_Queen, filename)
        for baris in full_solve:
            print(baris)
        all_solution.append(full_solve)
        num += 1
    save = input("Apakah ingin menyimpan solusi? (y/n) : \n")
    if save == "y":
        with open(f"./test/solusi_{nama_file}.txt", "w") as f:
            num = 1
            for solution in all_solution:
                f.write(f"Solusi ke - {num} : \n")
                for baris in solution:
                    f.write(baris + "\n")
                num += 1
        f.close()
        


def BruteForce_Warna(Koorwarna):
    optimized = input(f"Optimized? (y/n): \n")
    RowWarna = []
    ColWarna = []
    Result = []
    if optimized == "y":
        start = time.perf_counter()
        Result = check_Optimized(RowWarna, ColWarna, Koorwarna, Result)
        end = time.perf_counter()
    else:
        start = time.perf_counter()
        Result = check(RowWarna, ColWarna, Koorwarna, Result)
        end = time.perf_counter()
    runtime = end - start
    return Result, runtime


Iteration = 0
nama_file = input(f"Masukkan nama file test case : \n")
filename = f"./test/{nama_file}.txt"
# print(OpenCaseFile(filename))
KoorWarna = OpenCaseFile(filename)
if KoorWarna == []:
    print(f"File tidak valid")
Result, Runtime = BruteForce_Warna(KoorWarna)
if Result == []:
    print(f"Tidak ada solusi yang ditemukan")
else:
    print(f"Solusi ditemukan!\n")
    print(f"Jumlah solusi yang ditemukan : {len(Result)}\n")
printResult(Result, filename)
print(f"Jumlah iterasi/kasus : {Iteration}")
print(f"Runtime : {Runtime:.4f} s")

