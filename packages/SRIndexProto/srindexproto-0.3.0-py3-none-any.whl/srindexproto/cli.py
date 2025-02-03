import typer
import pandas as pd

def print_intro():
    intro_text = """
###########################################################

(English)
Introduction to the Social Relationship Index:

People invest various forms of resources in others to maintain social relationships. There can be numerous perspectives and views on the resources invested, and they can differ from person to person.
In this Index, resources are broadly classified into three elements: Money, Time, and Emotion. When evaluating each element, Importance and Performance are measured and used for Index calculation.

Importance reflects the respondent's own values and is quantified through a 5-point scale scaling for each element.
Performance is measured for each case of the respondent's social relationship (relationship with each person). 
For each element, Money: give-and-take between each other, Time: meetings spent together, and Emotion: Contact exchanged with each other are measured by scaling on a 5-point scale.

Finally, the Index is calculated by considering Importance and Performance.

###########################################################


###########################################################

(한국어)
Social Relationship Index의 소개:

사람들은 사회적 관계를 유지하기 위해서 상대방에게 다양한 형태의 자원을 투자합니다.
투자되는 자원에 대해서는 사람마다 수많은 관점과 견해가 있고 서로 다를 수 있습니다.
이 Index에서는 자원을 크게 3가지 요소: Money, Time, Emotion으로 분류합니다.
그리고 각 요소를 평가함에 있어, Importance와 Performance 를 측정하고, 이를 Index 계산에 활용합니다.

Importance는 응답자 본인의 가치관을 반영하여 요소별로 5점 척도 scaling을 통해 정량화합니다.
Performance는 응답자의 사회적 관계의 각 case (각각의 사람과의 관계)에 대해서 측정합니다.
요소별로는 Money: 상호간의 give-and-take, Time: 서로가 함께한 meeting, Emotion: 서로 주고받은 Contact를 5점 척도로 scaling하여 측정합니다.

최종적으로 Index는 Importance와 Performance를 고려하여 산출됩니다.

###########################################################"""
    print(intro_text)
    
    importance_prompt = """
###########################################################

(English)
"On a scale of 1 to 5, please rate the importance of Money, Time, and Emotion invested in your social relationships, based on your personal values." 
(한국어)
"사회적 관계에 있어 투자되는 Money, Time, Emotion의 중요도를 당신의 가치관에 따라 1~5점으로 입력해주세요"

###########################################################
"""
    print(importance_prompt)

def get_importance_weights():
    while True:
        try:
            importance1 = float(input("Money importance (1-5): "))
            importance2 = float(input("Time importance (1-5): "))
            importance3 = float(input("Emotion importance (1-5): "))
            
            if all(1 <= x <= 5 for x in [importance1, importance2, importance3]):
                total = importance1 + importance2 + importance3
                weight_money = (importance1 / total) * 100
                weight_time = (importance2 / total) * 100
                weight_emotion = (importance3 / total) * 100
                return importance1, importance2, importance3, weight_money, weight_time, weight_emotion
            else:
                print("Please enter values between 1 and 5.")
        except ValueError:
            print("Please enter valid numbers.")

