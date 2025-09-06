import gradio as gr
import requests

N8N_WEBHOOK_URL = "https://dattatreya123.app.n8n.cloud/webhook-test/4eaba510-3602-4418-a6eb-3b232228c93a"
def chat_with_agent(user_input):
    payload = {"message": user_input}
    response = requests.post(N8N_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        return response.json()  
    else:
        return f"Error: {response.status_code} - {response.text}"

iface = gr.Interface(
    fn=chat_with_agent,
    inputs=gr.Textbox(lines=2, placeholder="Ask about appointments..."),
    outputs="text",
    title="Medical Appointment Scheduler"
)

iface.launch()
