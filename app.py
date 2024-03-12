import streamlit as st
import time

from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain.chat_models import ChatOpenAI

from googlesearch import search

from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build

import os

YT_API_KEY = "Your Youtube Data API Key"


os.environ['OPEN_API_KEY'] = "YOUR OPEN AI API KEY"

chatllm = ChatOpenAI(openai_api_key=os.environ.get("OPEN_API_KEY"), 
                     temperature=0.6, model='gpt-3.5-turbo')


st.set_page_config(layout="wide")

if 'flowmessages' not in st.session_state:
  st.session_state['flowmessages'] = [
    SystemMessage(content = 'You are a pofessional Roadmap Giver for Programming Languages and Projects, you will give output and suggestion in Basic and Advanced Level, the points and word limit is 10 -10 points and 500 words for each basic and advanced, and at the end, can you make the timeline, what should learn from day 1 to 10, day 10 -30 and more')
  ]


def search_for_blogs(query):
    max_results = 10
    results = []
    for j in search(query, num_results=max_results):
        results.append(j)
    return results

def search_youtube_videos(query, max_results=10):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    return results['result']

def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    snippet = response['items'][0]['snippet']
    return {'video_id': video_id, 'title': snippet['title']}


def get_chatbot_response(question):
  st.session_state['flowmessages'].append(HumanMessage(content = question))
  answer = chatllm(st.session_state['flowmessages'])
  st.session_state['flowmessages'].append(AIMessage(content = answer.content))
  return answer.content



col1, col2 = st.columns(2)
# Set page title
with col1:
    st.title('Developer Content Recommendation System')
    st.write("Find your Path, Roadmaps, Video Recomendations and Developer Blogs tosolve your learning problems")

with col2:
    st.image('Image.jpg ')
    # st.write("OKAY LOOT AT THIS")

# Input box for user input
user_input = st.text_input('Enter Project or Skill You Want To Learn', key = 'user_input')

response = get_chatbot_response(user_input)


# Button to trigger action
if st.button('Submit'):
    # Show spinner
    with st.spinner('Processing...'):
        # Simulate processing time
        time.sleep(2)
        # Print input text
        st.header(f'Response:')
        st.write(response)

        if user_input:
            st.title(f"Searching for '{user_input}'...")
            videos = search_youtube_videos(user_input)

            blogs = search_for_blogs(user_input)


            st.title("Top 10 Blogs:")

            col1, col2 = st.columns(2)
            for i, blog in enumerate(blogs):
                if(i < 5):
                    col1.write(f"{i + 1}. {blog}")

                else:
                    col2.write(f"{i + 1}. {blog}")

            if videos:
                st.title("Top 10 YouTube Videos:")
                for i, video in enumerate(videos):
                    video_details = get_video_details(video['id'])
                    
                    # Display video ID using st.markdown
                    video_id = video_details.get('video_id', 'N/A')

                    # st.markdown(f"**Video ID:** `{video_id}`")

                    # Display video using iframe
                    title = video_details.get('title', 'N/A')
                    st1, st2 = st.columns(2)

                    if i < 5:
                        st1.markdown(f"**Title:** {title}")
                        st2.write(f'<iframe width="560" height="310" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    else:
                        st1.markdown(f"**Title:** {title}")
                        st2.write(f'<iframe width="560" height="310" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
  
                    # st.write(f"**Title :** {title}")

                    # st.write(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

                    # Display the title if available
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a query.")

