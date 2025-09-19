import plotly.graph_objects as go
import plotly.express as px

# Create system architecture diagram using Plotly
fig = go.Figure()

# Define colors for each major section
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Define component positions and sizes
components = [
    # Data Sources
    {'name': 'Data Sources', 'x': 0.15, 'y': 0.8, 'width': 0.25, 'height': 0.15, 'color': colors[0],
     'items': ['Market APIs', 'News Feeds', 'Sanctions', 'Documents']},
    
    # Pathway Pipeline  
    {'name': 'Pipeline', 'x': 0.375, 'y': 0.5, 'width': 0.25, 'height': 0.15, 'color': colors[1],
     'items': ['Streaming ETL', 'Vector Store', 'Live Indexing', 'Query Engine']},
    
    # AI Agents
    {'name': 'AI Agents', 'x': 0.6, 'y': 0.8, 'width': 0.25, 'height': 0.15, 'color': colors[2],
     'items': ['Trading Bot', 'Sanctions Mon', 'KYC Watchdog', 'Anomaly Det']},
    
    # API Layer
    {'name': 'API Layer', 'x': 0.6, 'y': 0.5, 'width': 0.25, 'height': 0.15, 'color': colors[3],
     'items': ['FastAPI', 'REST Endpoints', 'WebSocket', 'Auth']},
    
    # Frontend UI
    {'name': 'Frontend UI', 'x': 0.375, 'y': 0.2, 'width': 0.25, 'height': 0.15, 'color': colors[4],
     'items': ['Dashboard', 'Chat', 'Portfolio', 'Alerts']}
]

# Add component boxes
for comp in components:
    # Main component box
    fig.add_shape(
        type="rect",
        x0=comp['x'], y0=comp['y'], x1=comp['x']+comp['width'], y1=comp['y']+comp['height'],
        fillcolor=comp['color'], opacity=0.3,
        line=dict(color=comp['color'], width=2)
    )
    
    # Component title
    fig.add_annotation(
        x=comp['x'] + comp['width']/2, y=comp['y'] + comp['height'] - 0.02,
        text=f"<b>{comp['name']}</b>", showarrow=False,
        font=dict(size=14, color='black'), xanchor='center'
    )
    
    # Component items
    for i, item in enumerate(comp['items']):
        fig.add_annotation(
            x=comp['x'] + comp['width']/2, 
            y=comp['y'] + comp['height'] - 0.05 - (i+1)*0.025,
            text=item, showarrow=False,
            font=dict(size=10, color='black'), xanchor='center'
        )

# Add arrows for data flows
arrows = [
    # Data Sources -> Pipeline
    {'x0': 0.4, 'y0': 0.8, 'x1': 0.45, 'y1': 0.65, 'label': 'Live streams'},
    
    # Pipeline -> AI Agents  
    {'x0': 0.55, 'y0': 0.65, 'x1': 0.6, 'y1': 0.8, 'label': 'Processed data'},
    
    # AI Agents -> API Layer
    {'x0': 0.725, 'y0': 0.8, 'x1': 0.725, 'y1': 0.65, 'label': 'Insights'},
    
    # API Layer -> Frontend UI
    {'x0': 0.6, 'y0': 0.5, 'x1': 0.55, 'y1': 0.35, 'label': 'JSON response'},
    
    # API Layer -> Pipeline (feedback loop)
    {'x0': 0.6, 'y0': 0.55, 'x1': 0.5, 'y1': 0.55, 'label': 'User queries'}
]

for arrow in arrows:
    # Arrow line
    fig.add_annotation(
        x=arrow['x1'], y=arrow['y1'], ax=arrow['x0'], ay=arrow['y0'],
        xref='x', yref='y', axref='x', ayref='y',
        arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='#333333'
    )
    
    # Arrow label
    mid_x = (arrow['x0'] + arrow['x1']) / 2
    mid_y = (arrow['y0'] + arrow['y1']) / 2
    fig.add_annotation(
        x=mid_x, y=mid_y + 0.03,
        text=arrow['label'], showarrow=False,
        font=dict(size=9, color='#333333'), 
        bgcolor='white', bordercolor='#333333', borderwidth=1
    )

# Update layout
fig.update_layout(
    title="Fintech RAG Copilot Architecture",
    showlegend=False,
    xaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save as PNG and SVG
fig.write_image('architecture.png')
fig.write_image('architecture.svg', format='svg')

print("Architecture diagram created successfully")