import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#///////////////////////////
# READ THE DATA AND PROCESS
#///////////////////////////
def fill_name_columns(name_init, column):
    col = column.fillna(0)
    label = str(name_init)
    for i in range(len(col)):
        if col[i] == 0 or col[i] == label:
            col[i] = label
        elif col[i] != 0 and col[i] != label:
            label = col[i]
    return col

def read_and_process_data(filepath, skiprows=[0, 1, 2], last_version=False):
    print("Processing = ", filepath)
    # read the data
    data_raw = pd.read_excel(filepath, skiprows=skiprows)
    # for version 2019-2020
    try:
        data_raw = data_raw.drop("MODALIDAD DE ESTUDIOS", axis=1)
    except:
        data_raw = data_raw
    # process names of columns
    data_raw.rename(columns={data_raw.columns[0]: "State", data_raw.columns[1]: "Municipality",
                             data_raw.columns[2]: "Institute", data_raw.columns[3]: "College",
                             data_raw.columns[4]: "Program"}, inplace=True)

    if last_version == False:
        data_raw = data_raw.rename(columns={"Lugares Ofertados": "Offered_places",
                                            "Solicitudes de Primer Ingreso Hombres": "Applications_First_Entry_Male",
                                            "Solicitudes de Primer Ingreso Mujeres": "Applications_First_Entry_Female",
                                            "Solicitudes de Primer Ingreso": "Applications_First_Entry_Total",
                                            "Primer Ingreso Hombres": "First_Entry_Male",
                                            "Primer Ingreso Mujeres": "First_Entry_Female",
                                            "Primer Ingreso Total": "First_Entry_Total",
                                            "Matrícula Hombres": "Enrollment_Male",
                                            "Matrícula Mujeres": "Enrollment_women",
                                            "Matrícula Total": "Enrollment_Total",
                                            "Egresados Hombres": "All_Graduate_Male",
                                            "Egresados Mujeres": "All_Graduate_Female",
                                            "Egresados Total": "All_Graduate",
                                            "Titulados Hombres": "Graduate_with_Diploma_Male",
                                            "Titulados Mujeres": "Graduate_with_Diploma_Female",
                                            "Titulados Total": "Graduate_with_Diploma_Total"})

        # if last_version==False:
        # drop last value of dataframe (source)
        data_raw = data_raw[:-1]
        # store features
        # features = np.setdiff1d(data_raw.columns, ["State", "Municipality", "Institute", "College", "Program"])
        # create list of  missing values and print proportion of missing values by column
        missing = [[var, data_raw[var].isna().sum() / data_raw.shape[0]] for var in data_raw.iloc[:, 5:] if
                   data_raw[var].isna().sum() > 0]
        if len(missing) >= 1:
            print("Data contains missing values = ", missing)
        else:
            print("Data does not contain missing values.")

        # make a copy
        data = data_raw.copy(deep=True)

        # df_state_level = data[data.State.notnull()] # in case we want state-level
        # fill name of state column
        name_init = data['State'][0]  # initialize with first name
        column = data['State']
        state_column_filled = fill_name_columns(name_init, column)
        data['State'] = state_column_filled

        # fill name of municipality column
        name_init = data['Municipality'][1]  # initialize with first name
        column = data['Municipality']
        mun_column_filled = fill_name_columns(name_init, column)
        data['Municipality'] = mun_column_filled
        # create institute level df
        df_institute_level = data[data.Institute.notnull()]  # .set_index(["State","Municipality"])
        # clean columns
        cols_to_drop = ["College", "Program"]
        df_institute_level.drop([col for col in df_institute_level.columns if col in cols_to_drop], axis=1,
                                inplace=True)

        # fill name of institute column
        name_init = data['Institute'][2]  # 'CENTRO UNIVERSITARIO BRITÁNICO DE MÉXICO'
        column = data['Institute']
        inst_column_filled = fill_name_columns(name_init, column)
        data['Institute'] = inst_column_filled
        # df_college_level = data[data.College.notnull()] # in case we want college-level df

        # fill name of college column
        name_init = data['College'][3]  # 'initialize with first name
        column = data['College']
        coll_column_filled = fill_name_columns(name_init, column)
        data['College'] = coll_column_filled
        # create program level
        df_program_level = data[data.Program.notnull()]

    elif last_version == True:
        # 2019-2020 has different names
        data_raw = data_raw.rename(columns={"Lugares Ofertados Total": "Offered_places",
                                            "Solicitudes de Nuevo Ingreso Hombres": "Applications_First_Entry_Male",
                                            "Solicitudes de Nuevo Ingreso Mujeres": "Applications_First_Entry_Female",
                                            "Solicitudes de Nuevo Ingreso Total": "Applications_First_Entry_Total",
                                            "Nuevo Ingreso Hombres": "First_Entry_Male",
                                            "Nuevo Ingreso Mujeres": "First_Entry_Female",
                                            "Nuevo Ingreso Total": "First_Entry_Total",
                                            "Matrícula Hombres": "Enrollment_Male",
                                            "Matrícula Mujeres": "Enrollment_women",
                                            "Matrícula Total": "Enrollment_Total",
                                            "Egresados Hombres": "All_Graduate_Male",
                                            "Egresados Mujeres": "All_Graduate_Female",
                                            "Egresados Total": "All_Graduate",
                                            "Titulados Hombres": "Graduate_with_Diploma_Male",
                                            "Titulados Mujeres": "Graduate_with_Diploma_Female",
                                            "Titulados Total": "Graduate_with_Diploma_Total"})

        # rearrenge columns (2019-2020 version has different order)
        data_raw = data_raw[['State', 'Municipality', 'Institute', 'College', 'Program', 'Offered_places','Applications_First_Entry_Male',
                             'Applications_First_Entry_Female', 'Applications_First_Entry_Total', 'First_Entry_Male',
                             'First_Entry_Female', 'First_Entry_Total','Enrollment_Male', 'Enrollment_women', 'Enrollment_Total', 'All_Graduate_Male','All_Graduate_Female',
                             'All_Graduate', 'Graduate_with_Diploma_Male', 'Graduate_with_Diploma_Female', 'Graduate_with_Diploma_Total']]

        # drop last 6 values of version 2019-2020
        data_raw = data_raw[:-6]
        # store features
        # features = np.setdiff1d(data_raw.columns, ["State", "Municipality", "Institute", "College", "Program"])
        # create list of  missing values and print proportion of missing values by column
        missing = [[var, data_raw[var].isna().sum() / data_raw.shape[0]] for var in data_raw.iloc[:, 5:] if
                   data_raw[var].isna().sum() > 0]
        if len(missing) >= 1:
            print("Data contains missing values = ", missing)
        else:
            print("Data does not contain missing values.")

        # make a copy
        data = data_raw.copy(deep=True)
        df_program_level = data_raw
        df_institute_level = df_program_level.groupby(
            ["State", "Municipality", "Institute", "College"]).sum().reset_index()
        # clean columns
        cols_to_drop = ["College", "Program"]
        df_institute_level.drop([col for col in df_institute_level.columns if col in cols_to_drop], axis=1,
                                inplace=True)

    # print shape (# of rows, # of columns)
    print("Dimensions of raw  dataframe = ", data_raw.shape)
    print("Dimensions of Institute level dataframe = ", df_institute_level.shape)
    print("Dimensions of program level dataframe = ", df_program_level.shape)
    print("******* done *********")

    return df_institute_level, df_program_level
