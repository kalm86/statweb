import pandas as pd
import sqlite3

def load_data():
    return pd.DataFrame({
        "Fecha": pd.date_range(start="2024-01-01", periods=6, freq="M"),
        "Ventas": [150, 200, 250, 220, 300, 280],
        "Categoría": ["A", "B", "A", "C", "B", "A"],
        "Valor": [100, 200, 150, 300, 250, 180],
        "Latitud": [4.711, 6.252, 10.391, 7.125, 3.437, 11.004],
        "Longitud": [-74.072, -75.574, -75.479, -73.119, -76.522, -74.807]
    })

def loadCodigoMuerte():
    dfCodigoMuerte = pd.read_excel("data/CodigosMuerte.xlsx", sheet_name="Final")
    dfCodigoMuerte = dfCodigoMuerte.rename(
                                            columns={
                                                "Capítulo" : "Capitulo",
                                                "Nombre capítulo" : "DescripcionCapitulo",
                                                "Código de la CIE-10 tres caracteres" : "CodigoCIE3",
                                                "Descripción  de códigos mortalidad a tres caracteres" : "DescripcionCIE3",
                                                "Código de la CIE-10 cuatro caracteres" : "CodigoCIE10",
                                                "Descripcion  de códigos mortalidad a cuatro caracteres" : "DescripcionCIE10"
                                            }
                                    )
    return dfCodigoMuerte

def loadDivipola():
    dfDivipola = pd.read_excel("data/Divipola.xlsx", sheet_name="Hoja1")
    dfDivipola = dfDivipola.rename(
                                        columns={
                                            "COD_DANE" : "CodigoDane",
                                            "COD_DEPARTAMENTO" : "CodigoDpto",
                                            "DEPARTAMENTO" : "DescripcionDpto",
                                            "COD_MUNICIPIO" : "CodigoMpo",
                                            "MUNICIPIO" : "DescripcionMpo",
                                            "FECHA1erFIS" : "Fecha"
                                        }
                                )
    return dfDivipola

def loadNoFetal():
    dfNoFetal = pd.read_excel("data/NoFetal.xlsx", sheet_name="No_Fetales_2019")
    dfNoFetal = dfNoFetal.rename(
                                        columns={
                                            "COD_DANE" : "CodigoDane",
                                            "COD_DEPARTAMENTO" : "CodigoDpto",
                                            "COD_MUNICIPIO" : "CodigoMpo",
                                            "AREA_DEFUNCION" : "AreaDefuncion",
                                            "SITIO_DEFUNCION" : "SitioDefuncion",
                                            "AÑO" : "Anio",
                                            "MES" : "Mes",
                                            "HORA" : "Hora",
                                            "MINUTOS" : "Minutos",
                                            "SEXO" : "Sexo",
                                            "ESTADO_CIVIL" : "EstadoCivil",
                                            "GRUPO_EDAD1" : "GrupoEdad",
                                            "NIVEL_EDUCATIVO" : "NivelEducativo",
                                            "MANERA_MUERTE" : "ManeraMuerte",
                                            "COD_MUERTE" : "CodigoMuerte",
                                            "IDPROFESIONAL" : "IdProfesional",
                                        }
                                )
    															
    return dfNoFetal

def Conectar():
    oConexion = sqlite3.connect("estadisticas_muerte.db")
    return oConexion

def Desconectar(oConexion):
    oConexion.close()

def creaDataWarehouse(df, table_name):
    oConexion = Conectar()
    df.to_sql(table_name, oConexion, if_exists="replace", index=False)
    Desconectar(oConexion)

def ConsultaDatos(cCampos, cTabla, cFiltro, cAgrupacion):
    # Conectar a la base de datos del Data Warehouse
    oConexion = sqlite3.connect("estadisticas_muerte.db")
    qCursor = oConexion.cursor()

    # Realizar una consulta de ejemplo: Obtener datos de calidad del agua
    cSQL = ""
    cSQL = cSQL + "select " + cCampos
    cSQL = cSQL + " from " + cTabla
    if cFiltro != "":
      cSQL = cSQL + " where " + cFiltro
    if cAgrupacion != "":
      cSQL = cSQL + " group by " + cAgrupacion

    qCursor.execute(cSQL)
    oResultados = qCursor.fetchall()
    oConexion.close()

    return pd.DataFrame(oResultados)

def ProcesaDatawarehouse():
    # Cargar los datos desde los archivos Excel
    dfCodigoMuerte = loadCodigoMuerte()
    dfDivipola = loadDivipola()
    dfNoFetal = loadNoFetal()

    # Crear el Data Warehouse
    creaDataWarehouse(dfCodigoMuerte, "CodigosMuerte")
    creaDataWarehouse(dfDivipola, "Divipola")
    creaDataWarehouse(dfNoFetal, "NoFetal")