import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np
from scipy import stats

COLORS = {
    'BNP Paribas': '#00915A',
    'Société Générale': '#E60028', 
    'Crédit Agricole': '#0E6938',
}

# BENCHMARKS SECTORIELS (European banking averages 2023-2024)
SECTOR_BENCHMARKS = {
    'roe': 0.095,  # 9.5%
    'roa': 0.0035,  # 0.35%
    'profit_margin': 18.5,  # 18.5%
    'leverage_ratio': 14.2,
    'equity_ratio': 6.8,
    'basel3_cet1': 15.5,  # CET1 ratio minimum
    'npl_ratio': 3.2,  # Non-performing loans
}

def load_data():
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
    
    df_complete = df.copy()
    
    return df, df_complete, analyses, latest_year

def generate_detailed_analysis(bank, df, analyses):
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

def forecast_metrics(bank, df, years=3):
    """Projections linéaires de métriques clés"""
    bank_data = df[df['bank'] == bank].sort_values('year')
    
    if len(bank_data) < 2:
        return None
    
    projections = {}
    latest_year = bank_data['year'].max()
    
    for metric in ['roe', 'roa', 'profit_margin', 'leverage_ratio']:
        x = bank_data['year'].values
        y = bank_data[metric].dropna().values
        
        if len(y) < 2:
            continue
        
        try:
            slope, intercept = np.polyfit(x[-len(y):], y, 1)
            future_years = np.arange(latest_year + 1, latest_year + years + 1)
            future_values = slope * future_years + intercept
            projections[metric] = {
                'years': future_years.tolist(),
                'values': future_values.tolist(),
                'trend': 'Hausse' if slope > 0 else 'Baisse'
            }
        except:
            pass
    
    return projections

def create_risk_metrics_section(df):
    """Analyses des risques bancaires"""
    risk_analysis = {}
    
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank].sort_values('year')
        latest = bank_data.iloc[-1]
        
        # Asset Quality Indicators (simulated based on available data)
        roe_std = bank_data['roe'].std()
        volatility_score = 'Élevée' if roe_std > 0.025 else 'Modérée' if roe_std > 0.015 else 'Faible'
        
        # Liquidity proxy (based on equity ratio trend)
        equity_ratio_trend = bank_data['equity_ratio'].iloc[-1] - bank_data['equity_ratio'].iloc[0]
        
        # Solvency assessment
        above_basel3 = latest['equity_ratio'] > SECTOR_BENCHMARKS['basel3_cet1']
        
        risk_analysis[bank] = {
            'volatility': volatility_score,
            'volatility_score': roe_std,
            'leverage_vs_sector': latest['leverage_ratio'] - SECTOR_BENCHMARKS['leverage_ratio'],
            'equity_vs_sector': latest['equity_ratio'] - SECTOR_BENCHMARKS['equity_ratio'],
            'basel3_compliant': above_basel3,
            'equity_trend': 'Positive' if equity_ratio_trend > 0 else 'Négative',
        }
    
    return risk_analysis

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
        xaxis_title='Évolution',
        yaxis_title='ROE',
        height=400, 
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=50, r=20, t=60, b=50),
        font=dict(size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    return fig

def create_growth_charts(df):
    """Graphiques de croissance"""
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Revenus', 'Bénéfice', 'Actifs'),
        horizontal_spacing=0.08
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
                    line=dict(color=COLORS.get(bank, '#000'), width=2),
                    marker=dict(size=6)
                ),
                row=1, col=i
            )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=i)
    
    fig.update_layout(
        title_text="Taux de Croissance Année sur Année (%)",
        height=400,
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=40, r=20, t=80, b=50),
        font=dict(size=10),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(tickfont=dict(size=9))
    fig.update_yaxes(tickfont=dict(size=9))
    return fig

def create_box_plots(df):
    """Box plots pour distribution"""
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('ROE', 'ROA', 'Marge'),
        horizontal_spacing=0.1
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
        title_text="Distribution et Volatilité",
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=20, t=80, b=50),
        font=dict(size=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(tickfont=dict(size=9))
    fig.update_yaxes(tickfont=dict(size=9))
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
    
    categories = ['ROE', 'ROA', 'Marge', 'Equity', 'Solidité']
    
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
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=9)),
            angularaxis=dict(tickfont=dict(size=10))
        ),
        height=450,
        template='plotly_white',
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(size=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
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
            text=bank_data["year"].astype(str).str[-2:],
            textposition="top center",
            textfont=dict(size=9),
            marker=dict(
                size=12,
                color=COLORS.get(bank, '#000'),
                line=dict(width=1, color='white')
            )
        ))
    
    fig.add_vline(x=df["leverage_ratio"].median(), line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=df["roe"].median(), line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Risque-Rendement : ROE vs Levier",
        xaxis_title="Levier",
        yaxis_title="ROE",
        template='plotly_white',
        height=450,
        margin=dict(l=50, r=20, t=60, b=50),
        font=dict(size=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        )
    )
    return fig

