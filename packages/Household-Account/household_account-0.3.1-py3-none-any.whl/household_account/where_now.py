import typer
import pandas as pd

# 안좋은 소비 기준
bad_spending_money = 20000
bad_categories = ['택시비', '기타']

# 가계부 데이터 프레임 생성
columns = ["지출", "카테고리"]
data = []
df = pd.DataFrame(data, columns=columns)


def hha(expenses:int, category:str):
    if expenses <= bad_spending_money:
       print(f"{category}에 {expenses}를 썼습니다. 이는 효율적인 소비입니다.")
    elif category in bad_categories:
       print(f"{category}에 {expenses}원을 썼습니다. 이는 비효율적인 소비입니다.")
    else:
       print(f"그럴만할 일이 있었겠지..딱한것..")
    
    edf = pd.DataFrame([[expenses, category]], columns=["지출", "카테고리"])
    return edf

#분석
def sum_budget(df):
    total_expenses = df["지출"].sum()
    return f"총 지출 : {total_expenses}원"
 
# 메인작업함수
def print_hha(expenses: int, category: str):
    global df
    new_entry = hha(expenses, category)  # 새로운 데이터 생성
    df = pd.concat([df, new_entry], ignore_index=True)  # 기존 df에 추가    
    r = sum_budget(df)
    print(r)

def entry_point():
    typer.run(print_hha)

