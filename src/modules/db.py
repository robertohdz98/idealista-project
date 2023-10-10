""" Module for utils and functions for PostgreSQL interaction"""

import psycopg2

import os


class DBHandler():
    def __init__(self,
                 dbname=os.getenv("POSTGRES_DB"),
                 user=os.getenv("POSTGRES_USER"),
                 password=os.getenv("POSTGRES_PASSWORD"),
                 host="host.docker.internal", #if from inside of devContainer, localhost otherwise
                 port=5432):

        self.connection = psycopg2.connect(dbname, user, password, host, port)
        self.cursor = self.connection.cursor()

    def create_table(self, query: str):
        # """CREATE TABLE homes_rent (
        #     propertyId INT,
        #     url VARCHAR(100),
        #     operation VARCHAR(20),
        #     address VARCHAR(100) NOT NULL,
        #     province VARCHAR(100) NOT NULL,
        #     municipality VARCHAR(100),
        #     district VARCHAR(100),
        #     propertyType VARCHAR(30),
        #     size INT NOT NULL,
        #     floor VARCHAR(10), # bj
        #     rooms INT NOT NULL,
        #     bathrooms INT NOT NULL,
        #     exterior BOOLEAN, # 1 or 0
        #     hasLift BOOLEAN,
        #     hasParkingSpace BOOLEAN, # parkingSpace[hasParkingSpace]
        #     isParkingSpaceIncludedInPrice BOOLEAN, # parkingSpace[isParkingSpaceIncludedInPrice]
        #     hasVideo BOOLEAN,
        #     showAddress BOOLEAN,
        #     priceByArea INT,
        #     latitude FLOAT,
        #     longitude FLOAT,
        #     description VARCHAR(10000),
        #     numPhotos INT NOT NULL,
        #     price INT NOT NULL,
        #     );
        # """

        # not considered
        # thumbnail, hasPlan, has3DTour, has360, hasStaging, superTopHighlight, topNewDevelopment
        # detailedType, status, newDevelopment, suggestedTexts, externalReference, neighborhood, labels, highlight

        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self):
        self.connection.commit()

    def select_data(self,
                    db_table: str,
                    columns: str = None,
                    condition: str = None):
        """ Queries data from DB.

        Parameters
        ----------
            db_table:
            columns:
            condition:
        """
        if not columns:
            columns = "*"
        query = f"SELECT {columns} FROM {db_table};"

        if condition:
            query += f" WHERE {condition}"
        self.connection.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        """ Closes DB connection."""
        self.connection.close()