def print_evaluation_criteria():
    criteria_text = """
###########################################################

(English)
Consider as many people as you want from those with whom you have social relationships.
Evaluate the elements of money, time, and emotion on a scale of 1 to 5 in the case of the people you have in mind.

However, the time frame for the evaluation should be from the current time to a period equivalent to your current life routine, with a maximum of 3 years. (For example, if you were a college student and recently got a job, there is a big difference in your life routine before and after getting a job, so you should think within the period from the current time to after getting a job.)
The definition of a meeting is to intentionally spend time together with me and the other person at a specific promised time and place, with mutual agreement. (There are spatiotemporal constraints)
The definition of contact is to intentionally maintain remote communication such as phone calls and messengers with me and the other person with mutual agreement. (There are no spatiotemporal constraints)

The criteria for evaluating each element from 1 to 5 are as follows:

Money: When you think of the money you invested in the other person, estimate what percentage of the money the other person invested in you is. 
((Money you gave)/(Money you received))*100
- Less than 20: 1 point
- 20 or more and less than 40: 2 points
- 40 or more and less than 60: 3 points
- 60 or more and less than 80: 4 points
- 80 or more: 5 points

Time: When you think of the person you met for the most time, estimate what percentage of that person's time you invested in this person. 
((Time spent with this person)/(Time spent with the person you met the most))*100
- Less than 20: 1 point
- 20 or more and less than 40: 2 points
- 40 or more and less than 60: 3 points
- 60 or more and less than 80: 4 points
- 80 or more: 5 points

Emotion: When you think of the person you contacted most frequently, (roughly) estimate what percentage of that person's contact frequency your contact frequency with this person is. 
((Contact frequency with this person)/(Frequency of contact with the person you contacted most often))*100
- Less than 20: 1 point
- 20 or more and less than 40: 2 points
- 40 or more and less than 60: 3 points
- 60 or more and less than 80: 4 points
- 80 or more: 5 points

###########################################################





###########################################################

(한국어)

당신과 사회적 관계를 맺고 있는 사람들 중에서 원하는 숫자만큼의 사람을 떠올립니다.
다음은 당신이 떠올린 사람들과의 case에서 money, time, emotion 요소를 각각 1~5점으로 평가해 주시기 바랍니다.

단, 평가에서의 시간적 범위는 현재 시점부터 당신의 현재 삶의 루틴과 동일한 기간 동안이며, 최대 3년 이내입니다. 
(예: 최근 3년 이내 당신이 대학생이었다가 취업을 했을 경우, 삶의 루틴이 취업 전과 후가 큰 차이가 나므로, 현재 시점~취업 이후 기간 내에서 생각해야함)
만남의 정의는 특정 약속된 시공간적 지점에 나와 상대방 상호 합의 하에 의도적으로 함께하는 것입니다. (시공간적 제약이 있음)
연락의 정의는 전화, 메신저 등의 원격 의사소통을 나와 상대방 상호 합의 하에 의도적으로 유지하는 것입니다. (시공간적 제약이 없음)

각 요소별 1~5점 평가의 기준은 아래와 같습니다:

- money: 당신이 상대방에게 투자한 돈을 떠올렸을 떄, 상대방이 나에게 투자한 돈이 몇% 수준인지를 추정합니다. 
 ((당신이 받은 돈)/(당신이 준 돈))*100
- 그 정도가 20 미만: 1점 / 20이상 40미만: 2점 / 40이상 60미만: 3점 / 60이상 80미만: 4점 / 80이상: 5점

- time: 당신이 가장 많은 시간 동안 만났던 사람을 떠올렸을 때, 이 사람에게 투자한 시간이 그 사람의 몇 % 수준인지를 추정합니다.
 ((이 사람과 만났던 시간)/(가장 많이 만났던 사람의 시간))*100
- 그 정도가 20 미만: 1점 / 20이상 40미만: 2점 / 40이상 60미만: 3점 / 60이상 80미만: 4점 / 80이상: 5점

- emotion: 당신이 가장 자주 연락한 사람을 떠올렸을 때, 이 사람에게 연락한 빈도가 그 사람의 몇% 수준인지를 추정합니다.
 ((이 사람과의 연락 빈도)/(가장 자주 연락한 사람의 빈도))*100
- 그 정도가 20 미만: 1점 / 20이상 40미만: 2점 / 40이상 60미만: 3점 / 60이상 80미만: 4점 / 80이상: 5점

###########################################################

###########################################################

(English)
"How many people did you think of? Please respond with the information requested above for the corresponding number of cases."
(한국어)
"당신은 얼마나 많은 사람을 떠올렸습니까? 그 수만큼의 케이스에 대해 위에서 안내한 내용을 응답합니다"

###########################################################"""
    print(criteria_text)

def get_performance_scores():
    while True:
        try:
            num_cases = int(input("\nNumber of people you think of case: "))
            if num_cases > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    data = {'Case ID': [], 'Money': [], 'Time': [], 'Emotion': []}  # 빈 딕셔너리 생성

    for i in range(num_cases):
        print(f"\nCase {i+1}:")
        while True:
            try:
                perf_money = float(input("Money performance (1-5): "))
                perf_time = float(input("Time performance (1-5): "))
                perf_emotion = float(input("Emotion performance (1-5): "))

                if all(1 <= x <= 5 for x in [perf_money, perf_time, perf_emotion]):
                    index_money = ((perf_money - 1) * 100 / (5 - 1))
                    index_time = ((perf_time - 1) * 100 / (5 - 1))
                    index_emotion = ((perf_emotion - 1) * 100 / (5 - 1))

                    data['Case ID'].append(int(i+1))  # 딕셔너리에 case 열 추가
                    data['Money'].append(index_money)  # 딕셔너리에 값 추가
                    data['Time'].append(index_time)
                    data['Emotion'].append(index_emotion)
                    break
                else:
                    print("Please enter values between 1 and 5.")
            except ValueError:
                print("Please enter valid numbers.")

    df = pd.DataFrame(data)  # 딕셔너리를 DataFrame으로 변환
    return df

