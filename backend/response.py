from openai import OpenAI
import pdfplumber
import config

client = OpenAI(api_key=config.api_key)

def extract_text_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text

pdf_text = extract_text_pdf("./response-reference/shootingBiomechanics.pdf")
config.conversation_history.append({"role": "system", "content": f"Reference on general expectations for shooting form: \n\n{pdf_text}"})

def generateResponse(user_response: str) -> str:
    config.conversation_history.append({"role": "user", "content": user_response})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=config.conversation_history
    )
    bot_response = completion.choices[0].message.content
    config.conversation_history.append({"role": "assistant", "content": bot_response})
    return bot_response
