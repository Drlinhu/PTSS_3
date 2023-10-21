import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel('sample/Book1.xlsx')
    data = []
    for i in range(df.shape[0]):
        ref = df.loc[i, 'CX Procedure']
        amtoss = df.loc[i, 'AMTOSS'].split('\n')
        for x in amtoss:
            data.append([ref, x, 'AMM'])
    print(len(data))
    for x in data:
        print(x)
    df = pd.DataFrame(data)
    df.to_excel('proce.xlsx',  index=False)
