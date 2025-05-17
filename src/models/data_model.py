import pandas as pd
import sqlite3

def loadCodigoMuerte():
    dfCodigoMuerte = pd.read_excel("src/data/CodigosMuerte.xlsx", sheet_name="Final")
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
    dfDivipola = pd.read_excel("src/data/Divipola.xlsx", sheet_name="Hoja1")
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
    dfNoFetal = pd.read_excel("src/data/NoFetal.xlsx", sheet_name="No_Fetales_2019")
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
    oConexion = sqlite3.connect("src/data/estadisticas_muerte.db")
    return oConexion

def Desconectar(oConexion):
    oConexion.close()

def creaDataWarehouse(df, table_name):
    oConexion = Conectar()
    df.to_sql(table_name, oConexion, if_exists="replace", index=False)
    Desconectar(oConexion)

def ConsultaDatos(cCampos, cTabla, cFiltro, cAgrupacion):
    # Conectar a la base de datos del Data Warehouse
    oConexion = Conectar()
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