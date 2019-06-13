echo ---------------------------------------------
echo                login Server
echo ---------------------------------------------
ssh -i rsa root@118.89.65.154 << eeooff
echo ---------------------------------------------
echo                 stop uwsgi3
echo ---------------------------------------------
cd /root/Server/config
uwsgi3 --stop uwsgi.pid
echo ---------------------------------------------
echo                  git pull
echo ---------------------------------------------
cd /root/Server
git pull
echo ---------------------------------------------
echo                start uwsgi3
echo ---------------------------------------------
cd /root/Server/config
uwsgi3 --ini s_uwsgi.ini
eeooff
echo ---------------------------------------------
echo                logout server
echo ---------------------------------------------