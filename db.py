from asyncio.format_helpers import _get_function_source
from cgitb import Hook
from distutils.log import error
from re import A
import re
from select import select
from sre_parse import GLOBAL_FLAGS
from sys import get_coroutine_origin_tracking_depth
from sysconfig import get_paths
import re
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Configure MySQL and server
conn = pymysql.connect(host='localhost', 
					   port= 3306,
                       user='root',
                       password='',
                       db='Tandon',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Function to execute query and fetch all rows from database
def fetch_all(query, parameters=None):
    cursor = conn.cursor()
    try:
        cursor.execute(query, parameters)
        result = cursor.fetchall()
    finally:
        cursor.close()
    return result


# Function to execute query and fetch first row from database
def fetch_one(query, parameters=None):
    cursor = conn.cursor()
    try:
        cursor.execute(query, parameters)
        result = cursor.fetchone()
    finally:
        cursor.close()
    return result


# Function to execute inserting query
def insert(query, parameters=None):
    cursor = conn.cursor()
    try:
        cursor.execute(query, parameters)
        conn.commit()
        return True
            
    except Exception as e:		    
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        


