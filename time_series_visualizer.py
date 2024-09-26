import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# Registre conversores de data do Matplotlib
register_matplotlib_converters()

# 1 - Importar os dados e definir o índice para a coluna 'date'
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2 - Limpar os dados filtrando os dias em que as visualizações de página estavam nos 2,5% superiores ou inferiores
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

def draw_line_plot():
    # 3 - Criar um gráfico de linhas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='blue')
    
    # Configurar título e rótulos dos eixos
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar imagem e retornar fig (não mude esta parte)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # 4 - Copiar e modificar dados para gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupar por ano e mês e calcular a média das visualizações
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reordenar os meses para exibir corretamente
    months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
    
    # Desenhar gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar[months_order].plot(kind='bar', ax=ax)

    # Configurar título e rótulos dos eixos
    ax.set_title('Average Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    # Configurar legenda
    ax.legend(title='Months', labels=months_order)

    # Salvar imagem e retornar fig (não mude esta parte)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # 5 - Preparar dados para gráficos de caixa (esta parte já está feita!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Desenhar gráficos de caixa usando Seaborn
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Gráfico de caixa por ano
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    
    # Gráfico de caixa por mês
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2,
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    # Ajustar rótulo do eixo x para "Month"
    ax1.set_xlabel("Year")
    
    # Ajustar rótulo do eixo y para "Page Views"
    ax1.set_ylabel("Page Views")
    ax2.set_ylabel("Page Views")

    # Alterar o rótulo do eixo x do gráfico de meses para "Month"
    ax2.set_xlabel("Month")

    # Salvar imagem e retornar fig (não mude esta parte)
    fig.savefig('box_plot.png')
    return fig

# Não modifique as próximas duas linhas
if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()