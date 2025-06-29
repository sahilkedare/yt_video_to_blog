def insert_thumbnail_image(state):
    """
    Insert the YouTube thumbnail image at the top of the blog, just after the title.
    Expects 'optimized_blog' (str) and 'thumbnail' (str, URL) in state.
    Returns {'blog_with_image': ...}
    """
    blog = state.get('optimized_blog')
    thumbnail_url = state.get('thumbnail')
    if not blog or not thumbnail_url:
        return {'blog_with_image': blog}

    # Try to find the first title (h1 or first line)
    import re
    # Markdown h1
    h1_match = re.match(r'^(# .+)$', blog, re.MULTILINE)
    image_md = f"![YouTube Thumbnail]({thumbnail_url})\n"
    if h1_match:
        title = h1_match.group(1)
        # Insert image after h1
        blog_with_image = blog.replace(
            title,
            f"{title}\n\n{image_md}",
            1
        )
    else:
        # No h1, insert image after first line
        lines = blog.split('\n', 1)
        if len(lines) > 1:
            blog_with_image = lines[0] + f"\n\n{image_md}" + lines[1]
        else:
            blog_with_image = blog + f"\n\n{image_md}"
    return {'blog_with_image': blog_with_image}
