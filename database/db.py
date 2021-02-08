from PySide2.QtWidgets import QMessageBox, QApplication
from PySide2.QtCore import QObject
from mysql import connector

import sys


class MysqlClient(QObject):
    def __init__(self):
        super(MysqlClient, self).__init__()

        self.db = connector.connect(
            host="127.0.0.1",
            port=3306,
            user="gdcadminuser",
            passwd="GdcAdmin1968",
            database="gdcadmindb"
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.db.close()

    def get_mezonevek(self, table):
        self.cursor.execute(f"describe {table}")
        field_names = self.cursor.fetchall()
        return field_names

    def get_all(self, table):
        """ Tábla tartalmának lekérése ( select * from table)
            Visszaadott érték:
            ha a tábla nem üres: tuple-k listája
            ha a tábla üres: üres lista []
            Ha a tábla nem létezik: None
            A mezőneveket is lekérdezzük, és hozzáfűzzük a 'data' -hoz
            """
        data = []
        if self.exist_table(table):
            self.cursor.execute(f"SELECT * FROM {table}")
            # print(self.cursor.fetchall())

            field_names = [i[0] for i in self.cursor.description]
            adatok = [list(row) for row in self.cursor.fetchall()]

            data.append(adatok)

            data.append(field_names)
            print(data)
            return data

        return None

    def get_active_user(self):
        """ Tábla tartalmának lekérése ( select * from members)
            Visszaadott érték:
            ha a tábla nem üres: tuple-k listája
            ha a tábla üres: üres lista []
            Ha a tábla nem létezik: None
            A mezőneveket is lekérdezzük, és hozzáfűzzük a 'data' -hoz
            """
        data = []
        if self.exist_table("members"):
            self.cursor.execute("SELECT * FROM members WHERE aktiv")
            # print(self.cursor.fetchall())

            field_names = [i[0] for i in self.cursor.description]
            adatok = [list(row)[:-1] for row in self.cursor.fetchall()]

            data.append(adatok)

            data.append(field_names)
            print(data)
            return data

        return None

    def get_one_rekord(self, table, get_id):
        adatok = []
        if self.exist_table(table):
            self.cursor.execute(f"SELECT * FROM {table} WHERE id={get_id}")
            temp_adatok = [self.cursor.fetchone()]
            for i in range(len(temp_adatok[0])):
                adatok.append(temp_adatok[0][i])
            return adatok

        return None

    def update_table(self, table, rekord: list):
        print(rekord)
        sql = f"UPDATE {table} SET "
        all_rows2 = self.get_mezonevek(table)
        for i in range(1, len(all_rows2)):
            sql += f"{all_rows2[i][0]}="
            if "int" in all_rows2[i][1]:
                sql += f"{rekord[i]}, "
            if "varchar" in all_rows2[i][1]:
                sql += f"'{rekord[i]}', "
            if "date" in all_rows2[i][1]:
                sql += f"'{rekord[i]}', "
        sql += f"{all_rows2[0][0]}={rekord[0]}"
        sql += f" WHERE {all_rows2[0][0]}={rekord[0]}"
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return

    def insert_rekord(self, table, rekord: list):
        sql = f"INSERT INTO {table} ("
        all_rows2 = self.get_mezonevek(table)
        # print(all_rows2)
        for i in range(1, len(all_rows2) - 1):
            sql += f"{all_rows2[i][0]}, "
        sql += f"{all_rows2[len(all_rows2) - 1][0]}) VALUES ("
        for i in range(1, len(all_rows2) - 1):
            if "int" in all_rows2[i][1]:
                sql += f"{rekord[i]}, "
            if "decimal" in all_rows2[i][1]:
                sql += f"{rekord[i]}, "
            if "varchar" in all_rows2[i][1]:
                sql += f"'{rekord[i]}', "
            if "date" in all_rows2[i][1]:
                sql += f"'{rekord[i]}', "
        if "int" in all_rows2[len(all_rows2) - 1][1]:
            sql += f"{rekord[len(all_rows2) - 1]} "
        if "decimal" in all_rows2[len(all_rows2) - 1][1]:
            sql += f"{rekord[len(all_rows2) - 1]} "
        if "varchar" in all_rows2[len(all_rows2) - 1][1]:
            sql += f"'{rekord[len(all_rows2) - 1]}' "
        if "date" in all_rows2[len(all_rows2) - 1][1]:
            sql += f"'{rekord[len(all_rows2) - 1]}' "
        sql += ")"
        # print(sql)
        self.cursor.execute(sql)
        self.cursor.execute("SELECT LAST_INSERT_ID()")
        insert_id = self.cursor.fetchall()
        self.db.commit()

        return insert_id[0][0]

    def delete_rekord(self, table, value):
        """ Az átadott rekord_id-ú rekord törlése a table táblából. A táblából meg kell
            határozni az elsődleges kulcsot (egyedi azonosító) és annak típusától függően
            (int vagy str) kell az sql parancsot paraméterezni.  Amikor a view meghívja ezt a metódust,
            akkor átadja az elsődleges kulcsnak megfelelő mező értékét. Ennek vizsgálatával (type() )
            dönthető el, hogy az sql-ben int-ként vagy str-ként kell kezelni."""
        # A tábla elsődleges kulcsának meghatározása
        all_rows2 = self.get_mezonevek(table)
        for row in all_rows2:
            if 'PRI' in row:
                id_name = row[0]
        # Az elsődleges kulcs típusától függően (int vagy str) a törlés végrahajtása
        if type(value) == 'int':
            self.cursor.execute(f"DELETE FROM {table} WHERE {id_name}={value}")
        else:
            self.cursor.execute(f"DELETE FROM {table} WHERE {id_name}='{value}'")
        self.db.commit()

    def exist_table(self, table):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        for tables in rows:
            if table in tables:
                return True

        QMessageBox.about(None, 'Adatok lekérése', 'A megadott tábla nem létezik')
        sys.exit(1)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     client = MysqlClient()
#     client.close()
#     app.exec_()
if __name__ == '__main__':
    import doctest
    doctest.testmod()
