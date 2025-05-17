from flask import render_template
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from models.data_model import ConsultaDatos
import json
import requests

""" Gráfico de líneas: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año. """
def line_chart():
    df = ConsultaDatos("concat(Anio,'-',Mes) as Periodo, Count(CodigoMuerte) as TotalMuertes", "NoFetal", "", "Anio, Mes")
    df = df.rename(columns=
                        {
                            0: "Periodo",
                            1: "TotalMuertes"
                        }
                    )
    fig = px.line(
        df,
        x="Periodo",
        y="TotalMuertes",
        title="Total de Muertes por Mes en Colombia",
        markers=True,
        labels={"TotalMuertes": "Muertes", "Periodo": "Periodo"},
    )

    fig.update_layout(
        xaxis_title="Periodo",
        yaxis_title="Número de Muertes",
        title_x=0.5
    )


    return pio.to_html(fig, full_html=False)

def bar_chart():
    df = ConsultaDatos("NoFetal.CodigoDane, Divipola.DescripcionMpo, Count(CodigoMuerte) as TotalMuertes", "NoFetal INNER JOIN Divipola ON Divipola.CodigoDane = NoFetal.CodigoDane", "substr(CodigoMuerte,1,3)='X95'", "NoFetal.CodigoDane, Divipola.DescripcionMpo ORDER BY TotalMuertes DESC limit 5")
    df = df.rename(columns=
                        {
                            0: "CodigoDane",
                            1: "DescripcionMpo",
                            2: "TotalMuertes"
                        }
                    )
    
    fig = px.bar(df, x="DescripcionMpo", y="TotalMuertes", title="Total de Muertes por Ciudad (Top 5)", text="TotalMuertes")

    fig.update_layout(
        xaxis_title="Municipio",
        yaxis_title="Número de Muertes",
        title_x=0.5
    )
    return pio.to_html(fig, full_html=False)

def map_chart():
    df = ConsultaDatos(
        "DescripcionDpto, COUNT(CodigoMuerte)",
        "NoFetal INNER JOIN (SELECT DescripcionDpto, CodigoDpto FROM Divipola GROUP BY 1, 2) A USING(CodigoDpto)",
        "",
        "1"
    )
    df = df.rename(columns={
                            0: "Departamento", 
                            1: "NumeroMuertes"})
    
    df["Departamento"] = df["Departamento"].str.upper()

    url = "https://raw.githubusercontent.com/santiblanko/colombia.geojson/master/depto.json"
    response = requests.get(url)
    response.raise_for_status()
    try:
        geojson = response.json()
    except ValueError:
        text = response.text
        first = text.find('{')
        geojson = json.loads(text[first:])

    fig = px.choropleth(
        df,
        geojson=geojson,
        featureidkey="properties.NOMBRE_DPT",
        locations="Departamento",
        color="NumeroMuertes",
        color_continuous_scale="Reds",
        labels={"NumeroMuertes": "Nº Muertes"},
        title="Muertes por Departamento en Colombia"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title_x=0.5,
        margin={"r":0, "t":50, "l":0, "b":0}
    )
    return pio.to_html(fig, full_html=False)


def pie_chart():
    df = ConsultaDatos(
        "NoFetal.CodigoDane, Divipola.DescripcionMpo, Count(CodigoMuerte) AS TotalMuertes ",
        "NoFetal INNER JOIN Divipola USING(CodigoDane)",
        "",
        "1, 2 ORDER BY TotalMuertes ASC limit 10"
    )
    df = df.rename(columns={0: "CodigoDane", 1: "Municipio", 2: "TotalMuertes"})

    fig = px.pie(
        df,
        names="Municipio",
        values="TotalMuertes",
        title="Top 10 Municipios Menor Indice Mortalidad"
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_x=0.5)

    return pio.to_html(fig, full_html=False)

def tabla():
    df = ConsultaDatos(
        "CodigoMuerte, DescripcionCIE10, COUNT(*) AS TotalMuertes",
        "NoFetal INNER JOIN CodigosMuerte ON NoFetal.CodigoMuerte = CodigosMuerte.CodigoCIE10",
        "",
        "CodigoMuerte, DescripcionCIE10 ORDER BY TotalMuertes DESC LIMIT 10"
    )
    df = df.rename(columns={0: "Código Muerte", 1: "Descripcion Código Muerte", 2: "Total Muertes"})

    df["Total Muertes"] = df["Total Muertes"].astype(int).apply(lambda x: f"{x:,}".replace(",", "."))

    df.index = range(1, len(df) + 1)
    df.index.name = "No"
    df_reset = df.reset_index()

    html_table = df_reset.to_html(
        classes="table table-striped table-hover",
        index=False,
        border=0
    )

    html_table = html_table.replace("<th>", "<th class=\"text-center\">")

    return html_table


def histograma():
    df = ConsultaDatos(
        "GrupoEdad",
        "NoFetal",
        "",
        ""
    )

    df = df.rename(columns={0: "Edad"})
    df["Edad"] = df["Edad"].astype(int)
    max_age = df["Edad"].max()
    bin_size = 5

    bins = list(range(0, max_age + bin_size, bin_size))
    fig = go.Figure(
        data=[go.Histogram(
            x=df["Edad"],
            xbins=dict(start=0, end=bins[-1], size=bin_size),
            marker_line_width=1,
            marker_line_color="white"
        )]
    )
    fig.update_layout(
        title="Distribución de Edades de Personas Fallecidas",
        xaxis_title="Edad (años)",
        yaxis_title="Número de Fallecimientos",
        bargap=0.1,
        title_x=0.5
    )
    return pio.to_html(fig, full_html=False)


def bar_api():

    df = ConsultaDatos(
        "SUBSTR(DescripcionDpto, 1, 20), CASE WHEN Sexo = 1 THEN 'Masculino' WHEN Sexo = 2 THEN 'Femenino' ELSE 'Otro' END AS Sexo, COUNT(CodigoMuerte) AS TotalMuertes",
        "NoFetal INNER JOIN (SELECT DescripcionDpto, CodigoDpto FROM Divipola GROUP BY 1, 2) A USING(CodigoDpto)",
        "",
        "DescripcionDpto, Sexo"
    )

    df = df.rename(columns={0: "Departamento", 1: "Sexo", 2: "TotalMuertes"})

    fig = px.bar(
        df,
        x="Departamento",
        y="TotalMuertes",
        color="Sexo",
        title="Comparación de Muertes por Sexo en Cada Departamento",
        labels={"TotalMuertes": "Número de Muertes"},
        barmode="stack"
    )
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Departamento",
        yaxis_title="Número de Muertes",
        xaxis_tickangle=-45
    )

    return pio.to_html(fig, full_html=False)








# Mapa: Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.
# Gráfico de líneas: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año.
# Gráfico de barras: Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios (códigos X95, agresión con disparo de armas de fuego y casos no especificados).
# Gráfico circular: Muestra las 10 ciudades con menor índice de mortalidad.
# Tabla: Listado de las 10 principales causas de muerte en Colombia, incluyendo su código, nombre y total de casos (ordenadas de mayor a menor).
# Histograma: Distribución de muertes según rangos de edad quinquenales (0-4, 5-9, …, 85+ años), para identificar edades con mayor incidencia de mortalidad.
# Gráfico de barras apiladas: Comparación del total de muertes por sexo en cada departamento, para analizar diferencias significativas entre géneros.