import camelot
import sys
import pandas as pd
from zipfile import ZipFile

inFile = sys.argv[1]
outFile = sys.argv[2]
#print(inFile.split(".")[-1])
try:
    if inFile.split(".")[-1] == "pdf":
        tables = camelot.read_pdf(inFile, pages='2,3')
        df1 = pd.DataFrame(data=tables[0].df)
        df2 = pd.DataFrame(data=tables[1].df)
        df3 = pd.concat([df1, df2[2:]], axis=0, ignore_index=True)
        df3.to_csv(outFile)
    elif inFile.split(".")[-1] == "zip":
        pass
    else:
        raise Exception('zły typ pliku')
except Exception as err:
    print('Błąd: ', err)
