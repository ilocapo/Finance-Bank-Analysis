"""
Dashboard multi-pages professionnel
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# Couleurs
COLORS = {
    'BNP Paribas': '#00915A',
    'Société Générale': '#E60028', 
    'Crédit Agricole': '#0E6938',
}

def load_data():
    """Charge et analyse les données"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'banques_financials_complete.csv')
    
    df = pd.read_csv(data_path, index_col=0)
    df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
    
    latest_year = df['year'].max()
    
    # Analyses par banque
    analyses = {}
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank].sort_values('year')
        latest = bank_data[bank_data['year'] == latest_year].iloc[0]
        
        avg_roe = bank_data['roe'].mean()
        roe_change = ((bank_data['roe'].iloc[-1] / bank_data['roe'].iloc[0]) - 1) * 100
        
        analyses[bank] = {
            'latest_roe': latest['roe'],
            'latest_roa': latest['roa'],
            'latest_margin': latest['profit_margin'],
            'latest_leverage': latest['leverage_ratio'],
            'avg_roe': avg_roe,
            'roe_change': roe_change,
        }
    
    # df_complete avec toutes les colonnes (incluant les croissances)
    df_complete = df.copy()
    
    return df, df_complete, analyses, latest_year

def generate_detailed_analysis(bank, df, analyses):
    """Analyse détaillée par banque"""
    bank_data = df[df['bank'] == bank].sort_values('year')
    analysis = analyses[bank]
    
    strengths = []
    weaknesses = []
    
    if analysis['latest_roe'] > analysis['avg_roe']:
        strengths.append(f"ROE supérieur à la moyenne historique ({analysis['latest_roe']:.3f} vs {analysis['avg_roe']:.3f})")
    else:
        weaknesses.append(f"ROE en baisse par rapport à la moyenne historique")
    
    if analysis['roe_change'] > 0:
        strengths.append(f"Amélioration du ROE de {abs(analysis['roe_change']):.1f}% sur la période")
    else:
        weaknesses.append(f"Diminution du ROE de {abs(analysis['roe_change']):.1f}% sur la période")
        
    if analysis['latest_margin'] > 15:
        strengths.append(f"Marge bénéficiaire solide de {analysis['latest_margin']:.1f}%")
    else:
        weaknesses.append(f"Marge bénéficiaire à optimiser ({analysis['latest_margin']:.1f}%)")
    
    if analysis['latest_leverage'] < 12:
        strengths.append(f"Structure financière robuste (levier de {analysis['latest_leverage']:.2f})")
    else:
        weaknesses.append(f"Niveau d'endettement élevé (levier de {analysis['latest_leverage']:.2f})")
    
    # Statut
    summary = {
        'roe_performance': 'Excellente' if analysis['latest_roe'] > analysis['avg_roe'] else 'Modérée',
        'stability': 'Stable' if bank_data['roe'].std() < 0.02 else 'Variable',
        'growth_trend': 'Croissance' if analysis['roe_change'] > 0 else 'Déclin',
        'profitability': 'Forte' if analysis['latest_margin'] > 20 else 'Modérée' if analysis['latest_margin'] > 10 else 'Faible',
    }
    
    recommendations = []
    if analysis['latest_margin'] < 15:
        recommendations.append("Optimiser l'efficacité opérationnelle pour améliorer les marges")
    if analysis['latest_leverage'] > 12:
        recommendations.append("Renforcer les fonds propres pour réduire le risque financier")
    if analysis['roe_change'] < 0:
        recommendations.append("Analyser les facteurs de baisse de rentabilité")
    if not recommendations:
        recommendations.append("Maintenir la trajectoire actuelle")
    
    return {
        'summary': summary,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'recommendations': recommendations
    }

