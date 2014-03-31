=================================
Django X-File-Accel redirects app
=================================

This app allowes you to protect static files served by nginx with authorization
of your django project

Protecting files
================

This example will show how to protect 2 file positions from downloading:

* {static_url}/files/fbi
* {static_url}/files/cia


In this example we will assume that static url is /static/

Steps to protect files:

1. in nginx config disable access to desired locations:

   .. code-block:: nginx

        location /static/files/fbi {
            deny all;
        }
        location /static/files/cia {
            deny all;
        }

2. Add internal path to serve this files.
   We will add "root" directory to serve both locations with one configuration option:

   .. code-block:: nginx

        # needed for x-file-accell
        location /internal/files/ {
            internal;
            alias $project_base/static/files/;
        }


3. Configure x_file_accel_redirects app:

   1. Set ``settings.X_FILE_ACCEL = True``.
   2. add ``"x_file_accel_redirects"`` to ``settings.INSTALLED_APPS``.
   3. Add app to your root url config, e.g.:

      .. code-block:: python

        urlpatterns += patterns('',
            (r'^protected/', include('x_file_accel_redirects.urls')),
        )

   4. In django admin create new instance of x_file_accel_redirects.AccelRedirect with next values:

      * Description: anything meaningful.
      * URL prefix: any latin letters without slashes, e.g. "downloads".
      * Login required: True.
      * Internal path: "/internal/files/""  (as specified in nginx config).
      * serve document root: optionaly you can specify path to directory with needed files
        to serve them with django staticfiles app when ``settings.X_FILE_ACCEL == False``.

When everything is configured and restarted you will be able to get file
``$project_base/static/files/fbi/secrets/ufo.txt`` by next url:

``/protected/downloads/fbi/secrets/ufo.txt`` (/downloads/ if from "prefix" field of AccelRedirect)