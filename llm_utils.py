import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
#from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureChatOpenAI
import time
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

def get_model_to_use(seed):
    MODEL_TO_USE = os.getenv("MODEL_TO_USE")
    llm=""
    #print("-----------------------------------The model we will return is: ", MODEL_TO_USE)
    if "gpt-4-turbo" == MODEL_TO_USE.lower():
        #print("Returning : ", "gpt-4-turbo")
        llm = ChatOpenAI(
            # model="gpt-3.5-turbo",
            model=MODEL_TO_USE,
            temperature=1,
            max_tokens=4096,
            model_kwargs={
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0,
                "seed": int(seed),
            }

        )

    elif "claude" in MODEL_TO_USE.lower():
        #print("Returning : ", MODEL_TO_USE)
        llm = ChatAnthropic(
            model=MODEL_TO_USE,
            temperature=1,
            top_p=1,
            #model_kwargs={
            #    "seed": int(seed),
            #}
        )

    elif "gpt-4-32k" == MODEL_TO_USE.lower():
        #print("*********************************************in gpt-4-32k")
        llm = AzureChatOpenAI(
            name="gpt-4-32k",
            verbose=True,
            temperature=0.34,
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            openai_api_version=os.environ["CHAT_AZURE_OPENAI_API_VERSION"],
            deployment_name=os.environ["CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"],
            azure_endpoint=os.environ["CHAT_AZURE_ENDPOINT"],
            #base_url=os.environ["CHAT_AZURE_ENDPOINT"],
            model_kwargs={
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0,
                "seed": int(seed),
            },
        )
        #return llm
    elif "gpt-4-can-east" == MODEL_TO_USE.lower():
        llm = AzureChatOpenAI(
            name="gpt-4",
            verbose=True,
            temperature=0.34,
            api_key=os.environ["CAN_CHAT_AZURE_OPENAI_API_KEY"],
            openai_api_version=os.environ["CAN_CHAT_AZURE_OPENAI_API_VERSION"],
            deployment_name=os.environ["CAN_CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"],
            azure_endpoint=os.environ["CAN_CHAT_AZURE_ENDPOINT"],
            #base_url=os.environ["CHAT_AZURE_ENDPOINT"],
        )
    elif "gpt-4-turbo-eus2" == MODEL_TO_USE.lower():
            llm = AzureChatOpenAI(
                name="gpt-4",
                verbose=True,
                temperature=0.34,
                api_key=os.environ["EUS2_CHAT_AZURE_OPENAI_API_KEY"],
                openai_api_version=os.environ["EUS2_CHAT_AZURE_OPENAI_API_VERSION"],
                deployment_name=os.environ["EUS2_CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"],
                azure_endpoint=os.environ["EUS2_CHAT_AZURE_ENDPOINT"],
                #base_url=os.environ["CHAT_AZURE_ENDPOINT"],
            )
    elif "gpt-4o-mg" == MODEL_TO_USE.lower():
            llm = AzureChatOpenAI(
                name="gpt-4o",
                verbose=True,
                temperature=0.34,
                api_key=os.environ["EUS2_o_CHAT_AZURE_OPENAI_API_KEY"],
                openai_api_version=os.environ["EUS2_o_CHAT_AZURE_OPENAI_API_VERSION"],
                deployment_name=os.environ["EUS2_o_CHAT_AZURE_OPENAI_DEPLOYMENT_NAME"],
                azure_endpoint=os.environ["EUS2_o_CHAT_AZURE_ENDPOINT"],
                #base_url=os.environ["CHAT_AZURE_ENDPOINT"],
            )
    elif "gpt-4o" == MODEL_TO_USE.lower():
        llm = ChatOpenAI(
            #model="gpt-3.5-turbo",
            model=MODEL_TO_USE,
            temperature=0.34,
            max_tokens=4096,
            model_kwargs={
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0,
                "seed": int(seed),
            }

        )
    else:
        print("unknown model name:                   ", MODEL_TO_USE)
        exit()
    return llm