def create_roe_chart(df):
    """Graphique ROE"""
    fig = go.Figure()
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank].sort_values('year')
        fig.add_trace(go.Scatter(
            x=bank_data['year'], y=bank_data['roe'],
            mode='lines+markers', name=bank,
            line=dict(color=COLORS.get(bank, '#000'), width=3),
            marker=dict(size=10)
        ))
    fig.update_layout(
        title='Évolution du Return on Equity (ROE)',
        xaxis_title='Année',
        yaxis_title='ROE',
        height=500, 
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_growth_charts(df):
    """Graphiques de croissance"""
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Croissance des Revenus (%)', 'Croissance du Bénéfice Net (%)', 'Croissance des Actifs (%)')
    )
    
    for i, metric in enumerate([('revenue_growth', 'Revenus'), 
                                 ('net_income_growth', 'Bénéfice Net'),
                                 ('assets_growth', 'Actifs')], 1):
        for bank in df["bank"].unique():
            bank_data = df[df["bank"] == bank].dropna(subset=[metric[0]]).sort_values("year")
            fig.add_trace(
                go.Scatter(
                    x=bank_data["year"],
                    y=bank_data[metric[0]],
                    mode='lines+markers',
                    name=bank,
                    showlegend=(i==1),
                    line=dict(color=COLORS.get(bank, '#000'), width=2)
                ),
                row=1, col=i
            )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=i)
    
    fig.update_layout(
        title_text="Analyse des Taux de Croissance Année sur Année",
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_box_plots(df):
    """Box plots pour distribution"""
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Distribution du ROE', 'Distribution du ROA', 'Distribution de la Marge')
    )
    
    for i, metric in enumerate([('roe', 'ROE'), ('roa', 'ROA'), ('profit_margin', 'Marge (%)')], 1):
        for bank in df["bank"].unique():
            bank_data = df[df["bank"] == bank]
            fig.add_trace(
                go.Box(y=bank_data[metric[0]], name=bank, showlegend=(i==1),
                       marker_color=COLORS.get(bank, '#000')),
                row=1, col=i
            )
    
    fig.update_layout(
        title_text="Distribution des Indicateurs - Analyse de la Volatilité",
        height=500,
        template='plotly_white'
    )
    return fig

def create_radar_chart(df, latest_year):
    """Graphique radar"""
    df_latest = df[df['year'] == latest_year].copy()
    
    def normalize(series):
        return (series - series.min()) / (series.max() - series.min()) if series.max() != series.min() else series
    
    df_latest['roe_norm'] = normalize(df_latest['roe'])
    df_latest['roa_norm'] = normalize(df_latest['roa'])
    df_latest['margin_norm'] = normalize(df_latest['profit_margin'])
    df_latest['equity_norm'] = normalize(df_latest['equity_ratio'])
    df_latest['leverage_norm'] = 1 - normalize(df_latest['leverage_ratio'])
    
    fig = go.Figure()
    
    categories = ['ROE', 'ROA', 'Marge Bénéf.', 'Equity Ratio', 'Solidité (1/Levier)']
    
    for bank in df_latest["bank"].unique():
        bank_data = df_latest[df_latest["bank"] == bank].iloc[0]
        values = [
            bank_data['roe_norm'],
            bank_data['roa_norm'],
            bank_data['margin_norm'],
            bank_data['equity_norm'],
            bank_data['leverage_norm']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=bank,
            line=dict(color=COLORS.get(bank, '#000'), width=2)
        ))
    
    fig.update_layout(
        title=f'Performance Multi-dimensionnelle - {latest_year}',
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=600,
        template='plotly_white'
    )
    return fig

def create_risk_return_scatter(df):
    """Graphique ROE vs Levier"""
    fig = go.Figure()
    
    for bank in df["bank"].unique():
        bank_data = df[df["bank"] == bank].sort_values("year")
        
        fig.add_trace(go.Scatter(
            x=bank_data["leverage_ratio"],
            y=bank_data["roe"],
            mode='markers+text',
            name=bank,
            text=bank_data["year"],
            textposition="top center",
            marker=dict(
                size=12,
                color=COLORS.get(bank, '#000'),
                line=dict(width=2, color='white')
            )
        ))
    
    fig.add_vline(x=df["leverage_ratio"].median(), line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=df["roe"].median(), line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Relation Risque-Rendement : ROE vs Ratio de Levier",
        xaxis_title="Ratio de Levier (Risque →)",
        yaxis_title="ROE (Rendement →)",
        template='plotly_white',
        height=600
    )
    return fig