def create_sector_comparison(df, latest_year):
    """Comparaison avec benchmarks sectoriels"""
    df_latest = df[df['year'] == latest_year].copy()
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('ROE', 'Levier', 'Equity Ratio'),
        horizontal_spacing=0.12
    )
    
    banks = df_latest['bank'].unique()
    x_pos = list(range(len(banks)))
    
    # ROE comparison
    roe_values = [df_latest[df_latest['bank'] == b]['roe'].values[0] for b in banks]
    fig.add_trace(
        go.Bar(x=banks, y=roe_values, name='Banques', marker_color=[COLORS.get(b, '#000') for b in banks], showlegend=False),
        row=1, col=1
    )
    fig.add_hline(y=SECTOR_BENCHMARKS['roe'], line_dash="dash", line_color="red", 
                  annotation_text="Benchmark Secteur", row=1, col=1)
    
    # Leverage comparison
    lev_values = [df_latest[df_latest['bank'] == b]['leverage_ratio'].values[0] for b in banks]
    fig.add_trace(
        go.Bar(x=banks, y=lev_values, name='Levier', marker_color=[COLORS.get(b, '#000') for b in banks], showlegend=False),
        row=1, col=2
    )
    fig.add_hline(y=SECTOR_BENCHMARKS['leverage_ratio'], line_dash="dash", line_color="red", 
                  annotation_text="Benchmark", row=1, col=2)
    
    # Equity Ratio comparison
    eq_values = [df_latest[df_latest['bank'] == b]['equity_ratio'].values[0] for b in banks]
    fig.add_trace(
        go.Bar(x=banks, y=eq_values, name='Equity Ratio', marker_color=[COLORS.get(b, '#000') for b in banks], showlegend=False),
        row=1, col=3
    )
    fig.add_hline(y=SECTOR_BENCHMARKS['equity_ratio'], line_dash="dash", line_color="red", 
                  annotation_text="Benchmark", row=1, col=3)
    
    fig.update_layout(
        title_text="Benchmark Sectoriels - Performance vs Moyenne Européenne",
        height=450,
        template='plotly_white',
        margin=dict(l=40, r=20, t=80, b=50),
        font=dict(size=10),
    )
    fig.update_yaxes(tickfont=dict(size=9))
    return fig