def calculate_final_results(importance1, importance2, importance3, weight_money, weight_time, weight_emotion, performance_df): # DataFrame 받기
    
    print("\n###########################################################")
    print("""
(English)
"Now the Social Relationship Index can be calculated by summation of index(=importance*perfomance) of each elements you answered"
(한국어)
"이제 당신이 응답한 각 요소의 Index(importance*performance)의 합계로 Social Relationship Index를 계산할 수 있습니다."
""")
    print("###########################################################\n")
    
    if performance_df.empty: # DataFrame이 비어있는지 확인
        print("No performance data entered. Cannot calculate average.")
        return
    print("\n--------------------------------- RESULT ----------------------------------------")
    print("The importance of each elements you answered: scale of 100")
    print(f"- money: {weight_money:.2f}")
    print(f"- time: {weight_time:.2f}")
    print(f"- emotion: {weight_emotion:.2f}\n")
    
    avg_index_money = performance_df['Money'].mean()
    avg_index_time = performance_df['Time'].mean()
    avg_index_emotion = performance_df['Emotion'].mean()

    print("The average performance of each elements you answered: scale of 100")
    print(f"- money: {avg_index_money:.2f}")
    print(f"- time: {avg_index_time:.2f}")
    print(f"- emotion: {avg_index_emotion:.2f}")
    print("*The criteria for converting to a score out of 100 are as follows:")
    print("point1: 0 | point2: 25 | point3: 50 | point4: 75 | point5: 100")

    t_index_money = avg_index_money * (weight_money / 100)
    t_index_time = avg_index_time * (weight_time / 100)
    t_index_emotion = avg_index_emotion * (weight_emotion / 100)

    total_index = t_index_money + t_index_time + t_index_emotion

    #print(performance_df)
    # 화려한 테이블 만들기
    from rich.console import Console
    from rich.table import Table

    print(f"\nThe table of 'Performance' for each case of each element is as follows:")
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(performance_df.columns[0], style="dim", justify="center")
    table.add_column(performance_df.columns[1], justify="right")
    table.add_column(performance_df.columns[2], justify="right")
    table.add_column(performance_df.columns[3], justify="right")
 
    table.add_row("Average", str(round(avg_index_money,2)), str(round(avg_index_time,2)),str(round(avg_index_emotion,2))) # case 전체평균값 추가
    for row in performance_df.itertuples(index=False):  # itertuples 사용, index=False필수 
        table.add_row(
                str(row[0]), # 각 컬럼의 값을 개별적으로 문자열로 변환
                str(row[1]),
                str(row[2]),
                str(row[3])
                )

    console.print(table)


    print(f"\nTotally, the Social Relationship Index is: {total_index:.2f}")
    
    print(f"\nThe table of 'Index'(=Importance*Performance) by case is as follows:")
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(performance_df.columns[0], style="dim", justify="center")
    table.add_column(performance_df.columns[1], justify="center")
    table.add_column(performance_df.columns[2], justify="center")
    table.add_column(performance_df.columns[3], justify="center")
    table.add_column("Social Relationship Index", style="blink", justify="center")
    
    table.add_row("Average", str(round(t_index_money,2)), str(round(t_index_time,2)),str(round(t_index_emotion,2)), str(round(total_index,2))) # case 전체평균값 추가
    for row in performance_df.itertuples(index=False):  # itertuples 사용, index=False필수
        table.add_row(
                str(row[0]), # 각 컬럼의 값을 개별적으로 문자열로 변환
                str(round(row[1]*weight_money/100,2)),
                str(round(row[2]*weight_time/100,2)),
                str(round(row[3]*weight_emotion/100,2)),
                str(round((row[1]*weight_money+row[2]*weight_time+row[3]*weight_emotion)/100,2))
                )

    console.print(table)

    print("---------------------------------------------------------------------------------\n")
    print("Thank you for your participation!\n")

def main():
    print_intro()
    importance1, importance2, importance3, weight_money, weight_time, weight_emotion = get_importance_weights()
    print_evaluation_criteria()
    performance_df = get_performance_scores() # DataFrame 받기
    calculate_final_results(importance1, importance2, importance3, weight_money, weight_time, weight_emotion, performance_df) # DataFrame 전달

def print_main():
    print(main())

def entry_point():
    typer.run(main)

if __name__ == "__main__":
    main()
