import streamlit as st 
import tiktoken 

GPT_35_TURBO_PROMPT_COST = 0.0015/1000 
GPT_35_TURBO_COMPLETION_COST = 0.002/1000
GPT_4_PROMPT_COST = 0.03/1000
GPT_4_COMPLETION_COST = 0.06/1000

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens

def clear_text(): # not user yet
    st.session_state["prompt_text_area"] = ""

def main():
    st.set_page_config(layout="wide")
    st.title(":robot_face: LLM Cost Calculator")

    with st.form("section_1"):

        st.header("1. Prompt Token Counter")

        col1, col2 = st.columns([3, 1])
        with col1:
            prompt_text = st.text_area("Prompt Text", height=200, key="prompt_text_area")
            submitted_1 = st.form_submit_button("Submit")
        with col2:
            option4 = st.selectbox(
                label = 'Select an LLM:',
                options = ('GPT-3.5-Turbo', 'GPT-4'),
                index = 0)

        if submitted_1 and len(prompt_text) == 0:
            col1.write("Please enter a prompt")
        if submitted_1 and option4 and len(prompt_text) > 0:
            option4 = option4.lower()
            # print(tiktoken.encoding_for_model("gpt-3.5-turbo-instruct"))
            # print(tiktoken.encoding_for_model("text-embedding-ada-002"))
            encoding = tiktoken.encoding_for_model(option4)
            token_counts = num_tokens_from_string(prompt_text, "cl100k_base")
            col2.success("Encoding: \n" + str(encoding)[10:-1], icon = '🤖')
            col2.success("Token Count: " + str(token_counts), icon = '🤖')
            # st.info("Your Input Prompt: " + prompt_text)

    with st.form("section_2"):

        st.header("2. Cost Calculator (LLM)")
        st.write("Important Note: This calculator is based on several assumptions. "
            "It takes no responsibility for the accuracy of the calculation. "
            "Please use at your own risk.")
        col1, col2, col3 = st.columns([1, 1, 1])
        submitted_2 = st.form_submit_button("Submit")
        
        with col1:
            st.subheader("Configure Prompt Usage")
            average_number_of_employees = st.slider("Average number of Employees", 0, 200, 0)
            average_prompt_frequency = st.slider("Average number of Prompts (Per Day)/Employee", 0, 300, 0)
            average_prompt_tokens = st.slider("Average Prompt Tokens Length", 0, 300, 0)
            average_completion_tokens = st.slider("Average Completion Tokens Length", 0, 1000, 0)

        with col2:
            st.subheader("Configure the LLM")
            option1 = st.selectbox('Select an LLM:', ('GPT-3.5-Turbo', 'GPT-4'))
            # st.subheader("Configure Vector Store")
            # option2 = st.selectbox(
            #     label = 'Select Vector Store/DB:',
            #     options = ('Open Source', 'Pinecone'),
            #     index = 1)
            # if option2 == 'Pinecone':
            #     option3 = st.selectbox(
            #         label = 'Select Pinecone Service Level:',
            #         options = ('Free', 'Standard', 'Enterprise'),
            #         index = 1)

        with col3:
            st.subheader("Cost Analysis (Weekdays)") # Assume weekdays only
            if option1 in ['GPT-3.5-Turbo', 'GPT-4']:
                if option1 == 'GPT-3.5-Turbo':
                    prompt_cost = GPT_35_TURBO_PROMPT_COST
                    completion_cost = GPT_35_TURBO_COMPLETION_COST
                else:
                    prompt_cost = GPT_4_PROMPT_COST
                    completion_cost = GPT_4_COMPLETION_COST
                # Calculate average number of prompts per day
                average_prompts_per_day =  average_number_of_employees * average_prompt_frequency
                cost_per_day = average_prompts_per_day * average_prompt_tokens * prompt_cost + \
                    average_prompts_per_day * average_completion_tokens * completion_cost
                cost_per_month = cost_per_day * 365 * 5/7 / 12
                cost_per_year = cost_per_day * 365 * 5/7
                st.success("Cost Per Day: " + str(round(cost_per_day, 2)) + " $")
                st.success("Cost Per Month: " + str(round(cost_per_month, 2)) + " $")
                st.success("Cost Per Year: " + str(round(cost_per_year, 2)) + " $")
            else:
                st.error("Please select a valid LLM")

    with st.form("section_3"):

        st.header("3. Vector Store Cost")
        st.write("Important Note: This calculator is based on several assumptions. "
            "It takes no responsibility for the accuracy of the calculation. "
            "Please use at your own risk.")
        col1, col2, col3 = st.columns([1, 1, 1])
        submitted_3 = st.form_submit_button("Submit")

        with col1:
            st.subheader("Configure Vector Store")
            option2 = st.selectbox(
                label = 'Select Vector Store/DB:',
                options = ('Open Source', 'Pinecone'),
                index = 1)
            if option2 == 'Pinecone':
                option3 = st.selectbox(
                    label = 'Select Pinecone Service Level:',
                    options = ('Free', 'Standard', 'Enterprise'),
                    index = 1)
                option5 = st.selectbox(
                    label = 'Select Pinecone Pod Type:',
                    options = ('s1 - storage optimized', 'p1 - performance optimized', 'p2 - 2nd gen performance'),
                    index = 0)
                option6 = st.selectbox(
                    label = 'Select Pinecone Pod Size:',
                    options = ('x1', 'x2', 'x4', 'x8'),
                    index = 0)

        with col2:
            st.subheader("Cost Analysis")
            st.empty()
        
        if submitted_3 and option2 == 'Open Source':
            cost_per_hour = 0.0
        elif submitted_3 and option3 == 'Free':
            cost_per_hour = 0.0
        elif submitted_3 and option2 == 'Pinecone':
            if option3 == 'Standard' and option5.startswith('s1') and option6 == 'x1':
                cost_per_hour = 0.0960
            else:
                cost_per_hour = 0.0960
        else:
            cost_per_hour = 0.0960
        
        cost_per_day = cost_per_hour * 24
        cost_per_month = cost_per_day * 365 / 12
        cost_per_year = cost_per_day * 365
        col2.success("Cost Per Day: " + str(round(cost_per_day, 2)) + " $")
        col2.success("Cost Per Month: " + str(round(cost_per_month, 2)) + " $")
        col2.success("Cost Per Year: " + str(round(cost_per_year, 2)) + " $")

if __name__ == "__main__":
    main()
