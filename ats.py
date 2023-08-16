import openai

# Set your OpenAI API key
openai.api_key = "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"

# User's resume
user_resume = """
John Doe
Software Engineer
Email: john.doe@example.com
Phone: (123) 456-7890
LinkedIn: linkedin.com/in/johndoe
"""

# ATS Best Practices evaluation prompt
prompt = f"""
Evaluate the following resume against ATS best practices:

{user_resume}

Provide feedback on the ATS best practices adherence.
"""

# Use ChatGPT to evaluate ATS best practices
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100,
    stop=None,
    temperature=0.6,
    api_key="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"  # Replace with your API key
)

# Extract feedback from the response
feedback = response.choices[0].text.strip()

# Print the feedback
print("ATS Best Practices Evaluation:")
print(feedback)
