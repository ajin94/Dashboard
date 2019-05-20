import json, os, shutil
from flask import Flask, request
from flask import render_template
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
    return render_template('dashpages/nsinteriors/comment.html', comment_received=comment_dict)


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


@dashapp.route('/nsdashimage')
def nsdashimage():
    template_return_dict = {}
    image_info_dict = {}
    category_info_dict = {}
    image_path_info_query = "SELECT i.id, i.image_name, ic.image_for FROM image i INNER JOIN image_category ic on i.image_for=ic.id"
    image_category_info_query = "SELECT id, image_for FROM image_category"
    try:
        cursor, conn = get_connection_to(db_name='nsi')
        # getting image paths
        image_path_info_obj = cursor.execute(image_path_info_query)
        if image_path_info_obj:
            data = cursor.fetchall()
            image_info_dict = {id: (path, image_for) for (id, path, image_for) in data}
        # getting image categories
        image_category_info_obj = cursor.execute(image_category_info_query)
        if image_category_info_obj:
            data = cursor.fetchall()
            category_info_dict = {id: image_for for id, image_for in data}
    except Exception as e:
        image_info_dict = {}
        category_info_dict = {}
    template_return_dict['image_info'] = image_info_dict
    template_return_dict['category_info'] = category_info_dict
    return render_template('dashpages/nsinteriors/image.html', template_info=template_return_dict)


@dashapp.route('/_upload_image', methods=["POST"])
def upload_image():
    file_to_upload = request.files.get('image_files', None)
    image_for = request.form.get('image_category', None)
    if file_to_upload:
        filename = file_to_upload.filename.replace(" ", "")
        try:
            cursor, conn = get_connection_to('nsi')
            insert_query = "INSERT INTO image (image_name, image_for) VALUES (%s,%s)"
            args = (filename, int(image_for))
            cursor.execute(insert_query, args)
            conn.commit()
            try:
                # uploading files to server
                # file_to_upload.save(os.path.join("/home/mxp/projects/Dashboard/static/images", filename))
                # shutil.copy("/home/mxp/projects/Dashboard/static/images/{}".format(filename),
                #             "/home/mxp/projects/NSInteriors/static/images")
                # local dev
                file_to_upload.save(os.path.join("/media/ajin/Drive/MX-Work/Dashboard/static/images", filename))
                shutil.copy("/media/ajin/Drive/MX-Work/Dashboard/static/images/{}".format(filename),
                            "/media/ajin/Drive/MX-Work/NSInterios/static/images")
            except Exception as e:
                pass
        except Exception as e:
            pass
    return json.dumps({"status": "OK"})


@dashapp.route('/_delete_image', methods=["POST"])
def delete_image():
    image_name = request.form.get('image_name', None)
    image_id = int(request.form.get('image_id', None))

    if image_name and image_id:
        try:
            cursor, conn = get_connection_to('nsi')
            delete_query = "DELETE FROM image WHERE id=%s"
            args = (image_id,)
            cursor.execute(delete_query, args)
            conn.commit()
        except Exception as e:
            return json.dumps({"status": str(traceback.format_exc())})
        else:
            try:
                os.remove("/home/mxp/projects/Dashboard/static/images/{}".format(image_name))
                os.remove("/home/mxp/projects/NSInterios/static/images/{}".format(image_name))
                # local
                # os.remove("/media/ajin/Drive/MX-Work/Dashboard/static/images/{}".format(image_name))
                # os.remove("/media/ajin/Drive/MX-Work/NSInterios/static/images/{}".format(image_name))
            except Exception as e:
                return json.dumps({"status": str(traceback.format_exc())})

    return json.dumps({"status": "OK"})


# if __name__ == "__main__":
#     dashapp.run('0.0.0.0', '9878')
