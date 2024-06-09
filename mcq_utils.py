import json
import pandas as pd

def get_course_details(filepath):
    """returns a json of course details"""
    with open(filepath, 'r') as f:
        course_details = json.load(f)
    return course_details


def read_questions_to_analyze_as_dataframe(course_details):
    df=[]
    for sheet in course_details['sheets']:
        df.append(pd.read_excel(course_details['questions_to_improve_filepath'], sheet_name=sheet))
    df = pd.concat(df)

    #temp_df=[]
    #for unit in course_details['units_to_analyze']:
    #    temp_df.append(df[df['Unit No.']==unit])
    #df = pd.concat(temp_df)
    df = df[df['Unit No.']==course_details['unit_to_analyze']]
    
    return df


def generate_array_of_questions_for_analysis(df, course_details):
    btls = course_details['btls']
    question_template="""
    {question}
    {options}
    The correct option is: {correct_option}
    """
    list = []
    option_index = {"A":0, "B": 1, "C":2, "D":3}
    for index, row in df.iterrows():
        if index > 0:
            option_cols = option_index.keys()
            option_list = []
            options=""
            for col in option_cols:
                val = df.loc[index][col].strip()
                option = f"{col}. {val}\n"
                options += option
                option_list.append(option)
            question_to_append = {
                "unit_no": int(df.loc[index]["Unit No."]),
                "question": question_template.format(question=df.loc[index]["Question"].strip(), options=options, correct_option=df.loc[index]["Correct Option"]),
                "question_orig": df.loc[index]["Question"].strip(),
                "option_list": option_list,
                "correct_answer_index": option_index[df.loc[index]["Correct Option"]],
                "btl": btls[int(df.loc[index]["BTL"])-1],
            }

            list.append(question_to_append)
    #for question in list:
    #    print(question)
    return list

def get_learning_outcomes_for_unit(course_details, unit):
    los=[]
    for lo in course_details['learning_outcomes']:
        if lo['unit'] == unit:
            los = lo['outcome']
    return los


def get_learning_outcomes(course_details):
    lo={}
    for unit in course_details['units_to_analyze']:
        lo[unit]= get_learning_outcomes_for_unit(course_details, unit)
    return lo


def get_prompt_template_parts_for_mcq_generation(btl):
    overall_prompt_template=""
    with open("prompts/part_0_overall_mcq_instruction.txt", 'r') as f:
        overall_prompt_template = f.read()
    #print(overall_prompt_template)
    print("-----------------------------------------------")
    btl = btl.lower()
    with open(f"prompts/part_btl_{btl}_def.txt", "r") as f:
        btl_def = f.read()
    return overall_prompt_template, btl_def