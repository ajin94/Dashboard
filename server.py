import json
from flask import Flask, session, request, send_file
from flask import redirect, render_template
from flask import url_for
from flask_wtf.csrf import CsrfProtect
from connections import get_connection_to
import traceback

dashapp = Flask(__name__)
dashapp.secret_key = '6wfwef6AqwdwqdSDW676w6QDWD6748wd((FD'
dashapp.config['SESSION_TYPE'] = 'filesystem'
dashapp.config['WTF_CSRF_SECRET_KEY'] = 'asdaDawqdwd#$@%fewd#22342FWFQE'
csrf = CsrfProtect()
csrf.init_app(dashapp)


@dashapp.route('/nsdash')
def nsdash():
    comment_count_query = "SELECT count(*) FROM comments"
    query_count_query = "SELECT count(*) FROM query"
    try:
        cursor, conn = get_connection_to(db_name='nsi')
        comment_count_obj = cursor.execute(comment_count_query)
        if comment_count_obj:
            ((comment_count,),) = cursor.fetchall()
        query_count_obj = cursor.execute(query_count_query)
        if query_count_obj:
            ((query_count,),) = cursor.fetchall()
    except Exception as e:
        pass

    template_dict = {
        "comment_count": comment_count,
        "query_count": query_count
    }
    return render_template('dashpages/nsinteriors/index.html', template_data=template_dict)


@dashapp.route('/nsdashcomments')
def nsdashcomments():
    comment_dict = {}
    comment_query = "SELECT id, name, email, message FROM comments"
    try:
        cursor, conn = get_connection_to(db_name='nsi')
        comment_data_obj = cursor.execute(comment_query)
        if comment_data_obj:
            data = cursor.fetchall()
            comment_dict = {id: (name, email, comment) for (id, name, email, comment) in data}
    except Exception as e:
        comment_dict = {}
    return render_template('dashpages/nsinteriors/comments.html', comment_received=comment_dict)


@dashapp.route('/nsdashquery')
def nsdashquery():
    query_dict = {}
    comment_query = "SELECT id, name, email, query FROM query"
    try:
        cursor, conn = get_connection_to(db_name='nsi')
        comment_data_obj = cursor.execute(comment_query)
        if comment_data_obj:
            data = cursor.fetchall()
            query_dict = {id: (name, email, query) for (id, name, email, query) in data}
    except Exception as e:
        query_dict = {}
    return render_template('dashpages/nsinteriors/query.html', queries_received=query_dict)


# if __name__ == "__main__":
#     dashapp.run('0.0.0.0', '9878')