def create_projections_chart(df):
    """Projections des métriques sur 3 ans"""
    latest_year = df['year'].max()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Projection ROE', 'Projection Levier'),
        horizontal_spacing=0.12
    )
    
    for bank in df['bank'].unique():
        bank_data = df[df['bank'] == bank].sort_values('year')
        
        # ROE historical + projection
        x_hist = bank_data['year'].values
        y_hist = bank_data['roe'].values
        
        if len(x_hist) >= 2:
            slope, intercept = np.polyfit(x_hist, y_hist, 1)
            x_future = np.array([latest_year + 1, latest_year + 2, latest_year + 3])
            y_future = slope * x_future + intercept
            
            # Historical line
            fig.add_trace(
                go.Scatter(x=x_hist, y=y_hist, mode='lines+markers', name=bank, 
                          line=dict(color=COLORS.get(bank, '#000'), width=2),
                          marker=dict(size=6)),
                row=1, col=1
            )
            
            # Projection line
            fig.add_trace(
                go.Scatter(x=x_future, y=y_future, mode='lines+markers', 
                          line=dict(color=COLORS.get(bank, '#000'), width=2, dash='dash'),
                          marker=dict(size=6, symbol='diamond'), showlegend=False),
                row=1, col=1
            )
            
            # Leverage projection
            y_hist_lev = bank_data['leverage_ratio'].values
            y_future_lev = slope * x_future + (y_hist_lev[-1] - slope * latest_year)
            
            fig.add_trace(
                go.Scatter(x=x_hist, y=y_hist_lev, mode='lines+markers', showlegend=False,
                          line=dict(color=COLORS.get(bank, '#000'), width=2),
                          marker=dict(size=6)),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Scatter(x=x_future, y=y_future_lev, mode='lines+markers', 
                          line=dict(color=COLORS.get(bank, '#000'), width=2, dash='dash'),
                          marker=dict(size=6, symbol='diamond'), showlegend=False),
                row=1, col=2
            )
    
    fig.update_layout(
        title_text="Projections 3 ans (tendances linéaires)",
        height=450,
        template='plotly_white',
        hovermode='x unified',
        margin=dict(l=40, r=20, t=80, b=50),
        font=dict(size=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig.update_xaxes(tickfont=dict(size=9))
    fig.update_yaxes(tickfont=dict(size=9))
    return fig

def create_risk_heatmap(df, latest_year, risk_analysis):
    """Heatmap des risques"""
    df_latest = df[df['year'] == latest_year].copy()
    
    metrics = ['roe', 'roa', 'profit_margin', 'leverage_ratio', 'equity_ratio']
    banks = sorted(df_latest['bank'].unique())
    
    # Normalize metrics for heatmap
    z_data = []
    for metric in metrics:
        values = df_latest[metric].values
        normalized = (values - values.min()) / (values.max() - values.min()) if values.max() != values.min() else values
        z_data.append(normalized)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=banks,
        y=['ROE', 'ROA', 'Marge', 'Levier', 'Equity Ratio'],
        colorscale='RdYlGn',
        colorbar=dict(title="Performance<br>(normalisée)"),
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Heatmap des Performances Financières",
        height=400,
        template='plotly_white',
        xaxis_title="Banque",
        yaxis_title="Métrique",
        margin=dict(l=120, r=20, t=60, b=50),
        font=dict(size=11)
    )
    
    return fig


def create_financial_structure_charts(df):
    """Graphiques structure financière"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Levier', 'Equity Ratio', 
                        'Actifs (Mds $)', 'Fonds Propres (Mds $)'),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    for bank in df["bank"].unique():
        bank_data = df[df["bank"] == bank].sort_values("year")
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["leverage_ratio"],
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000')),
                      marker=dict(size=6)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["equity_ratio"],
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000')),
                      marker=dict(size=6)),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["Total Assets"]/1e9,
                      mode='lines+markers', name=bank, showlegend=True,
                      line=dict(color=COLORS.get(bank, '#000')),
                      marker=dict(size=6)),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=bank_data["year"], y=bank_data["Stockholders Equity"]/1e9,
                      mode='lines+markers', name=bank, showlegend=False,
                      line=dict(color=COLORS.get(bank, '#000')),
                      marker=dict(size=6)),
            row=2, col=2
        )
    
    fig.update_layout(
        title_text="Structure Financière",
        height=600,
        template='plotly_white',
        margin=dict(l=40, r=20, t=80, b=50),
        font=dict(size=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5
        )
    )
    fig.update_xaxes(tickfont=dict(size=9))
    fig.update_yaxes(tickfont=dict(size=9))
    return fig

def generate_html():
    """Génère le HTML"""
    print("Chargement des données...")
    df, df_complete, analyses, latest_year = load_data()
    
    print("Analyses détaillées...")
    detailed = {}
    for bank in df['bank'].unique():
        detailed[bank] = generate_detailed_analysis(bank, df, analyses)
    
    print("Analyses des risques...")
    risk_analysis = create_risk_metrics_section(df_complete)
    
    print("Graphiques...")
    fig_roe = create_roe_chart(df)
    fig_growth = create_growth_charts(df_complete)
    fig_box = create_box_plots(df_complete)
    fig_radar = create_radar_chart(df_complete, latest_year)
    fig_risk = create_risk_return_scatter(df_complete)
    fig_structure = create_financial_structure_charts(df_complete)
    fig_benchmark = create_sector_comparison(df_complete, latest_year)
    fig_projection = create_projections_chart(df_complete)
    fig_heatmap = create_risk_heatmap(df_complete, latest_year, risk_analysis)
    
    roe_html = fig_roe.to_html(include_plotlyjs='cdn', div_id="roe-chart")
    growth_html = fig_growth.to_html(include_plotlyjs=False, div_id="growth-chart")
    box_html = fig_box.to_html(include_plotlyjs=False, div_id="box-chart")
    radar_html = fig_radar.to_html(include_plotlyjs=False, div_id="radar-chart")
    risk_html = fig_risk.to_html(include_plotlyjs=False, div_id="risk-chart")
    structure_html = fig_structure.to_html(include_plotlyjs=False, div_id="structure-chart")
    benchmark_html = fig_benchmark.to_html(include_plotlyjs=False, div_id="benchmark-chart")
    projection_html = fig_projection.to_html(include_plotlyjs=False, div_id="projection-chart")
    heatmap_html = fig_heatmap.to_html(include_plotlyjs=False, div_id="heatmap-chart")
    
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
    
    # Tableau données complètes
    data_rows = ""
    for _, row in df_complete.sort_values(['bank', 'year']).iterrows():
        revenue_m = row['Total Revenue'] / 1e6 if pd.notna(row['Total Revenue']) else 0
        income_m = row['Net Income'] / 1e6 if pd.notna(row['Net Income']) else 0
        assets_m = row['Total Assets'] / 1e6 if pd.notna(row['Total Assets']) else 0
        liabilities_m = row['Total Liabilities Net Minority Interest'] / 1e6 if pd.notna(row['Total Liabilities Net Minority Interest']) else 0
        equity_m = row['Stockholders Equity'] / 1e6 if pd.notna(row['Stockholders Equity']) else 0
        
        revenue_growth = f"{row['revenue_growth']:.2f}" if pd.notna(row['revenue_growth']) else "—"
        income_growth = f"{row['net_income_growth']:.2f}" if pd.notna(row['net_income_growth']) else "—"
        assets_growth = f"{row['assets_growth']:.2f}" if pd.notna(row['assets_growth']) else "—"
        
        data_rows += f"""
            <tr>
                <td><strong style="color: {COLORS.get(row['bank'], '#000')}">{row['bank']}</strong></td>
                <td>{int(row['year'])}</td>
                <td>{revenue_m:,.0f}</td>
                <td>{income_m:,.0f}</td>
                <td>{assets_m:,.0f}</td>
                <td>{liabilities_m:,.0f}</td>
                <td>{equity_m:,.0f}</td>
                <td>{row['roe']:.4f}</td>
                <td>{row['roa']:.4f}</td>
                <td>{row['profit_margin']:.2f}</td>
                <td>{row['leverage_ratio']:.2f}</td>
                <td>{row['equity_ratio']:.2f}</td>
                <td>{revenue_growth}</td>
                <td>{income_growth}</td>
                <td>{assets_growth}</td>
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
        
        # Générer paragraphe analytique personnalisé
        roe_trend = "excellente" if bank_analysis['latest_roe'] > 0.10 else "satisfaisante" if bank_analysis['latest_roe'] > 0.08 else "modérée"
        leverage_assessment = "robuste" if bank_analysis['latest_leverage'] < 12 else "équilibrée" if bank_analysis['latest_leverage'] < 15 else "élevée"
        margin_quality = "très performante" if bank_analysis['latest_margin'] > 20 else "solide" if bank_analysis['latest_margin'] > 15 else "en amélioration"
        
        roe_evolution = "amélioration" if bank_analysis['roe_change'] > 0 else "ajustement"
        roe_evolution_detail = f"progression de {abs(bank_analysis['roe_change']):.1f}%" if bank_analysis['roe_change'] > 0 else f"recul de {abs(bank_analysis['roe_change']):.1f}%"
        
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
            
            <div style="background: linear-gradient(to right, #f8fafc, {color}08); padding: 20px; border-radius: 10px; border-left: 3px solid {color}; margin: 20px 0;">
                <p style="color: #1e293b; line-height: 1.8; margin-bottom: 14px;">
                    <strong>{bank}</strong> affiche une <strong>rentabilité {roe_trend}</strong> avec un ROE de <strong>{bank_analysis['latest_roe']:.1%}</strong> 
                    en {latest_year}, reflétant une {roe_evolution} ({roe_evolution_detail}) sur la période analysée. 
                    Ce niveau de performance positionne la banque dans le {"haut" if bank_analysis['latest_roe'] > 0.09 else "milieu" if bank_analysis['latest_roe'] > 0.06 else "bas"} 
                    du spectre de rentabilité du secteur bancaire français.
                </p>
                <p style="color: #1e293b; line-height: 1.8; margin-bottom: 14px;">
                    La <strong>structure financière</strong> de {bank} se caractérise par un ratio de levier <strong>{leverage_assessment}</strong> 
                    de <strong>{bank_analysis['latest_leverage']:.2f}</strong>, indiquant une gestion {"prudente" if bank_analysis['latest_leverage'] < 12 else "équilibrée" if bank_analysis['latest_leverage'] < 15 else "dynamique"} 
                    du capital. La marge bénéficiaire de <strong>{bank_analysis['latest_margin']:.1f}%</strong> témoigne d'une efficacité opérationnelle {margin_quality}, 
                    résultat de l'optimisation des coûts et de la maîtrise du mix produits.
                </p>
                <p style="color: #1e293b; line-height: 1.8; margin: 0;">
                    Le <strong>profil stratégique</strong> de {bank} s'inscrit dans une logique de {analysis['summary']['growth_trend'].lower()} 
                    avec une stabilité {analysis['summary']['stability'].lower()}. Les indicateurs de {latest_year} suggèrent une banque 
                    {"orientée vers la maximisation de la rentabilité" if bank_analysis['latest_roe'] > 0.09 else "focalisée sur la consolidation" if bank_analysis['roe_change'] < 0 else "en phase d'expansion contrôlée"}, 
                    adaptant son modèle opérationnel aux contraintes réglementaires et aux opportunités de marché.
                </p>
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
            margin: -30px auto 30px; max-width: 1200px; position: relative; z-index: 100;
        }}
        .nav-tabs {{ border: none; padding: 0; display: flex; flex-wrap: wrap; }}
        .nav-tabs .nav-link {{
            font-family: 'Outfit', sans-serif; font-weight: 500; color: #64748b;
            border: none; padding: 20px 28px; transition: all 0.3s; cursor: pointer;
            flex: 1; text-align: center; min-width: 180px;
        }}
        .nav-tabs .nav-link:hover {{ color: #6366f1; background: #f8fafc; }}
        .nav-tabs .nav-link.active {{ color: #6366f1; border-bottom: 3px solid #6366f1; font-weight: 600; background: #f8fafc; }}
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
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero-section {{ padding: 40px 0 30px; }}
            .hero-section h1 {{ font-size: 1.8rem; }}
            .hero-section p {{ font-size: 0.95rem; }}
            
            .nav-container {{ 
                margin: -20px 10px 20px; 
                border-radius: 8px;
            }}
            .nav-tabs {{ 
                flex-direction: column;
                align-items: stretch;
            }}
            .nav-tabs .nav-link {{ 
                padding: 16px 20px; 
                font-size: 0.95rem;
                border-bottom: 1px solid #f1f5f9;
                text-align: left;
                min-width: auto;
            }}
            .nav-tabs .nav-link.active {{
                border-bottom: 1px solid #f1f5f9;
                border-left: 4px solid #6366f1;
            }}
            .nav-tabs .nav-link:last-child {{ border-bottom: none; }}
            
            .container {{ padding: 0 15px; }}
            .section {{ padding: 20px; margin: 15px 0; border-radius: 8px; }}
            .section-title {{ font-size: 1.35rem; }}
            
            .metric-grid {{ 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 12px;
            }}
            .metric-box {{ padding: 14px; }}
            .metric-value {{ font-size: 1.3rem; }}
            
            .analysis-header {{ flex-direction: column; align-items: flex-start; }}
            .analysis-icon {{ margin-bottom: 12px; }}
            
            .row > div {{ margin-bottom: 20px; }}
            
            .comparison-table {{ font-size: 0.75rem; }}
            .comparison-table th,
            .comparison-table td {{ padding: 10px 8px; }}
        }}
        
        @media (max-width: 480px) {{
            .hero-section h1 {{ font-size: 1.5rem; }}
            .metric-grid {{ grid-template-columns: 1fr; }}
            .nav-tabs .nav-link {{ padding: 14px 16px; font-size: 0.85rem; }}
        }}
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
                    <a class="nav-link" data-page="risques"><i class="fas fa-exclamation-triangle"></i> Risques & Solidité</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="projections"><i class="fas fa-chart-line"></i> Projections 3 Ans</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="donnees"><i class="fas fa-table"></i> Données</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-page="methodologie"><i class="fas fa-book"></i> Méthodologie</a>
                </li>
            </ul>
        </div>
        
        <div class="page-section active" id="synthese">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-star"></i> Synthèse Exécutive</h2>
                
                <div style="background: linear-gradient(to right, #f8fafc, #eff6ff); padding: 24px; border-radius: 12px; border-left: 4px solid #6366f1; margin-bottom: 32px;">
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin-bottom: 16px;">
                        Cette analyse approfondie examine la <strong>performance financière</strong> des trois plus grandes banques françaises 
                        sur la période <strong>{df['year'].min()}-{latest_year}</strong>. L'étude s'appuie sur 8 indicateurs clés regroupés en trois axes : 
                        <strong>rentabilité</strong> (ROE, ROA, marge bénéficiaire), <strong>solidité financière</strong> (levier, equity ratio) 
                        et <strong>dynamique de croissance</strong> (revenus, bénéfices, actifs).
                    </p>
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin-bottom: 16px;">
                        Le secteur bancaire français fait face à des <strong>défis structurels</strong> : taux d'intérêt bas prolongés, 
                        transformation digitale accélérée, et renforcement des exigences réglementaires (Bâle III). Dans ce contexte, 
                        les banques ont dû <strong>optimiser leur efficacité opérationnelle</strong> tout en maintenant des ratios de solvabilité robustes.
                    </p>
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin: 0;">
                        Les résultats révèlent des <strong>stratégies différenciées</strong> : certaines banques privilégient la croissance organique 
                        avec un levier modéré, tandis que d'autres optimisent leur rentabilité via une gestion plus active du capital. 
                        Cette diversité de profils offre aux investisseurs et analystes un <strong>spectre complet</strong> du paysage bancaire français.
                    </p>
                </div>
                
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
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 32px 0 16px;"><i class="fas fa-chart-line" style="color: #6366f1; margin-right: 8px;"></i>Évolution du ROE</h3>
                <p style="color: #64748b; line-height: 1.7;">
                    Le <strong>Return on Equity (ROE)</strong> mesure la rentabilité des capitaux propres. 
                    Un ROE > 10% est considéré comme excellent dans le secteur bancaire. Ce graphique permet 
                    d'identifier les tendances à long terme et les points d'inflexion stratégiques.
                </p>
                {roe_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-chart-bar" style="color: #6366f1; margin-right: 8px;"></i>Analyse des Taux de Croissance</h3>
                <p style="color: #64748b; line-height: 1.7;">
                    La croissance des revenus, du bénéfice net et des actifs révèle la <strong>dynamique</strong> 
                    et la <strong>résilience</strong> de chaque banque. Une croissance du bénéfice supérieure à 
                    celle des revenus indique une amélioration de l'efficacité opérationnelle.
                </p>
                {growth_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-chart-area" style="color: #6366f1; margin-right: 8px;"></i>Distribution et Volatilité</h3>
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
                
                <div style="background: #f8fafc; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 32px;">
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.02rem; margin-bottom: 16px;">
                        Cette section compare les <strong>performances relatives</strong> des trois banques selon une approche multi-dimensionnelle. 
                        Au-delà des chiffres bruts, l'analyse révèle les <strong>arbitrages stratégiques</strong> entre rentabilité, risque et croissance 
                        que chaque établissement a effectués.
                    </p>
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.02rem; margin: 0;">
                        Le <strong>ROE</strong> (Return on Equity) est l'indicateur phare pour les investisseurs, mesurant la capacité à générer des profits 
                        avec les fonds propres. Le <strong>levier financier</strong> amplifie cette rentabilité mais accroît la vulnérabilité aux chocs. 
                        L'<strong>équilibre entre ces deux dimensions</strong> définit le profil risque-rendement de chaque banque.
                    </p>
                </div>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 16px;">Tableau Comparatif {latest_year}</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Les données ci-dessous présentent un <strong>instantané</strong> de la situation financière la plus récente. 
                    Observer l'<strong>écart entre ROE et ROA</strong> permet d'évaluer l'effet du levier : un écart important 
                    indique un usage intensif de l'endettement pour booster la rentabilité des capitaux propres.
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
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-bullseye" style="color: #6366f1; margin-right: 8px;"></i>Performance Multi-dimensionnelle</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Le graphique radar offre une <strong>vue d'ensemble synthétique</strong> en comparant 
                    simultanément 5 dimensions de performance. Plus la surface couverte est grande, meilleure 
                    est la performance globale. Un profil équilibré indique une performance homogène.
                </p>
                {radar_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-balance-scale" style="color: #6366f1; margin-right: 8px;"></i>Trade-off Risque-Rendement</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Ce graphique illustre le <strong>compromis fondamental</strong> entre risque (levier) et 
                    rendement (ROE). Les lignes médianes divisent l'espace en 4 quadrants stratégiques :
                </p>
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <ul style="list-style: none; padding: 0;">
                        <li style="padding: 8px 0;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i><strong>Haut-Gauche</strong> : ROE élevé + Levier faible = Profil idéal</li>
                        <li style="padding: 8px 0;"><i class="fas fa-exclamation-triangle" style="color: #f59e0b; margin-right: 8px;"></i><strong>Haut-Droit</strong> : ROE élevé + Levier élevé = Performance forte mais risquée</li>
                        <li style="padding: 8px 0;"><i class="fas fa-info-circle" style="color: #3b82f6; margin-right: 8px;"></i><strong>Bas-Gauche</strong> : ROE faible + Levier faible = Prudent, potentiel de développement</li>
                        <li style="padding: 8px 0;"><i class="fas fa-times-circle" style="color: #ef4444; margin-right: 8px;"></i><strong>Bas-Droit</strong> : ROE faible + Levier élevé = Situation à risque</li>
                    </ul>
                </div>
                {risk_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-university" style="color: #6366f1; margin-right: 8px;"></i>Structure Financière et Solidité</h3>
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
        
        <div class="page-section" id="risques">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-exclamation-triangle"></i> Analyse des Risques & Solidité Bancaire</h2>
                
                <div style="background: linear-gradient(to right, #f8fafc, #fef3c7); padding: 24px; border-radius: 12px; border-left: 4px solid #f59e0b; margin-bottom: 32px;">
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin-bottom: 16px;">
                        Beyond raw profitability, a bank's <strong>risk management capabilities</strong> are fundamental to its long-term health. 
                        Cette section examine la <strong>stabilité financière</strong>, l'<strong>adéquation du capital</strong> et les <strong>profils de risque</strong> 
                        selon les normes réglementaires internationales (Bâle III).
                    </p>
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin: 0;">
                        Les indicateurs clés incluent : volatilité des rendements (stabilité), ratio de levier vs benchmark sectoriel, 
                        compliance aux exigences de capitalisation minimum, et tendances de l'equity ratio.
                    </p>
                </div>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 16px;"><i class="fas fa-chart-bar" style="color: #f59e0b; margin-right: 8px;"></i>Benchmark Sectoriels (Moyenne Bancaire Européenne)</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    La comparaison avec les benchmarks sectoriels permet de <strong>contextualiser la performance</strong>. 
                    Les seuils ci-dessous reflètent les normes de solidité financière du secteur bancaire européen 2023-2024.
                </p>
                {benchmark_html}
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin: 40px 0 16px;"><i class="fas fa-fire" style="color: #ef4444; margin-right: 8px;"></i>Heatmap des Performances</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    La heatmap normalise tous les indicateurs (0-1) pour permettre une comparaison visuelle rapide. 
                    Les teintes <strong>vertes</strong> indiquent une performance <strong>supérieure</strong>, les teintes <strong>rouges</strong> une performance <strong>inférieure</strong>.
                </p>
                {heatmap_html}
                
                <div class="row" style="margin-top: 32px;">
                    <div class="col-md-6">
                        <div class="section" style="background: linear-gradient(135deg, #fef3c7, #ffe4e6);">
                            <h4 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 16px;">
                                <i class="fas fa-shield-alt" style="color: #f59e0b;"></i> Profils de Risque
                            </h4>
                            <div style="background: white; padding: 16px; border-radius: 8px; margin-bottom: 12px;">
                                <p style="margin: 0; font-weight: 600; color: #1e293b;"><i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i>BNP Paribas</p>
                                <p style="margin: 8px 0 0; font-size: 0.9rem; color: #64748b;">
                                    Volatilité: {risk_analysis['BNP Paribas']['volatility']}<br/>
                                    Levier vs Secteur: {risk_analysis['BNP Paribas']['leverage_vs_sector']:+.2f}<br/>
                                    Bâle III: {'✓ Conforme' if risk_analysis['BNP Paribas']['basel3_compliant'] else '✗ Attention'}
                                </p>
                            </div>
                            <div style="background: white; padding: 16px; border-radius: 8px; margin-bottom: 12px;">
                                <p style="margin: 0; font-weight: 600; color: #1e293b;"><i class="fas fa-check-circle" style="color: #ef4444; margin-right: 8px;"></i>Société Générale</p>
                                <p style="margin: 8px 0 0; font-size: 0.9rem; color: #64748b;">
                                    Volatilité: {risk_analysis['Société Générale']['volatility']}<br/>
                                    Levier vs Secteur: {risk_analysis['Société Générale']['leverage_vs_sector']:+.2f}<br/>
                                    Bâle III: {'✓ Conforme' if risk_analysis['Société Générale']['basel3_compliant'] else '✗ Attention'}
                                </p>
                            </div>
                            <div style="background: white; padding: 16px; border-radius: 8px;">
                                <p style="margin: 0; font-weight: 600; color: #1e293b;"><i class="fas fa-check-circle" style="color: #0E6938; margin-right: 8px;"></i>Crédit Agricole</p>
                                <p style="margin: 8px 0 0; font-size: 0.9rem; color: #64748b;">
                                    Volatilité: {risk_analysis['Crédit Agricole']['volatility']}<br/>
                                    Levier vs Secteur: {risk_analysis['Crédit Agricole']['leverage_vs_sector']:+.2f}<br/>
                                    Bâle III: {'✓ Conforme' if risk_analysis['Crédit Agricole']['basel3_compliant'] else '✗ Attention'}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="section" style="background: linear-gradient(135deg, #f0fdf4, #eff6ff);">
                            <h4 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 16px;">
                                <i class="fas fa-lightbulb" style="color: #3b82f6;"></i> AI & Tech Impact
                            </h4>
                            <p style="color: #1e293b; line-height: 1.7; margin-bottom: 16px;">
                                Le secteur bancaire intègre rapidement l'<strong>intelligence artificielle</strong> pour améliorer l'efficacité opérationnelle 
                                et la détection des risques.
                            </p>
                            <ul style="list-style: none; padding: 0;">
                                <li style="padding: 8px 0; border-bottom: 1px solid #e2e8f0;"><i class="fas fa-arrow-right" style="color: #3b82f6; margin-right: 8px;"></i><strong>Détection de fraude:</strong> ML réduirait NPL</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #e2e8f0;"><i class="fas fa-arrow-right" style="color: #3b82f6; margin-right: 8px;"></i><strong>Scoring crédit:</strong> IA améliore la qualité</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #e2e8f0;"><i class="fas fa-arrow-right" style="color: #3b82f6; margin-right: 8px;"></i><strong>Analyse prédictive:</strong> Forecast résilience</li>
                                <li style="padding: 8px 0;"><i class="fas fa-arrow-right" style="color: #3b82f6; margin-right: 8px;"></i><strong>Automatisation:</strong> Réduit coûts opérationnels</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="alert alert-warning" style="background: #fef3c7; border: 1px solid #f59e0b; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 20px; margin-top: 24px;">
                    <h4 style="color: #92400e; margin-bottom: 12px;"><i class="fas fa-exclamation-triangle"></i> Réglementation Bâle III</h4>
                    <p style="color: #92400e; margin-bottom: 12px; line-height: 1.7;">
                        <strong>Common Equity Tier 1 (CET1) Ratio:</strong> Minimum 4.5% pour absorber les pertes. 
                        Les banques françaises doivent également maintenir un <strong>Leverage Ratio > 3%</strong> (limite d'endettement absolu).
                    </p>
                    <p style="color: #92400e; margin: 0; line-height: 1.7;">
                        <strong>Implication:</strong> Une banque avec equity ratio > 6% et levier < 15 affiche une <strong>solidité robuste</strong> 
                        et une faible probabilité de défaut.
                    </p>
                </div>
            </div>
        </div>
        
        <div class="page-section" id="projections">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-chart-line"></i> Projections à 3 Ans & Tendances Futures</h2>
                
                <div style="background: linear-gradient(to right, #f8fafc, #f0fdf4); padding: 24px; border-radius: 12px; border-left: 4px solid #10b981; margin-bottom: 32px;">
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin-bottom: 16px;">
                        Bien que les prévisions passées ne garantissent pas les résultats futurs, les <strong>tendances linéaires</strong> 
                        permettent d'identifier les <strong>trajectoires actuelles</strong> de chaque banque. Cette analyse extrapole les données historiques 
                        (2021-2024) sur les <strong>3 prochaines années</strong> (2025-2027) sous l'hypothèse de continuité.
                    </p>
                    <p style="color: #1e293b; line-height: 1.8; font-size: 1.05rem; margin: 0;">
                        <i class="fas fa-info-circle" style="color: #10b981; margin-right: 8px;"></i>
                        <strong>Attention:</strong> Ces projections sont illustratives et doivent être complétées par une analyse qualitative 
                        (facteurs macro-économiques, changements réglementaires, transformations stratégiques).
                    </p>
                </div>
                
                <h3 style="font-size: 1.3rem; font-weight: 600; margin-bottom: 16px;"><i class="fas fa-chart-line" style="color: #10b981; margin-right: 8px;"></i>Projections ROE et Levier (Lignes Pleines = Historique, Pointillés = Projection)</h3>
                <p style="color: #64748b; line-height: 1.7; margin-bottom: 20px;">
                    Les projections utilisent une <strong>régression linéaire simple</strong> basée sur la tendance 2021-2024. 
                    Une projection en <strong>hausse du ROE</strong> indique une amélioration attendue de la rentabilité. 
                    Une projection en <strong>baisse du levier</strong> suggère une dé-risquification progressive.
                </p>
                {projection_html}
                
                <div class="row" style="margin-top: 32px;">
                    <div class="col-md-6">
                        <div class="section" style="background: #f0fdf4;">
                            <h4 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 16px;">
                                <i class="fas fa-chart-line" style="color: #10b981;"></i> Scénarios Positifs
                            </h4>
                            <ul style="list-style: none; padding: 0;">
                                <li style="padding: 8px 0; border-bottom: 1px solid #d1fae5;"><i class="fas fa-check" style="color: #10b981; margin-right: 8px;"></i>Amélioration ROE persistante</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #d1fae5;"><i class="fas fa-check" style="color: #10b981; margin-right: 8px;"></i>Compression des coûts opérationnels</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #d1fae5;"><i class="fas fa-check" style="color: #10b981; margin-right: 8px;"></i>Valorisation croissante des actifs</li>
                                <li style="padding: 8px 0;"><i class="fas fa-check" style="color: #10b981; margin-right: 8px;"></i>Retournement des taux d'intérêt</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="section" style="background: #fef2f2;">
                            <h4 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 16px;">
                                <i class="fas fa-warning" style="color: #ef4444;"></i> Risques Potentiels
                            </h4>
                            <ul style="list-style: none; padding: 0;">
                                <li style="padding: 8px 0; border-bottom: 1px solid #fee2e2;"><i class="fas fa-times" style="color: #ef4444; margin-right: 8px;"></i>Récession économique globale</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #fee2e2;"><i class="fas fa-times" style="color: #ef4444; margin-right: 8px;"></i>Hausse des défauts de crédit (NPL)</li>
                                <li style="padding: 8px 0; border-bottom: 1px solid #fee2e2;"><i class="fas fa-times" style="color: #ef4444; margin-right: 8px;"></i>Réglementation plus stricte (Bâle IV)</li>
                                <li style="padding: 8px 0;"><i class="fas fa-times" style="color: #ef4444; margin-right: 8px;"></i>Concurrence accrue (fintech, néobanques)</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="page-section" id="donnees">
            <div class="section">
                <h2 class="section-title"><i class="fas fa-table"></i> Données Financières Complètes</h2>
                
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-left: 3px solid #6366f1; margin-bottom: 24px;">
                    <p style="color: #1e293b; line-height: 1.7; margin: 0;">
                        Ce tableau présente l'ensemble des <strong>données brutes</strong> utilisées pour cette analyse, 
                        couvrant la période <strong>{df['year'].min()}-{latest_year}</strong> pour les trois banques. 
                        Les montants financiers sont exprimés en <strong>dollars US</strong>, les ratios en <strong>valeurs décimales</strong>, 
                        et les taux de croissance en <strong>pourcentage</strong>.
                    </p>
                </div>
                
                <div style="overflow-x: auto;">
                    <table class="comparison-table" style="font-size: 0.85rem;">
                        <thead>
                            <tr>
                                <th style="min-width: 120px;">Banque</th>
                                <th style="min-width: 80px;">Année</th>
                                <th style="min-width: 140px;">Revenus Totaux (M$)</th>
                                <th style="min-width: 140px;">Bénéfice Net (M$)</th>
                                <th style="min-width: 140px;">Actifs Totaux (M$)</th>
                                <th style="min-width: 140px;">Passifs (M$)</th>
                                <th style="min-width: 140px;">Capitaux Propres (M$)</th>
                                <th style="min-width: 100px;">ROE</th>
                                <th style="min-width: 100px;">ROA</th>
                                <th style="min-width: 110px;">Marge (%)</th>
                                <th style="min-width: 100px;">Levier</th>
                                <th style="min-width: 120px;">Equity Ratio (%)</th>
                                <th style="min-width: 130px;">Croiss. Revenus (%)</th>
                                <th style="min-width: 140px;">Croiss. Bénéfice (%)</th>
                                <th style="min-width: 130px;">Croiss. Actifs (%)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {data_rows}
                        </tbody>
                    </table>
                </div>
                
                <div style="background: #eff6ff; padding: 16px; border-radius: 10px; border-left: 3px solid #3b82f6; margin-top: 24px;">
                    <p style="color: #1e40af; margin: 0; line-height: 1.7;\">
                        <i class=\"fas fa-info-circle\" style=\"margin-right: 8px;\"></i>
                        <strong>Note :</strong> Les valeurs monétaires sont exprimées en millions de dollars US. 
                        Les ratios ROE et ROA sont des décimales (ex: 0.0805 = 8.05%). 
                        Les croissances marquées "—" correspondent à la première année (2021) sans référence antérieure.
                    </p>
                </div>
            </div>
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
                            <div style="font-size: 1.5rem; margin-bottom: 12px;"><i class="fas fa-chart-line" style="color: #6366f1;"></i></div>
                            <h5 style="font-weight: 600; margin-bottom: 8px;">Rentabilité</h5>
                            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">
                                ROE et ROA mesurent l'efficacité à générer des profits. 
                                Comparer à la moyenne historique et aux concurrents.
                            </p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-box">
                            <div style="font-size: 1.5rem; margin-bottom: 12px;"><i class="fas fa-shield-alt" style="color: #6366f1;"></i></div>
                            <h5 style="font-weight: 600; margin-bottom: 8px;">Solidité</h5>
                            <p style="font-size: 0.9rem; color: #64748b; margin: 0;">
                                Levier et Equity Ratio évaluent la structure financière. 
                                Un levier faible réduit le risque de solvabilité.
                            </p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="metric-box">
                            <div style="font-size: 1.5rem; margin-bottom: 12px;"><i class="fas fa-chart-bar" style="color: #6366f1;"></i></div>
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
        <h4><i class="fas fa-chart-line"></i> Dashboard Financier</h4>
        <p>Analyse des Banques Françaises</p>
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
    
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"{'='*60}")
    print(f"Dashboard généré: {output_file}")
    print(f"{'='*60}")
    
    return output_file

if __name__ == "__main__":
    generate_html()
