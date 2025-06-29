from langgraph.graph import StateGraph
from agents.summarizer_agent import summarize_transcript
from agents.blog_generator_agent import generate_blog_from_summary
from agents.seo_optimizer_agent import seo_optimize_blog
from agents.image_insertiion_agent import insert_thumbnail_image
from utils.youtube_transcript import get_transcript
from utils.youtube_images import extract_video_images
from typing import TypedDict

# Define the state schema
class BlogState(TypedDict):
    video_url: str
    transcript: list
    summary: str
    blog: str
    optimized_blog: str
    thumbnail: str
    blog_with_image: str

# Create the graph and add nodes by name and function
graph_builder = StateGraph(BlogState)
graph_builder.add_node("get_transcript", get_transcript)
graph_builder.add_node("extract_thumbnail", extract_video_images)
graph_builder.add_node("summarize_transcript", summarize_transcript)
graph_builder.add_node("generate_blog_from_summary", generate_blog_from_summary)
graph_builder.add_node("seo_optimize_blog", seo_optimize_blog)
graph_builder.add_node("insert_thumbnail_image", insert_thumbnail_image)

# Define edges (connections)
graph_builder.add_edge("get_transcript", "extract_thumbnail")
graph_builder.add_edge("extract_thumbnail", "summarize_transcript")
graph_builder.add_edge("summarize_transcript", "generate_blog_from_summary")
graph_builder.add_edge("generate_blog_from_summary", "seo_optimize_blog")
graph_builder.add_edge("seo_optimize_blog", "insert_thumbnail_image")

# Set entry and exit points
graph_builder.set_entry_point("get_transcript")
graph_builder.set_finish_point("insert_thumbnail_image")

graph = graph_builder.compile()