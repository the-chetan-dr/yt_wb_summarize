import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import os


#streamlit app
st.set_page_config(page_title="Langchain:Summary Text from YT on Website")
st.title("Langchain:Summarize Text from YT or website")
st.subheader('Summarize URL')



#asking user groq api key
with st.sidebar:
    groq_api_key = st.text_input("Enter your GROQ API Key", type="password")
    
generic_url=st.text_input("URL",label_visibility="collapsed")



##llm
#llm
llm=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)

#prompt template
prompt_template="""Provide a summary of a following content in 300 words:
Content:{text}
"""

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])


if st.button("summarize th content from YT or website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL.")
        
    else:
        try:
            with st.spinner("Hehe wait for a while .I also take time to summarize..."):
                if "youtube.com" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/119.0.0.0 Safari/537.36"
                    )
                })
                data=loader.load()
                
                
                #chain
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(data)
                
                st.success(output_summary)
                
        except Exception as e:
            st.exception(f"Exception:{e}")       
                         
                   
            