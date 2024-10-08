import streamlit as st
import requests

# Streamlit app
def main():
    st.title("IBM AI-Powered Wireless Communication Assistant")
    st.write("Enter your query related to Wireless Communication:")

    # Input from user
    user_input = st.text_area("Your Question:", height=100)
    
    if st.button("Generate Response"):
        if user_input.strip():
            # IBM AI API request parameters
            url = "https://us-south.ml.cloud.ibm.com"
            body = {
                "input": f"""<|system|>
You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior. You are a AI language model designed to function as a specialized Retrieval Augmented Generation (RAG) assistant. When generating responses, prioritize correctness, i.e., ensure that your response is correct given the context and user query, and that it is grounded in the context. Furthermore, make sure that the response is supported by the given document or context. Always make sure that your response is relevant to the question. If an explanation is needed, first provide the explanation or reasoning, and then give the final answer. Avoid repeating information unless asked.
You provide answers only to topics related to Wireless communication and nothing else.
<|assistant|>{user_input}
""",
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 900,
                    "repetition_penalty": 1.05
                },
                "model_id": "ibm/granite-13b-chat-v2",
                "project_id": "32d99adf-a1f6-4797-998f-13adc0a7713b"
            }

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {{api_key}}"  # Replace with your actual token
            }

            try:
                # Make the request to IBM AI API
                response = requests.post(url, headers=headers, json=body)
                response.raise_for_status()
                data = response.json()
                
                # Display the AI response
                st.write("### AI Response:")
                st.write(data.get('text', "No response received"))
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
