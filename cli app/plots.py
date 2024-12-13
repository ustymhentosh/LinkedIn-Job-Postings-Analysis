import pandas as pd
import plotly.express as px
import textwrap
import plotly.graph_objects as go

STATES = [
    "CA",
    "MI",
    "UT",
    "NJ",
    "NY",
    None,
    "TN",
    "NE",
    "IN",
    "CT",
    "IL",
    "PA",
    "FL",
    "VA",
    "WI",
    "AZ",
    "WA",
    "MD",
    "NC",
    "OH",
    "NM",
    "TX",
    "NH",
    "MT",
    "OR",
    "MA",
    "LA",
    "SC",
    "GA",
    "IA",
    "MN",
    "AK",
    "KY",
    "CO",
    "AL",
    "WV",
    "DC",
    "AR",
    "NV",
    "DE",
    "RI",
    "SD",
    "OK",
    "MO",
    "KS",
    "MS",
    "HI",
    "ID",
    "VT",
    "ME",
    "ND",
    "WY",
]


def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(
            textwrap.fill(text, width=width, break_long_words=break_long_words)
        )
    ax.set_yticklabels(labels, rotation=0)


def normalize_dict(data):
    values = [v for v in data.values() if isinstance(v, (int, float))]
    if not values:
        return data

    min_val = min(values)
    max_val = max(values)

    return {
        k: (v - min_val) / (max_val - min_val) if isinstance(v, (int, float)) else v
        for k, v in data.items()
    }


def get_states_score_for_jobs_list(df: pd.DataFrame, job_title_list):
    total_states_jobs = df.groupby(by="state").count()["job_link"]

    df = df[df["equivalent job title"].isin(job_title_list)]
    results = dict(df.groupby(by=["state", "equivalent job title"]).count()["job_link"])
    result_dct = {}

    # NOTE: i should be replaced by relevant score for each job.
    for state in STATES:
        result_dct[state] = 0
        for i, job in enumerate(job_title_list):
            if results.get(tuple([state, job])):
                result_dct[state] += (
                    (len(job_title_list) - i)
                    * results[tuple([state, job])]
                    / total_states_jobs[state]
                )
    return normalize_dict(result_dct)


def extract_body_content(html):
    body_start = html.find("<body>")
    body_end = html.find("</body>")
    if body_start == -1 or body_end == -1:
        raise ValueError("Invalid HTML: Missing <body> or </body> tag.")
    return html[body_start + len("<body>") : body_end].strip()


def create_html_file(jobs_list):
    """
    Creates an HTML file with a title and an ordered list based on the provided jobs list.

    Args:
        jobs_list (list of str): A list of job titles to include in the ordered list.
        output_file (str): Name of the output HTML file. Defaults to 'recommended_jobs.html'.
    """
    # HTML template with placeholders for dynamic content
    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Job Recommendations</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 1.5rem;
            margin: 20px;
        }}
        h1 {{
            color: #333;
        }}
        ol {{
            margin-top: 20px;
        }}
        ol li {{
            padding: 5px 0;
        }}
    </style>
</head>
<body>
    <h1>These are recommended jobs based on your skills</h1>
    <ol>
        {''.join(f'<li>{job}</li>' for job in jobs_list)}
    </ol>
</body>
</html>"""

    return html_content


class Plots:
    @staticmethod
    def get_satates_map_for_jobs_list(df: pd.DataFrame, job_list: list):
        result_dict = get_states_score_for_jobs_list(df, job_list)
        result_score_df = pd.DataFrame(
            list(result_dict.items()), columns=["state", "score"]
        )
        fig = px.choropleth(
            result_score_df,
            locations="state",
            locationmode="USA-states",
            color="score",
            scope="usa",
            title="Attractiveness of the each state",
            height=800,
        )
        fig.update_layout(title={"font": {"size": 28}})
        return fig

    @staticmethod
    def get_education_req_plot_for_jobs_list(df: pd.DataFrame, job_list: list):
        # Filter Dataframe
        df = df[df["equivalent job title"].isin(job_list)][
            ["equivalent job title", "edu_req"]
        ]
        jobs_edu_dist = {}
        for job in job_list:
            jobs_edu_dist[job] = df[df["equivalent job title"] == job][
                "edu_req"
            ].value_counts()

        # Prepare data for plotting
        df = pd.DataFrame(jobs_edu_dist).fillna(0).T
        df_normalized = df.div(df.sum(axis=1), axis=0) * 100
        df_sorted = df_normalized.sort_values(by="high_school", ascending=True)
        colors = ["#66b3ff", "#ff9999", "#ffcc99", "#99ff99", "#cc99ff", "#ffa64d"]
        list_categories = [
            "high_school",
            "bachelor_degree",
            "associate_degree",
            "master_degree",
            "no_education",
            "vocational",
        ]
        order = [
            category for category in list_categories if category in df_sorted.columns
        ]
        df_sorted = df_sorted[order]

        # Create plotly figure
        fig = go.Figure()
        for i, category in enumerate(order):
            fig.add_trace(
                go.Bar(
                    y=df_sorted.index,
                    x=df_sorted[category],
                    name=category.replace("_", " ").title(),
                    orientation="h",
                    marker=dict(color=colors[i]),
                )
            )

        # Update layout
        fig.update_layout(
            barmode="stack",
            title={
                "text": "Distribution of Education Requirements for Jobs",
                "y": 0.98,
                "x": 0.01,
                "xanchor": "left",
                "yanchor": "top",
                "font": {"size": 25},
            },
            xaxis_title="Percentage %",
            yaxis_title="Job Titles",
            xaxis=dict(tickformat=".0f"),
            legend=dict(
                orientation="h",
                x=0.01,
                y=1.1,
                xanchor="left",
            ),
            margin=dict(l=100, r=20, t=90, b=50),
            height=600,
            legend_traceorder="reversed",
        )
        return fig


def combine_htmls(main_list_text: str, html_1: str, html_2: str, dest: str):
    """
    Combines three html files(one main with list of jobs,
    and two plots) into one by extrating bodies.
    """

    with open(html_1, "r", encoding="utf-8") as file1, open(
        html_2, "r", encoding="utf-8"
    ) as file2:
        content_1 = file1.read()
        content_2 = file2.read()

    body_content_1 = extract_body_content(content_1)
    body_content_2 = extract_body_content(content_2)
    body_end_1 = main_list_text.find("</body>")
    combined_html = (
        main_list_text[:body_end_1]
        + body_content_1
        + body_content_2
        + main_list_text[body_end_1:]
    )

    with open(dest, "w", encoding="utf-8") as output_file:
        output_file.write(combined_html)
