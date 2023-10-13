import pyodbc


def read_procedure_from_um(ac_type):
    columns = []
    data = []
    try:
        cnxn = pyodbc.connect('DSN=ULP1_GONZO_BRIO#READ;UID=brio#read;PWD=brio#read;DBQ=ULP1_GONZO.WORLD')
        crsr = cnxn.cursor()

        if ac_type == 'all':
            sql = f"""SELECT SSU.PROCDURE.PROCEDURE_ID AS "proc_id",
                                            SSU.PROCDURE.LONG_DESC AS "description",
                                            SSU.PROCDURE.CRAFT_CODE AS "craft_code"
                                     FROM SSU.PROCDURE 
                                     WHERE SSU.PROCDURE.CURR_APPR_REV=1;"""
        else:
            sql = f"""SELECT SSU.PROCDURE.PROCEDURE_ID AS "proc_id",
                                    SSU.PROCDURE.LONG_DESC AS "description",
                                    SSU.PROCDURE.CRAFT_CODE AS "craft_code"
                             FROM SSU.PROCDURE 
                             WHERE SSU.PROCDURE.CURR_APPR_REV=1 AND SSU.PROCDURE."U##PROCEDURE_ID" LIKE '{ac_type}-%';"""
        crsr.execute(sql)
        columns = [x[0] for x in crsr.description]
        data = []

        for i, row in enumerate(crsr.fetchall()):
            temp: dict = dict(zip(columns, row))
            temp['description'] = temp['description'].strip()
            data.append(temp)
        return columns, data, True
    except Exception as e:
        return columns, e, False


read_procedure_from_um('777')
