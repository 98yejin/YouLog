import openai

def transform_script_to_blog(script, api_key):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Rewrite the following script into a detailed blog post, ensuring all information is retained:\n\n{script}",
            temperature=0.5,
            max_tokens=2048,
            n=1,
            stop=None,
        )
        blog_post = response.choices[0].text.strip()
        return blog_post
    except Exception as e:
        print(f"Error generating blog post: {e}")
        return "Error generating blog post."
