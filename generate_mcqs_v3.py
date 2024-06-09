# %%
import os
import re
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from llm_utils import call_llm, get_json_from_string, get_usage_details
from mcq_utils import get_course_details, get_prompt_template_parts_for_mcq_generation, get_learning_outcomes_for_unit
from math import ceil
import random
import time

# %%
global course_details
global domain
global concept
global MODEL_TO_USE
global number_of_api_calls
global number_of_questions_per_section
global difficulty_level
global audience
global btl

def mcq_init():
    print(os.getcwd())
    x=load_dotenv()
    seed = 11
    FILE_OF_COURSE_DETAILS=os.getenv("FILE_OF_COURSE_DETAILS")
    MODEL_TO_USE = os.getenv("MODEL_TO_USE")
    DIR_OF_COURSE_MATERIAL=os.getenv("DIR_OF_COURSE_MATERIAL")
    DIR_OF_TEXT_SEGMENTS=os.getenv("DIR_OF_TEXT_SEGMENTS")
    course_details = get_course_details(FILE_OF_COURSE_DETAILS)

    # Example usage
    domain = "Computer Science"
    concept = "Variables in programming"
    difficulty_level = 2 # Easy, Medium, Hard
    audience = "Undergraduate" # Undergraduate, Postgraduate
    btl = "Evaluating" # ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating", "Creating"]
    number_of_questions_per_section = 3
    number_of_api_calls=1

    return course_details

#with open("text_segment_v2.txt", "r") as f:
#    text_segment = f.read()
#    #print(text_segment)


#for seed in range(number_of_api_calls):
#    unique_mcqs = generate_unique_mcqs(domain, concept, text_segment, difficulty_level, audience, number_of_questions, btl, seed)
#    print(unique_mcqs.content)

# %%
def generate_mcq_prompt_1(prompt, domain, concept, difficulty_level, audience, number_of_questions=1, btl="knowledge"):
    prompt = prompt.format(domain=domain, concept=concept, difficulty_level=difficulty_level, audience=audience, number_of_questions=number_of_questions, btl=btl)
    #prompt=f"""{prompt}"""
    return prompt

def generate_prompt(template, text_segment, difficulty_level, audience, number_of_questions, btl, btl_def, learning_outcome):
    prompt = template.format(text_segment=text_segment, difficulty_level=difficulty_level, audience=audience, number_of_questions=number_of_questions, btl=btl, btl_definition=btl_def, learning_outcome=learning_outcome)
    #print(prompt)
    return prompt

def generate_unique_mcqs(domain, concept, text_segment, difficulty_level, audience, number_of_questions, btl, learning_outcome, seed):
    """Generate unique MCQs based on the specified parameters."""
    if btl != "":
        template, btl_def = get_prompt_template_parts_for_mcq_generation(btl)
        prompt = generate_prompt(template, text_segment, difficulty_level, audience, number_of_questions, btl, btl_def, learning_outcome)

    else:
        with open("prompts/mcq_prompt.txt", "r") as f:
            prompt = f.read()
        prompt = generate_mcq_prompt_1(domain, concept, difficulty_level, audience, number_of_questions, btl)

    with open("prompts/system_message.txt") as f:
        system_message = f.read()
    mcqs = call_llm(system_message, prompt, seed)
    
    # Here you'd include logic to check for uniqueness against previously generated questions.
    # For simplicity, this example assumes all generated questions are unique.
    
    return mcqs

def print_mcqs(choices):
    for choice in choices:
        print("\n******************************************************")
        print(choice.message.content)