def create_financial_structure_charts(df):
    """Graphiques structure financière"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Ratio de Levier', 'Equity Ratio (%)', 
                        'Actifs Totaux (Mds €)', 'Capitaux Propres (Mds €)')
    )
    
    for bank in df["bank"].unique():
        bank_data = df[df["bank"] == bank].sort_values("year")
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["leverage_ratio"],
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000'))),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["equity_ratio"],
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000'))),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["Total Assets"]/1e9,
                      mode='lines+markers', name=bank, showlegend=True,
                      line=dict(color=COLORS.get(bank, '#000'))),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["Stockholders Equity"]/1e9,
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000'))),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text="Analyse de la Structure Financière et de la Solidité",
        height=800,
        template='plotly_white'
    )
    return fig

def generate_html():
    """Génère le HTML"""
    print("Chargement des données...")
    df, df_complete, analyses, latest_year = load_data()
    
    print("Analyses détaillées...")
    detailed = {}
    for bank in df['bank'].unique():
        detailed[bank] = generate_detailed_analysis(bank, df, analyses)
    
    print("Graphiques...")
    fig_roe = create_roe_chart(df)
    fig_growth = create_growth_charts(df_complete)
    fig_box = create_box_plots(df_complete)
    fig_radar = create_radar_chart(df_complete, latest_year)
    fig_risk = create_risk_return_scatter(df_complete)
    fig_structure = create_financial_structure_charts(df_complete)
    
    roe_html = fig_roe.to_html(include_plotlyjs='cdn', div_id="roe-chart")
    growth_html = fig_growth.to_html(include_plotlyjs=False, div_id="growth-chart")
    box_html = fig_box.to_html(include_plotlyjs=False, div_id="box-chart")
    radar_html = fig_radar.to_html(include_plotlyjs=False, div_id="radar-chart")
    risk_html = fig_risk.to_html(include_plotlyjs=False, div_id="risk-chart")
    structure_html = fig_structure.to_html(include_plotlyjs=False, div_id="structure-chart")
    
    # Tableau comparaison
    df_latest = df[df['year'] == latest_year]
    table_rows = ""
    for _, row in df_latest.iterrows():
        table_rows += f"""
        <tr>
            <td><strong style="color: {COLORS.get(row['bank'], '#000')}">{row['bank']}</strong></td>
            <td>{row['roe']:.3f}</td>
            <td>{row['roa']:.3f}</td>
            <td>{row['profit_margin']:.2f}%</td>
            <td>{row['leverage_ratio']:.2f}</td>
        </tr>
        """
    
    # Analyses détaillées HTML
    analyses_html = ""
    for bank in sorted(df['bank'].unique()):
        analysis = detailed[bank]
        bank_analysis = analyses[bank]
        color = COLORS.get(bank, '#6366f1')
        
        strengths_html = "".join([f'<div class="strength-item"><i class="fas fa-check-circle"></i> {s}</div>' for s in analysis['strengths']])
        weaknesses_html = "".join([f'<div class="weakness-item"><i class="fas fa-exclamation-circle"></i> {w}</div>' for w in analysis['weaknesses']])
        recommendations_html = "".join([f'<div class="recommendation-item"><i class="fas fa-arrow-right"></i> {r}</div>' for r in analysis['recommendations']])
        
        analyses_html += f"""
        <div class="section">
            <div class="analysis-header">
                <div class="analysis-icon" style="background: {color}20; color: {color};">
                    <i class="fas fa-university"></i>
                </div>
                <div>
                    <h2 style="color: {color}; font-size: 1.75rem; font-weight: 600; margin: 0;">{bank}</h2>
                    <p style="color: #64748b; margin: 4px 0 0;">Analyse Approfondie</p>
                </div>
            </div>
            
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">ROE</div>
                    <div class="metric-value">{bank_analysis['latest_roe']:.3f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">ROA</div>
                    <div class="metric-value">{bank_analysis['latest_roa']:.3f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Marge</div>
                    <div class="metric-value">{bank_analysis['latest_margin']:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Levier</div>
                    <div class="metric-value">{bank_analysis['latest_leverage']:.2f}</div>
                </div>
                <div class="metric-box" style="border-left-color: #10b981;">
                    <div class="metric-label">Performance</div>
                    <div class="metric-value" style="font-size: 1.2rem; color: #10b981;">{analysis['summary']['roe_performance']}</div>
                </div>
                <div class="metric-box" style="border-left-color: #f59e0b;">
                    <div class="metric-label">Tendance</div>
                    <div class="metric-value" style="font-size: 1.2rem; color: #f59e0b;">{analysis['summary']['growth_trend']}</div>
                </div>
            </div>
            
            <div class="row" style="margin-top: 24px;">
                <div class="col-md-6">
                    <h4 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 12px;">
                        <i class="fas fa-thumbs-up" style="color: #10b981;"></i> Points Forts
                    </h4>
                    {strengths_html}
                </div>
                <div class="col-md-6">
                    <h4 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 12px;">
                        <i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i> Points d'Amélioration
                    </h4>
                    {weaknesses_html}
                </div>
            </div>
            
            <h4 style="font-size: 1.1rem; font-weight: 600; margin: 24px 0 12px;">
                <i class="fas fa-lightbulb" style="color: #3b82f6;"></i> Recommandations
            </h4>
            {recommendations_html}
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Financier - Banques Françaises</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fc; color: #1e293b; line-height: 1.6; }}
        .hero-section {{
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
            color: white; padding: 60px 0 40px; text-align: center;
            box-shadow: 0 4px 20px rgba(99,102,241,0.15);
        }}
        .hero-section h1 {{ font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 600; margin-bottom: 12px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 0 20px; }}
        
        .nav-container {{
            background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            margin: -30px auto 30px; max-width: 1200px; position: relative; z-index: 10;
        }}
        .nav-tabs {{ border: none; padding: 0; display: flex; }}
        .nav-tabs .nav-link {{
            font-family: 'Outfit', sans-serif; font-weight: 500; color: #64748b;
            border: none; padding: 20px 28px; transition: all 0.3s; cursor: pointer;
        }}
        .nav-tabs .nav-link:hover {{ color: #6366f1; background: #f8fafc; }}
        .nav-tabs .nav-link.active {{ color: #6366f1; border-bottom: 3px solid #6366f1; font-weight: 600; }}
        .nav-tabs .nav-link i {{ margin-right: 8px; }}
        
        .page-section {{ display: none; animation: fadeIn 0.4s; }}
        .page-section.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        
        .section {{
            background: white; border-radius: 12px; padding: 35px; margin: 20px 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04); border: 1px solid #e2e8f0;
        }}
        .section-title {{
            font-family: 'Outfit', sans-serif; font-size: 1.65rem; font-weight: 600;
            color: #1e293b; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 2px solid #e2e8f0;
        }}
        
        .analysis-header {{ display: flex; align-items: center; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 2px solid #e2e8f0; }}
        .analysis-icon {{
            width: 50px; height: 50px; border-radius: 10px; display: flex;
            align-items: center; justify-content: center; margin-right: 16px; font-size: 1.5rem;
        }}
        
        .metric-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; margin: 20px 0;
        }}
        .metric-box {{
            background: #f8fafc; padding: 18px; border-radius: 10px;
            border-left: 3px solid #6366f1; transition: all 0.3s;
        }}
        .metric-box:hover {{ transform: translateX(5px); background: #eff6ff; }}
        .metric-label {{ font-size: 0.8rem; color: #64748b; text-transform: uppercase; margin-bottom: 8px; }}
        .metric-value {{ font-size: 1.5rem; font-weight: 600; color: #1e293b; font-family: 'Outfit', sans-serif; }}
        
        .strength-item, .weakness-item, .recommendation-item {{
            padding: 12px 16px; margin-bottom: 10px; border-radius: 8px;
            display: flex; align-items: start; font-size: 0.95rem;
        }}
        .strength-item {{ background: #f0fdf4; border-left: 3px solid #10b981; color: #166534; }}
        .weakness-item {{ background: #fef2f2; border-left: 3px solid #ef4444; color: #991b1b; }}
        .recommendation-item {{ background: #eff6ff; border-left: 3px solid #3b82f6; color: #1e40af; }}
        .strength-item i, .weakness-item i, .recommendation-item i {{ margin-right: 10px; margin-top: 2px; }}
        
        .comparison-table {{
            width: 100%; border-collapse: separate; border-spacing: 0; margin: 20px 0;
            background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .comparison-table th {{
            background: #f8fafc; padding: 16px; text-align: left;
            font-weight: 600; color: #1e293b; border-bottom: 2px solid #e2e8f0;
        }}
        .comparison-table td {{ padding: 14px 16px; border-bottom: 1px solid #f1f5f9; }}
        .comparison-table tbody tr:hover {{ background: #f8fafc; }}
        
        .footer {{ background: #1e293b; color: white; text-align: center; padding: 40px 20px; margin-top: 50px; }}
    </style>
</head>
<body>
    
    <div class="hero-section">
        <div class="container">
            <h1><i class="fas fa-chart-line"></i> Dashboard Financier Multi-Pages</h1>
            <p>Analyse Approfondie des Banques Françaises {df['year'].min()} - {latest_year}</p>
        </div>
    </div>
    
    <div class="container">
        
        <div class="nav-container">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-page="synthese"><i class="fas fa-home"></i> Synthèse</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="comparaison"><i class="fas fa-balance-scale"></i> Comparaison</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="analyses"><i class="fas fa-microscope"></i> Analyses Détaillées</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="methodologie"><i class="fas fa-book"></i> Méthodologie</a>
                </li>
            </ul>
        </div>
        
        <div class="page-section active" id="synthese">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-star"></i> Synthèse Exécutive</h2>
                <p>Analyse comparative des 3 principales banques françaises sur la période {df['year'].min()}-{latest_year}.</p>
                
                <div class="metric-grid" style="margin-top: 24px;">
                    <div class="metric-box" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none;">
                        <div class="metric-label" style="color: white; opacity: 0.9;">PÉRIODE</div>
                        <div class="metric-value" style="color: white;">{df['year'].min()} - {latest_year}</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">BANQUES</div>
                        <div class="metric-value">3</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">INDICATEURS</div>
                        <div class="metric-value">8</div>
                    </div>
                </div>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 32px 0 16px;">📈 Évolution du ROE</h3>
                <p style="color: #64748b; line-height: 1.7;">
                    Le <strong>Return on Equity (ROE)</strong> mesure la rentabilité des capitaux propres. 
                    Un ROE > 10% est considéré comme excellent dans le secteur bancaire. Ce graphique permet 
                    d'identifier les tendances à long terme et les points d'inflexion stratégiques.
                </p>
                {roe_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;">📊 Analyse des Taux de Croissance</h3>
                <p style="color: #64748b; line-height: 1.7;">
                    La croissance des revenus, du bénéfice net et des actifs révèle la <strong>dynamique</strong> 
                    et la <strong>résilience</strong> de chaque banque. Une croissance du bénéfice supérieure à 
                    celle des revenus indique une amélioration de l'efficacité opérationnelle.
                </p>
                {growth_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;">📉 Distribution et Volatilité</h3>
                <p style="color: #64748b; line-height: 1.7;">
                    Les box plots révèlent la <strong>consistance</strong> de la performance. Une boîte étroite 
                    indique une performance stable et prévisible, tandis qu'une boîte large suggère une forte 
                    variabilité selon les années.
                </p>
                {box_html}
            </div>
        </div>
        
        <div class="page-section" id="comparaison">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-balance-scale"></i> Analyse Comparative Approfondie</h2>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 16px;">Tableau Comparatif {latest_year}</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Comparaison détaillée des principaux indicateurs de performance et de solidité financière.
                </p>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Banque</th>
                            <th>ROE</th>
                            <th>ROA</th>
                            <th>Marge (%)</th>
                            <th>Levier</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;">🎯 Performance Multi-dimensionnelle</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Le graphique radar offre une <strong>vue d'ensemble synthétique</strong> en comparant 
                    simultanément 5 dimensions de performance. Plus la surface couverte est grande, meilleure 
                    est la performance globale. Un profil équilibré indique une performance homogène.
                </p>
                {radar_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;">⚖️ Trade-off Risque-Rendement</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Ce graphique illustre le <strong>compromis fondamental</strong> entre risque (levier) et 
                    rendement (ROE). Les lignes médianes divisent l'espace en 4 quadrants stratégiques :
                </p>
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <ul style="list-style: none; padding: 0;">
                        <li style="padding: 8px 0;">✅ <strong>Haut-Gauche</strong> : ROE élevé + Levier faible = Profil idéal</li>
                        <li style="padding: 8px 0;">⚠️ <strong>Haut-Droit</strong> : ROE élevé + Levier élevé = Performance forte mais risquée</li>
                        <li style="padding: 8px 0;">📊 <strong>Bas-Gauche</strong> : ROE faible + Levier faible = Prudent, potentiel de développement</li>
                        <li style="padding: 8px 0;">⛔ <strong>Bas-Droit</strong> : ROE faible + Levier élevé = Situation à risque</li>
                    </ul>
                </div>
                {risk_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;">🏛️ Structure Financière et Solidité</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    L'analyse de la structure financière est cruciale pour évaluer la <strong>solidité</strong> 
                    et la <strong>solvabilité</strong> des banques. Le ratio de levier et l'equity ratio sont 
                    des indicateurs clés de la capacité à absorber des chocs économiques (normes Bâle III).
                </p>
                {structure_html}
                
                <div class="alert alert-info" style="background: #eff6ff; border: 1px solid #3b82f6; border-left: 4px solid #3b82f6; border-radius: 10px; padding: 20px; margin-top: 24px;">
                    <h4 style="color: #1e40af; margin-bottom: 12px;"><i class="fas fa-info-circle"></i> Réglementation Bâle III</h4>
                    <p style="color: #1e40af; margin: 0; line-height: 1.7;">
                        Les banques doivent maintenir des ratios de fonds propres minimum pour garantir leur stabilité. 
                        Un <strong>Equity Ratio > 8%</strong> indique une capitalisation forte. Un <strong>levier < 12</strong> 
                        suggère une structure financière robuste avec un risque modéré.
                    </p>
                </div>
            </div>
        </div>
        
        <div class="page-section" id="analyses">
            {analyses_html}
        </div>
        
        <div class="page-section" id="methodologie">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-book"></i> Méthodologie & Interprétation</h2>
                
                <div class="row">
                    <div class="col-md-6">
                        <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 16px;">
                            <i class="fas fa-database" style="color: #6366f1;"></i> Sources de Données
                        </h4>
                        <p><strong>API :</strong> Yahoo Finance via yfinance</p>
                        <p><strong>Type :</strong> Données annuelles officielles (Income Statement & Balance Sheet)</p>
                        <p><strong>Période :</strong> {df['year'].min()} - {latest_year} ({df['year'].max() - df['year'].min() + 1} années)</p>
                        
                        <h4 style="font-size: 1.2rem; font-weight: 600; margin: 24px 0 16px;">
                            <i class="fas fa-calculator" style="color: #6366f1;"></i> Formules de Calcul
                        </h4>
                        <div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-left: 3px solid #6366f1;">
                            <p style="margin-bottom: 12px;"><strong>ROE</strong> = Net Income / Stockholders' Equity</p>
                            <p style="margin-bottom: 12px;"><strong>ROA</strong> = Net Income / Total Assets</p>
                            <p style="margin-bottom: 12px;"><strong>Marge</strong> = (Net Income / Total Revenue) × 100</p>
                            <p style="margin-bottom: 12px;"><strong>Levier</strong> = Total Liabilities / Stockholders' Equity</p>
                            <p style="margin-bottom: 12px;"><strong>Equity Ratio</strong> = (Stockholders' Equity / Total Assets) × 100</p>
                            <p style="margin: 0;"><strong>Croissance</strong> = Variation année sur année (%)</p>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <h4 style="font-size: 1.2rem; font-weight: 600; margin-bottom: 16px;">
                            <i class="fas fa-chart-line" style="color: #6366f1;"></i> Seuils d'Interprétation
                        </h4>
                        
                        <div style="background: #f0fdf4; padding: 16px; border-radius: 10px; border-left: 3px solid #10b981; margin-bottom: 16px;">
                            <p style="font-weight: 600; color: #166534; margin-bottom: 8px;">ROE (Return on Equity)</p>
                            <ul style="margin: 0; padding-left: 20px; color: #166534;">
                                <li>> 10% : Excellent</li>
                                <li>8-10% : Bon</li>
                                <li>5-8% : Acceptable</li>
                                <li>< 5% : Faible</li>
                            </ul>
                        </div>
                        
                        <div style="background: #eff6ff; padding: 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin-bottom: 16px;">
                            <p style="font-weight: 600; color: #1e40af; margin-bottom: 8px;">Ratio de Levier</p>
                            <ul style="margin: 0; padding-left: 20px; color: #1e40af;">
                                <li>< 10 : Très solide</li>
                                <li>10-15 : Équilibré</li>
                                <li>> 15 : Risque élevé</li>
                            </ul>
                        </div>
                        
                        <div style="background: #fef3c7; padding: 16px; border-radius: 10px; border-left: 3px solid #f59e0b; margin-bottom: 16px;">
                            <p style="font-weight: 600; color: #92400e; margin-bottom: 8px;">Equity Ratio</p>
                            <ul style="margin: 0; padding-left: 20px; color: #92400e;">
                                <li>> 8% : Capitalisation forte</li>
                                <li>5-8% : Acceptable</li>
                                <li>< 5% : Vulnérabilité accrue</li>
                            </ul>
                        </div>
                        
                        <div style="background: #f8fafc; padding: 16px; border-radius: 10px; border-left: 3px solid #64748b;">
                            <p style="font-weight: 600; color: #1e293b; margin-bottom: 8px;">Coefficient de Variation (CV)</p>
                            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                                <li>< 20% : Stabilité élevée</li>
                                <li>20-40% : Stabilité modérée</li>
                                <li>> 40% : Forte volatilité</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <h4 style="font-size: 1.2rem; font-weight: 600; margin: 32px 0 16px;">
                    <i class="fas fa-lightbulb" style="color: #6366f1;"></i> Guide d'Analyse
                </h4>
                <div class="row">
                    <div class="col-md-4">
                        <div class="metric-box">
                            <div style="font-size: 1.5rem; margin-bottom: 12px;">📈</div>
                            <h5 style="font-weight: 600; margin-bottom: 8px;">Rentabilité</h5>
                            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">
                                ROE et ROA mesurent l'efficacité à générer des profits. 
                                Comparer à la moyenne historique et aux concurrents.
                            </p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-box">
                            <div style="font-size: 1.5rem; margin-bottom: 12px;">🛡️</div>
                            <h5 style="font-weight: 600; margin-bottom: 8px;">Solidité</h5>
                            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">
                                Levier et Equity Ratio évaluent la structure financière. 
                                Un levier faible réduit le risque de solvabilité.
                            </p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-box">
                            <div style="font-size: 1.5rem; margin-bottom: 12px;">📊</div>
                            <h5 style="font-weight: 600; margin-bottom: 8px;">Croissance</h5>
                            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">
                                Taux de croissance révèlent la dynamique. 
                                Une croissance des bénéfices > revenus = gains d'efficacité.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <h4><i class="fas fa-graduation-cap"></i> Projet Portfolio Data Science</h4>
        <p>Analyse financière approfondie des banques françaises</p>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
                this.classList.add('active');
                document.getElementById(this.getAttribute('data-page')).classList.add('active');
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});
        }});
    </script>
</body>
</html>
"""
    
    # Sauvegarder
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n{'='*60}")
    print(f"✨ Dashboard multi-pages généré: {output_file}")
    print(f"{'='*60}")
    
    return output_file

if __name__ == "__main__":
    generate_html()
