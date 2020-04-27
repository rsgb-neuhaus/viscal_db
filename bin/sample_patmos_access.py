#! /usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import sys
import os

import sqlite3
from sqlite3 import Error as sql_error


def connect():
    """
    Connect to the SQLite database with the PATMOS coefficients
    """

    dn_db = os.getenv( 'DB_DIR' )
    if( dn_db == None ):
        msg='Error: The environment variable {0} is not set.'
        print( msg.format('DB_DIR') )
        sys.exit(1)

    fn_db = os.path.join( os.getenv('DB_DIR'), 'avhrr.sqlite' )
    if not os.path.isfile(fn_db):
        msg='Error: The file {0} does not exist.'
        print( msg.format(fn_db) )
        sys.exit(1)

    connection = None
    try:
        connection = sqlite3.connect( fn_db )
    except sql_error as e_msg:
        print( e_msg )

    return connection


def main():
    """
    Sample script to access the PATMOS coefficients from the database
    """

    # connect to the database

    db = connect()
    dc = db.cursor()


    """
    # print the column titles

    dc.row_factory = sqlite3.Row
    dc.execute( 'SELECT * FROM "patmos.2017"' )
    titles = dc.fetchone()
    print( "column titles:" )
    for col in titles.keys():
        print( " - " + col )
    print
    """


    """
    # print the satellite identifiers

    dc.execute( 'SELECT id_patmos FROM "patmos.2017"' )
    ids = dc.fetchall()
    print( "identifiers (column 'id_patmos'):" )
    for id in ids:
        print( " - " + id[0] )
    print
    """


    # print the coefficients for Metop-A

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch1_low_gain_s0",
                            s1 = "ch1_low_gain_s1",
                            s2 = "ch1_low_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch1 low gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch1_high_gain_s0",
                            s1 = "ch1_high_gain_s1",
                            s2 = "ch1_high_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch1 high gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch2_low_gain_s0",
                            s1 = "ch2_low_gain_s1",
                            s2 = "ch2_low_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch2 low gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch2_high_gain_s0",
                            s1 = "ch2_high_gain_s1",
                            s2 = "ch2_high_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch2 high gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch3a_low_gain_s0",
                            s1 = "ch3a_low_gain_s1",
                            s2 = "ch3a_low_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch3a low gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    sql = "SELECT {s0},{s1},{s2} FROM '{view}' WHERE id_patmos='{id}'"
    dc.execute( sql.format( s0 = "ch3a_high_gain_s0",
                            s1 = "ch3a_high_gain_s1",
                            s2 = "ch3a_high_gain_s2",
                            view = "patmos.2017",
                            id = "m02" ) )
    coeffs = dc.fetchone()
    comment = '  ! ch3a high gain'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs ) + comment )

    db.close()


if __name__ == '__main__':
    main()
