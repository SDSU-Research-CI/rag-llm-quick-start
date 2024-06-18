import chromadb, gradio as gr, ollama
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

def run_query(message, history, question, level, year, college, time_basis, campus, age, residency, living_situation, smart_devices_owned):    
    # Establish connection to vector database
    client = chromadb.PersistentClient(path = "/chroma", settings = Settings())
    collection = client.get_collection(name = "docs")

    # Vectorize prompt
    response = ollama.embeddings(
      prompt = message,
      model = "nomic-embed-text"
    )

    # Apply user's filters, if applicable
    where = {"$and": [{"question": question}]}
    for filter, value in (("level", level), ("year", year), ("college", college), ("time_basis", time_basis), ("campus", campus), ("age", age), 
                         ("residency", residency), ("living_situation", living_situation), ("smart_devices", smart_devices_owned)):
        if value != "--":
            where["$and"].append({filter: value})
    if len(where["$and"]) == 1:
        where = where["$and"][0]
    
    # Find top 10 responses most related to prompts
    results = collection.query(
      query_embeddings = [response["embedding"]],
      n_results = 10,
      where = where
    )

    # Convert responses to RAG prompt
    data = results["documents"][0]
    rag_prompt = f"Here is some data from students' responses to a survey on their perceptions and use of AI:\n\n{data}.\n\nBased on this data, respond to this prompt: '{message}'. Provide direct quotations where possible."

    # Construct message history list
    messages = []
    for interaction in history:
        user_log = interaction[0]
        chatbot_log = interaction[1]
        messages.append({"role": "user", "content": user_log})
        messages.append({"role": "assistant", "content": chatbot_log})
    messages.append({"role": "user", "content": rag_prompt})

    # Generate response
    response = ollama.chat(
      model = "llama3",
      messages = messages,
    )

    # Pass response to interface
    return response["message"]["content"]

# External resources
head = """
<script type = "text/javascript" src = "https://cdn.jsdelivr.net/npm/sweetalert2@11.3.10/dist/sweetalert2.all.min.js"></script>
<script type = "text/javascript" src = "https://dgoldberg.sdsu.edu/ai_survey/scripts/script_chatbot.js"></script>
<link rel = "stylesheet" href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" />
<link rel = "stylesheet" href = "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" />
<link rel = "stylesheet" href = "https://dgoldberg.sdsu.edu/ai_survey/css/style_chatbot.css" />
"""

# Custom scripts
css = """
.fa {
    color: #0078e7;
    cursor: pointer;
}
footer {
    visibility: hidden
}
textarea {
    resize: none
}
.svelte-1b6s6s, .progress-text {
    visibility: hidden
}
.svelte-1gfkn6j {
    color: var(--body-text-color)
} 
.chatbot {
    font-size: 16px
}
"""

# Run Gradio interface
with gr.Blocks(theme = gr.themes.Base(font = ["sans-serif"], text_size = gr.themes.Size(xxs = "16px", xs = "16px", sm = "16px", md = "16px", lg = "16px", xl = "16px", xxl = "16px"),
                                     primary_hue = gr.themes.Color(c100 = "#dbeafe", c200 = "#bfdbfe", c300 = "#93c5fd", c400 = "#60a5fa", c50 = "#eff6ff", c500 = "#3b82f6",
                                                                   c600 = "#0078e7", c700 = "#1d4ed8", c800 = "#1e40af", c900 = "#1e3a8a", c950 = "#1d3660")),
               title = "SDSU AI Student Survey",
               fill_height = True,
               head = head,
               css = css) as app:

    # Page title
    html = gr.HTML("""<br /><h1 style = 'font-size: 2em'>SDSU AI Student Survey Chatbot&nbsp;<i class = 'fa fa-info-circle' style = 'font-size: 28px; color: #0078e7' onclick = 'info();'></i>&nbsp;<i class = 'fa fa-question-circle' style = 'font-size: 28px; color: #e778e7' onclick = 'help();'></i></h1>
                      <p style = "display: inline;"><i>To analyze quantitative questions:&nbsp;&nbsp;</i></p><div style = "cursor: pointer; background-color: #bfdbfe; color: #0078e7; display: inline; padding: 5px; border-radius: 5px; font-weight: 600;"><a style = "all: unset;" href = "https://dgoldberg.sdsu.edu/ai_survey/testing.php">Launch dashboard&nbsp;<i class = "fa fa-chart-simple"></i></a></div>""")
    
    # Question selection dropdown
    question = gr.Dropdown(choices = ["What are your main questions or concerns about how AI will be incorporated into classes at SDSU over the next 2-3 semesters?",
                                      "How has AI affected your study habits and approach to completing assignments, if at all?", "How do you envision the future role of AI in your career or field of study?",
                                      "What additional SDSU resources or training would you like to see related to AI?", "How should SDSU involve students in creating and guiding campus-level policies about how AI is used?"],
                                      value = "What are your main questions or concerns about how AI will be incorporated into classes at SDSU over the next 2-3 semesters?",
                                      label = "Survey question", filterable = False)

    # Filters
    with gr.Accordion(label = "Filters", open = False) as acc:
        with gr.Row():
            level = gr.Dropdown(choices = ["--", "Undergraduate", "Graduate"], value = "--", label = "Level", filterable = False)
            year = gr.Dropdown(choices = ["--", "1", "2", "3", "4", "5+"], value = "--", label = "Year", filterable = False)
            college = gr.Dropdown(choices = ["--", "Arts & Letters", "Business", "Education", "Engineering", "Health & Human Services", "Professional Studies & Fine Arts", "Sciences", "Graduate Division", "Undergraduate Studies", "Undeclared", "Unsure"], value = "--", label = "College", filterable = False)
            time_basis = gr.Dropdown(choices = ["--", "Full-time", "Part-time"], value = "--", label = "Time basis", filterable = False)
            campus = gr.Dropdown(choices = ["--", "San Diego", "Imperial Valley"], value = "--", label = "Campus", filterable = False)
        with gr.Row():
            age = gr.Dropdown(choices = ["--", "19 or younger", "20-29", "30-39", "40 or older"], value = "--", label = "Age", filterable = False)
            residency = gr.Dropdown(choices = ["--", "California resident", "Out-of-state", "International"], value = "--", label = "Residency", filterable = False)
            living_situation = gr.Dropdown(choices = ["--", "On-campus", "Off-campus"], value = "--", label = "Living situation", filterable = False)
            smart_devices_owned = gr.Dropdown(choices = ["--", "1", "2", "3", "4+"], value = "--", label = "Smart devices owned", filterable = False)
    
    # Chatbot
    chat_interface = gr.ChatInterface(run_query,
                    additional_inputs = [question, level, year, college, time_basis, campus, age, residency, living_situation, smart_devices_owned],
                    retry_btn = None,
                    undo_btn = None,
                    clear_btn = None
    )
    chat_interface.chatbot.value = [[None, "Welcome! I'm a friendly chatbot trained to assist in analyzing SDSU's AI student survey data. I can analyze any survey question from the dropdown above, and you can optionally filter by student demographics and/or background. When you're ready, ask me a question!"]]
    chat_interface.chatbot.show_copy_button = True
    chat_interface.chatbot.bubble_full_width = False
    app.launch(server_name = "0.0.0.0")