def call_llm(system_message, prompt, seed):

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt),
    ]

    template = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{prompt}"),
    ])


    #print("********************************************Trying to get the model")
    llm = get_model_to_use(seed)
    chain = template | llm


    #print("********************************************Trying to invoke the model")
    #output = llm.invoke(messages)
    #return output
    attempts = 0
    while attempts < 3:  # includes the first attempt and 2 retries
        try:
            #output = llm.invoke(messages)
            output = chain.invoke({"prompt": prompt})

            #output = ""
            #for chunk in chain.stream({"prompt": prompt}):
            #    output= output + chunk.content
            #    print(chunk, end="", flush=True)
            return output
        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")
            attempts += 1
            if attempts < 3:
                time.sleep(5)  # wait for 5 seconds before retrying
            else:
                raise Exception("Failed after 3 attempts")  # Optionally re-raise the last exception


def get_json_from_string(text):
    
    # Example mixed content string
    #mixed_str = "Here is the JSON data: {\"name\": \"John\", \"age\": 30, \"city\": \"New York\"} and some more text."
    #mixed_str = 'Here is the JSON output:\n\n{\n  "option chosen": "B",\n  "justification": "The course content mentions that \'Accounting Process\' includes the recording of financial transactions, ledger posting, preparation of financial statements and analysing and interpretation of them. This aligns with the definition provided in option B of the MCQ, which states that the collective process of recording, processing, classifying, and summarizing the business transactions in financial statements is known as the \'Accounting Cycle\'. Therefore, based on the information provided in the course content, option B is the most appropriate answer."\n}'
    pattern = r'\{.*?\}'
    pattern = r'(?:\{(?:[^{}]|(?R))*\}|\[(?:[^\[\]]|(?R))*\])'
    # Regular expression to find JSON (assuming JSON is always a dictionary)
    #match = re.search(pattern, text, re.DOTALL)
    
    #print(match.group(0))
    #return match.group(0)
    first_index = text.find('{')
    index2 = text.find('[')
    print(first_index, index2)
    min_value = min(first_index, index2) if first_index >= 0 and index2 >= 0 else max(first_index, index2)

    
    last_index = text.rfind('}')
    index2 = text.rfind(']')
    print(last_index, index2)

    max_value = max(last_index, index2)
    print("The min and the max: ", min_value, max_value)
    #print(text[first_index:last_index+1])
    return text[min_value:max_value+1]

def get_course_details_x():
    """ will return (course_code, course name, course unit number)"""

    code = FILE_OF_EXISTING_QUESTIONS.split("_")[0]
    name = '_'.join(DIR_OF_TEXT_SEGMENTS.split('/')[1].split("-")[0].split("_")[:-1])
    tokens = DIR_OF_TEXT_SEGMENTS.split("-")[0].split("_")
    unit_no_from_segment_dir = tokens[len(tokens)-1]
    return code, name, unit_no_from_segment_dir


def get_usage_details(output):
    MODEL_TO_USE = os.getenv("MODEL_TO_USE")
    if "claude" in MODEL_TO_USE.lower():
        usage = output.response_metadata['usage']
        new_usage =  {
            "completion_tokens": usage['output_tokens'],
            "prompt_tokens": usage['input_tokens'],
            "total_tokens": usage['output_tokens']+usage['input_tokens']
        }
        return new_usage
    elif "gpt" in MODEL_TO_USE.lower():
        try:
            usage = output.response_metadata['usage']
        except:
            usage = output.response_metadata['token_usage']
            
        return usage
    else:
        print("Unknown Model Usage: ", MODEL_TO_USE)
        exit()


#x=load_dotenv()
#with open("mcq-analysis-prompts/system_message.txt", "r") as f:
#    system_message = f.read()
#with open("mcq-analysis-prompts/analyze.txt", "r") as f:
#    prompt = f.read()
#analysis = call_llm(system_message, "say a joke", 11)
