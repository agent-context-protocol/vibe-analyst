import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import asyncio
from agent_context_protocol.acp_manager import ACP
from agent_context_protocol import MCPToolManager
import asyncio
import json
from openai import OpenAI, AsyncOpenAI
import streamlit.components.v1 as components
import json
from ui_helpers import update_and_draw_dag

st.set_page_config(layout = "wide") 
client = OpenAI()
client_async = AsyncOpenAI()
model_name = "gpt-4.1-2025-04-14"
def load_css():
    st.markdown("""
        <style>
        /* Grid styling */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr); /* Two columns */
            gap: 20px;
            padding: 10px;
        }

        .grid-item {
            padding: 15px;
            background-color: #f1f1f1;
            border-radius: 8px;
            text-align: left;
            box-shadow: none;
            font-size: 16px;
            cursor: default;
        }

        /* Custom font styling */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Arial', sans-serif;
            font-weight: normal;
        }

        p {
            font-family: 'Helvetica', sans-serif;
        }

        /* Simplified progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }

        /* Minimal button styling */
        .stButton>button {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            border-radius: 6px;
        }

        /* Scrollbar customization */
        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: #888;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        /* SubTask max height with scrollable content */
        .scrollable-panel {
            width: 100%;  /* Take up 100% of the column width */
            max-height: 500px;  /* Set maximum height */
            padding: 20px;
            border: 2px solid white;
            border-radius: 10px;
            background-color: black;
            color: white;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);  
            overflow-y: auto;  /* Scrollable when content exceeds max height */
        }

        /* Ensure headings and paragraphs are white */
        .scrollable-panel h3, .scrollable-panel h4, .scrollable-panel p {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)


class StreamlitACP:
    def __init__(self):
        self.mcp_manager = None
        self.ACP = None
        self.output = {}
        self.group_containers = {}
        self.subtasks = []

    async def async_init(self):
        self.mcp_manager = MCPToolManager()
        await self.mcp_manager.load_from_config("files/config.yml")
        self.ACP = ACP(mcp_tool_manager=self.mcp_manager)

    def create_group_sections(self, execution_blueprint):
        """For each group in the execution blueprint, create a full‑width UI container
        and render its DAG panel in the sidebar.

        Error‑handling now relies solely on **print** statements so that any failure
        is reported to the terminal without crashing the whole app.
        """

        # --- Basic type check ----------------------------------------------------
        if not isinstance(execution_blueprint, dict):
            print(
                f"[create_group_sections] ❌  execution_blueprint must be a dict; got {type(execution_blueprint).__name__}"
            )
            return

        # Reset placeholders for a fresh render ----------------------------------
        self.dag_placeholders = {}

        for gid, gdata in execution_blueprint.items():
            # 1️⃣  Create a container for this group -----------------------------
            try:
                container = st.container()
                self.group_containers[gid] = container
            except Exception as err:
                print(f"[create_group_sections] ❌  Could not create container for {gid}: {err}")
                continue  # Skip this group

            # 2️⃣  Reserve sidebar space for the DAG -----------------------------
        try:
            placeholder = st.sidebar.empty()
            self.dag_placeholder = placeholder
            placeholder.subheader("Execution DAG")
        except Exception as err:
            print(f"[create_group_sections] ❌  Could not create sidebar placeholder for {gid}: {err}")

            # 3️⃣  Draw the DAG ---------------------------------------------------
        try:
            update_and_draw_dag(
                    execution_blueprint,
                    completed=set(),
                    placeholder=placeholder,
                )
            print(f"[create_group_sections] ✅  Rendered DAG for group {gid}")
        except Exception as err:
            print(f"[create_group_sections] ❌  Error rendering DAG for {gid}: {err}")


    def update_group_section(self, group_id, user_query):
        
        with open(f"files/dashboard_prompt.txt", "r") as f:
            system_prompt = f.read()
        with open(f"execution_blueprint_updated_{group_id}.json", "r") as f:
            data = json.load(f)

        input_data = json.dumps(data, indent=2)
        completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_data}
            ],
                        temperature = 0
                    ) 
        
        raw_html_snippet = completion.choices[0].message.content.split("### FORMATTED_OUTPUT")[-1].strip()
        print("Raw HTML Snippet: ", raw_html_snippet)
        full_doc = f"""
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8"/>
          </head>
          <body style="margin:0; padding:1rem;">
            {raw_html_snippet}
          </body>
        </html>
        """
        container = self.group_containers[group_id]
        with container:
            components.html(full_doc, height=1200, scrolling=True)
    async def run_acp(self, user_query, execution_blueprint):
        print('Creating Group Sections...')
        self.create_group_sections(execution_blueprint)
        print('Executing Group Sections...')
        async for group_id in self.ACP.run(user_query, execution_blueprint):
            self.output[group_id] = 'group_results'
            self.update_group_section(group_id, user_query)

async def main():
    # Load custom CSS
    
    
    load_css()

    st.title("Vibe Analyst")
    acp_app = StreamlitACP()
    await acp_app.async_init()

    # Sidebar for user input
    with st.sidebar:
        st.header("User Input")
        user_query = st.text_area("Enter your query:")

    if st.button("Analyze Vibes"):
        with st.spinner("Agent Context Protocol (ACPs) at work ..."):
            try:
            # st.write("Running execution_blueprint...")
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Initialize the execution_blueprint
                execution_blueprint = await acp_app.ACP.initialise(user_query)

                async def update_progress():
                    total = len(acp_app.ACP.communication_manager.agents)
                    while True:
                        done = len(acp_app.ACP.communication_manager.completed_agents)
                        pct = done / total * 100
                        progress_bar.progress(done/total)
                        status_text.text(f"{pct:.0f}%")
                        if done >= total:
                            break
                        await asyncio.sleep(0.1)

                async def refresh_dags():
                    cm = acp_app.ACP.communication_manager
                    prev = 0                                   
                    while True:
                        cur = len(cm.completed_agents)
                        if cur > prev:                        
                            completed = set(map(str, cm.completed_agents))
                            # for gid, ph in acp_app.dag_placeholders.items():
                            #     fp = f"execution_blueprint_updated_{gid}.json"
                            #     with open(fp) as f:
                            #         data = json.load(f)
                            update_and_draw_dag(acp_app.ACP.dag_compiler.execution_blueprint, completed, acp_app.dag_placeholder)
                            prev = cur
                        if cur >= len(cm.agents):               
                            break
                        await asyncio.sleep(0.1)

                await asyncio.gather(
                    acp_app.run_acp(user_query, execution_blueprint),
                    update_progress(),
                    refresh_dags()
                )

                st.success("ACP completed!")
            except asyncio.TimeoutError:
                st.error("The operation timed out. Please try again.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())