import plotly.graph_objects as go

def generate_html_report(ranked_results):
    """
    Generate a simple HTML table report
    """
    html = "<table border='1' style='border-collapse: collapse; width: 100%; text-align: center;'>"
    html += "<tr><th>Resume</th><th>Final Score</th></tr>"
    for filename, score in ranked_results:
        html += f"<tr><td>{filename}</td><td>{score:.2f}</td></tr>"
    html += "</table>"
    return html

def generate_score_graph(ranked_results):
    """
    Generate a bar chart of scores
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[r[0] for r in ranked_results],
        y=[r[1] for r in ranked_results],
        marker_color='blue'
    ))
    fig.update_layout(title="Candidate Scores", xaxis_title="Resume", yaxis_title="Score")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_skills_radar(skills_flags):
    """
    Radar charts for matched and missing skills
    """
    charts_html = ""
    
    for candidate, flags in skills_flags.items():
        if not flags:
            continue

        skills = list(flags.keys())
        matched = [1 if flags[skill] else 0 for skill in skills]
        missing = [0 if flags[skill] else 1 for skill in skills]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=matched, theta=skills, fill='toself', name='Matched Skills', line=dict(color='green')))
        fig.add_trace(go.Scatterpolar(r=missing, theta=skills, fill='toself', name='Missing Skills', line=dict(color='red')))

        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
                          showlegend=True, title=f"Skill Match Radar: {candidate}")
        charts_html += fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return charts_html
