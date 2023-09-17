import streamlit as st
import openai
import json
from streamlit_cytoscapejs import st_cytoscapejs


# Page title
st.title("Plan my financial roadmap")

# Create a form to take user input
with st.form("Enter details"):
    # Add a text input field for the user to enter some data
    user_input = st.text_area("Tell us about your financial goals")

    # Add a button to submit the form
    submit_button = st.form_submit_button(label="Plan my roadmap")


# Check if the form is submitted
if submit_button:
    if user_input:
        # Query Open AI for knowledge graph
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "user",
                    "content": f"Help me understand following by describing as a detailed knowledge graph: {{user_input}}",
                }
            ],
            functions=[
                {
                    "name": "knowledge_graph",
                    "description": "Generate a knowledge graph with entities and relationships. Use the colors to help differentiate between different node or edge types/categories. Always provide light pastel colors that work well with black font.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metadata": {
                                "type": "object",
                                "properties": {
                                    "createdDate": {"type": "string"},
                                    "lastUpdated": {"type": "string"},
                                    "description": {"type": "string"},
                                },
                            },
                            "nodes": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "label": {"type": "string"},
                                        "color": {"type": "string"},
                                        "properties": {
                                            "type": "object",
                                            "description": "Additional attributes for the node",
                                        },
                                    },
                                    "required": [
                                        "id",
                                        "label",
                                        "type",
                                        "color",
                                    ],
                                },
                            },
                            "edges": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "from": {"type": "string"},
                                        "to": {"type": "string"},
                                        "relationship": {"type": "string"},
                                        "direction": {"type": "string"},
                                        "color": {"type": "string"},
                                        "properties": {
                                            "type": "object",
                                            "description": "Additional attributes for the edge",
                                        },
                                    },
                                    "required": [
                                        "from",
                                        "to",
                                        "relationship",
                                        "color",
                                    ],
                                },
                            },
                        },
                        "required": ["nodes", "edges"],
                    },
                }
            ],
            function_call={"name": "knowledge_graph"},
        )

        response_data = json.loads(
            completion.choices[0]["message"]["function_call"]["arguments"]
        )

        print(response_data)
        print(type(response_data))

        nodes = [
            {
                "data": {
                    "id": node["id"],
                    "label": node["label"],
                    "color": node.get("color", "defaultColor"),
                }
            }
            for node in response_data["nodes"]
        ]
        edges = [
            {
                "data": {
                    "source": edge["from"],
                    "target": edge["to"],
                    "label": edge["relationship"],
                    "color": edge.get("color", "defaultColor"),
                }
            }
            for edge in response_data["edges"]
        ]
        elements = {"nodes": nodes, "edges": edges}

        stylesheet = [
            {
                "selector": "node",
                "style": {
                    # "background-color": "data(color)",
                    # "label": "data(label)",
                    "text-valign": "center",
                    "text-halign": "center",
                    "shape": "rectangle",
                    "height": "50px",
                    "font-size": "12px",
                },
            },
            {
                "selector": "edge",
                "style": {
                    "width": 3,
                    # "line-color": "data(color)",
                    # "target-arrow-color": "data(color)",
                    "target-arrow-shape": "triangle",
                    # "label": "data(label)",
                    "curve-style": "unbundled-bezier",
                    "line-dash-pattern": [4, 4],
                    "text-background-color": "#ffffff",
                    "text-background-opacity": 1,
                    "text-background-shape": "rectangle",
                    "font-size": "10px",
                },
            },
        ]

        clicked_elements = st_cytoscapejs(elements, stylesheet)

        if clicked_elements is not None:
            st.write(clicked_elements)

        # st.components.v1.html(
        #     f"""
        #     <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.16/dist/tailwind.min.css" rel="stylesheet" />
        #     <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.19.0/cytoscape.min.js"></script>

        #     <div class="container mx-auto mt-10 p-4 bg-white rounded shadow-md flex space-x-4">
        #         <div class="flex-grow md:flex-grow-0 md:w-2/3 bg-white rounded-md shadow" id="cy">
        #             <!-- Graph will be displayed here -->
        #         </div>
        #         <div class="md:w-1/3 bg-white rounded-md shadow p-2.5">
        #             <!-- List of available graphs will be displayed here -->
        #             <div class="space-y-2 overflow-y-auto" id="history"></div>
        #         </div>
        #     </div>

        #     <script>
        #         function createGraph(data) {{
        #             cytoscape({{
        #                 container: document.getElementById("cy"),
        #                 elements: {json.dump({"nodes": nodes, "edges": edges})},
        #                 style: [
        #                     {{
        #                         selector: "node",
        #                         style: {{
        #                             "background-color": "data(color)",
        #                             label: "data(label)",
        #                             "text-valign": "center",
        #                             "text-halign": "center",
        #                             shape: "rectangle",
        #                             height: "50px",
        #                             width: (ele) => calcNodeWidth(ele.data("label")),
        #                             color: function (ele) {{
        #                                 return getTextColor(ele.data("color"));
        #                             }},
        #                             "font-size": "12px",
        #                         }},
        #                     }},
        #                     {{
        #                         selector: "edge",
        #                         style: {{
        #                             width: 3,
        #                             "line-color": "data(color)",
        #                             "target-arrow-color": "data(color)",
        #                             "target-arrow-shape": "triangle",
        #                             label: "data(label)",
        #                             "curve-style": "unbundled-bezier",
        #                             "line-dash-pattern": [4, 4],
        #                             "text-background-color": "#ffffff",
        #                             "text-background-opacity": 1,
        #                             "text-background-shape": "rectangle",
        #                             "font-size": "10px",
        #                         }},
        #                     }},
        #                 ],
        #                 layout: {{
        #                     name: "cose",
        #                     fit: true,
        #                     padding: 30,
        #                     avoidOverlap: true,
        #                 }},
        #             }});
        #         }}

        #         function getTextColor(bgColor) {{
        #             bgColor = bgColor.replace("#", "");
        #             const [r, g, b] = [0, 2, 4].map((start) => parseInt(bgColor.substr(start, 2), 16));
        #             const brightness = r * 0.299 + g * 0.587 + b * 0.114;
        #             return brightness < 40 ? "#ffffff" : "#000000";
        #         }}

        #         function getTextColor(backgroundColor) {{
        #             // Remove the '#' from the color value if present
        #             backgroundColor = backgroundColor.replace("#", "");
        #             console.log("backgroundColor:" + backgroundColor);

        #             // Convert the color to its R, G, B components
        #             let r = parseInt(backgroundColor.substring(0, 2), 16);
        #             let g = parseInt(backgroundColor.substring(2, 4), 16);
        #             let b = parseInt(backgroundColor.substring(4, 6), 16);

        #             // Calculate the brightness
        #             let brightness = r * 0.299 + g * 0.587 + b * 0.114;
        #             console.log("brightness:" + brightness);

        #             // Determine text color based on brightness
        #             if (brightness < 40) {{
        #                 return "#ffffff"; // Use white textw
        #             }} else {{
        #                 return "#000000"; // Use black text
        #             }}
        #         }}
        #     </script>
        #     """,
        #     height=600,
        # )
    else:
        st.warning("Please tell us more about your financial goals.")
