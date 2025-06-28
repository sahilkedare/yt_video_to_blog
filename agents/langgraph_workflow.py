from langgraph.graph import StateGraph
from agents.summarizer_agent import summarize_transcript
from agents.blog_generator_agent import generate_blog_from_summary
from agents.seo_optimizer_agent import seo_optimize_blog
from utils.youtube_transcript import get_transcript
from typing import TypedDict

# Define the state schema
class BlogState(TypedDict):
    video_url: str
    transcript: list
    summary: str
    blog: str
    optimized_blog: str

# Create the graph and add nodes by name and function
graph_builder = StateGraph(BlogState)
graph_builder.add_node("get_transcript", get_transcript)
graph_builder.add_node("summarize_transcript", summarize_transcript)
graph_builder.add_node("generate_blog_from_summary", generate_blog_from_summary)
graph_builder.add_node("seo_optimize_blog", seo_optimize_blog)

# Define edges (connections)
graph_builder.add_edge("get_transcript", "summarize_transcript")
graph_builder.add_edge("summarize_transcript", "generate_blog_from_summary")
graph_builder.add_edge("generate_blog_from_summary", "seo_optimize_blog")

# Set entry and exit points
graph_builder.set_entry_point("get_transcript")
graph_builder.set_finish_point("seo_optimize_blog")

graph = graph_builder.compile()