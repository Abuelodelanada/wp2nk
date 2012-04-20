#! /usr/bin/python
# -*- coding: utf-8 -*-

# COPYLEFT
#       Copyleft © 2012 José C. Massón.
#       Licencia GPLv3 o superior <http://gnu.org/licenses/gpl.html>.
#       Esto es Software Libre, podés estudiarlo, modificarlo y redistribuirlo.

import MySQLdb, subprocess

DB_HOST = 'db_host'
DB_USER = 'db_user'
DB_PASS = 'db_pass'
DB_NAME = 'db_name'

wpdb = MySQLdb.connect(host=DB_HOST ,user=DB_USER, passwd=DB_PASS, db=DB_NAME)
cursor = wpdb.cursor()
query_posts = '''SELECT ID, DATE_FORMAT(post_date, "%Y/%m/%d %h:%i") as date, post_title, post_name, post_content 
FROM wp_posts 
WHERE post_status = "publish";'''

cursor.execute(query_posts)
posts = cursor.fetchall()

query_tags = '''SELECT wp.ID, wt.name FROM wp_terms wt 
INNER JOIN wp_term_taxonomy wtt ON (wt.term_id = wtt.term_id AND taxonomy = 'post_tag')
INNER JOIN wp_term_relationships wtr ON (wtt.term_taxonomy_id = wtr.term_taxonomy_id) 
INNER JOIN wp_posts wp ON (wtr.object_id = wp.id AND wp.post_status = "publish");'''

cursor.execute(query_tags)
post_tags = cursor.fetchall()

tags_dict = {}

def html2rst(html):
    p = subprocess.Popen(['pandoc', '--from=html', '--to=rst'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return p.communicate(html)[0]


for post_tag in post_tags:

    t = tags_dict.get(post_tag[0], [])
    tag = post_tag[1]
    t.append(tag)
    tags_dict[post_tag[0]] = t
    

for post in posts:
 
    # Genero archivos .meta
    #FIXME: Es horrible como pongo el salto de linea... 
    file1 = open("posts/"+post[3]+".meta", "w")
    lines = (post[2],'\n', post[3],'\n', post[1],'\n')
    file1.writelines(lines)

    if(tags_dict.has_key(post[0]) is True):
        t = ', '.join(tags_dict[post[0]])
        file1.write(t)

    file1.close()

    # Genero archivos .txt
    file2 = open("posts/"+post[3]+".txt", "w")
    file2.write(html2rst(post[4]))
