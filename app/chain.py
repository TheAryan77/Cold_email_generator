import os

from click import prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __int__(self):
        self.llm = llm = ChatGroq(
    model_name="llama3-8b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0)
    def extract_jobs(self,cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ###SCRAPED TEXT FROM WEBSITE: 
            {page_data}
            ### INSTRUCTION: 
            Extract job postings from the given text and return them as a JSON array.
            Ensure the JSON contains objects with the keys: `role`, `experience`, `skills`, and `description`.
            Output **only** valid JSON—no explanations, preamble, or additional text.
            Respond with JSON **only**.
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data":cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs!!")
        return res if isinstance(res,list) else [res]

    def write_mail(self,job,links):
        prompt_email = PromptTemplate.from_template(
            """
                    ### JOB DESCRIPTION:
                    {job_description}
    
                    ### INSTRUCTION:
                    You are Aryan Mahendru, a business development executive at Mahendru AI Dynamics. Mahendru AI Dynamics is an AI & Software Consulting company dedicated to facilitating
                    the seamless integration of business processes through automated tools. 
                    Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                    process optimization, cost reduction, and heightened overall efficiency. 
                    Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Mahendru AI Dynamics 
                    in fulfilling their needs.
                    Also add the most relevant ones from the following links to showcase Mahendru AI Dynamics's portfolio: {link_list}
                    Remember you are Aryan Mahendru, BDE at Mahendru AI Dynamics. 
                    Do not provide a preamble.
                    ### EMAIL (NO PREAMBLE):
    
                    """
        )
        chain_email = prompt_email | self.llm
        res = chain_email({"job_description": str(job[0]),"link_list":links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))