# %%
def mcq_generate(course_details):
    number_of_questions_per_api_call=1
    questions=[]
    files_to_create_segments_for=[]
    DIR_OF_TEXT_SEGMENTS = course_details['dir_of_course_unit_segments']
    btl=course_details['btl_at_which_to_generate_mcqs']
    difficulty_level=course_details['difficulty_at_which_to_generate_mcqs']
    course=course_details['name']
    course_code=course_details['code']
    audience=course_details['audience']
    number_of_mcqs_to_generate=course_details["number_of_mcqs_to_generate"]
    number_of_questions_per_section = 3
    number_of_api_calls = ceil(float(number_of_mcqs_to_generate)/float(number_of_questions_per_section))
    unit_to_generate_mcqs_for = course_details["unit_to_generate_mcqs_for"]
    condition = lambda obj: obj.get('unit') == unit_to_generate_mcqs_for
    learning_outcome = next((obj['outcome'] for obj in course_details['learning_outcomes'] if condition(obj)), None)
    learning_outcome = '\n'.join(learning_outcome)
    print('learning_outcome: ', learning_outcome)
    print("NUMBER OF API CALLS: ", number_of_api_calls)
    for dirpath, dirnames, filenames in os.walk(f"{DIR_OF_TEXT_SEGMENTS}"):
        #if dirpath == "DIR_OF_COURSE_MATERIAL":
        print(filenames)
        print("dir path: ------------------------------------" + dirpath)
        for file in filenames:
            print("filename: " + file)
            #course=file.split("-")[0]
            metadata = {"course": course, "course_code": course_code, "unit_numbers": [unit_to_generate_mcqs_for],  "btl": btl, "difficulty": difficulty_level, "audience": audience, "section": file, "model_used": os.getenv("MODEL_TO_USE"), "learning_outcomes": get_learning_outcomes_for_unit(course_details, unit_to_generate_mcqs_for)}
            files_to_create_segments_for.append(file)
            f = open(f"{DIR_OF_TEXT_SEGMENTS}/{file}", "r", encoding="utf-8")
            text_segment = f.read()
            f.close()
            for temp_seed in range(number_of_api_calls):
                # Seed the random number generator with the current time
                current_time = time.time()
                random.seed(current_time)

                # Generate a random number
                random_number = random.randint(1, 9223372036854775807)
                #random_number = random.randint(1, 1000) 
                domain = "Computer Science"
                concept = "Variables in programming"
                unique_mcqs = generate_unique_mcqs(domain, concept, text_segment, difficulty_level, audience, number_of_questions_per_section, btl, learning_outcome, random_number) #seed+temp_seed)
                try:
                    if "can't generate" not in unique_mcqs.content:
                        token_usage = get_usage_details(unique_mcqs)
                        
                        unique_mcqs_json = json.loads(get_json_from_string(unique_mcqs.content))
                        token_usage = {key: int(value / len(unique_mcqs_json)) for key, value in token_usage.items()}
                        mcqs_updated_with_metadata = [{**mcq, **metadata, 'usage': token_usage} for mcq in unique_mcqs_json]
                        
                        #questions_returned = get_json_formatted_questions(unique_mcqs, metadata)
                        #questions_returned = json.loads(get_json_from_string(unique_mcqs))
                        #questions
                        # print("****questions returned: \n", mcqs_updated_with_metadata)
                        questions = questions + mcqs_updated_with_metadata
                    else:
                        print("COULD NOT GENERATE MCQs")
                except:
                    print("*****************There is a failure---------------------------------------------")
                    print(unique_mcqs)
    print(questions)
    return questions
            

# %%
# from pprint import pprint
# print(unique_mcqs.content)
# number_of_api_calls
# c = mcq_init()
# print(mcq_generate(c))

# %%
# seed

# %%
# def save_work(filename, object):
#     with open(filename, 'w') as f:
#         json.dump(object, f, indent=4)
# if questions != []:
#     file_to_save=DIR_OF_COURSE_MATERIAL+f"/generated/{seed}-{course}-{unit_to_generate_mcqs_for}-{btl}-{difficulty_level}-{audience}.txt"
#     save_work(file_to_save, questions)
#     print("****MCQs SAVED IN: ", file_to_save)


