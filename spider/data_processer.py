import pandas as pd

def pre_process(df):
    # 去除N类 + 去重，你也可自行修改
    return df[df["Class"] != 'N'].drop_duplicates()

if __name__ == '__main__':
    csv_url = 'data/' + '20220101-20240320.csv' # 后半部分是你要处理的文件名
    df = pd.read_csv(csv_url)
    df = pre_process(df)

    df.to_csv('output.csv', mode='w', index=False) # 注意这个操作会覆盖之前的output.csv文件，注意保存

