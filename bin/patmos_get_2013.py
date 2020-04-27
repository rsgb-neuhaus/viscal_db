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

    dn_db = os.getenv( 'VTT_DATA' )
    if( dn_db == None ):
        msg='Error: The environment variable {0} is not set.'
        print( msg.format('DB_DIR') )
        sys.exit(1)

    fn_db = os.path.join( dn_db, 'avhrr.sqlite' )
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


def get_satids( db ):
    """
    Get a list of the available satellite identifiers.
    """

    dc = db.cursor()

    dc.execute( 'SELECT id_patmos FROM "patmos.2013"' )
    ids = dc.fetchall()

    return [ id[0] for id in ids ]


def print_coeffs( db, sat ):
    """
    Print all the PATMOS coefficients for a specific satellite.
    """

    dc = db.cursor()
    print( sat.upper() )


    # gain switch, dark count

    sql = "SELECT {c0_1},{sw_1},{c0_2},{sw_2},{c0_3},{sw_3}"
    sql += " FROM '{view}' WHERE id_patmos='{id}'"

    dc.execute(
        sql.format(
            c0_1 = "ch1_c0",  sw_1 = "ch1_gain_switch",
            c0_2 = "ch2_c0",  sw_2 = "ch2_gain_switch",
            c0_3 = "ch3a_c0", sw_3 = "ch3a_gain_switch",
            view = "patmos.2013",
            id = sat
        )
    )
    switch_c0 = dc.fetchone()
    

    # AVHRR channel 1

    sql = "SELECT {s0_l},{s1_l},{s2_l},{s0_h},{s1_h},{s2_h}"
    sql += " FROM '{view}' WHERE id_patmos='{id}'"

    dc.execute(
        sql.format(
            s0_l = "ch1_low_gain_s0",
            s1_l = "ch1_low_gain_s1",
            s2_l = "ch1_low_gain_s2",
            s0_h = "ch1_high_gain_s0",
            s1_h = "ch1_high_gain_s1",
            s2_h = "ch1_high_gain_s2",
            view = "patmos.2013",
            id = sat
        )
    )
    coeffs = dc.fetchone()
    comment_1 = '  ! ch1 low gain'
    comment_2 = '  ! ch1 high gain'
    comment_3 = '  ! ch1 gain switch, ch1 dark count'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[0:3] ) + comment_1 )
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[3:6] ) + comment_2 )
    print( " ".join( "%6.4f" % coeff for coeff in switch_c0[0:2] ) + comment_3 )
    

    # AVHRR channel 2

    sql = "SELECT {s0_l},{s1_l},{s2_l},{s0_h},{s1_h},{s2_h}"
    sql += " FROM '{view}' WHERE id_patmos='{id}'"

    dc.execute(
        sql.format(
            s0_l = "ch2_low_gain_s0",
            s1_l = "ch2_low_gain_s1",
            s2_l = "ch2_low_gain_s2",
            s0_h = "ch2_high_gain_s0",
            s1_h = "ch2_high_gain_s1",
            s2_h = "ch2_high_gain_s2",
            view = "patmos.2013",
            id = sat
        )
    )
    coeffs = dc.fetchone()
    comment_1 = '  ! ch2 low gain'
    comment_2 = '  ! ch2 high gain'
    comment_3 = '  ! ch2 gain switch, ch2 dark count'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[0:3] ) + comment_1 )
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[3:6] ) + comment_2 )
    print( " ".join( "%6.4f" % coeff for coeff in switch_c0[2:4] ) + comment_3 )
    

    # AVHRR channel 3A

    sql = "SELECT {s0_l},{s1_l},{s2_l},{s0_h},{s1_h},{s2_h}"
    sql += " FROM '{view}' WHERE id_patmos='{id}'"

    dc.execute(
        sql.format(
            s0_l = "ch3a_low_gain_s0",
            s1_l = "ch3a_low_gain_s1",
            s2_l = "ch3a_low_gain_s2",
            s0_h = "ch3a_high_gain_s0",
            s1_h = "ch3a_high_gain_s1",
            s2_h = "ch3a_high_gain_s2",
            view = "patmos.2013",
            id = sat
        )
    )
    coeffs = dc.fetchone()
    comment_1 = '  ! ch3a low gain'
    comment_2 = '  ! ch3a high gain'
    comment_3 = '  ! ch3a dark count, ch3a gain switch'
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[0:3] ) + comment_1 )
    print( " ".join( "%6.4f" % coeff for coeff in coeffs[3:6] ) + comment_2 )
    print( " ".join( "%6.4f" % coeff for coeff in switch_c0[4:6] ) + comment_3 )

    print()
    return


def main():

    """
    Print all the PATMOS coefficients from 2013.
    """

    db = connect()
    satids = get_satids( db )

    for sat in satids:
        print_coeffs( db, sat )

    db.close()


if __name__ == '__main__':
    main()
