'''
Esta función extrae data de los archivos excel de la SBS (datos de los bancos). Está hecho de
manera que se extraiga los datos de los respectivos meses y años, además los archivos deben
estar ordenados de la siguiente manera:

|--GetData.py
|--Carpeta_principal
    #Son los años de los cuales uno quiere extraer los valores de la data
    |--2008
        |--archivos_excel_de_cada_mes
    |--2009
        |--archivos_excel_de_cada_mes
'''

import pandas as pd

def get_values(fullpath, months, name_col_val, rows_des, col_compar, year, code_file, header):
    """
    Función principal que extrae los datos de los archivos excel.

    Keyword arguments:

    fullpath: Debe ser la ruta hacia la carpeta donde están todas las carpetas de los años. Variable
    de tipo string.

        Ejemplo:
            mainpath = os.getcwd()
            file_name = Carpeta_princpal
            fullpath = os.join(mainpath, file_name)

    months: Son los meses que se quieren extraer. La SBS tiene sus respectivas abreviaciones para
    cada mes. Variable de tipo List con strings de contenido

    name_col_val: Conjunto de nombres de columnas de las cuales se quiere extraer el valor. Variable
    de tipoList con strings de contenido (nombres de las columnas).

    rows_des: Conjuntos de nombres de filas de las cuales queremos obtener el valor. Variable de
    tipo List con strings de contenido (nombres de las filas).

    col_compar: Nombre de la columna en la que están los valores de "rows_des". Variable de tipo
    string.

    year: Conjunto de los años de los cuales se quieren extraer sus datos. Variable de tipo List con
    contendio strings (año que se desea).

    code_file: Son los códigos con los cuales la SBS identifica cada conjunto de archivos excel.
    Variable de tipo string.

        Ejemplo:
            code_file = 'B-2343-' #Los códigos los puedes observar al descargar cada archivo excel.

    header: Es el número de fila en la que empieza la tabla en el excel (donde empiezan las
    columnas). Variable de tipo int.

    """

    data = {}
    index = []

    for i in rows_des:

        data[i] = []

    for i in range(len(year)):

        filepath = fullpath + '/' + year[i] + '/'

        for j in range(len(months)):

            path = filepath + code_file + months[j] + year[i] + '.XLS'

            index += [months[j]+year[i]]
            df = pd.read_excel(path, header=header, sheet_name=0)
            df = df.dropna(how='all', axis=1)

            for k in range(len(rows_des)):

                try:
                    data[rows_des[k]] += [float(df[name_col_val][df[col_compar] == rows_des[k]])]

                except:
                    data[rows_des[k]] += ['NaN']

    df = pd.DataFrame(data, index=index)

    return df
